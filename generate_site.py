#!/usr/bin/env python3
"""
静的サイト生成スクリプト
教材のMarkdownファイルからGitHub Pages用のHTMLを生成する
"""

import os
import re
import markdown
from pathlib import Path
from html import escape

# パス設定
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "docs"

# サイト情報
SITE_TITLE = "COACHTECH × フロントエンド ガイド"
SITE_DESCRIPTION = "Laravelエンジニアのためのフロントエンド学習ロードマップ"

# コンテンツ情報（リポジトリ内のディレクトリ）
# slug: 公開URLに使う短い英数字パス。日本語ディレクトリ名をURLに出さないための要。
#       変更すると公開URLが変わるので、既存の共有リンクを壊さないよう安易に変えないこと。
CONTENTS_INFO = {
    "laravelエンジニアのためのフロントエンド学習ロードマップ": {
        "order": 1,
        "slug": "roadmap",
        "title": "Laravelエンジニアのためのフロントエンド学習ロードマップ",
        "description": "PHP/Laravelエンジニアがフロントエンド開発（JavaScript/TypeScript/React/Next.js）を習得し、2年目レベルのスキルを身につけるための教材です。",
        "time": "700時間"
    }
}

# チュートリアル情報（順序と説明）
TUTORIAL_INFO = {
    "tutorial01_開発環境とWebの基礎固め": {
        "order": 1,
        "title": "Tutorial 1: 開発環境とWebの基礎固め",
        "time": "40時間",
        "description": "VS Codeとターミナルの基本操作、Webの仕組み（HTTP、DNS）を学びます。"
    },
    "tutorial02_HTML_CSS基礎": {
        "order": 2,
        "title": "Tutorial 2: HTML/CSS基礎",
        "time": "50時間",
        "description": "HTMLの基本構造、CSSの基本、Flexbox/Gridによるレイアウトを学びます。"
    },
    "tutorial03_Tailwind_CSS徹底習得": {
        "order": 3,
        "title": "Tutorial 3: Tailwind CSS徹底習得",
        "time": "50時間",
        "description": "パッケージ管理、Tailwind CSSの導入、レスポンシブデザインを学びます。"
    },
    "tutorial04_JavaScript_基礎とDOM操作": {
        "order": 4,
        "title": "Tutorial 4: JavaScript基礎とDOM操作",
        "time": "50時間",
        "description": "JavaScriptの基本構文、配列・オブジェクト、DOM操作を学びます。"
    },
    "tutorial05_JavaScript_応用と非同期処理": {
        "order": 5,
        "title": "Tutorial 5: JavaScript応用と非同期処理",
        "time": "50時間",
        "description": "非同期処理（Promise, async/await）、fetch API、エラーハンドリングを学びます。"
    },
    "tutorial06_TypeScript入門": {
        "order": 6,
        "title": "Tutorial 6: TypeScript入門",
        "time": "70時間",
        "description": "TypeScriptの基本的な型、開発環境設定、高度な型操作を学びます。"
    },
    "tutorial07_React入門": {
        "order": 7,
        "title": "Tutorial 7: React入門",
        "time": "80時間",
        "description": "Reactの基本概念、Props、Stateによる状態管理を学びます。"
    },
    "tutorial08_React応用": {
        "order": 8,
        "title": "Tutorial 8: React応用",
        "time": "80時間",
        "description": "useEffect、カスタムフック、React Hook Form/Zodなどのライブラリを学びます。"
    },
    "tutorial09_Next.js": {
        "order": 9,
        "title": "Tutorial 9: Next.js",
        "time": "90時間",
        "description": "Next.jsの基本、ルーティング、レンダリングとパフォーマンスを学びます。"
    },
    "tutorial10_Laravel_x_Next.js": {
        "order": 10,
        "title": "Tutorial 10: Laravel × Next.js",
        "time": "80時間",
        "description": "Laravel SailとNext.jsの連携、API呼び出し、認証機能を学びます。"
    },
    "tutorial11_テスト": {
        "order": 11,
        "title": "Tutorial 11: テスト",
        "time": "60時間",
        "description": "Vitestによるユニットテスト、PlaywrightによるE2Eテスト、Storybookを学びます。"
    },
    "tutorial12_column": {
        "order": 12,
        "title": "上級コラム: Webレンダリングの深層理解",
        "time": "60時間（任意）",
        "description": "ブラウザのレンダリングプロセス、各種レンダリング戦略、RSCを学びます。",
        "is_column": True  # コラム形式のフラグ
    }
}


