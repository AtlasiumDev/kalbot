import discord
import responses
import bot_config
import logging
from responses import yaml_to_dict
import yaml
logger = logging.getLogger('discord')

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(message)
        if not response == None:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

def add_or_create(data,prompt,value):
    if not prompt in data:
        data[prompt] = []
    data[prompt].append(value)
    return data

def run_discord_bot():
    TOKEN = bot_config.TOKEN
    intents =discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event 
    async def on_ready():
        logger.info(f"{client.user} is now running")
    @client.event 
    async def on_message(message):
        if message.author == client.user:
            return 
        username = str(message.author)
        user_message = str(message.content) 
        channel = str(message.channel)

        logger.info(f"{username} said {user_message} in {channel}")

        lower_message = user_message.lower()
        # Special commands code goes here
        if len(user_message)>1 and str(message.author) in bot_config.admins:
            if user_message[0]==bot_config.trigger_char:
                command_str = user_message[len(bot_config.trigger_char):]
                command = command_str.split(" ")
                if command[0] == "add":
                    data = yaml_to_dict(bot_config.responses_yml)
                    if len(command)==3:
                        prompt = command[1]
                        value = command[2]
                        with open(bot_config.responses_yml,"w",encoding="utf-8") as file:
                            data["find"] = add_or_create(data["find"],prompt,value)
                            yaml.dump(data,file)
                            logger.warning(f"Prompt added : {prompt}")

        # Check responses and reply
        await send_message(message,user_message,False)
        
    client.run(TOKEN)
