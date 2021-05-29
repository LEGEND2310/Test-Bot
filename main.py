import discord
import os
import requests
import json
import random
from replit import db
from keepalive import keep_alive

client = discord.Client()

sad_words = ['sad', 'depressed', 'unhappy', 'angry', 'miserable', 'depressing']

starter_encouragements = [
  'Cheer Up!',
  'Hang in there bud',
  'You are awesome'
]

if "responding" not in db.keys():
  db["responding"] = True

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return quote

def update_encouragements(enc_msg):
  if 'encouragements' in db.keys():
    encouragements = list(db["encouragements"])
    encouragements.append(enc_msg)
    db["encouragements"] = encouragements
  else:
    db["encouragements"] = [enc_msg]

def delete_encouragement(index):
  encouragements = list(db["encouragements"])
  if len(encouragements) > index:
    del encouragements[index]
    db["encouragements"] = encouragements

def get_meme():
  response = requests.get("https://some-random-api.ml/meme")
  json_data = json.loads(response.text)
  image = json_data['image']
  cap = json_data['caption']
  return(image, cap)


@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  msg = message.content
  
  if msg.startswith('$inspire'):
    quote = get_quote()
    await message.channel.send("Hey there {}! Here's your inspiration for the day - {}".format(message.author.name, quote))

  if msg.startswith('$meme'):
    image, cap = get_meme()
    await message.channel.send(image)
    await message.channel.send(cap)

  if db["responding"]:
    options = starter_encouragements
    if "encouragements" in db.keys():
      options = options + list(db["encouragements"])

    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(options))

  if msg.startswith("$new"):
    enc_msg = msg.split("$new ",1)[1]
    update_encouragements(enc_msg)
    await message.channel.send("New encouraging message added!")

  if msg.startswith("$del"):
    encouragements = []
    if "encouragements" in db.keys():
      index = int(msg.split("$del",1)[1])
      delete_encouragement(index)
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)

  if msg.startswith("$list"):
    encouragements = []
    if "encouragements" in db.keys():
      encouragements = list(db["encouragements"])
    await message.channel.send(encouragements)

  if msg.startswith("$responding"):
    value = msg.split("$responding ",1)[1]

    if value.lower() == "true":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    
    else:
      db["responding"] = False
      await message.channel.send("Responding is off.")

keep_alive()
client.run(os.getenv('TOKEN')) 