# This example requires the 'message_content' intent.

import discord
import godvile
import config
from helpers import is_good_god, is_higher_than_cardinal
from db import User
import io

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

    if message.author == client.user:
        return
    if not message.guild:
        try:
            god_name, token = message.content.split(':')
            hero_json, status = godvile.get_hero(god_name=god_name,token=token)
            curent_user = await User.get_user_by_discord_id(message.author.id)
            if curent_user:
                hero = await User.upsert_user(hero_json, message.author.id, token)
                await update_user(hero.discord_id)
                await message.author.send("Обновил, спасибо!")
            else:
                hero = await User.upsert_user(hero_json, message.author.id, token)
                if status==200 and hero.clan == "Хренелли":
                    await update_user(hero.discord_id)
                    await message.author.send("Привязал, спасибо!")
                    await logger(f'``{message.author}`` привязал бога ``{hero.godname}``')
                else:
                    await logger(f'``{message.author}`` неудачно пытался привязать бога ``{god_name}``')
                    await message.author.send("Что-то пошло не так. Попробуй еще раз в фомате: 'имя_бога:токен'")
        except Exception as e:
            print(e)

async def logger(text):
    log_channel = client.get_channel(int(config.LOG_CHANNEL))
    await log_channel.send(text)

async def update_user(discord_id):
    try:
        server = client.get_guild(int(config.SERVER_ID))
        member = server.get_member(discord_id)
        member_roles = [role.name for role in member.roles if role.name == "Отступник" or role.name == "Семья" or role.name == "Соучастник"]
        hero = await User.get_user_by_discord_id(discord_id=discord_id)

        if is_good_god(hero.alignment):
            role = discord.utils.get(server.roles, name = "Отступник")
        else:
            if is_higher_than_cardinal(hero.clan_position):
                role = discord.utils.get(server.roles, name = "Семья")
            else:
                role = discord.utils.get(server.roles, name = "Соучастник")
        if role.name not in member_roles:
            await member.add_roles(role)
            await logger(f'``{member.name}`` выдана роль ``{role.name}``')

        for r in [r for r in member_roles if r != role.name]:
            remove_role = discord.utils.get(server.roles, name = r)
            member.remove_roles(remove_role)
            await logger(f'``{member.name}`` удалена роль ``{role.name}``')

        if member.id != server.owner_id and (hero.godname != member.nick or hero.godname != member.display_name):
            try:
                await member.edit(nick=hero.godname)
                await logger(f'``{member.name}`` поменян ник на  ``{hero.godname}``')
            except discord.Forbidden:
                await logger(f'Не хватило прав на изменения ника для ``{member.name}``')
    except Exception as e:
        print(e)

async def remove_all_roles(discord_id):
    server = client.get_guild(int(config.SERVER_ID))
    member = server.get_member(discord_id)
    member_roles = [role.name for role in member.roles if role.name != server.default_role]
    for r in member_roles:
        remove_role = discord.utils.get(server.roles, name = r)
        member.remove_roles(remove_role)
        await logger(f'``{member.name}`` удалена роль ``{r}``')

async def send_screenshot(screenshot_bytes):
    channel = client.get_channel(int(config.CROSS_CHANNEL))
    screenshot_file = discord.File(io.BytesIO(screenshot_bytes), filename="element_screenshot.png")
    await channel.send(file=screenshot_file)