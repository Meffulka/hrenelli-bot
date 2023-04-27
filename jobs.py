from db import User
import godvile
import bot

async def update_user():
    user = await User.get_first_user_not_updated_async()
    if user:
        hero_json, status = godvile.get_hero(user.name)
        if status == 200:
            new_clan = hero_json.get('clan', None)
            new_clan_position = hero_json.get('clan_position', None)
            new_alignment = hero_json.get('alignment', None)

            if user.clan != new_clan and new_clan != "Хренелли":
                await bot.remove_all_roles(user.discord_id)
            elif user.clan_position != new_clan_position or user.alignment != new_alignment:
                await bot.update_user(user.discord_id)
            await User.upsert_user(hero_json, user.discord_id)
        else:
            print(f"Ошибка при получении данных героя: {status}")
