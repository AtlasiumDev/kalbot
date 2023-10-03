import csv
import yaml
import random
import logging
import bot_config
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
    # User specific
    # if str(inst_message.author) == "anood8254":
    #     logger.warning(f"Sbit {inst_message.author}")
    #     return f"Lah yn3el tbonmok a {inst_message.author.mention}"
                
    # Hidden mysteryes
    if random.randint(0,100)==42:
        logger.warning(f"Sbit {inst_message.author}")
        return f"9awd 3lia tl3tili f kerri a {inst_message.author.mention}"
    if random.randint(0,100)==1:
        logger.warning(f"I loved {inst_message.author}")
        return f"I love you a {inst_message.author.mention}"
    
    # Import yml data   
    data = yaml_to_dict(bot_config.responses_yml)
    message = str(inst_message.content)
    p_message = message.lower()

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
