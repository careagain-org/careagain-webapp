"""
OSMD Registry Scraper
=====================
Pipeline completo para construir la base de datos del MedCommons OS Registry.

Fuentes de descubrimiento:
  1. OSHWA API          — proyectos de hardware abierto certificados
  2. GitHub Search API  — repos con keywords de dispositivos médicos OS
  3. Awesome lists      — listas curadas en GitHub (semillas curadas)

Enriquecimiento:
  - GitHub API          — licencia, actividad, stars, maintainer, lenguajes, BOM
  - PubMed E-utilities  — papers que citan o mencionan el proyecto

Clasificación automática (Claude API):
  - Categoría de dispositivo
  - FDA class estimada
  - Fase de desarrollo
  - LMIC relevance

Salida:
  - osmd_registry.csv   — listo para importar en Airtable / Google Sheets

Uso:
  python3 osmd_registry_scraper.py

  Variables de entorno opcionales (mejoran rate limits):
    GITHUB_TOKEN   — Personal Access Token de GitHub (recomendado)
    ANTHROPIC_KEY  — API key de Anthropic (para clasificación con Claude)

  Sin tokens: el scraper funciona con rate limits reducidos de la API pública.
  Con GITHUB_TOKEN: 5000 req/hora en vez de 60.
"""

import json
import csv
import time
import os
import sys
import urllib.request
import urllib.parse
import urllib.error
from datetime import datetime, timezone


# ─── Configuración ────────────────────────────────────────────────────────────

GITHUB_TOKEN   = os.getenv("GITHUB_TOKEN", "")
ANTHROPIC_KEY  = os.getenv("ANTHROPIC_KEY", "")

OUTPUT_FILE    = "osmd_registry.csv"
SLEEP_GITHUB   = 1.2   # segundos entre llamadas a GitHub (sin token: 60 req/hora)
SLEEP_PUBMED   = 0.4   # 3 req/segundo máx en PubMed E-utilities
MAX_GITHUB_PER_QUERY = 30   # proyectos por query de búsqueda (max 100)
USE_CLAUDE     = bool(ANTHROPIC_KEY)   # clasificación automática si hay API key


# ─── Fuentes semilla ──────────────────────────────────────────────────────────

# Repos de GitHub que contienen listas curadas de OSMDs
AWESOME_LISTS = [
    "GlobalHealthLabs/awesome-open-source-medical-devices",
    "makersmakingchange/open-source-at",
]

# Queries de búsqueda en GitHub
GITHUB_QUERIES = [
    "open source medical device hardware",
    "open hardware medical diagnostic",
    "open source ventilator medical",
    "open source prosthetic limb",
    "open source pulse oximeter",
    "open source ECG monitor hardware",
    "open source ultrasound hardware",
    "open source insulin pump OpenAPS",
    "open source EEG OpenBCI",
    "open source ophthalmoscope",
    "open source spirometer hardware",
    "open source fetal monitor",
    "OSMD open medical hardware",
    "open source MRI hardware",
    "open source stethoscope hardware",
    "open source phototherapy neonatal",
    "open source surgical instrument",
    "open source wheelchair hardware",
    "open source hearing aid hardware",
    "low cost medical device open source LMIC",
]

