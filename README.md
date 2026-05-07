# 🎮 ENT Crawler

Reddit と Hacker News からエンタメ・ゲームの人気投稿を自動収集するクローラーです。
GitHub Actions で毎日自動実行され、結果を `results.csv` に保存します。

## ファイル構成

```
📁 あなたのリポジトリ
├── crawler.py                        ← クローラー本体
├── requirements.txt                  ← 必要なライブラリ一覧
├── results.csv                       ← 収集結果（自動生成）
└── .github/
    └── workflows/
        └── crawl.yml                 ← 自動実行スケジュール設定
```

## 実行スケジュール

毎日 日本時間 朝9時に自動実行されます。
GitHubの「Actions」タブから手動実行もできます。

## カスタマイズ

`crawler.py` の上部を編集するだけで変更できます：

```python
REDDIT_SUBS = ["gaming", "games", "movies", "anime"]  # 対象subreddit
MIN_SCORE = 100  # この点数以上の投稿だけ取得
```
