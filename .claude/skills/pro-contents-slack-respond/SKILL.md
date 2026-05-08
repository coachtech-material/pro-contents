---
name: pro-contents-slack-respond
description: 教材リポジトリ pro-contents への問い合わせ Slack スレッド URL を受け取り、スレッド読解→教材調査→修正→docs再生成→commit/push→元スレッドに Slack 下書き返信、までを一気通貫で処理するスキル。「このSlackリンク確認して」「このスレッド対応して」「コーチから来たやつ見て」など、pro-contents プロジェクト内で生徒からの教材問い合わせ Slack URL（`https://estrahq.slack.com/archives/<channel>/p<ts>` 形式、特に #ct_service_contact = C08SY9BLPCP）を渡されたら、ユーザーが「スキル使って」と明示しなくても積極的にこのスキルを使うこと。pro-contents 以外のプロジェクトでは起動しない。
---

# pro-contents-slack-respond

教材リポジトリ pro-contents（CoachTech フロントエンド学習教材）に対する生徒からの問い合わせ Slack スレッドを、コーチ（岡部さん／永島さんなど）からエスカレされた立場で対応するためのスキル。

## このスキルがやること

ユーザーが Slack URL を投げたら、以下を一気通貫で実施する：

1. Slack スレッドを読んで質問内容と該当箇所を把握
2. 教材ソースを調べて問題（教材ミス／誤読／表示崩れなど）を特定
3. 必要なら教材を修正（リネーム・構造変更含む）
4. `docs/` 再生成、リネームで残った古いHTMLを掃除
5. 生成 HTML を検証
6. commit + push（main へ反映）
7. 元スレッドに Slack **下書き** で返信を作成（送信はしない）

ゴールは「コーチが内容を確認すれば、そのまま生徒さんに転送できる返信が下書きに保存されている」状態。

## 起動条件

- 現在の作業ディレクトリが pro-contents（`CLAUDE.md` の冒頭に「教材リポジトリ。Markdownで書かれた教材を `generate_site.py` で…」とあれば該当）
- ユーザーから `https://estrahq.slack.com/archives/.../p...` 形式の URL を受け取った
- 文脈的に「このスレッド見て／確認して／対応して／返事して」のような依頼

cwd が pro-contents でなさそうなら、起動前にユーザーに確認する。

## 手順

### Step 1: 必要な MCP ツールをロード

これらは deferred で、最初は schema が読み込まれていないので一括ロードする：

```
ToolSearch(query="select:mcp__claude_ai_Slack__slack_read_thread,mcp__claude_ai_Slack__slack_send_message_draft,TaskCreate,TaskUpdate")
```

### Step 2: Slack URL を分解

URL `https://estrahq.slack.com/archives/<channel_id>/p<digits>` から：

- **channel_id**: `archives/` の直後（例 `C08SY9BLPCP`）
- **message_ts**: `p` の直後の連続数字を `XXXXXXXXXX.XXXXXX` 形式に変換（後ろ6桁が小数部）

例: `https://estrahq.slack.com/archives/C08SY9BLPCP/p1778208293099039`
→ `channel_id=C08SY9BLPCP`, `message_ts=1778208293.099039`

### Step 3: スレッドを読む

```
mcp__claude_ai_Slack__slack_read_thread(channel_id, message_ts)
```

抽出すべき情報：
- 質問者（`【生徒様】◯◯様`）
- 件名（`件名：…`）
- 担当コーチ（`<@U08M7KKDF8Q|Yasuhiro Okabe>` = 岡部さん、`<@U06Q4JYJ6EL|Chiaki Nagashima>` = 永島さん など）
- 質問内容（`■お問い合わせ内容`以下）
- スレッド内のコーチからの自分宛て確認依頼（`<@U09147DL1LP|Yotaro Tomiie> こちら確認をお願いします！` のようなメッセージ）

下書きの宛先はこの「確認依頼してきたコーチ」になる。生徒に直接返信ではない。

