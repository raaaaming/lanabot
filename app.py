# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import os

import random

import discord
from discord import Option

bot = discord.Bot()
    
@bot.slash_command(name="안녕", description="라나와 인사하기")
async def hello(ctx):
    await ctx.respond("안녕하세요!")

@bot.slash_command(name="주사위", description="라나의 주사위 굴리기")
async def roll(ctx, max: Option(int, "주사위의 최댓값을 적어주세요!")):
    num = random.randrange(1, max + 1)
    await ctx.respond(f":game_die: *{max}!*")

@bot.slash_command(name="공지", description="라나의 공지 보내기")
async def notice(ctx, ch: Option(discord.TextChannel, "공지를 보낼 채널을 선택해주세요!"), message: Option(str, "공지할 메시지를 작성해주세요!")):
  if ctx.author.guild_permissions.administrator:
    embed = discord.Embed(title="공지사항", description=f"{message}", color=0x00ff00)
    embed.set_footer(text=f"Announce by {ctx.author}")
    await ch.send(embed=embed)
    await ctx.respond("공지를 전송했어요!")

@bot.slash_command(name="도움말", description="라나의 도움말 보기")
async def help(ctx):

    page = discord.Embed(title="도움말", color=0x00ff00)

    helpView = discord.ui.View(timeout=None)
    
    back = discord.ui.Button(style=discord.ButtonStyle.red, label='이전', emoji=u"\u2B05")
    next = discord.ui.Button(style=discord.ButtonStyle.green, label='다음', emoji=u"\u27A1")

    #view.add_item()

    async def back_button_callback(interaction: discord.Interaction):
        await ctx.send("이전")

    async def next_button_callback(interaction: discord.Interaction):
        await ctx.send("다음")

    back.callback = back_button_callback
    next.callback = next_button_callback

    helpView.add_item(back)
    helpView.add_item(next)

    await ctx.respond("도움말을 가져왔어요!")
    await ctx.send(embed=page, view=helpView)

@bot.slash_command(name="인증", descrption="라나의 인증하기")
async def check(ctx):
    guild_id = ctx.guild.id
    role = discord.utils.get(ctx.guild.roles, name="인증")
    
    view = discord.ui.View()
    button = discord.ui.Button(label="인증하기", style=discord.ButtonStyle.green)
    
    async def button_callback(interaction: discord.Interaction):
        await interaction.user.add_roles(role)
        await interaction.response.send_message("인증이 완료되었어요!")
    
    button.callback = button_callback
    view.add_item(button)
    
    await ctx.respond("인증하려면 아래 버튼을 눌러주세요!", view=view)

token = os.environ.get("TOKEN") or ""
bot.run(token)
