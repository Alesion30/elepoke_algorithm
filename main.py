# %%
from elepoke import *

mypokeList = ["ヒートロトム", "アイアント", "ローブシン", "ゴリランダー", "バイウールー", "トゲキッス"]
oppokeList = ["タチフサグマ", "ワタシラガ", "ウォッシュロトム", "アイアント", "ドリュウズ", "リザードン"]

# Elepokeモデルを初期化
el = Elepoke()

# セット
el.append(name=[mypokeList, oppokeList], reset=True)

# 計算
el.fit()

# 結果
for item in el.result[0]:
    print(item)

print("")

for item in el.result[1]:
    print(item)


# %%