### Step 4: 教材調査

質問が章節番号（例 `2-4-3`、`Col-1-1` 等）を含むなら、対応する md を探す：

```bash
find laravelエンジニアのためのフロントエンド学習ロードマップ -name "2-4-3*.md"
```

- 該当 md を Read して、生徒の指摘が事実か確認
- 必要なら同じチャプター内の他のセクションも合わせて読む（「前のセクション」のような相対参照があるとき）
- 表示崩れの相談なら、生成済み HTML を `docs/` 配下から grep して、`<br />`／`<em>` の混入や `<pre><code>` の有無で症状を再現する

### Step 5: 修正範囲を確定（同種の問題は一括修正がデフォルト）

**生徒が指摘していなくても、同じ書き方で同じ崩れを起こしている他ファイルが見つかったら、一緒に直すのがこのプロジェクトの方針**。同種の生徒指摘が後追いで来るのを防ぐため、一括対応が望ましい（過去事例：5ファイル一括修正）。

具体的には Step 4 の調査と並行して、症状の grep を全教材に対して走らせて、影響範囲を把握する：

```bash
# 例: リスト内 fenced code を疑う場合
grep -rln '^  ```' --include="*.md" laravelエンジニアのためのフロントエンド学習ロードマップ/

# 例: 生成HTMLで <br /> 過多を疑う場合（間接指標）
for f in docs/...; do echo "$(grep -c '<br />' "$f") $f"; done
```

見つかった同種問題は、生徒指摘外でも一括で Step 6 の修正に含める。Slack 下書きには「指摘いただいた2ファイル＋同じ書き方で同様の崩れがあった他N件も併せて修正しました」と明記する。

以下の判断は **必ずユーザーに相談**（AskUserQuestion 推奨）：

- 教材ミスを認めるか／別の解釈で回答するか（複数の方針がありうる場合）
- ファイルリネームの是非（影響範囲が広いため）
- main への push を実施するか

ユーザーは「修正が簡単に済むのなら、修正しちゃって、修正した報告ができたら理想」というスタンスなので、低リスクなものは直接進めて報告でも良いが、blast radius が広がる判断はワンクッション置く。

### Step 6: 教材修正

- 通常のテキスト修正は `Edit` で
- ファイル名変更は `git mv`（手動で `mv` してから `git add` ではなく、git にリネームを認識させる）
- 触ってはいけない箇所は `CLAUDE.md` 参照（`generate_site.py` の `BASE_DIR`、`extension_configs`、`TUTORIAL_INFO` など）

#### よくある教材修正パターン

**パターン A: リスト内 fenced code の表示崩れ**

`- **HTML:**` の直下に2スペースインデントで ` ```html` を書いている箇所が崩れる（Python-Markdown の `fenced_code` 拡張がリスト内のフェンスを認識しない）。修正方針：

```markdown
# 崩れる書き方
- **HTML:**
  ```html
  <div>...</div>
  ```

# 修正後
**HTML:**

```html
<div>...</div>
```
```

リスト構造を解除してフラットにし、フェンスをトップレベル（インデントなし）に書き直す。

**パターン B: 章節間の参照不整合**

「前のセクションで作成した◯◯」の参照先が存在しない、ファイル名と中身がズレている、など。質問者が混乱している原因を特定し、当該セクション内で自己完結する形に書き直す。

### Step 7: docs 再生成

```bash
python3 generate_site.py
```

末尾に `生成されたHTMLファイル数: 211` 前後と出ることを確認。大きくズレていたら構造変更を疑う（CLAUDE.md 記載）。

### Step 8: 古い HTML を掃除（リネーム時のみ）

`generate_site.py` は古い HTML を自動削除しない。リネームしたら：

```bash
git status --short  # 旧HTMLが M ではなく未削除のまま、新HTMLが ?? で残るので確認
git rm "docs/.../<旧HTMLファイル>"
```

### Step 9: 生成 HTML を検証

修正したセクションの HTML を確認：