def get_html_template(title, content, breadcrumb, sidebar_html, css_path="style.css"):
    """HTMLテンプレートを生成"""
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)} | {SITE_TITLE}</title>
    <meta name="description" content="{SITE_DESCRIPTION}">
    <link rel="stylesheet" href="{css_path}">
</head>
<body>
    <div id="outer">
        <header>
            <h1><a href="index.html">{SITE_TITLE}</a></h1>
            <p class="description">{SITE_DESCRIPTION}</p>
        </header>
        <div id="container">
            <aside>
                <div id="side-inner">
                    {sidebar_html}
                </div>
            </aside>
            <div id="content">
                <div class="inner">
                    {breadcrumb}
                    {content}
                </div>
            </div>
        </div>
        <footer>
            &copy; 2025 {SITE_TITLE}
        </footer>
    </div>
</body>
</html>
'''


def generate_sidebar_top(contents):
    """トップページ用サイドバーHTMLを生成"""
    html = '<div class="side-title">コンテンツ一覧</div>\n'
    html += '<div class="side"><ul>\n'
    
    for content_dir, info in sorted(contents.items(), key=lambda x: x[1]["order"]):
        html += f'<li><a href="{info["slug"]}/index.html">{info["title"]}</a></li>\n'
    
    html += '</ul></div>\n'
    return html


def generate_sidebar_tutorials(tutorials, current_tutorial=None):
    """チュートリアル用サイドバーHTMLを生成"""
    html = '<div class="side-title">チュートリアル一覧</div>\n'
    html += '<div class="side"><ul>\n'
    
    for tutorial_dir, info in sorted(tutorials.items(), key=lambda x: x[1]["order"]):
        current_class = ' class="current"' if tutorial_dir == current_tutorial else ''
        html += f'<li><a href="{tutorial_slug(tutorial_dir)}.html"{current_class}>{info["title"]}</a></li>\n'
    
    html += '</ul></div>\n'
    return html


def get_tutorials(content_path):
    """コンテンツ内のチュートリアルを取得"""
    tutorials = {}
    if content_path.exists():
        for tutorial_dir, info in TUTORIAL_INFO.items():
            if (content_path / tutorial_dir).exists():
                tutorials[tutorial_dir] = info
    return tutorials


def get_chapters(tutorial_path):
    """チュートリアル内のチャプターを取得"""
    chapters = []
    if tutorial_path.exists():
        for item in sorted(tutorial_path.iterdir()):
            if item.is_dir() and item.name.startswith("chapter"):
                chapters.append(item)
    return chapters


def get_column_chapters(tutorial_path):
    """コラム形式のチュートリアル内のチャプター（col形式）を取得"""
    chapters = []
    if tutorial_path.exists():
        for item in sorted(tutorial_path.iterdir()):
            if item.is_dir() and item.name.startswith("col"):
                chapters.append(item)
    return chapters


def get_sections(chapter_path):
    """チャプター内のセクションを取得"""
    sections = []
    if chapter_path.exists():
        for item in sorted(chapter_path.iterdir()):
            if item.is_file() and item.suffix == ".md":
                sections.append(item)
    return sections


def extract_section_number(filename):
    """ファイル名からセクション番号を抽出"""
    # 通常形式: 1-1-1
    match = re.match(r'^(\d+-\d+-\d+)', filename)
    if match:
        return match.group(1)
    # コラム形式: Col-1-1
    match = re.match(r'^(Col-\d+-\d+)', filename)
    if match:
        return match.group(1)
    return ""


def clean_title(filename):
    """ファイル名からタイトルを抽出"""
    # 拡張子を除去
    name = filename.replace(".md", "")
    # セクション番号を除去（通常形式）
    name = re.sub(r'^\d+-\d+-\d+[:\s]*', '', name)
    # セクション番号を除去（コラム形式）
    name = re.sub(r'^Col-\d+-\d+[:\s]*', '', name)
    return name


def format_chapter_title(chapter_name):
    """チャプター名を整形"""
    # chapter01_xxx -> Chapter 1: xxx
    match = re.match(r'chapter(\d+)_(.+)', chapter_name)
    if match:
        num = int(match.group(1))
        title = match.group(2).replace("_", " ")
        return f"Chapter {num}: {title}"
    return chapter_name


def format_column_chapter_title(chapter_name):
    """コラムチャプター名を整形"""
    # col01_xxx -> Column 1: xxx
    match = re.match(r'col(\d+)_(.+)', chapter_name)
    if match:
        num = int(match.group(1))
        title = match.group(2).replace("_", " ")
        return f"Column {num}: {title}"
    return chapter_name


# ---------------------------------------------------------------------------
# 短縮URL用のスラッグ生成
#
# 公開URLを日本語パス（%E3%82... で数百文字になる）から解放するための仕組み。
#   チュートリアル: t1.html      （tutorial01_開発環境とWebの基礎固め）
#   チャプター:     1-1.html     （tutorial01 / chapter01）
#   セクション:     1-1-1.html   （1-1-1: このチュートリアルで学ぶこと.md）
#   コラム:         col-1.html / col-1-1.html
# セクション番号は教材全体で一意かつディレクトリ位置と一致していることを確認済み。
# ---------------------------------------------------------------------------

def tutorial_slug(tutorial_dir):
    """tutorial01_開発環境とWebの基礎固め -> t1"""
    match = re.match(r'tutorial(\d+)', tutorial_dir)
    if match:
        return f"t{int(match.group(1))}"
    return tutorial_dir


def chapter_slug(tutorial_dir, chapter_name):
    """(tutorial02_..., chapter03_...) -> 2-3 / (tutorial12_column, col01_...) -> col-1"""
    match = re.match(r'(chapter|col)(\d+)', chapter_name)
    if not match:
        return f"{tutorial_slug(tutorial_dir)}-{chapter_name}"
    kind, num = match.group(1), int(match.group(2))
    if kind == "col":
        return f"col-{num}"
    tutorial_match = re.match(r'tutorial(\d+)', tutorial_dir)
    tutorial_num = int(tutorial_match.group(1)) if tutorial_match else 0
    return f"{tutorial_num}-{num}"


def section_slug(tutorial_dir, chapter_name, section_filename, section_index):
    """'2-3-1: xxx.md' -> 2-3-1 / 'Col-1-1: xxx.md' -> col-1-1"""
    number = extract_section_number(section_filename)
    if number:
        return number.lower()
    # 番号なしのファイルが将来増えた場合のフォールバック
    return f"{chapter_slug(tutorial_dir, chapter_name)}-{section_index}"


def get_redirect_html(target, title):
    """旧URL用の転送ページを生成

    GitHub Pages は 301 リダイレクトを設定できないため、
    meta refresh + canonical + JS の三段構えで新URLへ飛ばす。
    """
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="refresh" content="0; url={target}">
    <link rel="canonical" href="{target}">
    <meta name="robots" content="noindex">
    <title>{escape(title)} | {SITE_TITLE}</title>
    <style>
        body {{ font-family: sans-serif; margin: 4em auto; max-width: 40em; padding: 0 1em; line-height: 1.8; color: #333; }}
        a {{ color: #0b6bcb; }}
    </style>
    <script>location.replace("{target}");</script>
</head>
<body>
    <p>このページは新しいURLへ移動しました。自動で切り替わります。</p>
    <p><a href="{target}">切り替わらない場合はこちらをクリックしてください</a></p>
</body>
</html>
'''


