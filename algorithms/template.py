from elepoke import *


class SuperElepoke(Elepoke):
    def __init__(self, datas=pd.read_csv("./data/pokemon.csv", index_col=0)):
        super().__init__(datas)

    def _calc(self) -> list:
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
