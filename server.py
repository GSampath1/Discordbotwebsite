import os 
from flask import Flask, redirect, url_for, render_template, request
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
from threading import Thread
import requests
import json

app = Flask(__name__,
template_folder="template")
app.static_folder = 'static'

with open("static/database/config.json", "r") as f:
    config = json.load(f)

app.secret_key = b"%\xe0'\x01\xdeH\x8e\x85m|\xb3\xffCN\xc9g"
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"    # !! Only in development environment.
app.config["DISCORD_CLIENT_ID"] = config["DISCORD_CLIENT_ID"]
app.config["DISCORD_CLIENT_SECRET"] = config["DISCORD_CLIENT_SECRET"]
app.config["DISCORD_BOT_TOKEN"] = config["token"]
app.config["DISCORD_REDIRECT_URI"] = "https://192.168.0.166:4000/callback"

discord = DiscordOAuth2Session(app)
HYPERLINK = '<a href="{}">{}</a>'


@app.route("/login/")
async def login():
    return discord.create_session()

@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect(url_for("login"))

@app.route("/callback")
async def callback():
    data = discord.callback()
    redirect_to = data.get("redirect", "/")
    return redirect(redirect_to)

@app.errorhandler(404)
async def page_not_found(error):
    return redirect("/404")

@app.route("/logout/")
async def logout():
    discord.revoke()
    return redirect(url_for(".index"))

@app.route("/404")
async def error404():
    return render_template('404.html'), 404

@app.route("/support")
async def support(): 
        return redirect('https://discord.gg/Z8JqBrpCh8')

@app.route("/invite")
async def invite(): 
        return redirect('')

@app.route("/")
async def index():
    if not discord.authorized:
        return render_template('index.html',authorized=False)
    
    user = discord.fetch_user()
    return render_template('index.html',authorized=True,username=user)

@app.route("/secret/")
@requires_authorization
async def secret():
    return os.urandom(16)

if __name__ == "__main__":
  app.run(host="0.0.0.0", port=4000)    