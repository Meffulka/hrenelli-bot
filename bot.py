# This example requires the 'message_content' intent.

import discord
import godvile
import config
from helpers import is_good_god, is_higher_than_cardinal

intents = discord.Intents.all()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

# @client.event

# async def on_member_join (member):
#     log_channel = client.get_channel(1099062165270450276)
#     channel = client.get_channel(1099060395186061374)
#     await log_channel.send(f'``{member.name}`` присоиединился')
#     await channel.send(f'Привет, {member.name}! Отправь мне в личные сообщения имя своего бога и токен через пробел')


@client.event
async def on_message(message):
    log_channel = client.get_channel(int(config.LOG_CHANNEL))
    server = client.get_guild(int(config.SERVER_ID))
    if message.author == client.user:
        return
    if not message.guild:
        god_name, token = message.content.split(':')
        hero, status = godvile.get_hero(god_name=god_name,token=token)
        if status==200 and hero['clan'] == "Хренелли":
            await log_channel.send(f'``{message.author}`` привязал бога ``{god_name}``')
            await message.author.send("Привязал, спасибо!")
            if is_good_god(hero['alignment']):
                role = discord.utils.get(server.roles, name = "Отступник")
            else:
                if is_higher_than_cardinal(hero['clan_position']):
                    role = discord.utils.get(server.roles, name = "Семья")
                else:
                    role = discord.utils.get(server.roles, name = "Соучастник")
            member = server.get_member(message.author.id)
            await member.add_roles(role)
            await log_channel.send(f'``{message.author}`` выдана роль ``{role.name}``')
            if member.id != server.owner_id:
                try:
                    await member.edit(nick=god_name)
                    await log_channel.send(f'``{message.author}`` поменян ник на  {god_name}')
                except discord.Forbidden:
                    await log_channel.send(f'Не хватило прав на изменения ника для ``{message.author}``')
        else:
            await log_channel.send(f'``{message.author}`` неудачно пытался привязать бога ``{god_name}``')
            await message.author.send("Что-то пошло не так. Попробуй еще раз в фомате: 'имя_бога:токен'")

client.run(config.DC_TOKEN)
