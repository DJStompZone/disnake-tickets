import subprocess, threading, disnake, asyncio, os
from disnake.ext import commands 
from subprocess import run as sh

TOKEN = os.environ.get('TOKEN')
prefix = '!'
intents = disnake.Intents().all()
intents.members = True
bot = commands.Bot(
      command_prefix=prefix,
      case_insensitive=True, 
      intents=INTENTS,
      test_guilds=os.environ.get('GUILDS'),
      sync_commands_debug=True)

# bot.remove_command('help')


def zoom():
    while True:
        try:
            task, arg1, arg2 = queue.pop(0).split('-')
            sh([f'{task}', f'{arg1}', f'{arg2}'])
        except:
            pass

threading.Thread(target=zoom).start()

@bot.event
async def on_ready():
    print(f'Servers: {len(bot.guilds)}')
#    for guild in bot.guilds:
#        print(guild.name)
#    print()
#    while True:
#        members = sum([guild.member_count for guild in bot.guilds])
#        activity = disnake.Activity(type=disnake.ActivityType.watching, name=f'{members} users!')
#        await bot.change_presence(activity=activity)
#        await asyncio.sleep(60)


@bot.event
async def on_command_error(ctx, error: Exception):
    if ctx.channel.id == bots_channel:
        if isinstance(error, commands.CommandOnCooldown):
            embed = disnake.Embed(color=16379747, description=f'{error}')
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingRequiredArgument):
            embed = disnake.Embed(color=16379747, description='Missing arguments required to use this command!')
            await ctx.send(embed=embed)
            ctx.command.reset_cooldown(ctx)
        elif 'You do not own this bot.' in str(error):
            embed = disnake.Embed(color=16379747, description='You **DON'T** have permission to use this command!')
            await ctx.send(embed=embed)
        else:
            print(str(error))
    else:
        try:
            await ctx.message.delete()
        except:
            pass

@bot.slash_command()
async def help(ctx):
    print(f'{ctx.author} | {ctx.author.id} ->!help')
    if ctx.channel.type != disnake.ChannelType.private:
        embed = disnake.Embed(color=16379747)
        embed.add_field(name='Help', value='`!help`', inline=True)
        embed.add_field(name='Open Ticket', value='`!ticket`', inline=True)
        embed.add_field(name='Close Ticket', value='`!close`', inline=True)
        await ctx.send(embed=embed)

@bot.slash_command()
async def ticket(ctx):
    print(f'{ctx.author} | {ctx.author.id} ->!ticket')
    if ctx.channel.type != disnake.ChannelType.private:
        channels = [str(x) for x in bot.get_all_channels()]
        if f'ticket-{ctx.author.id}' in str(channels):
            embed = disnake.Embed(color=16379747, description='You already have a ticket open!')
            await ctx.reply(embed=embed)
        else:
            ticket_channel = await ctx.Dr guild.create_text_channel(f'ticket-{ctx.message.author.name}')
            await ticket_channel.set_permissions(ctx.guild.get_role(ctx.guild.id), send_messages=False, read_messages=False)
            await ticket_channel.set_permissions(ctx.author, send_messages=True, read_messages=True, add_reactions=True, embed_links=True, attach_files=True, read_message_history=True, external_emojis=True)
            embed = disnake.Embed(color=16379747, description='Please enter the reason for this ticket, type `!close` if you want to close this ticket.')
            await ticket_channel.send(f'{ctx.author.mention}', embed=embed)
            await ctx.message.delete()

@bot.slash_command()
async def close(ctx):
    print(f'{ctx.author} | {ctx.author.id} ->!close')
    if ctx.channel.type != disnake.ChannelType.private:
        if ctx.channel.name == f'ticket-{ctx.message.author.name}':
            await ctx.channel.delete()
        elif ctx.author.id in administrators and 'ticket' in ctx.channel.name:
            await ctx.channel.delete()
        else:
            embed = disnake.Embed(color=16379747, description=f'You do not have permission to run this command!')
            await ctx.reply(embed=embed)

if __name__ == "__main__":
  bot.run(TOKEN)