# Proyectos semilla conocidos — se añaden directamente al dataset
SEED_PROJECTS = [
    {"name": "OpenAPS",          "url": "https://github.com/openaps/openaps",             "category_hint": "diabetes/APS"},
    {"name": "Loop (iOS APS)",   "url": "https://github.com/LoopKit/Loop",                "category_hint": "diabetes/APS"},
    {"name": "Tidepool",         "url": "https://github.com/tidepool-org",                "category_hint": "diabetes/data"},
    {"name": "OpenBCI",          "url": "https://github.com/OpenBCI/OpenBCI_GUI",         "category_hint": "neurotechnology/EEG"},
    {"name": "EchOpen",          "url": "https://github.com/echopen",                     "category_hint": "imaging/ultrasound"},
    {"name": "GliaX",            "url": "https://github.com/gliax",                      "category_hint": "humanitarian/prosthetics"},
    {"name": "OpenFlexure",      "url": "https://github.com/openflexure/openflexure-microscope", "category_hint": "diagnostics/microscopy"},
    {"name": "RespiraWorks",     "url": "https://github.com/RespiraWorks/Ventilator",    "category_hint": "respiratory/ventilator"},
    {"name": "OHIF Viewer",      "url": "https://github.com/OHIF/Viewers",               "category_hint": "imaging/DICOM software"},
    {"name": "Open Source Hearing Aid", "url": "https://github.com/chipaudette/OpenHearing", "category_hint": "prosthetics/hearing"},
    {"name": "COSMIIC",          "url": "https://github.com/COSMIIC-Inc",                "category_hint": "neurostimulation"},
    {"name": "Openwater",        "url": "https://github.com/openwater",                  "category_hint": "imaging/optical"},
    {"name": "OSI2 Open MRI",    "url": "https://github.com/OpenSourceImaging",          "category_hint": "imaging/MRI"},
    {"name": "Freesurfer",       "url": "https://github.com/freesurfer/freesurfer",      "category_hint": "imaging/neuroimaging software"},
    {"name": "3D Slicer",        "url": "https://github.com/Slicer/Slicer",             "category_hint": "imaging/surgical planning"},
    {"name": "OpenEMR",          "url": "https://github.com/openemr/openemr",            "category_hint": "health IT/EHR"},
    {"name": "Karopka FOSS list","url": "https://github.com/karopka/foss-medical",       "category_hint": "meta/list"},
]


# ─── Helpers HTTP ─────────────────────────────────────────────────────────────

def http_get(url, headers=None, timeout=15):
    """GET request con reintentos. Devuelve (dict|list|str|None)."""
    req = urllib.request.Request(url, headers=headers or {})
    req.add_header("User-Agent", "MedCommons-OS-Registry-Scraper/1.0")
    if GITHUB_TOKEN and "api.github.com" in url:
        req.add_header("Authorization", f"Bearer {GITHUB_TOKEN}")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
                ct  = resp.headers.get("Content-Type", "")
                if "json" in ct:
                    return json.loads(raw)
                return raw
        except urllib.error.HTTPError as e:
            if e.code == 403:
                print(f"  [rate-limit] esperando 60s… ({url[:60]})")
                time.sleep(60)
            elif e.code == 404:
                return None
            else:
                print(f"  [HTTP {e.code}] {url[:60]}")
                return None
        except Exception as ex:
            if attempt < 2:
                time.sleep(2 ** attempt)
            else:
                print(f"  [error] {ex} — {url[:60]}")
                return None
    return None


# ─── GitHub helpers ───────────────────────────────────────────────────────────

def github_search(query, max_results=MAX_GITHUB_PER_QUERY):
    """Busca repos en GitHub. Devuelve lista de items."""
    q = urllib.parse.quote(query + " language:Python language:C language:C++ language:Arduino")
    url = f"https://api.github.com/search/repositories?q={q}&sort=stars&per_page={min(max_results,30)}"
    data = http_get(url)
    time.sleep(SLEEP_GITHUB)
    if isinstance(data, dict) and "items" in data:
        return data["items"]
    return []


def github_repo(owner_repo):
    """Devuelve metadata completa de un repo dado 'owner/repo'."""
    url = f"https://api.github.com/repos/{owner_repo}"
    data = http_get(url)
    time.sleep(SLEEP_GITHUB)
    return data if isinstance(data, dict) else None


def github_readme(owner_repo):
    """Devuelve el texto del README (primeros 4000 chars)."""
    url = f"https://api.github.com/repos/{owner_repo}/readme"
    data = http_get(url)
    time.sleep(SLEEP_GITHUB * 0.5)
    if isinstance(data, dict) and "content" in data:
        import base64
        try:
            raw = base64.b64decode(data["content"]).decode("utf-8", errors="replace")
            return raw[:4000]
        except Exception:
            pass
    return ""


