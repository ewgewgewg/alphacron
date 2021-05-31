import discord
import os
import datetime
import urllib.request
import requests
import inspect
from actions.guessNumber import guessNumber
from actions.toArchive import toArchive
from actions.stale import stale

from keep_alive import keep_alive
token = os.environ['TOKEN']

client = discord.Client()

thresholdDays = 30
lastDays = 6

@client.event
async def on_ready():
  print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith('$whatcategory'):
    print(message.channel.category)
    await message.channel.send(message.channel.category)
    return
  
  if message.content.startswith('$callbotstring'):
    date = datetime.datetime.now()
    await message.channel.send(f'alphacron says hello to {message.author} on {date} in channel at position {message.channel.position}!')
    return

  if message.content.startswith('$staleprintdebug'):
    staleList = await stale(message, thresholdDays)
    print('these are stale channels')
    await message.channel.send('these are stale channels')
    for staleItem in staleList:
      print(staleItem.name)
      await message.channel.send(f'alphacron thinks {staleItem.name} is a stale channel!')
    return

  if message.content.startswith('Weekly cleanup check!'):
    staleList = await stale(message, thresholdDays)
    print('these are stale channels')
    for staleItem in staleList:
      print(staleItem.name)
      await staleItem.send(f'Inactivity Warning! This is a stale channel, and has been inactive for greater than the following number of days: {thresholdDays}. In about {lastDays+1} days this channel will be moved to Archive unless new activity appears. This is an automatic message.')

    channels = message.guild.channels
    for channel in channels:
          print(channel.name)
          try:
            last = channel.last_message_id
            if last:
              now = datetime.datetime.now()
              curmessage = await channel.fetch_message(last)
              created = curmessage.created_at
              since = now - created
              text = curmessage.content
              if text.startswith('Inactivity Warning! This is a stale channel, and') and since.days >= lastDays:
                await toArchive(curmessage)
            else:
              pass
          except:
            print('no messages possible in this channel type!')

  if message.content.startswith('$_toarchive'):
    await toArchive(message)

  if message.content.startswith('$get-hacker-news'):
    # get top stories IDS
    with urllib.request.urlopen('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty') as response:
      top_story_ids = response.read()
      # only_five = top_story_ids[0:4]
      # use IDS to fetch top story URLS (and blurbs?)
      print(top_story_ids)

  if message.content.startswith('$test-get'):
    tester = requests.get('https://hacker-news.firebaseio.com/v0/topstories.json?print=pretty')
    top_story_ids = tester[0:4]
    print(top_story_ids)

  if message.content.startswith("?guess a number"):
    await guessNumber(client, message)

keep_alive(client)
client.run(token)