# ibis
IBIS (Information Budget Insight System) is a a web-based portal that aggregates and consolidates data from various institutional source systems and prepares it for reporting.

## Development

### Starting the development environment

Start the local container with Docker Compose:

```sh
docker compose -f compose.local.yml up --build
```

The container startup script installs the locked frontend and Python dependencies, then starts Django and Tailwind's watcher. Tailwind rebuilds the stylesheet when templates or CSS sources change. The site is available at `http://localhost:8010`; stop both processes with Ctrl+C.

To build the stylesheet once without starting the watcher, run this inside the container:

```sh
npm run css:build
```

### Committing

As we use `commitizen` to ensure correct commit formatting, we recommend using its command-line tool to generate the commit message:

```
pdm run cz commit
```

## Get in Touch with us! 📬

- **Project Website**: <a href="https://www.tu-braunschweig.de/ub/wir-ueber-uns/projektuebersicht/ibis" target="_blank" rel="noopener noreferrer">The website of the IBIS project</a>
