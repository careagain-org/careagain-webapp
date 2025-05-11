## Developer guide

### Prerequisites

- **Python 3.12 or higher**: The library requires modern Python features. [Download Python here](https://www.python.org/downloads/)
  > 💡 When installing Python, make sure to check "Add Python to PATH" on Windows!
- **Docker** and Docker Compose (optional, for containerized setup). [Check Docker documentation](https://www.docker.com/)

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

### Libraries and tools

The development of CareAgain webapp used:

- **Language**: [Python 3.12 or higher](https://www.python.org/)
- **Frontend**: [Reflex framework](https://reflex.dev/)
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Documentation**: [Mkdocs-Material](https://squidfunk.github.io/mkdocs-material/getting-started/)
- **Version control and deployment**: [Github and github actions](https://github.com/)
- **Contanarization**: [Docker](https://github.com/)
- **Database and storage**: [Supabase](https://supabase.com/)

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
