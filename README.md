<p align="center">
    <img src="/images/icon.jpg"/>
</p>
<h1 align="center">Xythrion v2.0</h1>
<h3 align="center">Graphing manipulated data through discord.py</h3>
<p align="center">
    <a href="https://discordapp.com/oauth2/authorize?client_id=591885341812850699&scope=bot&permissions=1077267520">Invite</a> -
    <a href="#checklist">Checklist</a> -
    <a href="#commands">Commands</a> -
    <a href="#setup">Setup</a> -
    <a href="#changelog">Changelog</a>
</p>


# Setup:
*NOTE*:
- This guide assumes you've copied the template from `.env-example` to a file called `.env` that you've created yourself.

```sh
$ docker pull postgres
# "placeholder" in this command should replace the placeholder with the same name in the .env file.
$ docker run --name postgres -e POSTGRES_PASSWORD=placeholder -d postgres
$ docker-compose up --build
```
