# Codex Meeting Skills

チーム内の面談準備・議事録作成・面談後フォローを効率化する、Codex 用の共有スキル集です。同じ会社の利用者が、それぞれ自分のアカウントで使うことを想定しています。

個人名、メールアドレス、電話番号、個人のホームディレクトリ、固定アカウントIDはスキルに含めません。顧客データ、文字起こし、送付PDF、認証情報も同梱しません。利用者固有の情報は公開対象外のローカル設定へ分離します。

## 含まれるスキル

| スキル | 役割 |
| --- | --- |
| `meeting-create-minutes` | HubSpot の本人担当・本日予定の取引から未作成の面談原本を作成 |
| `meeting-transcript-to-minutes` | 指定原本と tldv / 明示文字起こしを照合し、議事録を更新 |
| `meeting-create-gmail-draft` | 合意済みの次アクションと承認済みPDFを含む Gmail 下書きを作成 |
| `meeting-write-deal-history` | 議事録を対象取引の新規 HubSpot ミーティングログへ転記 |
| `meeting-post-slack` | 事前情報・メールアドレスを除いて指定 Slack チャンネルの下書きを作成 |
| `meeting-run-followup` | 議事録更新 → 一括承認 → Gmail → HubSpot → Slack を直列実行 |

元の個人用 `yk-meeting-create-minutes`、`yk-meeting-run-followup` とその子スキルを共有向けに調整しています。公開版は個人用との重複を避けるため `meeting-*` 名で呼び出します。Slack 子スキル名は `meeting-post-slack` です。

## 導入

Codex で作業する既存のフォルダと、Python 3.10 以上を用意します。インストーラは Python 標準ライブラリだけを使い、管理者権限やシンボリックリンク権限を必要としない **コピー方式** を標準にします。macOS / Linux / Windows のファイルパスに対応する設計です。Windows実機と各OS上のCodexでの認識は未検証です。

### 1. 共有版を取得

GitHub のこのページで **Code → HTTPS** からURLをコピーし、次の `REPOSITORY_URL` をその値へ置き換えます。Git が必要です。Git を使わない場合は **Code → Download ZIP** で取得して展開し、展開先をターミナルで開いて手順2へ進めます。

```text
git clone "REPOSITORY_URL" codex-meeting-skills
cd codex-meeting-skills
```

### 2. 作業フォルダへ導入

`/path/to/workspace` または `C:\path\to\workspace` は、面談原本を置く既存の作業フォルダへ置き換えます。空白・日本語を含むパスも引用符で囲んでください。dry-run は予定を表示するだけで書き込みません。

macOS / Linux:

```bash
python3 --version
python3 scripts/install.py --workspace "/path/to/workspace" --dry-run
python3 scripts/install.py --workspace "/path/to/workspace"
```

Windows（PowerShell）:

```powershell
py -3 --version
py -3 scripts/install.py --workspace "C:\path\to\workspace" --dry-run
py -3 scripts/install.py --workspace "C:\path\to\workspace"
```

`py` がなく `python --version` で Python 3.10 以上を確認できる場合は、`py -3` を `python` に置き換えます。Python がない場合は利用端末の社内手順で導入してください。

6スキルを作業フォルダの `.agents/skills/` へまとめてコピーします。共通参照と空の議事録テンプレートも含まれ、導入後は取得元フォルダを移動しても動作します。同じ内容への再実行は変更せず終了し、異なる内容の既存スキルや既存設定は上書きしません。権限エラーの場合は書き込み可能な作業フォルダを指定してください。

取得元の更新を即座に反映したい場合だけ `--mode link` を指定できます。この方式は取得元フォルダの保持とリンク作成権限が必要です。Windowsの権限設定を変更する必要はなく、リンクできない場合は標準の `--mode copy` を使ってください。

コピー版は `git pull` だけでは更新されません。新版導入時は、既存の `.agents/skills/meeting-*` を別の場所へバックアップし、差分と独自変更を確認してから新版を導入します。`.meeting-skills.local.md` と面談原本は保持してください。旧リンク版は取得元の更新を参照するため、そのまま使えます。

### 3. 利用者本人の設定とアプリ接続

