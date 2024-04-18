from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, File
from responses import get_response
import json

with open("keywords.json", "r") as file:
    jdata = json.load(file)


load_dotenv()
TOKEN: Final[str] = os.getenv('TOKEN')

intents: Intents = Intents.default()
intents.members = True
intents.messages = True
intents.message_content = True # NOQA
client: Client = Client(intents=intents)

async def  send_message(message: Message, user_message: str) -> None:
    if not user_message:
        print('(Message was empty because intents were not enabled probably)')
        return
    
    if is_private := user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

@client.event
async def on_ready() -> None:
    print(f'{client.user} is now running!')

@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    keyword_dict = {
        "貼貼": jdata["貼貼"],
        "D:": jdata["D:"],
        "累": jdata["累了"],
        "衝": jdata["衝鴨"],
        "。": jdata["無語"],
        "讚": jdata["讚"],
        "耐斯": jdata["good"],
        "小丑": jdata["joker"],
        "smile": jdata["?"],
        "笑": jdata["?"],
        "難過": jdata["T^T"]
    }

    for keyword in keyword_dict:
        if keyword in message.content and message.author != client.user:
            await message.channel.send(file=File(str(keyword_dict[keyword])))
            break  
    else:
        username: str = str(message.author)
        user_message: str = message.content
        channel: str = str(message.channel)

        print(f'[{channel}] {username}: "{user_message}"')
        await send_message(message, user_message)


@client.event
async def on_member_join(member):

    welcome_channel = client.get_channel(int(os.getenv('WELCOME_CHANNEL_ID')))
    print(welcome_channel)
    
    if welcome_channel:
        await welcome_channel.send(f"Welcome to the server, {member.mention}!")

@client.event
async def on_member_remove(member):

    welcome_channel = client.get_channel(int(os.getenv('WELCOME_CHANNEL_ID')))
    print(welcome_channel)

    if welcome_channel:
        await welcome_channel.send(f"{member} bye:(")

def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()