def write_redirect(legacy_path, target, title):
    """旧URLのパスに転送ページを書き出す"""
    legacy_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_path.write_text(get_redirect_html(target, title), encoding="utf-8")
    REDIRECTS_WRITTEN.append(legacy_path)


REDIRECTS_WRITTEN = []


def md_to_html(md_content):
    """MarkdownをHTMLに変換"""
    md = markdown.Markdown(
        extensions=[
            'tables',
            'fenced_code',
            'codehilite',
            'toc',
            'nl2br'
        ],
        extension_configs={
            'codehilite': {'use_pygments': False}
        }
    )
    return md.convert(md_content)


def generate_top_index_page(contents):
    """トップページ（コンテンツ一覧）を生成"""
    content = '<h2>コンテンツ一覧</h2>\n'
    content += '<p>Laravelエンジニアがさらなる技術力を高めていくための学習コンテンツです。</p>\n'
    content += '<div class="tutorial-list">\n'
    
    for content_dir, info in sorted(contents.items(), key=lambda x: x[1]["order"]):
        content_path = BASE_DIR / content_dir
        tutorials = get_tutorials(content_path)
        tutorial_count = len(tutorials)
        
        content += f'''<div class="tutorial-card">
    <h3><a href="{info["slug"]}/index.html">{info["title"]}</a></h3>
    <div class="meta">学習時間: {info["time"]} | {tutorial_count}チュートリアル</div>
    <div class="description">{info["description"]}</div>
</div>
'''
    
    content += '</div>\n'
    
    breadcrumb = '<div class="breadcrumb"><a href="index.html">ホーム</a></div>'
    sidebar = generate_sidebar_top(contents)
    
    html = get_html_template("ホーム", content, breadcrumb, sidebar)
    
    output_path = OUTPUT_DIR / "index.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")


