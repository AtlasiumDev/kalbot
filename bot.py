import discord
import responses
import bot_config
import logging
logger = logging.getLogger('discord')

async def send_message(message, user_message, is_private):
    try:
        response = responses.handle_response(message)
        if not response == None:
            await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

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
        if user_message[0]==bot_config.trigger_char:
            user_message = user_message[len(bot_config.trigger_char):]
            # Special commands code goes here
        # Check responses and reply
        await send_message(message,user_message,False)
        
             
        


    client.run(TOKEN)
