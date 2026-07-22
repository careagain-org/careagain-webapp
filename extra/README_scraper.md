# OSMD Registry Scraper
### MedCommons OS — Construcción automatizada de la base de datos

---

## Qué hace

Pipeline en 3 fases que construye la base de datos del Registry automáticamente:

```
Descubrimiento → Enriquecimiento → Clasificación → CSV (Airtable-ready)
```

**Fase 1 — Descubrimiento** (encuentra los proyectos):
- Seeds conocidos (OpenAPS, OpenBCI, EchOpen, GliaX, etc.)
- Awesome lists curadas en GitHub
- GitHub Search con 20 queries especializadas en dispositivos médicos OS

**Fase 2 — Enriquecimiento** (rellena los campos automáticamente):
- GitHub API: licencia, actividad, stars, maintainer, BOM, lenguaje, topics
- PubMed E-utilities: cuántos papers citan el proyecto y títulos
- Detección de archivos BOM en el repo

**Fase 3 — Clasificación con Claude** (si tienes API key):
- Categoría de dispositivo (diabetes/APS, imaging, prosthetics...)
- FDA class estimada (I, II, III, software-only)
- Fase de desarrollo (concept, prototype, validated, cleared)
- Relevancia LMIC (high, medium, low) con razón
- Filtro: descarta repos que claramente no son dispositivos médicos

**Salida**: `osmd_registry.csv` con ~30 campos por proyecto, listo para Airtable.

---

## Instalación

Solo necesitas Python 3.8+. Sin dependencias externas.

```bash
# Verifica que tienes Python 3
python3 --version

# Descarga el script
# (ya lo tienes en esta carpeta)
```

---

## Uso básico (sin tokens)

```bash
python3 osmd_registry_scraper.py
```

Funciona sin tokens, pero con límites:
- GitHub: 60 requests/hora → solo procesa seeds + awesome lists
- Sin clasificación automática → campos `device_category`, `fda_class_estimate` vacíos
- PubMed: 3 requests/segundo (sin límites, funciona bien)

Tiempo estimado: ~5 minutos, ~30-50 proyectos.

---

## Uso recomendado (con tokens)

### 1. GitHub Personal Access Token (gratis)

1. Ve a https://github.com/settings/tokens
2. "Generate new token (classic)"
3. Permisos: solo `public_repo` (read-only es suficiente)
4. Copia el token

```bash
export GITHUB_TOKEN=ghp_tutoken_aqui
python3 osmd_registry_scraper.py
```

Con token: 5000 req/hora, activa GitHub Search completo (20 queries × 30 resultados = 600 repos candidatos).

### 2. Anthropic API key (para clasificación automática)

```bash
export ANTHROPIC_KEY=sk-ant-api03-tukey_aqui
python3 osmd_registry_scraper.py
```

Con ambos tokens:

```bash
export GITHUB_TOKEN=ghp_tutoken
export ANTHROPIC_KEY=sk-ant-api03-tukey
python3 osmd_registry_scraper.py
```

Tiempo estimado con ambos tokens: 30-60 minutos, 150-300 proyectos clasificados.

---

## Campos del CSV

| Campo | Fuente | Notas |
|-------|--------|-------|
| `name` | GitHub | Nombre del repo |
| `description` | GitHub | Descripción corta |
| `github_url` | GitHub | URL del repo |
| `stars` | GitHub API | Indicador de adopción |
| `forks` | GitHub API | Indicador de uso activo |
| `license` | GitHub API | SPDX ID (MIT, GPL-3.0...) |
| `last_push` | GitHub API | Fecha última actividad |
| `activity_status` | Calculado | active / maintenance / stale |
| `months_since_push` | Calculado | Meses desde último push |
| `has_bom` | GitHub API | Si detecta archivos BOM |
| `topics` | GitHub API | Tags del repo |
| `pubmed_citations` | PubMed | Nº papers que citan el proyecto |
| `device_category` | Claude | Categoría del dispositivo |
| `fda_class_estimate` | Claude | Clase FDA estimada |
| `development_phase` | Claude | Fase de desarrollo |
| `lmic_relevance` | Claude | high / medium / low |
| `regulatory_status` | **Manual** | Completar con outreach |
| `maintainer_contact` | **Manual** | Email/Slack del maintainer |
| `clinical_evidence` | **Manual** | Ensayos, validaciones |
| `funding_sources` | **Manual** | Grants recibidos |
| `verified_by_maintainer` | **Manual** | True tras confirmación |

---

## Flujo de trabajo completo

```
1. Ejecutar scraper → osmd_registry.csv (campos automáticos)
        ↓
2. Importar en Airtable (File > Import CSV)
        ↓
3. Revisar clasificaciones de Claude (corregir errores)
        ↓
4. Outreach a maintainers (completar campos manuales)
        ↓
5. Publicar Registry v0 con los proyectos verificados
        ↓
6. Ejecutar scraper semanalmente para mantener actividad actualizada
```

---

## Automatización semanal

Para mantener el Registry actualizado automáticamente:

```bash
# En macOS/Linux, añadir al crontab:
# Ejecutar cada domingo a las 8am
0 8 * * 0 cd /ruta/al/scraper && python3 osmd_registry_scraper.py >> scraper.log 2>&1
```

O en GitHub Actions (gratis para repos públicos):

```yaml
# .github/workflows/update-registry.yml
name: Update OSMD Registry
on:
  schedule:
    - cron: '0 8 * * 0'  # cada domingo
  workflow_dispatch:       # también manual

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run scraper
        env:
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
          ANTHROPIC_KEY: ${{ secrets.ANTHROPIC_KEY }}
        run: python3 osmd_registry_scraper.py
      - name: Commit updated CSV
        run: |
          git config --local user.email "registry-bot@medcommons.os"
          git config --local user.name "Registry Bot"
          git add osmd_registry.csv
          git diff --staged --quiet || git commit -m "chore: weekly registry update"
          git push
```

---

## Campos que NUNCA se rellenan solos

Estos campos siempre requieren outreach al maintainer:

- **`regulatory_status`**: Si han tenido contacto con FDA/MDR, si tienen Pre-Sub meeting, si están en proceso de 510(k)
- **`maintainer_contact`**: Email directo o Slack del maintainer principal
- **`clinical_evidence`**: Ensayos no publicados, validaciones en hospitales
- **`funding_sources`**: Grants NIH/NSF/Gates recibidos o en proceso
- **`verified_by_maintainer`**: Solo True si el maintainer confirmó el perfil

El scraper te da el 70% del trabajo. El outreach te da el 30% que hace que el Registry sea genuinamente valioso — esa información que no está en ningún GitHub.

---

## Soporte

Script escrito por MedCommons OS Registry.  
Problemas o sugerencias → abre un issue en el repo del proyecto.