def generate_content_index_page(content_dir, content_info, tutorials):
    """コンテンツのトップページ（チュートリアル一覧）を生成"""
    content = f'<h2>{content_info["title"]}</h2>\n'
    content += f'<p>{content_info["description"]}</p>\n'
    content += '<div class="tutorial-list">\n'
    
    content_path = BASE_DIR / content_dir
    
    for tutorial_dir, info in sorted(tutorials.items(), key=lambda x: x[1]["order"]):
        tutorial_path = content_path / tutorial_dir
        
        # コラム形式かどうかで取得方法を変える
        if info.get("is_column"):
            chapters = get_column_chapters(tutorial_path)
        else:
            chapters = get_chapters(tutorial_path)
        chapter_count = len(chapters)
        
        content += f'''<div class="tutorial-card">
    <h3><a href="{tutorial_slug(tutorial_dir)}.html">{info["title"]}</a></h3>
    <div class="meta">学習時間: {info["time"]} | {chapter_count}チャプター</div>
    <div class="description">{info["description"]}</div>
</div>
'''

    content += '</div>\n'

    breadcrumb = f'<div class="breadcrumb"><a href="../index.html">ホーム</a><span>></span>{content_info["title"]}</div>'
    sidebar = generate_sidebar_tutorials(tutorials)

    html = get_html_template(content_info["title"], content, breadcrumb, sidebar, css_path="../style.css")

    # 短縮URL側（実ページ）
    content_output_dir = OUTPUT_DIR / content_info["slug"]
    content_output_dir.mkdir(exist_ok=True)

    output_path = content_output_dir / "index.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")

    # 旧URL側（転送ページ）
    write_redirect(
        OUTPUT_DIR / content_dir / "index.html",
        f'../{content_info["slug"]}/index.html',
        content_info["title"]
    )


def generate_tutorial_page(content_dir, content_info, tutorial_dir, tutorial_info, tutorials):
    """チュートリアルページ（チャプター一覧）を生成"""
    content_path = BASE_DIR / content_dir
    tutorial_path = content_path / tutorial_dir
    
    # コラム形式かどうかで取得方法を変える
    is_column = tutorial_info.get("is_column", False)
    if is_column:
        chapters = get_column_chapters(tutorial_path)
    else:
        chapters = get_chapters(tutorial_path)
    
    content = f'<h2>{tutorial_info["title"]}</h2>\n'
    content += f'<p>学習時間: {tutorial_info["time"]}</p>\n'
    content += f'<p>{tutorial_info["description"]}</p>\n'
    content += '<div class="chapter-list">\n'
    
    for chapter in chapters:
        if is_column:
            chapter_title = format_column_chapter_title(chapter.name)
        else:
            chapter_title = format_chapter_title(chapter.name)
        sections = get_sections(chapter)
        section_count = len(sections)

        content += f'''<div class="chapter-item">
    <h3><a href="{chapter_slug(tutorial_dir, chapter.name)}.html">{chapter_title}</a></h3>
    <div class="section-count">{section_count}セクション</div>
</div>
'''

    content += '</div>\n'

    breadcrumb = f'<div class="breadcrumb"><a href="../index.html">ホーム</a><span>></span><a href="index.html">{content_info["title"]}</a><span>></span>{tutorial_info["title"]}</div>'
    sidebar = generate_sidebar_tutorials(tutorials, tutorial_dir)

    html = get_html_template(tutorial_info["title"], content, breadcrumb, sidebar, css_path="../style.css")

    # 短縮URL側（実ページ）
    output_path = OUTPUT_DIR / content_info["slug"] / f"{tutorial_slug(tutorial_dir)}.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")

    # 旧URL側（転送ページ）
    write_redirect(
        OUTPUT_DIR / content_dir / f"{tutorial_dir}.html",
        f'../{content_info["slug"]}/{tutorial_slug(tutorial_dir)}.html',
        tutorial_info["title"]
    )


