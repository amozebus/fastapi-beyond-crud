 <div align="center">

# FastAPI Beyond CRUD 

Fork of [jod35/fastapi-beyond-CRUD](https://github.com/jod35/fastapi-beyond-CRUD) with simplified auth and removed CRUD

Using [uvicorn web server](https://uvicorn.org) with [nginx](https://nginx.org)

Auth using [OAuth2](https://datatracker.ietf.org/doc/html/rfc6749) with password credentials as authorization grant

[JWTs](https://datatracker.ietf.org/doc/html/rfc7519) (HS256 encryption) as access and refresh tokens

[<img src="https://jwt.io/img/icon.svg" alt="JWT Logo" height=100 />](https://jwt.io) [<img src="https://upload.wikimedia.org/wikipedia/commons/d/d2/Oauth_logo.svg" alt="OAuth Logo" height=100 />](https://oauth.net)

Also see [README.md of original repository](https://github.com/jod35/fastapi-beyond-CRUD/blob/main/README.md)

</div>

## How to launch (Docker Compose)

1. Rename [`.env.example`](./.env.example) to `.env` and fill empty fields:

    * .env fields descriptions:

> [!IMPORTANT]
> Use Docker Compose services names in values of `DATABASE_URL` and `JTI_BLOCKLIST_URL` instead of hosts IPs

    
    DATABASE_URL (str): PostgreSQL-database URL

    JWT_SECRET_KEY (str): secret for JWTs signature

    ACCESS_TOKEN_EXPIRE (int): access tokens expiry time in minutes

    REFRESH_TOKEN_EXPIRE (int): refresh tokens expiry time in days

    JTI_BLOCKLIST_URL (str): JTI blocklist Redis-database URL
    

For Windows:

2. Install and start [Docker Desktop](https://docker.com)

For Linux:

2. Install `docker`, `docker-compose` packages with package manager of your distro

3. Run this command in root of project:

```sh
docker compose up -d --build
```

4. Run database migrations:

```sh
docker compose exec api alembic upgrade head
```

4. Check [Swagger UI](http://localhost/api/docs)
