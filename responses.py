import csv
import yaml
import random
import logging
import bot_config
import requests

def get_playingsong(channel="main"):
    channels = {
        "main":"1003",
        "90s":"1005"
    }
    headers = {
        'authority': 'youradio.ma',
        'accept': '*/*',
        'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6,ar;q=0.5',
        'origin': 'https://uradio.ma',
        'referer': 'https://uradio.ma/',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36',
    }

    response = requests.get(f'https://youradio.ma/appservices/api/playinfo/{channels[channel]}', headers=headers)
    json_dict = response.json()
    PlayingSong = json_dict["PlayingSong"]
    return PlayingSong


logger = logging.getLogger('discord')
logging.basicConfig(filename="index.log")

def yaml_to_dict(yaml_file):
    with open(yaml_file, 'r',encoding="utf-8") as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

def render(inst_message,to_render):
    rendered = to_render.replace("{mention}",inst_message.author.mention)
    return rendered

# Example usage:
def handle_response(inst_message) -> str:
    if str(inst_message.content).find("whatsplaying90s")>-1:
        whatsplaying = get_playingsong("90s")
        return f"""{whatsplaying['Title']} - {whatsplaying['Artist']} """
    if str(inst_message.content).find("whatsplaying")>-1:
        whatsplaying = get_playingsong()
        return f"""{whatsplaying['Title']} - {whatsplaying['Artist']} """
    
    # Hidden mysteryes
    if random.randint(0,100)==42:
        logger.warning(f"Sbit {inst_message.author}")
        return f"9awd 3lia tl3tili f kerri a {inst_message.author.mention}"
    if random.randint(0,100)==1:
        logger.warning(f"I loved {inst_message.author}")
        return f"I love you a {inst_message.author.mention}"
    
    message = str(inst_message.content)
    p_message = message.lower()
    # Specific orders
    # hh+ order
    if p_message[:3] == "hh+" and len(p_message)>3:
        num = int(p_message.split("+")[1])
        if num>420 or num == None:
            num=420
        return "h"*num
    # Import yml data   
    data = yaml_to_dict(bot_config.responses_yml)

    # random case
    if p_message.find("random")>-1:
        length = len(list(data["find"].keys())) 
        key = list(data["find"].keys())[random.randint(0,length-1)]
        found = data["find"][key][0]
        rendered = render(inst_message,found) 
        return rendered 
    
    # search in responses
    for find_prompt in data["find"]:
        if p_message == find_prompt:
            found = data["find"][find_prompt]
            index = random.randint(0,len(found)-1)
            rendered = render(inst_message,found[index]) 
            return rendered
    
    # User specific
    if str(inst_message.author) in bot_config.moulays:
        if random.randint(0,100)==1:
            logger.warning(f"chi moulays hdr")
            return f"Ayih kayna, I7tiramati a moulay {inst_message.author.mention}"