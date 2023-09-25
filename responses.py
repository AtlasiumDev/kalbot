import csv
import yaml
import random
import logging
logger = logging.getLogger('discord')
logging.basicConfig(filename="index.log")

def yaml_to_dict(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data

def render(inst_message,to_render):
    rendered = to_render.replace("{mention}",inst_message.author.mention)
    return rendered

# Example usage:
def handle_response(inst_message) -> str:
    if random.randint(0,100)==42:
        logger.warning(f"Sbit {inst_message.author}")
        return f"9awd 3lia tl3tili f kerri a {inst_message.author.mention}"
    yaml_file = 'responses.yml' 
    data = yaml_to_dict(yaml_file)
    message = str(inst_message.content)
    p_message = message.lower()
    for find_prompt in data["find"]:
        if p_message.find(find_prompt)>-1:
            found = data["find"][find_prompt]
            index = random.randint(0,len(found)-1)
            rendered = render(inst_message,found[index]) 
            return rendered
