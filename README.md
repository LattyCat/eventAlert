# Event Alert (イベントステータス監視スクリプト)

このプロジェクトは、[PHONE APPLI イベントページ](https://phoneappli.net/event/)を定期的にスクレイピングし、**開催日が過ぎているにもかかわらず「開催終了」のステータスになっていないイベント**を自動的に検知して通知するツールです。

検知されたイベントは、Microsoft Teams の Webhook を通じて通知されます。

## 機能概要

- **Web スクレイピング**: BeautifulSoup4 を使用してイベント情報を抽出します。
- **ステータスチェック**: イベントの日付と現在の日付を比較し、終了ステータスの不整合を特定します。
- **Teams 通知**: 問題のあるイベントが見つかった場合、Adaptive Card 形式で見やすく通知します。
- **自動実行**: GitHub Actions を利用して、平日の毎朝 8:00 (JST) に自動チェックを行います。

## 必要要件

- Python 3.9 以上
- 必要なライブラリは `requirements.txt` に記載されています。

## セットアップ手順

### 1. リポジトリのクローン

```bash
git clone <repository-url>
cd eventAlert
```

### 2. 依存関係のインストール

```bash
python -m venv .venv
source .venv/bin/activate  # Windowsの場合は .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 環境変数の設定

プロジェクトルートに `.env` ファイルを作成し、Teams の Webhook URL を設定してください。

```bash
TEAMS_WEBHOOK_URL=your_teams_webhook_url_here
```

※ `.env` ファイルは git の管理対象外（.gitignore）になっています。

## 使用方法

手動でスクリプトを実行してチェックを行う場合：

```bash
python extract_events.py
```

問題のあるイベントが検知された場合、コンソールに出力されるとともに、設定された Teams チャンネルに通知が飛びます。
問題がない場合は、その旨がコンソールに表示されます。

## 自動化 (GitHub Actions)

このリポジトリには `.github/workflows/daily_check.yml` が含まれており、以下のスケジュールで自動実行されるように設定されています。

- **スケジュール**: 平日（月〜金）の 日本時間 8:00 (UTC 23:00)

GitHub Actions で動作させるためには、リポジトリの Settings > Secrets and variables > Actions に以下のシークレットを設定する必要があります。

- `TEAMS_WEBHOOK_URL`: Teams の Incoming Webhook URL
