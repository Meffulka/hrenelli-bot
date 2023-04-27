from db import User
import godvile
import bot
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


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

async def cross():
    try:
        url = "https://gv.erinome.net/db?cross=current&lang=ru"  # Замените на URL страницы, которую хотите открыть
        element_selector = "body > div.wrapper > div:nth-child(2) > div.cdata.crosshinter > table > tbody"
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
        driver.set_window_size(1280, 720)
        driver.get(url)
        element = driver.find_element(By.CSS_SELECTOR, element_selector)
        screenshot_bytes = element.screenshot_as_png
        driver.quit()
        await bot.send_screenshot(screenshot_bytes)
    except Exception as e:
        print(e)