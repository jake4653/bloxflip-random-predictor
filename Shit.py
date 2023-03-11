import discord
from discord.ext import commands
import cloudscraper
import random
bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
scraper = cloudscraper.create_scraper(browser={'custom': 'ScraperBot/1.0'})

@bot.command()
async def mines(ctx, spots: int):
    if spots < 0 or spots > 25:
        await ctx.send("Please provide a number between 0 and 25.")
        return
    spots_list = random.sample(range(25), spots)
    bombs = random.randint(0, 5)
    bomb_spots = random.sample([i for i in range(25) if i not in spots_list], bombs)

    grid = ""
    for i in range(25):
        if i in spots_list:
            grid += "✅"
        elif i in bomb_spots:
            grid += "💣"
        else:
            grid += "❌"

        if (i + 1) % 5 == 0:
            grid += "\n"

    embed = discord.Embed(title=f"Mines with {spots} spots", description=grid, color=discord.Color.purple())
    pfp = 'https://cdn.discordapp.com/attachments/1079890703137648710/1081642567621423194/a.gif'
    embed.set_footer(text="✅: Safe | 💣: Bomb | ❌: Unknown\nMade by Semai")
    embed.set_thumbnail(url=pfp)
    await ctx.send(embed=embed)




@bot.command()
async def towers(ctx, rows: int):
    if rows < 1 or rows > 8:
        await ctx.send("Please provide a number between 1 and 8.")
        return
    
    grid = ""
    for i in range(rows):
        checkmark_position = random.randint(0, 2)
        bomb_position = random.randint(0, 2)
        while bomb_position == checkmark_position:
            bomb_position = random.randint(0, 2)

        row = ""
        for j in range(3):
            if j == checkmark_position:
                row += "✅"
            elif j == bomb_position:
                row += "💣"
            else:
                row += "❓"

        grid += row + "\n"

    embed = discord.Embed(title=f"Towers with {rows} rows", description=grid, color=discord.Color.purple())
    pfp = 'https://cdn.discordapp.com/attachments/1079890703137648710/1081642567621423194/a.gif'
    embed.set_thumbnail(url=pfp)
    embed.set_footer(text="✅: Safe | 💣: Bomb | ❓: Unknown\nMade by Semai")
    await ctx.send(embed=embed)

@bot.command()
async def roulette(ctx):
    colors = [":red_square:", ":yellow_square:", ":purple_square:"]
    accuracy = [random.uniform(0.0, 1.0) * 100 for _ in range(3)]
    accuracy[1] = random.uniform(0.0, 0.1) * 100 
    
    embed = discord.Embed(title="Roulette", color=discord.Color.purple())
    pfp = 'https://cdn.discordapp.com/attachments/1079890703137648710/1081642567621423194/a.gif'
    embed.set_thumbnail(url=pfp)
    embed.add_field(name=colors[0], value=f"Accuracy: {accuracy[0]:.2f}%")
    embed.add_field(name=colors[1], value=f"Accuracy: {accuracy[1]:.2f}%")
    embed.add_field(name=colors[2], value=f"Accuracy: {accuracy[2]:.2f}%")
    embed.set_footer(text="Higher the accuracy higher the chance of you winning.\nMade by Semai")

    
    await ctx.send(embed=embed)
@bot.command()
async def crash(ctx):
    games = scraper.get("https://rest-bf.blox.land/games/crash").json()

    def prediction():
        r = scraper.get(
            "https://rest-bf.blox.land/games/crash").json()["history"]
        yield [
            r[0]["crashPoint"],
            [float(crashpoint["crashPoint"]) for crashpoint in r[-2:]]
        ]

    for game in prediction():
        games = game[1]
        avg = sum(games) / len(games)
        chance = 1
        for game in games:
            chance = chance = 95 / game
            prediction = (1 / (1 - (chance)) + avg) / 2

    desc = f"""
**🎰 Crash Prediction:** {prediction:.2f}x
**🎲 Accuracy:** {chance:.2f}%
        """
    em = discord.Embed(title="🚀 Prediction Results", description=desc, color=0x9b59b6)
    em.set_footer(text="Higher the accuracy higher the chance of you winning.\nMade by Semai")
    pfp = 'https://cdn.discordapp.com/attachments/1079890703137648710/1081642567621423194/a.gif'
    em.set_thumbnail(url=pfp)
    await ctx.send(embed=em)
@bot.command()
async def cmds(ctx):
    embed=discord.Embed(color=0x9b59b6)
    pfp = 'https://cdn.discordapp.com/attachments/1079890703137648710/1081642567621423194/a.gif'
    embed.set_thumbnail(url=pfp)
    embed.add_field(name="*Commands*", value=f"**.mines (spots)**\n**.towers (rows)**\n**.roulette**\n**.crash**\n")
    embed.set_footer(text="Made by Semai")
    await ctx.reply(embed=embed)
    
    

bot.run("TOKENHERE")