def github_has_bom(owner_repo):
    """Detecta si el repo tiene archivos BOM o BoM."""
    url = f"https://api.github.com/search/code?q=BOM+OR+BoM+OR+%22bill+of+materials%22+repo:{owner_repo}"
    data = http_get(url)
    time.sleep(SLEEP_GITHUB * 0.5)
    if isinstance(data, dict):
        return data.get("total_count", 0) > 0
    return False


def github_list_contents(owner_repo):
    """Lista archivos en la raíz del repo para detectar hardware docs."""
    url = f"https://api.github.com/repos/{owner_repo}/contents"
    data = http_get(url)
    time.sleep(SLEEP_GITHUB * 0.3)
    if isinstance(data, list):
        return [f["name"].lower() for f in data if isinstance(f, dict)]
    return []


def enrich_from_github(repo_data):
    """Extrae todos los campos disponibles de la respuesta de la API de GitHub."""
    if not repo_data:
        return {}
    owner_repo = repo_data.get("full_name", "")
    pushed = repo_data.get("pushed_at", "")
    if pushed:
        try:
            dt = datetime.fromisoformat(pushed.replace("Z", "+00:00"))
            months_since = (datetime.now(timezone.utc) - dt).days // 30
            activity_status = "active" if months_since < 6 else ("maintenance" if months_since < 18 else "stale")
        except Exception:
            activity_status = "unknown"
            months_since = -1
    else:
        activity_status = "unknown"
        months_since = -1

    license_info = repo_data.get("license") or {}
    topics = repo_data.get("topics", [])

    # Detectar BOM en nombre de archivos root (rápido, sin query de code search)
    contents = github_list_contents(owner_repo) if owner_repo else []
    has_bom_file = any("bom" in f or "bill_of_material" in f or "hardware" in f for f in contents)

    return {
        "github_url":       f"https://github.com/{owner_repo}",
        "github_stars":     repo_data.get("stargazers_count", 0),
        "github_forks":     repo_data.get("forks_count", 0),
        "github_watchers":  repo_data.get("subscribers_count", 0),
        "license":          license_info.get("spdx_id", "unknown"),
        "license_name":     license_info.get("name", ""),
        "language":         repo_data.get("language", ""),
        "last_push":        pushed[:10] if pushed else "",
        "activity_status":  activity_status,
        "months_since_push": months_since,
        "topics":           ", ".join(topics),
        "open_issues":      repo_data.get("open_issues_count", 0),
        "has_wiki":         repo_data.get("has_wiki", False),
        "has_bom":          has_bom_file,
        "org_or_user":      repo_data.get("owner", {}).get("type", ""),
        "owner_login":      repo_data.get("owner", {}).get("login", ""),
        "owner_url":        repo_data.get("owner", {}).get("html_url", ""),
        "created_at":       (repo_data.get("created_at") or "")[:10],
        "homepage":         repo_data.get("homepage", "") or "",
    }


# ─── PubMed helper ────────────────────────────────────────────────────────────

def pubmed_citations(project_name):
    """Busca papers en PubMed que mencionen el proyecto. Devuelve count + top titles."""
    q = urllib.parse.quote(f'"{project_name}" AND ("open source" OR "open hardware")')
    url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term={q}&retmax=3&retmode=json&tool=osmd-registry&email=registry@medcommons.os"
    data = http_get(url)
    time.sleep(SLEEP_PUBMED)
    if not isinstance(data, dict):
        return 0, ""
    result = data.get("esearchresult", {})
    count = int(result.get("count", 0))
    ids = result.get("idlist", [])
    titles = []
    if ids:
        ids_str = ",".join(ids[:3])
        summary_url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={ids_str}&retmode=json"
        sdata = http_get(summary_url)
        time.sleep(SLEEP_PUBMED)
        if isinstance(sdata, dict):
            for uid in ids[:3]:
                t = sdata.get("result", {}).get(uid, {}).get("title", "")
                if t:
                    titles.append(t[:80])
    return count, " | ".join(titles)


