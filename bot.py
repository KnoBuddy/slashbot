import disnake # The whole bot relies on this
import os # This is just used for some basic stuff like making directories and looking for files
import asyncio # This allows us to pause a function and wait until a certain event happens
import json5 as json # This is used to load the config file

from disnake.ext.commands import Bot # This imports the class Bot from the disnake.ext.commands module, which is used to create the bot

# Init Vars
ran = False # Used to check if the cogs have been loaded before
with open('config.json') as file: # Open config.json
    config = json.load(file) # Load config.json

# Init Bot
bot = Bot(intents=disnake.Intents.all())  # We are literally creating a copy of the Bot class, but with a few extra things

# Load Cogs
async def load_cogs():  # Cogs are like normal python files, but they are used to add features and make it easier to manage
    global ran # We need to use the global ran variable
    if ran == False: # If the cogs haven't been loaded before
        for filename in os.listdir('./cogs'): # Loop through all files in the cogs folder
            if filename.endswith('.py'): # If the file ends with .py
                try:
                    bot.load_extension(f'cogs.{filename[:-3]}') # Load the cog
                    print(f'{filename[:-3]} loaded!') # Print that the cog has been loaded
                    ran = True
                except Exception as e: 
                    exception = f'{type(e).__name__}: {e}'  
                    print(f'Failed to load extension {filename[:-3]}' + exception)
    else: # If the cogs have been loaded before
        print('Reloading Cogs...') 
        for filename in os.listdir('./cogs'): # Loop through all files in the cogs folder
            if filename.endswith('.py'): # If the file ends with .py
                try:
                    bot.reload_extension(f'cogs.{filename[:-3]}') # Reload the cog
                    print(f'{filename[:-3]} reloaded!')
                except Exception as e:
                    exception = f'{type(e).__name__}: {e}'
                    print(f'Failed to reload extension {filename[:-3]}' + exception)

# Events
@bot.event
async def on_ready(): # This event is called when the bot is ready
    print(f'Logged in as {bot.user} (ID: {bot.user.id})') # Print that the bot is ready

@bot.event
async def on_message(message): # This event is called when a message is sent
    if message.author.bot: # If the message was sent by a bot
        return # Return, so the bot doesn't respond to itself
    await bot.process_commands(message) # This is needed to make commands work

# Here is an example of how create your first slash command
@bot.slash_command(name='ping')
async def ping(interaction: disnake.ApplicationCommandInteraction):
    await interaction.response.send_message(f'Pong! {round(bot.latency * 1000)}ms')

# We will be using cogs, which are like normal python files, but they are used to add features and make it easier to manage
# This is a slash command to reload all the cogs
@bot.slash_command(
    name="reload-cogs",
    description="Reload cogs!"
)
async def reload_cogs(interaction: disnake.ApplicationCommandInteraction) -> None:
    await interaction.response.send_message("Reloading cogs...")
    await load_cogs()

# Run Bot
if __name__ == '__main__': 
    asyncio.run(load_cogs()) # Load the cogs
    bot.run(config['token']) # Run the bot using the token we got from config.json