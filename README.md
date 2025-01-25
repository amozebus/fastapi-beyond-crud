 <div align="center">

# FastAPI Beyond CRUD 

Fork of [jod35/fastapi-beyond-CRUD](https://github.com/jod35/fastapi-beyond-CRUD) with simplified auth and CRUD

Using [uvicorn web server](https://uvicorn.org) with [nginx](https://nginx.org)

Auth using [OAuth 2.0](https://datatracker.ietf.org/doc/html/rfc6749) with password credentials as authorization grant with refresh tokens and [JSON Web Tokens](https://datatracker.ietf.org/doc/html/rfc7519) (HS256 encryption)

[<img src="https://jwt.io/img/icon.svg" alt="JWT Logo" height=100 />](https://jwt.io) [<img src="https://upload.wikimedia.org/wikipedia/commons/d/d2/Oauth_logo.svg" alt="OAuth Logo" height=100 />](https://oauth.net)

See [README.md of original repository](https://github.com/jod35/fastapi-beyond-CRUD/blob/main/README.md)

</div>

## How to launch (Docker Compose)

- Rename [`.env.example`](./.env.example) to `.env` and fill empty fields

For Windows:

- Install and start [Docker Desktop](https://docker.com)

For Linux(example for Arch):

- Install `docker`, `docker-compose` packages with pacman:

```sh
pacman -S docker docker-compose
```

Run this command in root of project:

```sh
docker compose up --build
```

Check [Swagger UI](http://localhost/api/docs)
