from pokemontcgsdk import RestClient as pokemontcgsdk_Client
import os
import random
from flask import Flask
from flask_discord_interactions import DiscordInteractions, Context, Message
from pokemon import get_random_booster
import threading
from db import get_user_data, add_pack

app = Flask(__name__)
discord = DiscordInteractions(app)

app.config["DISCORD_CLIENT_ID"] = os.environ["DISCORD_APP_ID"]
app.config["DISCORD_PUBLIC_KEY"] = os.environ["DISCORD_PUBLIC_KEY"]
app.config["DISCORD_CLIENT_SECRET"] = os.environ["DISCORD_BOT_SECRET"]
POKEMONTCG_IO_API_KEY = os.environ.get("pokemontcgio")
pokemontcgsdk_Client.configure(POKEMONTCG_IO_API_KEY)


@discord.command()
def pull(ctx: Context):

    def pull_and_show_booster() -> None:
        booster = get_random_booster()
        if booster is None:
            ctx.edit("Sorry no cards for you")
        add_pack(ctx.author.id, booster)
        for card in booster:
            ctx.send(card.images.small)

    threading.Thread(target=pull_and_show_booster).start()
    return Message(content="Pulling", deferred=True)


@discord.command()
def check_inventory(ctx: Context):
    user_data = get_user_data(ctx.author.id)
    if len(user_data["inventory"]) == 0:
        return "You have no cards!"
    return Message(content='\n'.join(user_data["inventory"]))


discord.set_route("/interactions")

discord.update_commands(guild_id="640115584939327488")

if __name__ == '__main__':
    app.run(  # Starts the site
        host=
        '0.0.0.0',  # EStablishes the host, required for repl to detect the site
        port=random.randint(
            2000, 9000)  # Randomly select the port the machine hosts on.
    )
