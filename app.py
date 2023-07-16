import discord
import random

TOKEN = "YOUR_DISCORD_BOT_TOKEN"
client = discord.Client()

# Общая информация по игрокам
players = {}


# Класс игрока
class Player:
    def __init__(self, name):
        self.name = name
        self.location = None
        self.health = 100
        self.strength = 10
        self.magic = 20
        self.mental = 15
        self.inventory = []
        self.is_in_battle = False
        self.current_enemy = None


# Класс врага
class Enemy:
    def __init__(self, name, health, strength, magic, mental):
        self.name = name
        self.health = health
        self.strength = strength
        self.magic = magic
        self.mental = mental


# Локации в игре
locations = {
    "Темный замок": ["Гоблины", "Минотавр", "Лич"],
    "Гиблые топи": ["Волки", "Гоблины"],
    "Логово людоедов": ["Гоблины", "Мертвец"],
    "Форт Оберош": ["Гоблины", "Минотавр"],
}

# Сообщение с кнопками для выбора действия
message_template = (
    "Вы находитесь в **{location}**.\n"
    "Что вы хотите сделать?\n"
    "1. Выбрать локацию\n"
    "2. Характеристики персонажа\n"
    "3. Инвентарь\n"
    "4. Заклинания"
)


# Функция для создания и отправки сообщения с кнопками
async def send_menu(ctx):
    location = players[ctx.author.id].location
    menu = message_template.format(location=location)
    buttons = [
        discord.Button(label="Выбрать локацию", style=discord.ButtonStyle.blurple),
        discord.Button(label="Характеристики персонажа", style=discord.ButtonStyle.blurple),
        discord.Button(label="Инвентарь", style=discord.ButtonStyle.blurple),
        discord.Button(label="Заклинания", style=discord.ButtonStyle.blurple),
    ]
    action_row = discord.ActionRow(*buttons)
    await ctx.send(menu, components=[action_row])


# Функция для обработки нажатия кнопок
@client.event
async def on_button_click(interaction):
    if not interaction.author.id in players:
        return

    player = players[interaction.author.id]

    if interaction.component.label == "Выбрать локацию":
        await choose_location(interaction)
    elif interaction.component.label == "Характеристики персонажа":
        await show_character_stats(interaction)
    elif interaction.component.label == "Инвентарь":
        await show_inventory(interaction)
    elif interaction.component.label == "Заклинания":
        await show_spells(interaction)


# Функция для выбора локации
async def choose_location(interaction):
    if not players[interaction.author.id].is_in_battle:
        location_list = list(locations.keys())
        location = random.choice(location_list)
        players[interaction.author.id].location = location
        await send_menu(interaction)


# Функция для показа характеристик персонажа
async def show_character_stats(interaction):
    player = players[interaction.author.id]
    stats_message = (
        f"Характеристики для **{player.name}**:\n"
        f"Здоровье: {player.health}\n"
        f"Сила: {player.strength}\n"
        f"Магия: {player.magic}\n"
        f"Психика: {player.mental}\n"
    )
    await interaction.channel.send(stats_message)


# Функция для показа инвентаря
async def show_inventory(interaction):
    player = players[interaction.author.id]
    if not player.inventory:
        await interaction.channel.send("Ваш инвентарь пуст.")
    else:
        inventory_message = (
            f"Инвентарь для **{player.name}**:\n" + ", ".join(player.inventory)
        )
        await interaction.channel.send(inventory_message)


# Функция для показа заклинаний
async def show_spells(interaction):
    player = players[interaction.author.id]
    spells_message = f"Заклинания для **{player.name}**:\nМагия: {player.magic}"
    await interaction.channel.send(spells_message)


# Функция для обработки сообщений
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith("!start"):
        if not message.author.id in players:
            players[message.author.id] = Player(message.author.name)
            await choose_location(message)

    if message.content.startswith("!stop"):
        if message.author.id in players:
            del players[message.author.id]
            await message.channel.send("Игра остановлена.")


# Запуск бота
client.run(TOKEN)
