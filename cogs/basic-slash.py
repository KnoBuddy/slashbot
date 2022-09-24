import disnake # This is used for the bot
import random # This is used to generate random numbers
import json5 as json # This is used to load the config file

from bot import load_cogs # This loads the function load_cogs from bot.py

from disnake import ApplicationCommandInteraction, Option, OptionType # This is used for slash commands
from disnake.ext import commands, tasks # This is used for the bot

# Init Vars
with open('config.json') as file: # This opens the config file
    config = json.load(file) # This loads the config file

class Buttons(disnake.ui.View): # This creates a class for buttons
    def __init__(self, *, timeout=180): 
        super().__init__(timeout=timeout)

    @disnake.ui.button(label='Button 1', style=disnake.ButtonStyle.blurple) # This creates a button
    async def button1(self, button: disnake.ui.Button, interaction: disnake.Interaction): # This function runs when the button is clicked
        button.style = disnake.ButtonStyle.red # This changes the style of the button
        await interaction.response.edit_message('Button 1 clicked', view=self) # This edits the message and changes the reloads the button with the new style
    
    @disnake.ui.button(label='Button 2', style=disnake.ButtonStyle.blurple)
    async def button2(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        button.style = disnake.ButtonStyle.green
        await interaction.response.edit_message('Button 2 clicked', view=self)

class Basic(commands.Cog, name="basic-slash"): # This creates a class for the Basic Commands cog
    def __init__(self, bot): 
        self.bot = bot  # This sets the bot variable to the bot
        self.spam_bool = False # This is used to check if the spam command is running
    
    @commands.Cog.listener() # This listends for the event on_ready
    async def on_ready(self) -> None: # This function runs when the bot is ready
        print(f'{self.bot.user} is ready!') 
        await self.bg_worker.start() # This starts the background task

    # This is your basic Slash Command
    @commands.slash_command( # This creates a slash command
        name="wave", # This is the name of the slash command
        description="Wave back at a user!" # This is the description of the slash command
    )
    async def wave(self, interaction: ApplicationCommandInteraction) -> None: # This function runs when the slash command is used
        await interaction.response.send_message(f"Hello!") # This sends a message in the channel the slash command was used in
    
    # This is a more advanced slash command
    @commands.slash_command( # This creates a slash command
        name="backtalk", # This is the name of the slash command
        description="Backtalk a user!", # This is the description of the slash command
        options=[ # This is the options for the slash command
            Option( # This creates an option
                name="user", # This is the name of the option
                description="The user to backtalk", # This is the description of the option
                type=OptionType.string, # This is the type of the option
                required=True # This makes the option required
            )
        ]
    )
    async def backtalk(self, interaction: ApplicationCommandInteraction, user: disnake.User) -> None:   # This is a joke function to show an example of how to use options
        # roll random number and send a different message depending on the number
        number = random.randint(1, 3)
        if number == 1:
            await interaction.response.send_message(f"Shut up {user}!") 
        elif number == 2:
            await interaction.response.send_message(f"Screw off! {user}!")
        elif number == 3:
            await interaction.response.send_message(f"Go away {user}!")

    # Here is an example of how to use an embed
    @commands.slash_command( 
        name="send-embed",
        description="Send an embed!"
    )
    async def send_embed(self, interaction: ApplicationCommandInteraction) -> None:
        # There are two way you can send the embed. I reccomend declaring the embed first and then sending it
        # This is the first way
        embed = disnake.Embed( # This creates an embed
            title="Embed Title", # This is the title of the embed
            description="Embed Description", # This is the description of the embed
            color=disnake.Color.blurple() # This is the color of the embed
        )
        embed.add_field(name="Field 1", value="Value 1") # This adds a field to the embed
        embed.add_field(name="Field 2", value="Value 2") # This adds a field to the embed
        embed.add_field(name="Field 3", value="Value 3") # This adds a field to the embed
        await interaction.response.send_message(embed=embed) # This sends the embed in the channel the slash command was used in

        # This is the second way
        # Both ways work, but as you can see the second way is a bit messy
        await interaction.response.send_message(embed=disnake.Embed(
            title="Embed Title",
            description="Embed Description",
            color=disnake.Color.blurple()
        ).add_field(name="Field 1", value="Value 1").add_field(name="Field 2", value="Value 2").add_field(name="Field 3", value="Value 3"))

        # Now you can also edit the interaction response and the embed
        embed = disnake.Embed( 
            title="I edited the embed!",
            description="Python is cool!",
            color=disnake.Color.red()
        )
        await interaction.response.edit_message(embed=embed) # This edits the message and changes the embed

    # Here is an example of sending an embed with buttons
    @commands.slash_command(
        name="send-embed-buttons",
        description="Send buttons!"
    )
    async def send_buttons(self, interaction: ApplicationCommandInteraction) -> None:
        embed = disnake.Embed(title="EMBED WITH BUTTONS", description="BUTTONS 'N EMBEDS", color=0x00FF00)
        await interaction.send(embed=embed, content="settings", view=Buttons(), ephemeral=True)

    # Here is an example of a stupid setting to toggle on and off to demonstrate how to spam using a background task
    @commands.slash_command(
        name="spam",
        description="Spam a channel!",
        type=OptionType.boolean
    )
    async def spam(self, interaction: ApplicationCommandInteraction, option: bool) -> None:
        self.spam_bool = option
        print(self.spam_bool)
        if self.spam_bool == True:
            await interaction.response.send_message("Spamming...")
        else:
            await interaction.response.send_message("Not spamming...")

    # Here is an example of a background task
    @tasks.loop(seconds=10)
    async def bg_worker(self):
        if self.spam_bool == True: # This checks if the spam setting is on
            # Use config['server_id'] to get the guid_id and the channel id
            guild = self.bot.get_guild(int(config['server_id']))
            channel = guild.get_channel(int(config['announ_channel_id']))
            print(f"Guild: {str(guild)} | Channel: {str(channel)}") # This prints the guild and channel to the console
            await channel.send(f"Guild: {str(guild)} | Channel: {str(channel)}") # This sends a message to the channel

def setup(bot):
    bot.add_cog(Basic(bot))
