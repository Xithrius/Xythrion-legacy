<p align="center">
    <img src="/images/icon.jpg" alt=""/>
</p>
<h1 align="center">Xythrion v2.0</h1>
<h3 align="center">Graphing manipulated data through discord.py</h3>
<p align="center">
    <a href="#commands">Commands</a> -
    <a href="#setup">Setup</a> -
    <a href="#changelog">Changelog</a>
</p>


# Setup:
*NOTE*:
- The following examples of setup assumes that you've copied and modified the contents of `.env-example` to `.env`.

1. Setting up the database
```shell
docker pull postgres
docker run --name postgres -e POSTGRES_PASSWORD=placeholder -d postgres
```

2. Options for running the bot
- If running through pipenv (for development), `docker-compose up postgres` must be run before `pipenv run start`.
- If only using docker, the entire bot can be set up with `docker-compose up`.
