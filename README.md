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

Python 3 と Git を利用します。このリポジトリを取得し、面談原本を置く作業ワークスペースへ6スキルをまとめてリンクします。

```bash
git clone <REPOSITORY_URL>
cd codex-meeting-skills
python3 scripts/install.py --workspace /path/to/workspace --dry-run
python3 scripts/install.py --workspace /path/to/workspace
```

`/path/to/workspace` は既存の作業フォルダへ置き換えてください。インストーラは `.agents/skills/` にシンボリックリンクを作り、既存のスキルは上書きしません。依存関係があるため6スキルを一緒に導入します。リンク元となる取得フォルダは移動・削除しないでください。

この配置とシンボリックリンクの利用は [OpenAI 公式ドキュメント](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills) に準拠します。認識されない場合は Codex を再起動してください。

## 初回設定

1. `meeting-skills.example.md` を作業ワークスペースの `.meeting-skills.local.md` へコピーし、利用者本人のアカウント・署名・報告先・送付PDFのパスを記入します。[共通設定](skills/meeting-run-followup/references/configuration.md) に段階別の必須項目があります。
2. 作業ワークスペース側の `.gitignore` または `.git/info/exclude` に `.meeting-skills.local.md` と `面談準備/` を追加します。このリポジトリの ignore 設定は別ワークスペースへ自動適用されません。顧客記録を社内の専用リポジトリで管理する場合は、その管理ルールに従ってください。
3. Codex で利用者本人の HubSpot、Gmail、Slack、tldv を接続します。文字起こしを明示する場合は tldv 接続を省略できます。
4. HubSpot の利用権限・カスタムプロパティ、Gmail の PDF 添付・下書き再取得、Slack の下書き作成・再取得が利用可能か確認します。アプリ接続はこのリポジトリやインストーラでは設定しません。

## 使い方

作業ワークスペースで Codex を開き、会話から呼び出します。

```text
$meeting-create-minutes 本日の担当取引から面談原本を作成して

$meeting-run-followup 面談準備/YYMMDD_会社名.md を文字起こしから更新し、フォローまで進めて
```

原本作成時の議事録・ネクストアクションは未記入です。実施前の面談に過去の文字起こしを流用しません。フォロー時は対象原本を1件明示してください。文字起こしを貼り付けるか入力ファイルを指定した場合、tldv は検索しません。

外部書き込みの前に、送信元・宛先・件名・本文・添付一覧、HubSpot 取引、Slack ワークスペース・チャンネルと本文をまとめて提示し、1回の明示承認を取得します。承認後は追加確認を挟まず直列実行し、失敗した段階で停止します。Gmail 送信と Slack 投稿、既存データの更新は行いません。HubSpot には新しい活動ログが作成されます。

単独実行する子スキルでも、外部書き込みは対象・内容の承認後に行います。接続機能が不足する場合はブラウザや CLI を代替経路にせず停止します。

## 保守と公開範囲

共有版の更新はこのリポジトリの `skills/` を編集してください。個人用スキルの正本とは独立した公開用の派生版です。更新時は差分を確認し、個人設定・署名・顧客情報・送付資料を取り込まないでください。空の議事録テンプレートは `meeting-create-minutes/assets/` に同梱しています。

この公開版では事前情報の除外見出しを現行テンプレートと整合させ、固定された送信者・添付パス・報告チャンネルをローカル設定へ置き換えています。元の業務ルール（推測禁止、重複防止、承認、直列実行、失敗時停止、改行・添付の再取得検証）を引き継いでいます。

公開版での接続先への実書き込みテストは実施していません。導入後は各自の権限・設定を確認し、承認画面で対象と内容を確認して利用してください。
