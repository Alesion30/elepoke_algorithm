## [ELEPOKE](https://elepoke.herokuapp.com/)で使用するアルゴリズム

### 開発方法

1. template.py を同じ階層にコピーする。
2. \_calc()を構築する。
3. 必要に応じて関数を作成する。（関数名にはアンダーバー \_をつける）

#### Nuxt.js から送られてくるデータ構造

```js
{
    mypoke: [
        { index: 0, name: "ヒートロトム", Evaluation: 0.0, rank: 0 },
        { index: 1, name: "アイアント", Evaluation: 0.0, rank: 0 },
        { index: 2, name: "ローブシン", Evaluation: 0.0, rank: 0 },
        { index: 3, name: "ゴリランダー", Evaluation: 0.0, rank: 0 },
        { index: 4, name: "バイウールー", Evaluation: 0.0, rank: 0 },
        { index: 5, name: "トゲキッス", Evaluation: 0.0, rank: 0 }
    ],
    oppoke: [
        { index: 0, name: "タチフサグマ", Evaluation: 0.0, rank: 0 },
        { index: 1, name: "ワタシラガ", Evaluation: 0.0, rank: 0 },
        { index: 2, name: "ウォッシュロトム", Evaluation: 0.0, rank: 0 },
        { index: 3, name: "アイアント", Evaluation: 0.0, rank: 0 },
        { index: 4, name: "ドリュウズ", Evaluation: 0.0, rank: 0 },
        { index: 5, name: "リザードン", Evaluation: 0.0, rank: 0 }
    ]
}
```

#### Nuxt.js へ送るデータ構造

```py
[
    [
        {'index': 0, 'name': 'ヒートロトム', 'Evaluation': 156, 'rank': 1},
        {'index': 1, 'name': 'アイアント', 'Evaluation': 74, 'rank': 4},
        {'index': 2, 'name': 'ローブシン', 'Evaluation': 136, 'rank': 2},
        {'index': 3, 'name': 'ゴリランダー', 'Evaluation': 64, 'rank': 5},
        {'index': 4, 'name': 'バイウールー', 'Evaluation': 47, 'rank': 6},
        {'index': 5, 'name': 'トゲキッス', 'Evaluation': 98, 'rank': 3}
    ],
    [
        {'index': 0, 'name': 'タチフサグマ', 'Evaluation': 59, 'rank': 5},
        {'index': 1, 'name': 'ワタシラガ', 'Evaluation': 37, 'rank': 6},
        {'index': 2, 'name': 'ウォッシュロトム', 'Evaluation': 86, 'rank': 3},
        {'index': 3, 'name': 'アイアント', 'Evaluation': 80, 'rank': 4},
        {'index': 4, 'name': 'ドリュウズ', 'Evaluation': 132, 'rank': 2},
        {'index': 5, 'name': 'リザードン', 'Evaluation': 150, 'rank': 1}
    ]
]
```

### アルゴリズム集

#### \_calc - ダメージの通りを重視（現在適用中）

自分のポケモンが、相手のポケモンに対して与えることのできる最大打点を平均化した。

[問題点]

- HP, 素早さがまったく考慮されない。
- 防御、特防もそこまで重視されない。
- 受けポケモンに対する評価が低くなりがちになる。
