# %%
from elepoke import *


class SuperElepoke(Elepoke):
    def __init__(self, datas=pd.read_csv("./data/pokemon.csv", index_col=0)):
        super().__init__(datas)

    def _winRate(self, pokemon: list, iteration: int = 10, show: bool = False) -> list:
        # ポケモンの情報を取得
        poke1 = self._spec(pokemon[0])
        poke2 = self._spec(pokemon[1])

        # ポケモンの名前からタイプを取得
        poke1_types = [poke1["type1_int"], poke1["type2_int"]]
        poke2_types = [poke2["type1_int"], poke2["type2_int"]]

        # 攻撃と特攻の種族値を比較し、攻撃技or特攻技を決定
        if poke1["a"] >= poke1["c"]:
            skill1 = "a"
        else:
            skill1 = "c"
        if poke2["a"] >= poke2["c"]:
            skill2 = "a"
        else:
            skill2 = "c"

        # タイプ一致技からよりダメージの通る技のタイプを決定
        # 一匹目
        dmList = []
        for item in poke1_types:
            if item != -1:
                if skill1 == "a":
                    attack1 = poke1["a"]
                    defence2 = poke2["b"]
                else:
                    attack1 = poke1["c"]
                    defence2 = poke2["d"]

                # タイプ相性による倍率のセット
                rate = 1.5
                rate *= getCompatibility(item, poke2_types[0])
                if poke2_types[1] != -1:
                    rate *= getCompatibility(item, poke2_types[1])

                dm = damage(100, skill1, attack1, defence2, rate)
                dmList.append(dm)

        # ダメージを比較してタイプを決定
        if len(dmList) == 2:
            if dmList[0] < dmList[1]:
                poke1_type = poke1_types[1]
            else:
                poke1_type = poke1_types[0]
        else:
            poke1_type = poke1_types[0]

        # 二匹目
        dmList = []
        for item in poke2_types:
            if item != -1:
                if skill2 == "a":
                    attack2 = poke2["a"]
                    defence1 = poke1["b"]
                else:
                    attack2 = poke2["c"]
                    defence1 = poke1["d"]

                # タイプ相性による倍率のセット
                rate = 1.5
                rate *= getCompatibility(item, poke1_types[0])
                if poke1_types[1] != -1:
                    rate *= getCompatibility(item, poke1_types[1])

                dm = damage(100, skill1, attack2, defence1, rate)
                dmList.append(dm)

        # ダメージを比較してタイプを決定
        if len(dmList) == 2:
            if dmList[0] < dmList[1]:
                poke2_type = poke2_types[1]
            else:
                poke2_type = poke2_types[0]
        else:
            poke2_type = poke2_types[0]

        # <-- 対面対戦の開始  -->
        if show:
            print("{} vs {}\n".format(pokemon[0], pokemon[1]))

        dead1 = False
        dead2 = False

        # HPの初期化
        HP1 = poke1["h"]
        HP2 = poke2["h"]
        if show:
            print("{} HP: {}".format(pokemon[0], HP1))
        if show:
            print("{} HP: {}\n".format(pokemon[1], HP2))

        # 総ダメージ
        sum1 = 0
        sum2 = 0

        # 各ターンの結果を格納
        result = [dead1, dead2, HP1, HP2, sum1, sum2]

        # poke1の攻撃
        def action1(dead1, dead2, HP1, HP2, sum1, sum2):
            if not(dead1):
                if show:
                    print("> {}の攻撃！".format(pokemon[0]))
                rate = getCompatibility(poke1_type, poke2_types[0])
                if poke2_types[1] != -1:
                    rate *= getCompatibility(poke1_type, poke2_types[1])
                if show:
                    if rate >= 2:
                        print("> 効果は抜群だ！")
                    elif rate <= 0.5:
                        print("> 効果はいまひとつだ！")
                    elif rate == 0:
                        print("> 効果は無いようだ！")
                rate *= 1.5
                dm = damage(100, skill1, attack1, defence2, rate)
                if show:
                    print("> {}は{}ダメージを受けた！".format(pokemon[1], dm))
                sum1 += dm
                HP2 -= dm
                # 生死判定
                if (HP2 <= 0):
                    dead2 = True
                    HP2 = poke2["h"]
                    if show:
                        print("{} HP: {}".format(pokemon[1], 0))
                        print("> {}は倒れた!\n".format(pokemon[1]))
                else:
                    if show:
                        print("{} HP: {}\n".format(pokemon[1], HP2))
            else:
                dead1 = False

            return [dead1, dead2, HP1, HP2, sum1, sum2]

        # poke2の攻撃
        def action2(dead1, dead2, HP1, HP2, sum1, sum2):
            if not(dead2):
                if show:
                    print("> {}の攻撃！".format(pokemon[1]))
                rate = getCompatibility(poke2_type, poke1_types[0])
                if poke1_types[1] != -1:
                    rate *= getCompatibility(poke2_type, poke1_types[1])
                if show:
                    if rate >= 2:
                        print("> 効果は抜群だ！")
                    elif rate <= 0.5:
                        print("> 効果はいまひとつだ！")
                    elif rate == 0:
                        print("> 効果は無いようだ！")
                rate *= 1.5
                dm = damage(100, skill1, attack2, defence1, rate)
                if show:
                    print("> {}は{}ダメージを受けた！".format(pokemon[0], dm))
                sum2 += dm
                HP1 -= dm
                # 生死判定
                if (HP1 <= 0):
                    dead1 = True
                    HP1 = poke1["h"]
                    if show:
                        print("{} HP: {}".format(pokemon[0], 0))
                        print("> {}は倒れた!\n".format(pokemon[0]))
                else:
                    if show:
                        print("{} HP: {}\n".format(pokemon[0], HP1))
            else:
                dead2 = False

            return [dead1, dead2, HP1, HP2, sum1, sum2]

        for i in range(iteration):
            if show:
                print("--------------------------------------")
                print("[{}ターン目]".format(i+1))
                print("--------------------------------------\n")

            if poke1["s"] > poke2["s"]:
                # poke1の攻撃
                result = action1(
                    result[0], result[1], result[2], result[3], result[4], result[5])
                # poke2の攻撃
                result = action2(
                    result[0], result[1], result[2], result[3], result[4], result[5])

            elif poke1["s"] < poke2["s"]:
                # poke2の攻撃
                result = action2(
                    result[0], result[1], result[2], result[3], result[4], result[5])
                # poke1の攻撃
                result = action1(
                    result[0], result[1], result[2], result[3], result[4], result[5])

            else:
                # 同速対決
                rand = np.random.randint(0, 2)
                if rand:
                    # poke1の攻撃
                    result = action1(
                        result[0], result[1], result[2], result[3], result[4], result[5])
                    # poke2の攻撃
                    result = action2(
                        result[0], result[1], result[2], result[3], result[4], result[5])
                else:
                    # poke2の攻撃
                    result = action2(
                        result[0], result[1], result[2], result[3], result[4], result[5])
                    # poke1の攻撃
                    result = action1(
                        result[0], result[1], result[2], result[3], result[4], result[5])

        # 平均を算出
        average1 = result[4] / iteration
        average2 = result[5] / iteration

        return [average1, average2]

    def calc(self) -> list:
        """アルゴリズムのテンプレート

        Returns:
            list -- 計算結果
        """
        # 初期化
        self.result = [[], []]

        # 結果格納用の配列
        myPokeList = []
        opPokeList = []

        # ここに計算処理を記述する

        # 結果をセット
        self.result = [myPokeList, opPokeList]

        return self.result


# %%
SuperElepoke()._winRate(["ルカリオ", "クレセリア"], show=True)


# %%
print("iter: 10", SuperElepoke()._winRate(["ルカリオ", "ルカリオ"], iteration=10))
print("iter: 100", SuperElepoke()._winRate(["ルカリオ", "ルカリオ"], iteration=100))
print("iter: 1000", SuperElepoke()._winRate(["ルカリオ", "ルカリオ"], iteration=1000))


# %%
