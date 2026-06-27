# Contributing to JobPulse AI

Thank you for your interest in contributing to JobPulse AI! We value rigorous engineering and operational excellence.

## Local Setup

1. Clone the repository and configure your `.env` file:
   ```bash
   cp .env.example .env
   ```
2. Setup your local environment:
   ```bash
   make setup
   ```
3. Install Git pre-commit hooks to enforce style checking:
   ```bash
   pre-commit install
   ```

## Development Workflow

1. Create a feature branch from `main` using Conventional Commits prefixes (`feat/`, `fix/`, `chore/`).
2. Implement your changes.
3. Validate locally:
   ```bash
   make verify
   ```
   *This single command will run formatting, type checking, unit tests, integration tests, and security scans.*
4. Submit a Pull Request following our template.

## Architectural Boundaries

Please review our Architectural Decision Records (`docs/adr/`) before introducing major changes. Do not introduce dependencies from the UI client into the backend APIs.
