import pickle
import random
import os
import discord

bot = discord.Bot()
token = "MTE3Mjg2NzQ3MjU2Nzg0NDk2NQ.G2DEfI.gb3ZMyMsAgaMzvahL4wDufrTq9-7gydnyS9b9k"


# 확률: C60 B25 A13 S2


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
                UserData = [0, 0, 0, 0, 0]
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
            value=f"""C: {UserData[0]}
B: {UserData[1]}
**A**: {UserData[2]}
***S***: {UserData[3]}
***S+***: {UserData[4]}""",
            inline=False,
        )
        embed.set_footer(
            text="나오는 카드의 등급은 C, B, A, S로 총 4종류입니다. 강화를 통해 S+ 카드를 만들 수 있습니다."
        )
    else:
        embed = discord.Embed(title="등록되지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입한 후 다시 사용해주세요.", inline=False)
    await ctx.respond(embed=embed)


def Gacha(x, UserID):
    result = []
    CRate = [60, 50, 40, 40, 30, 20, 20, 20, 20, 20, 20]
    BRate = [25, 30, 35, 35, 40, 45, 45, 40, 35, 35, 30]
    ARate = [13, 15, 17, 17, 20, 22, 22, 25, 27, 27, 30]
    with open(f"{UserID}.pkl", "rb") as f:
        UserData = pickle.load(f)
    SPlus = UserData[5]
    for i in range(x):
        item = random.randint(0, 100)
        if item <= CRate[SPlus]:
            result.append("C")
        elif item > CRate[SPlus] and item <= CRate[SPlus] + BRate[SPlus]:
            result.append("B")
        elif (
            item > CRate[SPlus] + BRate[SPlus]
            and item <= CRate[SPlus] + BRate[SPlus] + ARate[SPlus]
        ):
            result.append("A")
        else:
            result.append("S")
    UserData[0] += result.count("C")
    UserData[1] += result.count("B")
    UserData[2] += result.count("A")
    UserData[3] += result.count("S")
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
                    embed.set_footer(text="이전 포함 전체 결과는 `/기록` 명령어를 통해 확인할 수 있습니다.")
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
                    embed.set_footer(text="이전 포함 전체 결과는 `/기록` 명령어를 통해 확인할 수 있습니다.")
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
async def 합성(ctx, mergetpe: discord.Option(str, "합성할 종류를 선택하세요.", choices=MergeType)):
    if os.path.isfile(f"{ctx.user.id}.pkl"):
        CAmount = [150, 100, 70, 50]
        BAmount = [100, 70, 50, 30]
        AAmount = [50, 30, 20, 10]
        with open(f"{ctx.user.id}.pkl", "rb") as f:
            UserData = pickle.load(f)
        Splus = UserData[4]
        if Splus >= 2 and Splus <= 5:
            level = 1
        elif Splus >= 6 and Splus <= 8:
            level = 2
        elif Splus >= 9:
            level = 3
        else:
            level = 0
        if mergetpe == MergeType[0] and UserData[0] >= CAmount[level]:
            UserData[0] -= CAmount[level]
            UserData[1] += 1
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            embed = discord.Embed(title="합성 완료", description="")
            embed.add_field(
                name="", value=f"C 카드 {CAmount[level]}개를 B 1개로 합성하였습니다.", inline=False
            )
            await ctx.respond(embed=embed)
        elif mergetpe == MergeType[1] and UserData[1] >= BAmount[level]:
            UserData[1] -= BAmount[level]
            UserData[2] += 1
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            embed = discord.Embed(title="합성 완료", description="")
            embed.add_field(
                name="", value=f"B 카드 {BAmount[level]}개를 A 1개로 합성하였습니다.", inline=False
            )
            await ctx.respond(embed=embed)
        elif mergetpe == MergeType[2] and UserData[2] >= AAmount[level]:
            UserData[2] -= AAmount[level]
            UserData[3] += 1
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            embed = discord.Embed(title="합성 완료", description="")
            embed.add_field(
                name="", value=f"A 카드 {AAmount[level]}개를 S 1개로 합성하였습니다.", inline=False
            )
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="개수 부족", description="")
            embed.add_field(name="", value="합성하려는 카드의 개수와 종류를 확인해주세요.", inline=False)
            await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(title="등록되지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입한 후 다시 사용해주세요.", inline=False)
        await ctx.respond(embed=embed)


EnforceType = ["S 10", "S 15", "S 20", "S 23"]