def generate_chapter_page(content_dir, content_info, tutorial_dir, chapter, tutorial_info, tutorials, is_column=False):
    """チャプターページ（セクション一覧）を生成"""
    if is_column:
        chapter_title = format_column_chapter_title(chapter.name)
    else:
        chapter_title = format_chapter_title(chapter.name)
    sections = get_sections(chapter)
    
    content = f'<h2>{chapter_title}</h2>\n'
    content += '<div class="section-list">\n'
    
    for i, section in enumerate(sections, 1):
        section_num = extract_section_number(section.name)
        section_title = clean_title(section.name)
        section_href = f"{section_slug(tutorial_dir, chapter.name, section.name, i)}.html"

        content += f'''<div class="section-item">
    <div class="section-number">{section_num or i}</div>
    <div class="section-title"><a href="{section_href}">{section_title}</a></div>
</div>
'''

    content += '</div>\n'

    breadcrumb = f'<div class="breadcrumb"><a href="../index.html">ホーム</a><span>></span><a href="index.html">{content_info["title"]}</a><span>></span><a href="{tutorial_slug(tutorial_dir)}.html">{tutorial_info["title"]}</a><span>></span>{chapter_title}</div>'
    sidebar = generate_sidebar_tutorials(tutorials, tutorial_dir)

    html = get_html_template(chapter_title, content, breadcrumb, sidebar, css_path="../style.css")

    # 短縮URL側（実ページ）
    output_path = OUTPUT_DIR / content_info["slug"] / f"{chapter_slug(tutorial_dir, chapter.name)}.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")

    # 旧URL側（転送ページ）
    write_redirect(
        OUTPUT_DIR / content_dir / f"{tutorial_dir}_{chapter.name}.html",
        f'../{content_info["slug"]}/{chapter_slug(tutorial_dir, chapter.name)}.html',
        chapter_title
    )


def generate_section_page(content_dir, content_info, tutorial_dir, chapter, section, tutorial_info, tutorials, sections, section_index, is_column=False):
    """セクションページを生成"""
    if is_column:
        chapter_title = format_column_chapter_title(chapter.name)
    else:
        chapter_title = format_chapter_title(chapter.name)
    section_title = clean_title(section.name)
    
    # Markdownを読み込んでHTMLに変換
    md_content = section.read_text(encoding="utf-8")
    html_content = md_to_html(md_content)
    
    content = f'<div class="section-content">\n{html_content}\n</div>\n'
    
    # 前後のセクションへのナビゲーション
    content += '<div class="section-nav">\n'
    
    if section_index > 0:
        prev_section = sections[section_index - 1]
        prev_href = f"{section_slug(tutorial_dir, chapter.name, prev_section.name, section_index)}.html"
        prev_title = clean_title(prev_section.name)
        content += f'<a href="{prev_href}" class="prev">{prev_title}</a>\n'
    else:
        content += '<span></span>\n'

    if section_index < len(sections) - 1:
        next_section = sections[section_index + 1]
        next_href = f"{section_slug(tutorial_dir, chapter.name, next_section.name, section_index + 2)}.html"
        next_title = clean_title(next_section.name)
        content += f'<a href="{next_href}" class="next">{next_title}</a>\n'
    else:
        content += '<span></span>\n'

    content += '</div>\n'

    section_short = section_slug(tutorial_dir, chapter.name, section.name, section_index + 1)

    breadcrumb = f'<div class="breadcrumb"><a href="../index.html">ホーム</a><span>></span><a href="index.html">{content_info["title"]}</a><span>></span><a href="{tutorial_slug(tutorial_dir)}.html">{tutorial_info["title"]}</a><span>></span><a href="{chapter_slug(tutorial_dir, chapter.name)}.html">{chapter_title}</a><span>></span>{section_title}</div>'
    sidebar = generate_sidebar_tutorials(tutorials, tutorial_dir)

    html = get_html_template(section_title, content, breadcrumb, sidebar, css_path="../style.css")

    # 短縮URL側（実ページ）
    output_path = OUTPUT_DIR / content_info["slug"] / f"{section_short}.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")

    # 旧URL側（転送ページ）
    write_redirect(
        OUTPUT_DIR / content_dir / f"{tutorial_dir}_{chapter.name}_{section.stem}.html",
        f'../{content_info["slug"]}/{section_short}.html',
        section_title
    )