1. 同梱の `meeting-skills.example.md` を作業フォルダ直下の `.meeting-skills.local.md` へコピーします。既存ファイルがあれば保持し、不足項目だけ追記します。メール・署名・送付PDFの絶対パスを利用者本人の値で記入します。[共通設定](skills/meeting-run-followup/references/configuration.md) に段階別の必須項目があります。
2. 作業フォルダ側の `.gitignore` または `.git/info/exclude` に `.meeting-skills.local.md` と `面談準備/` を追加します。このリポジトリの ignore 設定は別フォルダへ自動適用されません。社内専用リポジトリで顧客記録を管理する場合は、その管理ルールに従ってください。
3. Codex で利用者本人の HubSpot、Gmail、Slack、tldv を接続します。文字起こしを明示する場合は tldv を省略できます。Slack のワークスペース・チャンネル名・IDは、接続後に Codex へ「設定する報告先のIDを読み取りだけで確認して」と依頼して取得できます。推測したIDを記入しないでください。
4. HubSpotのカスタムプロパティ・権限、GmailのファイルパスによるPDF添付とメッセージ再取得、Slackの下書き作成機能を確認します。アプリ接続・権限はインストーラでは設定しません。

### 4. 書き込まずに初回確認

作業フォルダを Codex で開き、必要なら再起動してから次を依頼します。`.agents/skills/` とリンクの発見規則は [OpenAI 公式ドキュメント](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) を参照してください。

```text
面談スキル6件が認識されているか、共通設定・テンプレートを読めるか確認して。
ローカル設定の不足、接続済みアプリの利用可否、添付PDFの読み取り可否を確認して。
メールアドレスや署名の全文は報告せず、設定済みかどうかだけ示して。
面談原本の更新や外部サービスへの書き込みは行わないで。
```

面談原本作成だけなら Gmail・Slack の設定を先に完了させる必要はありません。一括フォローは全段階の設定・機能を、外部書き込みの前に確認します。

## 使い方

作業ワークスペースで Codex を開き、会話から呼び出します。

```text
$meeting-create-minutes 本日の担当取引から面談原本を作成して

$meeting-run-followup 面談準備/YYMMDD_会社名.md を文字起こしから更新し、フォローまで進めて
```

原本作成時の議事録・ネクストアクションは未記入です。実施前の面談に過去の文字起こしを流用しません。フォロー時は対象原本を1件明示してください。文字起こしを貼り付けるか入力ファイルを指定した場合、tldv は検索しません。

外部書き込みの前に、送信元・宛先・件名・本文・添付一覧、HubSpot 取引、Slack ワークスペース・チャンネルと本文をまとめて提示し、1回の明示承認を取得します。承認後は追加確認を挟まず直列実行し、失敗した段階で停止します。Gmail 送信と Slack 投稿、既存データの更新は行いません。HubSpot には新しい活動ログが作成されます。

Slackは現行コネクタで下書き本文を再取得できないため、作成後は **作成済み・表示確認待ち** になります。返されたチャンネルURLから利用者が下書きの本文・見出し・空行を確認し、一致したと伝えた時点で全工程を完了とします。画面確認を省略して検証済み成功とは扱いません。

単独実行する子スキルでも、外部書き込みは対象・内容の承認後に行います。接続機能が不足する場合はブラウザや CLI を代替経路にせず停止します。

## 保守と公開範囲

共有版の更新はこのリポジトリの `skills/` を編集してください。個人用スキルの正本とは独立した公開用の派生版です。更新時は差分を確認し、個人設定・署名・顧客情報・送付資料を取り込まないでください。空の議事録テンプレートは `meeting-create-minutes/assets/` に同梱しています。

この公開版では事前情報の除外見出しを現行テンプレートと整合させ、固定された送信者・添付パス・報告チャンネルをローカル設定へ置き換えています。元の業務ルール（推測禁止、重複防止、承認、直列実行、失敗時停止、Gmail・HubSpotの再取得検証、Slackの原文・改行の表示確認）を引き継いでいます。

公開版での接続先への実書き込みテストは実施していません。導入後は各自の権限・設定を確認し、承認画面で対象と内容を確認して利用してください。

独立レビューの3指摘と検証方法の変更は [互換性の修正記録](docs/compatibility.md) に記載しています。