# ─── Claude classifier ────────────────────────────────────────────────────────

CLASSIFY_PROMPT = """Analiza este proyecto de hardware/software médico open source y devuelve SOLO un JSON con estos campos exactos (sin texto adicional, sin markdown):

{
  "device_category": "una de: diabetes/APS | imaging/ultrasound | imaging/MRI | imaging/microscopy | imaging/software | neurotechnology/EEG | neurotechnology/stimulation | prosthetics/limb | prosthetics/hearing | respiratory/ventilator | respiratory/other | diagnostics/point-of-care | diagnostics/lab | cardiovascular/ECG | cardiovascular/other | monitoring/wearable | monitoring/vitals | surgical/instrument | surgical/planning | rehabilitation | health-IT/EHR | health-IT/other | humanitarian/equipment | meta/list | other",
  "fda_class_estimate": "I | II | III | software-only | unknown",
  "development_phase": "concept | prototype | validated | cleared | deployed | unknown",
  "lmic_relevance": "high | medium | low | unknown",
  "lmic_reason": "una frase corta explicando la relevancia LMIC o vacío",
  "is_medical_device": true o false,
  "confidence": "high | medium | low"
}

Proyecto: {name}
Descripción: {description}
README (primeros 2000 chars): {readme}
Topics GitHub: {topics}
"""

def classify_with_claude(name, description, readme, topics):
    """Clasifica un proyecto usando Claude API. Devuelve dict con campos clasificados."""
    if not ANTHROPIC_KEY:
        return {}
    prompt = CLASSIFY_PROMPT.format(
        name=name[:100],
        description=(description or "")[:300],
        readme=(readme or "")[:2000],
        topics=topics or ""
    )
    payload = json.dumps({
        "model": "claude-sonnet-4-20250514",
        "max_tokens": 400,
        "messages": [{"role": "user", "content": prompt}]
    }).encode()
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "x-api-key": ANTHROPIC_KEY,
            "anthropic-version": "2023-06-01",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            data = json.loads(resp.read().decode())
        text = data.get("content", [{}])[0].get("text", "")
        # limpiar posible markdown
        text = text.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
        return json.loads(text)
    except Exception as e:
        print(f"  [claude] error clasificando {name}: {e}")
        return {}


# ─── Descubrimiento ───────────────────────────────────────────────────────────

def discover_from_awesome_lists():
    """Extrae repos referenciados en awesome-lists curadas."""
    found = []
    for list_repo in AWESOME_LISTS:
        print(f"  → Awesome list: {list_repo}")
        readme = github_readme(list_repo)
        if not readme:
            continue
        # Extraer URLs de GitHub de formato markdown [name](https://github.com/...)
        import re
        urls = re.findall(r'https://github\.com/([\w\-]+/[\w\-\.]+)', readme)
        for owner_repo in set(urls):
            if owner_repo not in [lr for lr in AWESOME_LISTS]:
                found.append(owner_repo)
    return list(set(found))


def discover_from_github_search():
    """Busca repos por queries predefinidas."""
    found = []
    for i, query in enumerate(GITHUB_QUERIES):
        print(f"  → Query {i+1}/{len(GITHUB_QUERIES)}: '{query[:50]}'")
        items = github_search(query)
        for item in items:
            fn = item.get("full_name", "")
            if fn:
                found.append(fn)
    return list(set(found))


def discover_from_seeds():
    """Extrae owner/repo de las URLs semilla conocidas."""
    found = []
    import re
    for seed in SEED_PROJECTS:
        m = re.search(r'github\.com/([\w\-]+(?:/[\w\-\.]+)?)', seed["url"])
        if m:
            found.append(m.group(1))
    return found


