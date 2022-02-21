from discord.ext import  commands
from datetime import datetime
from colorama import init
import nest_asyncio
import threading
import requests
import discord
import asyncio
import time

botToken = "token" #Your bots token goes here
webHook = "https://discord.com/api/webhooks/" #Web hook to send name alert to
Webhook = "https://discord.com/api/webhooks/" #Hall Of Shame 

access = [
	"ID" #channel ids for commands
		]

bot = commands.Bot(command_prefix="+", help_command=None)

def add_Reminder(name):
	r = requests.get(f"http://api.star.shopping/droptime/{name}", headers={"User-Agent": "Sniper"})

	if r.status_code >= 400:
		requests.post(webHook, json={"embeds": [{"title": "Error", "description": f"This name isn't dropping", "color": 15533317}]})
	else:
		dropTime = float(r.json()["unix"])

		while dropTime > time.time():
			if(int(dropTime-60) == int(time.time())):
				requests.post(webHook, json={"embeds": [{"title": "Warning", "description": f"The name {name} is dropping in 1 minute", "color": 15533317}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})
				time.sleep(1) 
			elif(int(dropTime-300) == int(time.time())):
				requests.post(webHook, json={"embeds": [{"title": "Warning", "description": f"The name {name} is dropping in 5 minutes", "color": 15548679}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})
				time.sleep(1)
			elif(int(dropTime-600) == int(time.time())):
				requests.post(webHook, json={"embeds": [{"title": "Warning", "description": f"The name {name} is dropping in 10 minutes", "color": 15767830}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})
				time.sleep(1)
			elif(int(dropTime-1800) == int(time.time())):
				requests.post(webHook, json={"embeds": [{"title": "Warning", "description": f"The name {name} is dropping in 30 minutes", "color": 2538802}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})
				time.sleep(1)

		requests.post(webHook, json={"embeds": [{"title": "Dropped", "description": f"The name {name} has dropped", "color": 1406952}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})

@bot.event
async def on_ready():
	print(f'\033[90m[\033[92m+\033[90m]\033[39m {bot.user} Is now: \033[92mOnline\033[39m')

@bot.command(name='remind', description="Set a reminder for a name")
async def set_reminder(ctx, name):
	if(str(ctx.message.channel.id) in access):
		await ctx.send(f"Setting reminder for: {name}")
		print(f"\033[90m[\033[92m+\033[90m]\033[39m {ctx.message.author} Setting reminder for: {name}")
		threading.Thread(target=add_Reminder, args=(name,)).start()
	else:
		print(f"\033[90m[\033[92m+\033[90m]\033[39m {ctx.message.author.id} : ({ctx.message.author}) Tried to set a reminder without access")
		await ctx.reply(f"You just tried to set a reminder in a non access channel")
		requests.post(Webhook, json={"embeds": [{"title": "Hall Of Shame", "description": f"{ctx.message.author} Tried to set a reminder in a non access channel", "color": 15533317}], "content": "[](@everyone)", "allowed_mentions": { "parse": ["everyone"] }})
		time.sleep(60) 

nest_asyncio.apply()
init() 
bot.run(botToken) 
