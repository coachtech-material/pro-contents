# CLAUDE.md

教材リポジトリ。Markdownで書かれた教材を `generate_site.py` で静的HTMLにし、GitHub Pages (https://coachtech-material.github.io/pro-contents/) で公開している。GitHub Actionsには **カスタムワークフローが存在せず**、Pagesの "legacy" 自動デプロイが `main` ブランチの `/docs` をそのまま配信しているだけ。

## 教材を修正したら必ずやること

```bash
python3 generate_site.py     # ← .md → HTML 再生成（必須）
git add laravelエンジニアのためのフロントエンド学習ロードマップ docs/
git commit -m "教材修正: ..."
git push origin main         # ← /docs が自動デプロイされ、~1分で反映
```

**忘れがちな注意点：**
- GitHub Actions側に `generate_site.py` を走らせる仕組みは無い → `docs/` を再生成せず `.md` だけpushしても**公開サイトは何も変わらない**
- `.md` を直したら必ず `docs/` も**両方**コミットすること
- 生成されるHTMLは211ファイル前後（増減があれば構造変更を疑う）

## ディレクトリ構造

- `laravelエンジニアのためのフロントエンド学習ロードマップ/` — 編集対象（.mdソース）
  - `tutorialNN_*/chapterNN_*/N-N-N: タイトル.md` — 通常チュートリアル
  - `tutorial12_column/colNN_*/Col-N-N: タイトル.md` — 上級コラム（`is_column=True` で別処理。`format_column_chapter_title` / `get_column_chapters` を経由する）
- `generate_site.py` — Markdown→HTML変換スクリプト（python3 + markdownライブラリ + nl2br/codehilite/toc/tables/fenced_code 拡張）
- `docs/` — 生成物。GitHub Pagesが直接配信する場所。**手動コミット必須**
- `docs/style.css` — 唯一手書きで管理しているCSS。スクリプトは生成しないので、デザイン変更は直接編集する
- `執筆計画_v12.md` — 教材構成のマスタープラン

## `generate_site.py` で触ってはいけない箇所

以下は意図的な設定なので、安易に変えない：

| 該当行 | 値 | 理由 |
|---|---|---|
| `BASE_DIR` | `Path(__file__).resolve().parent` | クロスプラットフォーム対応（Manus / macOS / Codespaces どこでも動く）。元は `/home/ubuntu/pro-contents` ハードコードだった |
| `extension_configs` | `{'codehilite': {'use_pygments': False}}` | `style.css` がPygmentsクラス（`.cp` `.nt` `.s` 等）を未対応。有効化すると**コードブロックの色が消える** |
| `TUTORIAL_INFO` の各エントリ | order/title/time/description（+ tutorial12のみ `is_column: True`） | サイドバーやトップページの表示に直結。新規チュートリアル追加時はここを更新 |

## ローカルプレビュー

```bash
python3 generate_site.py
python3 -m http.server -d docs 8000
# http://localhost:8000/
```

## デプロイ確認

```bash
gh run list --limit 3                                    # "pages build and deployment" の状態
curl -sI https://coachtech-material.github.io/pro-contents/  # HTTP 200 か
```

## 教材執筆の経緯（参考）

23/33コミット（〜2025-12-18）が `manus-ai <support@manus.im>` 名義。「Manus AI」というクラウドAIエージェントが教材本体を執筆した。コード中に `/home/ubuntu/` の痕跡があれば、Manus サンドボックスの作業ディレクトリ由来。現在の `generate_site.py` はクロスプラットフォーム対応済みのため、その痕跡はもう影響しない。