# ─── Pipeline principal ───────────────────────────────────────────────────────

def build_registry():
    print("\n╔══════════════════════════════════════════════╗")
    print("║  OSMD Registry Scraper — MedCommons OS       ║")
    print("╚══════════════════════════════════════════════╝\n")

    if GITHUB_TOKEN:
        print(f"✓ GitHub Token configurado — 5000 req/hora")
    else:
        print("⚠ Sin GITHUB_TOKEN — rate limit: 60 req/hora (lento)")
        print("  Configura: export GITHUB_TOKEN=ghp_tutoken\n")

    if USE_CLAUDE:
        print(f"✓ Anthropic API key configurada — clasificación automática activa\n")
    else:
        print("⚠ Sin ANTHROPIC_KEY — clasificación automática desactivada")
        print("  Configura: export ANTHROPIC_KEY=sk-ant-tukey\n")

    # ── 1. Descubrimiento ──────────────────────────────────────────────────
    print("═══ FASE 1: Descubrimiento de proyectos ═══")

    all_repos = set()

    print("\n[A] Seeds conocidas:")
    seeds = discover_from_seeds()
    all_repos.update(seeds)
    print(f"  {len(seeds)} repos desde seeds")

    print("\n[B] Awesome lists curadas:")
    awesome = discover_from_awesome_lists()
    all_repos.update(awesome)
    print(f"  {len(awesome)} repos desde awesome lists")

    print("\n[C] GitHub Search (puede tardar varios minutos):")
    if GITHUB_TOKEN:
        gh_found = discover_from_github_search()
        all_repos.update(gh_found)
        print(f"  {len(gh_found)} repos desde búsqueda GitHub")
    else:
        print("  Saltando búsqueda GitHub sin token (rate limit muy bajo)")
        print("  Tip: añade GITHUB_TOKEN para activar esta fase")

    print(f"\n→ Total repos candidatos únicos: {len(all_repos)}")

    # ── 2. Enriquecimiento ─────────────────────────────────────────────────
    print("\n═══ FASE 2: Enriquecimiento de metadatos ═══")

    records = []
    repos_list = sorted(all_repos)
    total = len(repos_list)

    for i, owner_repo in enumerate(repos_list):
        # Saltar repos que claramente no son médicos (listas meta, orgs sin repo)
        if "/" not in owner_repo:
            continue

        print(f"  [{i+1}/{total}] {owner_repo}")

        # GitHub metadata
        repo_data = github_repo(owner_repo)
        if not repo_data:
            print(f"    ✗ No encontrado")
            continue

        gh = enrich_from_github(repo_data)

        # Filtro rápido: descartar repos con <5 stars y sin actividad reciente
        # (excepto seeds conocidas)
        is_seed = owner_repo in [s for s in seeds]
        if not is_seed and gh.get("github_stars", 0) < 3:
            print(f"    ✗ Descartado (< 3 stars)")
            continue

        # README para clasificación
        readme = ""
        if USE_CLAUDE:
            readme = github_readme(owner_repo)

        # PubMed
        name = repo_data.get("name", owner_repo.split("/")[-1])
        pubmed_count, pubmed_titles = pubmed_citations(name)

        # Clasificación con Claude
        cl = {}
        if USE_CLAUDE:
            cl = classify_with_claude(
                name=name,
                description=repo_data.get("description", ""),
                readme=readme,
                topics=gh.get("topics", "")
            )
            # Filtrar si Claude dice que no es dispositivo médico
            if cl.get("is_medical_device") is False and cl.get("confidence") == "high":
                print(f"    ✗ Claude: no es dispositivo médico")
                continue

        record = {
            # Identidad
            "name":                 name,
            "full_name":            owner_repo,
            "description":          (repo_data.get("description") or "")[:300],
            "homepage":             gh.get("homepage", ""),
            "github_url":           gh.get("github_url", ""),

            # GitHub metrics
            "stars":                gh.get("github_stars", 0),
            "forks":                gh.get("github_forks", 0),
            "license":              gh.get("license", "unknown"),
            "license_name":         gh.get("license_name", ""),
            "primary_language":     gh.get("language", ""),
            "topics":               gh.get("topics", ""),
            "last_push":            gh.get("last_push", ""),
            "activity_status":      gh.get("activity_status", "unknown"),
            "months_since_push":    gh.get("months_since_push", -1),
            "open_issues":          gh.get("open_issues", 0),
            "created_at":           gh.get("created_at", ""),
            "has_wiki":             gh.get("has_wiki", False),
            "has_bom":              gh.get("has_bom", False),
            "org_type":             gh.get("org_or_user", ""),
            "owner":                gh.get("owner_login", ""),
            "owner_url":            gh.get("owner_url", ""),

            # PubMed
            "pubmed_citations":     pubmed_count,
            "pubmed_top_titles":    pubmed_titles,

            # Clasificación Claude (vacío si sin API key)
            "device_category":      cl.get("device_category", ""),
            "fda_class_estimate":   cl.get("fda_class_estimate", ""),
            "development_phase":    cl.get("development_phase", ""),
            "lmic_relevance":       cl.get("lmic_relevance", ""),
            "lmic_reason":          cl.get("lmic_reason", ""),
            "is_medical_device":    cl.get("is_medical_device", ""),
            "classification_confidence": cl.get("confidence", ""),

            # Campos para completar manualmente (outreach)
            "regulatory_status":    "",   # completar con outreach
            "maintainer_contact":   "",   # completar con outreach
            "clinical_evidence":    "",   # completar con outreach
            "funding_sources":      "",   # completar con outreach
            "verified_by_maintainer": "", # True/False tras confirmación

            # Metadata del registry
            "indexed_at":           datetime.now().strftime("%Y-%m-%d"),
            "last_updated":         datetime.now().strftime("%Y-%m-%d"),
            "registry_notes":       "",
        }

        records.append(record)
        print(f"    ✓ {name} | ★{record['stars']} | {record['activity_status']} | {record.get('device_category','—')}")

    # ── 3. Exportar CSV ────────────────────────────────────────────────────
    print(f"\n═══ FASE 3: Exportando {len(records)} proyectos ═══")

    if not records:
        print("  ⚠ No hay registros para exportar. Comprueba la conexión y los tokens.")
        return

    fieldnames = list(records[0].keys())
    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    print(f"\n✓ CSV exportado: {OUTPUT_FILE}")
    print(f"  Proyectos totales:          {len(records)}")
    print(f"  Con clasificación Claude:   {sum(1 for r in records if r['device_category'])}")
    print(f"  Con citas PubMed:           {sum(1 for r in records if r['pubmed_citations'] > 0)}")
    print(f"  Activos (< 6 meses):        {sum(1 for r in records if r['activity_status'] == 'active')}")
    print(f"  Con BOM detectado:          {sum(1 for r in records if r['has_bom'])}")

    # Top 10 por stars
    print("\n  Top 10 por GitHub stars:")
    top = sorted(records, key=lambda r: int(r.get("stars", 0)), reverse=True)[:10]
    for r in top:
        print(f"    ★{r['stars']:5d}  {r['name'][:40]}  [{r.get('device_category','—')}]")

    print(f"\n→ Importa {OUTPUT_FILE} en Airtable o Google Sheets.")
    print("→ Completa los campos vacíos (regulatory_status, maintainer_contact) con outreach.")
    if not USE_CLAUDE:
        print("\n→ Para activar clasificación automática:")
        print("   export ANTHROPIC_KEY=sk-ant-tukey && python3 osmd_registry_scraper.py")
    if not GITHUB_TOKEN:
        print("\n→ Para activar búsqueda GitHub completa:")
        print("   export GITHUB_TOKEN=ghp_tutoken && python3 osmd_registry_scraper.py")


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    build_registry()
