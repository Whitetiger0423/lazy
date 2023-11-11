import pickle
import random
import os

user = int(input("ID를 입력하세요: "))
if os.path.isfile(f"{user}.pkl") != True:
    UserData = []
    with open(f"{user}.pkl", "wb") as f:
        pickle.dump(UserData, f)


ItemRate = ["C"] * 60 + ["B"] * 25 + ["A"] * 10 + ["S"] * 5


def Gacha(x):
    result = []
    for i in range(x):
        result.append(random.choice(ItemRate))
    result.sort(key=lambda x: "CBAS".index(x))
    print(*result)
    with open(f"{user}.pkl", "rb") as f:
        UserData = pickle.load(f)
    UserData.extend(result)
    with open(f"{user}.pkl", "wb") as f:
        pickle.dump(UserData, f)


def Check():
    with open(f"{user}.pkl", "rb") as f:
        UserData = pickle.load(f)
    print(
        f"""    C: {UserData.count('C')}
    B: {UserData.count('B')}
    A: {UserData.count('A')}
    S: {UserData.count('S')}"""
    )


Gacha(10)
Check()
