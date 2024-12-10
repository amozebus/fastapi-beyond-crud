# FastAPI Beyond CRUD 

Fork of [jod35/fastapi-beyond-CRUD](https://github.com/jod35/fastapi-beyond-CRUD) with simplified auth and CRUD

Using [uvicorn web server](https://uvicorn.org)

Auth using [OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749) with client credentials as authorization grant and [JSON Web Tokens](https://datatracker.ietf.org/doc/html/rfc7519) (HS256 encryption) [<img src="http://jwt.io/img/logo-asset.svg" alt="JWT logo" height=30 />](http://jwt.io)

See [original README.md](https://github.com/jod35/fastapi-beyond-CRUD/blob/main/README.md)

## How to launch (Docker Compose)

- Rename [`.env.example`](./.env.example) to `.env` and fill empty fields

For Windows:

- Install and start [Docker Desktop](https://docker.com)

For Linux:

- Install `docker`, `docker-compose` packages with package manager of your distro (example for Arch):

```sh
pacman -S docker docker-compose
```

Run this command in root of project:

```sh
docker compose up --build
```

Check [Swagger UI](http://localhost:8000/docs)