@bot.slash_command(description="카드 강화를 진행합니다.")
async def 강화(
    ctx, enforcetpe: discord.Option(str, "강화 재료의 개수를 선택하세요.", choices=EnforceType)
):
    if os.path.isfile(f"{ctx.user.id}.pkl"):
        with open(f"{ctx.user.id}.pkl", "rb") as f:
            UserData = pickle.load(f)
        if enforcetpe == EnforceType[0] and UserData[3] >= 10:
            UserData[3] -= 10
            if random.randint(1, 10) <= 3:
                UserData[4] += 1
                embed = discord.Embed(title="강화 완료", description="")
                embed.add_field(name="", value="30%의 확률로 S+ 카드로 강화되었습니다.", inline=False)
            else:
                embed = discord.Embed(title="강화 실패", description="")
                embed.add_field(name="", value="강화에 실패하였습니다..", inline=False)
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            await ctx.respond(embed=embed)
        elif enforcetpe == EnforceType[1] and UserData[3] >= 15:
            UserData[3] -= 15
            if random.randint(1, 10) <= 6:
                UserData[4] += 1
                embed = discord.Embed(title="강화 완료", description="")
                embed.add_field(name="", value="60%의 확률로 S+ 카드로 강화되었습니다.", inline=False)
            else:
                embed = discord.Embed(title="강화 실패", description="")
                embed.add_field(name="", value="강화에 실패하였습니다..", inline=False)
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            await ctx.respond(embed=embed)
        elif enforcetpe == EnforceType[2] and UserData[3] >= 20:
            UserData[3] -= 20
            if random.randint(1, 10) <= 9:
                UserData[4] += 1
                embed = discord.Embed(title="강화 완료", description="")
                embed.add_field(name="", value="90%의 확률로 S+ 카드로 강화되었습니다.", inline=False)
            else:
                embed = discord.Embed(title="강화 실패", description="")
                embed.add_field(name="", value="강화에 실패하였습니다..", inline=False)
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            await ctx.respond(embed=embed)
        elif enforcetpe == EnforceType[3] and UserData[3] >= 23:
            UserData[3] -= 23
            UserData[4] += 1
            embed = discord.Embed(title="강화 완료", description="")
            embed.add_field(name="", value="100%의 확률로 S+ 카드로 강화되었습니다.", inline=False)
            with open(f"{ctx.user.id}.pkl", "wb") as f:
                pickle.dump(UserData, f)
            await ctx.respond(embed=embed)
        else:
            embed = discord.Embed(title="개수 부족", description="")
            embed.add_field(name="", value="강화하려는 카드의 개수를 확인해주세요.", inline=False)
            await ctx.respond(embed=embed)
    else:
        embed = discord.Embed(title="등록되지 않은 유저", description="")
        embed.add_field(name="", value="`/등록`을 통해 가입한 후 다시 사용해주세요.", inline=False)
        await ctx.respond(embed=embed)


DebugType = ["유저 데이터 확인", "가챠 횟수 확인", "강제 부여"]


def force(CardType, CardAmount, UserID):
    with open(f"{UserID}.pkl", "rb") as f:
        UserData = pickle.load(f)
    if CardType == "C":
        UserData[0] += CardAmount
    elif CardType == "B":
        UserData[1] += CardAmount
    elif CardType == "A":
        UserData[2] += CardAmount
    elif CardType == "S":
        UserData[3] += CardAmount
    elif CardType == "S+":
        UserData[4] += CardAmount
    with open(f"{UserID}.pkl", "wb") as f:
        pickle.dump(UserData, f)


@bot.slash_command(description="개발자 전용 명령어")
async def 디버그(
    ctx,
    type: discord.Option(str, "디버그 내용 선택", choices=DebugType),
    num: discord.Option(int, "가챠 횟수 확인, 강제 부여시 입력", required=False, default=0),
    debuguser: discord.Option(
        discord.SlashCommandOptionType.user,
        "유저 데이터 확인, 강제 부여시 입력",
        required=False,
        default=0,
    ),
    card: discord.Option(
        str, "강제 부여시 입력", choices=["C", "B", "A", "S", "S+"], required=False, default=0
    ),
):
    if ctx.user.id == 763422064794796042 and os.path.isfile(f"{ctx.user.id}.pkl"):
        with open(f"{ctx.user.id}.pkl", "rb") as f:
            UserData = pickle.load(f)
        if type == DebugType[0]:
            if debuguser == 0:
                embed = discord.Embed(
                    title="유저 정보",
                    description=f"<@{ctx.user.id}>({ctx.user.id})",
                )
                embed.add_field(name="", value=f"{str(UserData)}")
            elif os.path.isfile(f"{debuguser.id}.pkl"):
                with open(f"{debuguser.id}.pkl", "rb") as f:
                    UserData = pickle.load(f)
                embed = discord.Embed(
                    title="유저 정보",
                    description=f"<@{debuguser.id}>({debuguser.id})",
                )
                embed.add_field(name="", value=f"{str(UserData)}")
            else:
                embed = discord.Embed(title="유저 정보", description="")
                embed.add_field(name="", value=f"<@{debuguser.id}> 유저는 등록하지 않은 유저입니다.")
            await ctx.respond(embed=embed)

        elif type == DebugType[1]:
            result = Gacha(num, ctx.user.id)
            await ctx.response.defer()
            embed = discord.Embed(title=f"{num}회 가챠 결과", description="")
            embed.add_field(
                name=f"",
                value=f"""C: {result.count('C')}
B: {result.count('B')}
**A**: {result.count('A')}
***S***: {result.count('S')}""",
                inline=False,
            )
            embed.set_footer(text="이전 포함 전체 결과는 `/기록` 명령어를 통해 확인할 수 있습니다.")
            await ctx.followup.send(embed=embed)

        elif type == DebugType[2]:
            if card == 0:
                card = "C"
            if debuguser == 0:
                force(card, num, ctx.user.id)
                embed = discord.Embed(
                    title="강제 부여",
                    description=f"<@{ctx.user.id}>({ctx.user.id})",
                )
                embed.add_field(name="", value=f"{card} 카드 {num}개가 강제 부여되었습니다.")
            elif os.path.isfile(f"{debuguser.id}.pkl"):
                force(card, num, debuguser.id)
                embed = discord.Embed(
                    title="강제 부여",
                    description=f"<@{debuguser.id}>({debuguser.id})",
                )
                embed.add_field(name="", value=f"{card} 카드 {num}개가 강제 부여되었습니다.")
            else:
                embed = discord.Embed(title="유저 정보", description="")
                embed.add_field(name="", value=f"<@{debuguser.id}> 유저는 등록하지 않은 유저입니다.")
            await ctx.respond(embed=embed)

    else:
        embed = discord.Embed(title="개발자 전용 명령어", description="")
        embed.add_field(
            name="", value="개발자가 아닙니다. 확인 후 다시 사용해주세요. 개발자가 맞다면 등록이 되어있는지 확인해주세요."
        )
        await ctx.respond(embed=embed)


bot.run(token)
