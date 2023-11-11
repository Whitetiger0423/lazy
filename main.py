import pickle
import random
import os
import discord

bot = discord.Bot()
token = "MTE3Mjg2NzQ3MjU2Nzg0NDk2NQ.G2DEfI.gb3ZMyMsAgaMzvahL4wDufrTq9-7gydnyS9b9k"


ItemRate = ["C"] * 60 + ["B"] * 25 + ["A"] * 13 + ["S"] * 2


@bot.event
async def on_ready():
    print(f"Log In as {bot.user.name}({bot.user.id})")


@bot.slash_command(description="유저 정보를 등록합니다.")
async def 등록(ctx):
    if os.path.isfile(f"{ctx.user.id}.pkl") == False:
        embed = discord.Embed(
            title="등록", description="봇의 서비스에 등록합니다. 동의하지 않을 경우 서비스 이용에 제한이 있을 수 있습니다."
        )
        embed.add_field(name="수집하는 정보", value="유저의 디스코드 id", inline=False)

        class Button(discord.ui.View):
            @discord.ui.button(label="⭕ 동의", style=discord.ButtonStyle.primary)
            async def primary(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                UserData = []
                if interaction.user.id == ctx.user.id:
                    with open(f"{interaction.user.id}.pkl", "wb") as f:
                        pickle.dump(UserData, f)
                    await ctx.respond(
                        f"<@!{interaction.user.id}>님, 등록을 완료하였습니다. 아이디는 {interaction.user.id}입니다."
                    )
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self)

            @discord.ui.button(label="❌ 취소", style=discord.ButtonStyle.danger)
            async def danger(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    await ctx.respond(f"등록을 취소하였습니다.")
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self)

        await ctx.respond(embed=embed, view=Button())

    else:
        embed = discord.Embed(title="등록된 유저", description="")
        embed.add_field(
            name="", value="이미 등록되었습니다. `/탈퇴` 명령어를 통해 탈퇴할 수 있습니다.", inline=False
        )
        await ctx.respond(embed=embed)


@bot.slash_command(description="봇 서비스를 탈퇴합니다.")
async def 탈퇴(ctx):
    if os.path.isfile(f"{ctx.user.id}.pkl"):
        embed = discord.Embed(
            title="탈퇴", description="봇의 서비스를 탈퇴합니다. 탈퇴할 경우 모든 데이터가 파기되며, 복구하기 어렵습니다."
        )
        embed.add_field(
            name="파기하는 정보", value="유저의 디스코드 id, 서비스 이용 중 가챠 기록", inline=False
        )

        class Button(discord.ui.View):
            @discord.ui.button(label="⭕ 동의", style=discord.ButtonStyle.primary)
            async def primary(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    os.remove(f"{interaction.user.id}.pkl")
                    await ctx.respond(f"<@!{interaction.user.id}>님, 탈퇴가 완료되었습니다.")
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self)

            @discord.ui.button(label="❌ 취소", style=discord.ButtonStyle.danger)
            async def danger(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    await ctx.respond(f"탈퇴를 취소하였습니다.")
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self)

        await ctx.respond(embed=embed, view=Button())

    else:
        embed = discord.Embed(title="등록하지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입해주세요.", inline=False)
        await ctx.respond(embed=embed)


@bot.slash_command(description="가챠 기록을 확인합니다.")
async def 기록(ctx):
    if os.path.isfile(f"{ctx.user.id}.pkl"):
        with open(f"{ctx.user.id}.pkl", "rb") as f:
            UserData = pickle.load(f)
        embed = discord.Embed(title="가챠 기록", description="")
        embed.add_field(
            name="",
            value=f"""C: {UserData.count('C')}
B: {UserData.count('B')}
**A**: {UserData.count('A')}
***S***: {UserData.count('S')}""",
            inline=False,
        )
        embed.set_footer(text="나오는 카드의 등급은 C, B, A, S로 총 4종류입니다.")
    else:
        embed = discord.Embed(title="등록되지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입한 후 다시 사용해주세요.", inline=False)
    await ctx.respond(embed=embed)


