# Stage 1: build the Tailwind stylesheet
FROM node:22-alpine AS assets

WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run css:build

# Stage 2: the production application
FROM python:3.14-slim-bookworm

RUN apt-get update \
    && apt-get install --no-install-recommends -y libpq-dev ca-certificates \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:0.12.19 /uv /uvx /bin/

RUN groupadd app && useradd --create-home --gid app app

WORKDIR /app
RUN chown app:app /app
COPY --chown=app:app . .
COPY --chown=app:app --from=assets /app/config/interfaces/http/static/css/tailwind.css ./config/interfaces/http/static/css/tailwind.css

USER app
ENV PATH="/home/app/.local/bin:${PATH}"

RUN uv sync --frozen --no-dev

# Bakes the static files into the image (Django serves them without runserver magic)
RUN uv run python manage.py collectstatic --noinput

RUN chmod +x /app/dockerfiles/production/entrypoint /app/dockerfiles/production/start

EXPOSE 8000

ENTRYPOINT ["/app/dockerfiles/production/entrypoint"]
CMD ["/app/dockerfiles/production/start"]
