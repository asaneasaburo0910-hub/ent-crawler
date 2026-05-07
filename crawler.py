import requests
import json
import csv
import os
from datetime import datetime

# ============================
# 設定（ここだけ変えればOK）
# ============================
REDDIT_SUBS = ["gaming", "games", "movies", "anime"]  # 対象subreddit
MIN_SCORE = 100  # この点数以上の投稿だけ取得
OUTPUT_FILE = "results.csv"  # 保存先ファイル名


def fetch_reddit():
    """Redditから投稿を取得"""
    results = []
    headers = {"User-Agent": "crawler-bot/1.0"}

    for sub in REDDIT_SUBS:
        try:
            url = f"https://www.reddit.com/r/{sub}/hot.json?limit=20"
            res = requests.get(url, headers=headers, timeout=10)
            data = res.json()

            for post in data["data"]["children"]:
                p = post["data"]
                if p["score"] < MIN_SCORE:
                    continue
                results.append({
                    "source": "Reddit",
                    "title": p["title"],
                    "score": p["score"],
                    "comments": p["num_comments"],
                    "category": f"r/{sub}",
                    "url": f"https://reddit.com{p['permalink']}",
                    "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                })
            print(f"✅ Reddit r/{sub}: {len(results)}件取得")

        except Exception as e:
            print(f"❌ Reddit r/{sub} 失敗: {e}")

    return results


def fetch_hn():
    """Hacker Newsから投稿を取得"""
    results = []
    try:
        url = "https://hn.algolia.com/api/v1/search?query=gaming+entertainment&tags=story&hitsPerPage=30&numericFilters=points>50"
        res = requests.get(url, timeout=10)
        data = res.json()

        for hit in data["hits"]:
            if not hit.get("title"):
                continue
            results.append({
                "source": "Hacker News",
                "title": hit["title"],
                "score": hit.get("points", 0),
                "comments": hit.get("num_comments", 0),
                "category": "HackerNews",
                "url": hit.get("url") or f"https://news.ycombinator.com/item?id={hit['objectID']}",
                "fetched_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
        print(f"✅ Hacker News: {len(results)}件取得")

    except Exception as e:
        print(f"❌ Hacker News 失敗: {e}")

    return results


def save_csv(items):
    """結果をCSVに保存（追記モード）"""
    file_exists = os.path.exists(OUTPUT_FILE)
    fieldnames = ["source", "title", "score", "comments", "category", "url", "fetched_at"]

    with open(OUTPUT_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if not file_exists:
            writer.writeheader()  # 初回だけヘッダーを書く
        writer.writerows(items)

    print(f"💾 {OUTPUT_FILE} に {len(items)}件保存しました")


def main():
    print(f"🚀 クロール開始: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

    reddit_items = fetch_reddit()
    hn_items = fetch_hn()

    all_items = reddit_items + hn_items
    all_items.sort(key=lambda x: x["score"], reverse=True)  # スコア順に並べる

    save_csv(all_items)

    # 上位5件をコンソールに表示
    print("\n📊 上位5件:")
    for i, item in enumerate(all_items[:5], 1):
        print(f"  {i}. [{item['source']}] {item['title'][:60]}... (スコア: {item['score']})")

    print(f"\n✨ 完了！合計 {len(all_items)} 件")


if __name__ == "__main__":
    main()
