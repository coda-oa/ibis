---
icon: lucide/server-cog
---

# Production deployment

IBIS is designed to run in Docker containers. [Docker](https://docker.com) is the
only mandatory dependency; it is recommended to run IBIS on a Linux machine.

## Getting IBIS

As we do not provide pre-built Docker images yet, the easiest way to deploy IBIS
is to clone the Git repository:

```bash
git clone https://github.com/coda-oa/ibis
```

After cloning, open the `ibis` directory.

IBIS is started with the production compose file, which provides two services:

- **django** — the application, running gunicorn with the static files baked
  into the image (built with Tailwind CSS at image build time)
- **postgres** — a PostgreSQL database, stored in a named Docker volume

```bash
docker compose -f compose.production.yml up --build
```

On startup, the application waits until the database is reachable, runs all
outstanding migrations, and only then starts serving. The first release of the
database data (tables, rows) is kept in the `ibis_production_postgres_data`
volume, so restarting or updating the application never deletes it.

## Preparing environment variables

IBIS uses environment variable files to configure certain settings.
The variable files you need to edit are located in the `.envs/production`
directory. They are committed in a blank state: **IBIS will not start until
they are filled in** — if a required value is missing, the startup fails with
an error message naming the missing variable. This is intentional: a
misconfigured production instance should fail loudly rather than start with
wrong settings.

### django.env

In `django.env` you must set the following variables:

```
DJANGO_SECRET_KEY=<your-secret-key>
DJANGO_ALLOWED_HOSTS=<your-allowed-hosts>
DATABASE_URL=<your-database-url>
```

`DJANGO_SECRET_KEY` should be a long random string. You can generate one with:

```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

`DJANGO_ALLOWED_HOSTS` is a comma-separated list of hosts IBIS is allowed to
serve. If IBIS runs on the address `ibis.example.com`, for example, it would be

```
DJANGO_ALLOWED_HOSTS=ibis.example.com
```

`DATABASE_URL` is the connection string of the default database and must match
the user, password, and database name set in `postgres.env`. For the defaults
shipped with this file, it looks like:

```
DATABASE_URL=postgres://ibis:<your-password>@postgres:5432/ibis
```

For more information about these values, see the official Django documentation:

- [Secret Key](https://docs.djangoproject.com/en/6.1/ref/settings/#secret-key)
- [Allowed Hosts](https://docs.djangoproject.com/en/6.1/ref/settings/#allowed-hosts)

### postgres.env

In `postgres.env` you must set a password for the database:

```
POSTGRES_PASSWORD=<your-password>
```

The user (`ibis`) and database name (`ibis`) are fixed.

It is recommended to comment out unused variables with a leading `#`.

## Starting and stopping

The compose file exposes the application on port 8011 by default. Adjust the
`ports` section of the `django` service in `compose.production.yml` if IBIS
should run under a different port — or, on a public server, terminate TLS in a
reverse proxy in front of it.

```bash
docker compose -f compose.production.yml up --build    # start
docker compose -f compose.production.yml down          # stop
```

Note that the development environment (`compose.local.yml`) and the production
stack use separate Docker Compose project names, so both can run side by side
on the same machine.

## Backups

The database data lives in the `ibis_production_postgres_data` volume. To back
it up, dump it with `pg_dump`, for example:

```bash
docker compose -f compose.production.yml exec postgres \
    pg_dump -U ibis ibis > ibis-backup-$(date +%F).sql
```

Restore it by piping a dump back into a fresh database:

```bash
docker compose -f compose.production.yml exec -T postgres \
    psql -U ibis ibis < ibis-backup-2026-10-21.sql
```

It is highly recommended to create backups on a regular schedule.
