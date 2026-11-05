# 共通設定

設定ファイルは、面談原本を置く作業ワークスペース直下の `.meeting-skills.local.md`。共有版リポジトリの設定例をコピーし、利用者が自分の情報を記入する。これは認証情報の保管先ではない。トークン・パスワードは書かず、各利用者が Codex の接続済みアプリを認証する。

## 段階ごとの必須設定

| 段階 | 必須設定・接続 |
| --- | --- |
| 面談原本作成 | HubSpot 接続、本人 owner の取得、利用ポータルのプロパティ確認 |
| 文字起こし反映 | 明示した文字起こし、または本人がアクセスできる tldv 接続 |
| Gmail 下書き | `gmail_account`、`sender_company`、`sender_name`、`self_introduction`、`signature`、`attachments.product_guide`、`attachments.standard_pricing`、Gmail 接続 |
| HubSpot 履歴 | HubSpot read/write access と明示承認 |
| Slack 下書き | `slack_workspace`、`slack_channel_name`、`slack_channel_id`、Slack 下書き作成・再取得機能 |

原本作成・文字起こし反映だけなら、Gmail・Slack の設定不足を理由に停止しない。一括実行は外部書き込み前に全段階の必須設定と機能を確認する。

`gmail_account` は承認対象の送信元。接続アカウントと一致しない場合は作成しない。`signature` は利用者が記入した値をそのまま使う。送信者名・肩書き・電話番号を CRM や記憶から補わない。件名の会社名・送信者名は `sender_company` と `sender_name` から作る。

Slack は接続先ワークスペースと設定名・IDをすべて照合する。名前だけの一致で別ワークスペースへ書き込まない。下書き作成や再取得の機能がなければ停止し、投稿・ブラウザ操作へ切り替えない。

添付パスは利用者が持つローカルPDFの絶対パスとする。未設定・未承認の資料は検索して補わない。通常の必須2件以外は [添付基準](../../meeting-create-gmail-draft/references/attachments.md) に従う。`video_urls` と `service_url` は任意。空なら本文の対応する紹介文も省く。

## HubSpot のプロパティ

この共有版は同社の運用に合わせ、初回面談日 `first_appointment_date`、面談チャネル分類 `mql__`、面談事前情報 `memoisfs` を前提とする。利用ポータルで内部名と用途を検証してから読む。存在しない場合はユーザーに対応する項目を確認し、別項目や「次回面談」を推測で使わない。owner ID は固定せず毎回本人情報から取得する。

## 原本とテンプレート

原本の配置は作業ワークスペースの `面談準備/`。テンプレートは [同梱テンプレート](../../meeting-create-minutes/assets/meeting-minutes-template.md) を参照する。ワークスペースに明示された正本テンプレートがある場合はそれを優先し、後続スキルが必要とする4見出し・取引ID・面談日との互換性を確認する。矛盾があれば書き込み前に確認する。

HubSpot に必須の開始時刻が原本・同一面談の予定から確認できない場合は、外部書き込み開始前の承認提示に不足として含める。日付から時刻を推測しない。