def Gacha(x, UserID):
    result = []
    for i in range(x):
        result.append(random.choice(ItemRate))
    result.sort(key=lambda x: "CBAS".index(x))
    with open(f"{UserID}.pkl", "rb") as f:
        UserData = pickle.load(f)
    UserData.extend(result)
    with open(f"{UserID}.pkl", "wb") as f:
        pickle.dump(UserData, f)
    return result


@bot.slash_command(description="카드 가챠를 진행합니다.")
async def 가챠(ctx):
    if os.path.isfile(f"{ctx.user.id}.pkl"):
        embed = discord.Embed(title="가챠", description="")
        embed.add_field(name="", value="버튼을 누르면 가챠를 진행합니다.", inline=False)
        embed.set_footer(text="나오는 카드의 등급은 C, B, A, S로 총 4종류입니다.")

        class Button(discord.ui.View):
            @discord.ui.button(label="1회", style=discord.ButtonStyle.primary)
            async def OneTime(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    result = Gacha(1, ctx.user.id)
                    embed = discord.Embed(title="1회 가챠 결과", description="")
                    embed.add_field(
                        name=f"",
                        value=f"{' '.join(result).replace('C', '`C`').replace('B', '`B`').replace('A', '**`A`**').replace('S', '***`S`***')}",
                        inline=False,
                    )
                    embed.set_footer(text="전체 결과는 `/기록` 명령어를 통해 확인할 수 있습니다.")
                    await ctx.respond(embed=embed)
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self)

            @discord.ui.button(label="10회", style=discord.ButtonStyle.primary)
            async def TenTimes(
                self, button: discord.ui.Button, interaction: discord.Interaction
            ):
                if interaction.user.id == ctx.user.id:
                    result = Gacha(10, ctx.user.id)
                    embed = discord.Embed(title="10회 가챠 결과", description="")
                    embed.add_field(
                        name=f"",
                        value=f"{' '.join(result).replace('C', '`C`').replace('B', '`B`').replace('A', '**`A`**').replace('S', '***`S`***')}",
                        inline=False,
                    )
                    embed.set_footer(text="전체 결과는 `/기록` 명령어를 통해 확인할 수 있습니다.")
                    await ctx.respond(embed=embed)
                    self.disable_all_items()
                    await interaction.response.edit_message(view=self)

        await ctx.respond(embed=embed, view=Button())

    else:
        embed = discord.Embed(title="등록되지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입한 후 다시 사용해주세요.", inline=False)
        await ctx.respond(embed=embed)


MergeType = ["C 150 -> B 1", "B 100 -> A 1", "A 50 -> S 1"]


@bot.slash_command(description="카드 합성을 진행합니다.")
async def 합성(ctx, type: discord.Option(str, choices=MergeType)):
    if os.path.isfile(f"{ctx.user.id}.pkl"):
        with open(f"{ctx.user.id}.pkl", "rb") as f:
            UserData = pickle.load(f)
        if type == MergeType[0] and UserData.count("C") >= 150:
            for i in range(150):
                UserData.remove("C")
            UserData.append("B")
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            embed = discord.Embed(title="교환 완료", description="")
            embed.add_field(name="", value="C 카드 150개를 B 1개로 합성하였습니다.", inline=False)
            await ctx.respond(embed=embed)
        elif type == MergeType[1] and UserData.count("B") >= 100:
            for i in range(100):
                UserData.remove("B")
            UserData.append("A")
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            embed = discord.Embed(title="교환 완료", description="")
            embed.add_field(name="", value="B 카드 100개를 A 1개로 합성하였습니다.", inline=False)
            await ctx.respond(embed=embed)
        elif type == MergeType[0] and UserData.count("A") >= 50:
            for i in range(50):
                UserData.remove("A")
            UserData.append("S")
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            embed = discord.Embed(title="교환 완료", description="")
            embed.add_field(name="", value="A 카드 50개를 S 1개로 합성하였습니다.", inline=False)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="개수 부족", description="")
            embed.add_field(name="", value="교환하려는 카드의 개수와 종류를 확인해주세요.", inline=False)
            await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(title="등록되지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입한 후 다시 사용해주세요.", inline=False)
        await ctx.respond(embed=embed)


bot.run(token)