def main():
    """メイン処理"""
    print("静的サイト生成を開始します...")
    
    # 出力ディレクトリを作成
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 存在するコンテンツのみを対象にする
    contents = {}
    for content_dir, info in CONTENTS_INFO.items():
        if (BASE_DIR / content_dir).exists():
            contents[content_dir] = info
    
    # トップページを生成（コンテンツ一覧）
    generate_top_index_page(contents)
    
    # 各コンテンツのページを生成
    for content_dir, content_info in contents.items():
        content_path = BASE_DIR / content_dir
        tutorials = get_tutorials(content_path)
        
        # コンテンツのトップページ（チュートリアル一覧）
        generate_content_index_page(content_dir, content_info, tutorials)
        
        # 各チュートリアルのページを生成
        for tutorial_dir, tutorial_info in tutorials.items():
            tutorial_path = content_path / tutorial_dir
            
            # コラム形式かどうかを判定
            is_column = tutorial_info.get("is_column", False)
            
            # チュートリアルページ（チャプター一覧）
            generate_tutorial_page(content_dir, content_info, tutorial_dir, tutorial_info, tutorials)
            
            # 各チャプターのページ
            if is_column:
                chapters = get_column_chapters(tutorial_path)
            else:
                chapters = get_chapters(tutorial_path)
            
            for chapter in chapters:
                # チャプターページ（セクション一覧）
                generate_chapter_page(content_dir, content_info, tutorial_dir, chapter, tutorial_info, tutorials, is_column)
                
                # 各セクションのページ
                sections = get_sections(chapter)
                for i, section in enumerate(sections):
                    generate_section_page(content_dir, content_info, tutorial_dir, chapter, section, tutorial_info, tutorials, sections, i, is_column)
    
    # 短縮URLの衝突チェック
    # スラッグが重複すると後勝ちで静かに上書きされ、ページが消える。
    # 「期待ページ数 == 実ファイル数」で検知する。
    for content_dir, content_info in contents.items():
        content_path = BASE_DIR / content_dir
        tutorials = get_tutorials(content_path)
        expected = 1  # index.html
        for tutorial_dir, tutorial_info in tutorials.items():
            tutorial_path = content_path / tutorial_dir
            if tutorial_info.get("is_column"):
                chapters = get_column_chapters(tutorial_path)
            else:
                chapters = get_chapters(tutorial_path)
            expected += 1 + len(chapters)
            for chapter in chapters:
                expected += len(get_sections(chapter))

        actual = len(list((OUTPUT_DIR / content_info["slug"]).glob("*.html")))
        if actual != expected:
            raise SystemExit(
                f"[ERROR] 短縮URLのスラッグが衝突しています: "
                f"{content_info['slug']} 期待 {expected} ページ / 実際 {actual} ページ"
            )

    total = len(list(OUTPUT_DIR.rglob('*.html')))
    print(f"\n生成完了！出力先: {OUTPUT_DIR}")
    print(f"  実ページ（短縮URL）: {total - len(REDIRECTS_WRITTEN)}")
    print(f"  旧URLからの転送ページ: {len(REDIRECTS_WRITTEN)}")
    print(f"生成されたHTMLファイル数: {total}")


if __name__ == "__main__":
    main()