- コードブロックが `<pre><code class="language-...">` で正しく出ているか
- 不要な `<br />` や `<em>` が混入していないか（リスト内フェンス崩れの典型症状）

```bash
grep -c "<br />" "docs/.../<該当HTML>"
grep -c "<pre><code class=\"language" "docs/.../<該当HTML>"
```

### Step 10: commit + push

CLAUDE.md のフローに従い、`.md` と `docs/` を**両方**コミット：

```bash
git add laravelエンジニアのためのフロントエンド学習ロードマップ/ docs/laravelエンジニアのためのフロントエンド学習ロードマップ/
git commit -m "$(cat <<'EOF'
教材修正: <要約>

<詳細>

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
EOF
)"
```

**push を実施するかは Step 5 のユーザー確認結果に従う**。push しない選択なら、commit のみで止め、Slack 下書き本文も「修正をローカルで完了、push はユーザー操作待ち」など実状に合わせる。

push する場合：

```bash
git push origin main
```

push 後の追加検証（`gh run list` 等）は不要。明示要請がない限りやらない（メモリ `feedback_post_push_verification.md` 参照）。

### Step 11: Slack 下書きを作成

```
mcp__claude_ai_Slack__slack_send_message_draft(
  channel_id=<URLから抽出したID>,
  thread_ts=<URLから抽出したts>,
  message=<下記テンプレート>
)
```

**重要**: 下書き本文は実際の状態と整合させる。push 前なら「push 予定」、push 完了後なら「main にpushして公開サイトに反映済み」。実状と乖離があると Slack MCP 側で integrity violation として拒否される。

#### 下書きテンプレート

```
<@確認依頼してきたコーチのID>
お疲れ様です！確認結果です。

■ 結論
<教材ミスを認める／意図を説明／状況の総括>

■ 原因（教材ミスの場合）
<具体的な原因（マークダウンの書き方／参照不整合／リネーム漏れなど）>

■ 対応
- <修正したファイル・内容のリスト>
- <push 済みなら「main にpushして公開サイトに反映済み（数分以内に最新へ切り替わります）」、未pushなら「main にpush次第、公開サイトに反映されます」など実状に合わせる>

■ <生徒様の名字>様への伝え方（案）
> ご指摘ありがとうございます。<具体的な事実説明>。<アクション提案（再読み込み／修正済みなど）>。
```

下書きは作るだけ。送信はユーザー操作。

## 守るべき制約

1. **整合性**: 下書きの記述は実状と一致していること。「push済み」「反映済み」は push 後のみ。
2. **生徒名／コーチ名の取り違え注意**: 宛先（コーチ）と伝え方案の主語（生徒）を間違えない。スレッドに `【生徒様】` と `<@COACH_ID>` の両方が必ず登場する。
3. **触ってはいけない箇所**: `generate_site.py` の `BASE_DIR` / `extension_configs` / `TUTORIAL_INFO` は CLAUDE.md で警告されている。
4. **destructive な git 操作の自走禁止**: `--force`, `reset --hard`, `--no-verify` などは明示要請がない限り使わない。
5. **post-push verification はやらない**: メモリ `feedback_post_push_verification.md` の方針。
6. **下書きまでで止める**: Slack への送信、PR 作成などはこのスキルの範囲外。

## 参照

- リポジトリ直下 `CLAUDE.md` — 教材編集→公開フロー、触ってはいけない箇所
- `MEMORY.md` の以下のエントリ:
  - `project_pro_contents.md` — プロジェクト全体像
  - `feedback_post_push_verification.md` — push 後検証不要
  - `feedback_generate_site_basedir.md` — `BASE_DIR` の罠
- 過去の対応事例（このスキル作成のもとになった2例）:
  - 「前のセクションで作成したギャラリーレイアウト」参照不整合（2-4-3）
  - リスト内 fenced code 表示崩れ（2-3-2 / 2-3-3 / 2-4-2 / 2-4-4 / 2-4-5）
