# CareAgain WebApp

**CareAgain WebApp** is a web application built using the [Reflex](https://reflex.dev/) framework.
It serves as the frontend for CareAgain's platform, aiming to connect institutions and organizations involved in medical devices—such as R&D, manufacturing, logistics, and hospitals—into a unified network to foster a thriving community.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Development](#development)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [License](#license)

## Features

- Modular and extensible architecture using Reflex.
- Predefined components and templates for rapid development.
- Dockerized setup for consistent development and deployment environments.
- Integration-ready with backend services and databases.

## Project Structure

The project follows the standard Reflex template structure:

```
├── README.md
├── assets/
├── rxconfig.py
├── webapp/
│   ├── __init__.py
│   ├── components/
│   │   ├── __init__.py
│   │   └── sidebar.py
│   ├── pages/
│   │   ├── __init__.py
│   │   ├── dashboard.py
│   │   ├── index.py
│   │   └── settings.py
│   ├── styles.py
│   ├── templates/
│   │   ├── __init__.py
│   │   └── template.py
│   └── webapp.py
├── Dockerfile
├── docker-compose.yaml
├── requirements.txt
├── requirements_manual.txt
├── pyproject.toml
├── alembic/
├── alembic.ini
├── devops/
└── .github/workflows/
```

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Docker and Docker Compose (optional, for containerized setup)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/careagain-org/careagain-webapp.git
   cd careagain-webapp
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:

   ```bash
   reflex run
   ```

   The application will be accessible at `http://localhost:3000`.

## Development

- To add new pages, create a Python file in `webapp/pages/` and define a function with the `@template` decorator.
- For reusable components, add them to `webapp/components/`.
- Use `webapp/styles.py` for styling and theming.

## Deployment

### Using Docker

1. Build the Docker image:

   ```bash
   docker build -t careagain-webapp .
   ```

2. Run the Docker container:

   ```bash
   docker run -p 3000:3000 careagain-webapp
   ```

   The application will be accessible at `http://localhost:3000`.

## Contributing

We welcome contributions from the community. To contribute:

1. Fork the repository.
2. Create a new branch:

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. Make your changes and commit them:

   ```bash
   git commit -m "Add your message here"
   ```

4. Push to your forked repository:

   ```bash
   git push origin feature/your-feature-name
   ```

5. Open a pull request detailing your changes.

## License

This project is licensed under the [MIT License](LICENSE).

---

For more information on the Reflex framework, visit the [official documentation](https://reflex.dev/docs).
