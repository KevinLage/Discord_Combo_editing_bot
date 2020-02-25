import discord
import requests
import random
import time
import threading
from datetime import datetime
import datetime
from zipfile import ZipFile
import json

token = "YOUR_TOKEN"

def dm(message,latest):
    global response

    if message.author.dm_channel != None:
        dmid = message.author.dm_channel.id
    else:
        r=requests.post("https://discordapp.com/api/v7/users/@me/channels",headers={'Host': 'discordapp.com', 'User-Agent': 'DiscordBot (https://github.com/Rapptz/discord.py 1.3.1) Python/3.8 aiohttp/3.6.2', 'X-Ratelimit-Precision': 'millisecond', 'Authorization': 'Bot ' + token, 'Content-Type': 'application/json', 'Accept': '*/*', 'Cookie': '__cfduid=dfe6240a57d664f20012add39b19197bf1582476181; __cfruid=de095c72f67bcd53ba853c7b85c7f9b768b09c9e-1582476181', 'Accept-Encoding': 'gzip, deflate'},data=json.dumps({"recipient_id": message.author.id})) #creates a PM
        dmid = json.loads(r.text)["id"]

    r = requests.post("https://discordapp.com/api/v7/channels/" + str(dmid) + "/messages",headers={'Host': 'discordapp.com', 'User-Agent': 'DiscordBot (https://github.com/Rapptz/discord.py 1.3.1) Python/3.8 aiohttp/3.6.2', 'X-Ratelimit-Precision': 'millisecond', 'Authorization': 'Bot ' + token, 'Content-Type': 'application/json', 'Accept': '*/*', 'Cookie': '__cfduid=d5a6acaee7ff42669dbe5bfe96e9bf1ca1582474864; __cfruid=714eca7b59808b544e5f2336f83f14db04e8eec1-1582474864', 'Accept-Encoding': 'gzip, deflate'},data=json.dumps({"content": response}))     #sends a PM to the author
    r = requests.patch("https://discordapp.com/api/v7/channels/" + str(dmid) + "/messages/" + str(latest.id),headers={'Host': 'discordapp.com', 'User-Agent': 'DiscordBot (https://github.com/Rapptz/discord.py 1.3.1) Python/3.8 aiohttp/3.6.2', 'X-Ratelimit-Precision': 'millisecond', 'Authorization': 'Bot ' + token, 'Content-Type': 'application/json', 'Accept': '*/*', 'Cookie': '__cfduid=db6e920123b8a45e9806cb31eab21ad711582486918; __cfruid=f1339618e2889d475c5cd64dd99b132fef73d7b7-1582486918', 'Accept-Encoding': 'gzip, deflate'},data='{"content":"Finished"}')   # edits the message

class MyClient(discord.Client):
    usage = {}
    async def on_ready(self):
        print("logged in")
    
    async def on_message(self, message):
        
        global response
        
        if message.author == client.user:
            return

        if message.content == "$help": #help command
            await message.channel.send("Use $combo + link \n e.g. $combo https://cdn.discordapp.com/attachments/402887105820229633/680436463761883141/46k_es.txt") #sends the answer in the same channel


        if message.content.startswith("$combo"):    #combo command
            latest = await message.author.send("Started editing the Combo") #sends the answer in the same channel
            threading.Thread(target=self.linksender,args=[message,latest]).start()  #starts threads for requests to the api
            await message.delete()  #deletes the command message

            
    def linksender(self,message,latest):
        global response
        url = ["http://localhost:1337/comboapi?url=","http://localhost:1338/comboapi?url=","http://localhost:1339/comboapi?url=","http://localhost:1340/comboapi?url="]
        bid = message.content.split(" ")[1]
        print(bid)
        r = requests.get(random.choice(url) + bid)  #makes a get request to a random port to the local api
        response = r.text
        print(r.text)
        dm(message,latest)




client = MyClient()
client.run(token)