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
BASE_DIR = Path("/home/ubuntu/pro-contents")
CONTENT_DIR = BASE_DIR / "laravelエンジニアのためのフロントエンド学習ロードマップ"
OUTPUT_DIR = BASE_DIR / "docs"

# サイト情報
SITE_TITLE = "Laravelエンジニアのためのフロントエンド学習ロードマップ"
SITE_DESCRIPTION = "PHP/Laravelエンジニアがフロントエンド開発を習得するための教材"

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
        "description": "ブラウザのレンダリングプロセス、各種レンダリング戦略、RSCを学びます。"
    }
}


def get_html_template(title, content, breadcrumb, sidebar_html):
    """HTMLテンプレートを生成"""
    return f'''<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{escape(title)} | {SITE_TITLE}</title>
    <meta name="description" content="{SITE_DESCRIPTION}">
    <link rel="stylesheet" href="style.css">
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


def generate_sidebar(tutorials, current_tutorial=None):
    """サイドバーHTMLを生成"""
    html = '<div class="side-title">チュートリアル一覧</div>\n'
    html += '<div class="side"><ul>\n'
    
    for tutorial_dir, info in sorted(tutorials.items(), key=lambda x: x[1]["order"]):
        current_class = ' class="current"' if tutorial_dir == current_tutorial else ''
        html += f'<li><a href="{tutorial_dir}.html"{current_class}>{info["title"]}</a></li>\n'
    
    html += '</ul></div>\n'
    return html


def get_chapters(tutorial_path):
    """チュートリアル内のチャプターを取得"""
    chapters = []
    if tutorial_path.exists():
        for item in sorted(tutorial_path.iterdir()):
            if item.is_dir() and item.name.startswith("chapter"):
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
    match = re.match(r'^(\d+-\d+-\d+)', filename)
    if match:
        return match.group(1)
    return ""


def clean_title(filename):
    """ファイル名からタイトルを抽出"""
    # 拡張子を除去
    name = filename.replace(".md", "")
    # セクション番号を除去
    name = re.sub(r'^\d+-\d+-\d+[:\s]*', '', name)
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


def md_to_html(md_content):
    """MarkdownをHTMLに変換"""
    md = markdown.Markdown(extensions=[
        'tables',
        'fenced_code',
        'codehilite',
        'toc',
        'nl2br'
    ])
    return md.convert(md_content)


def generate_index_page(tutorials):
    """トップページ（チュートリアル一覧）を生成"""
    content = '<h2>チュートリアル一覧</h2>\n'
    content += '<p>このロードマップは、PHP/Laravelエンジニアがフロントエンド開発（JavaScript/TypeScript/React/Next.js）を習得し、2年目レベルのスキルを身につけるための教材です。</p>\n'
    content += '<div class="tutorial-list">\n'
    
    for tutorial_dir, info in sorted(tutorials.items(), key=lambda x: x[1]["order"]):
        tutorial_path = CONTENT_DIR / tutorial_dir
        chapters = get_chapters(tutorial_path)
        chapter_count = len(chapters)
        
        content += f'''<div class="tutorial-card">
    <h3><a href="{tutorial_dir}.html">{info["title"]}</a></h3>
    <div class="meta">学習時間: {info["time"]} | {chapter_count}チャプター</div>
    <div class="description">{info["description"]}</div>
</div>
'''
    
    content += '</div>\n'
    
    breadcrumb = '<div class="breadcrumb"><a href="index.html">ホーム</a></div>'
    sidebar = generate_sidebar(tutorials)
    
    html = get_html_template("ホーム", content, breadcrumb, sidebar)
    
    output_path = OUTPUT_DIR / "index.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")


def generate_tutorial_page(tutorial_dir, info, tutorials):
    """チュートリアルページ（チャプター一覧）を生成"""
    tutorial_path = CONTENT_DIR / tutorial_dir
    chapters = get_chapters(tutorial_path)
    
    content = f'<h2>{info["title"]}</h2>\n'
    content += f'<p>学習時間: {info["time"]}</p>\n'
    content += f'<p>{info["description"]}</p>\n'
    content += '<div class="chapter-list">\n'
    
    for chapter in chapters:
        chapter_title = format_chapter_title(chapter.name)
        sections = get_sections(chapter)
        section_count = len(sections)
        
        chapter_id = f"{tutorial_dir}_{chapter.name}"
        
        content += f'''<div class="chapter-item">
    <h3><a href="{chapter_id}.html">{chapter_title}</a></h3>
    <div class="section-count">{section_count}セクション</div>
</div>
'''
    
    content += '</div>\n'
    
    breadcrumb = f'<div class="breadcrumb"><a href="index.html">ホーム</a><span>></span>{info["title"]}</div>'
    sidebar = generate_sidebar(tutorials, tutorial_dir)
    
    html = get_html_template(info["title"], content, breadcrumb, sidebar)
    
    output_path = OUTPUT_DIR / f"{tutorial_dir}.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")


def generate_chapter_page(tutorial_dir, chapter, info, tutorials):
    """チャプターページ（セクション一覧）を生成"""
    chapter_title = format_chapter_title(chapter.name)
    sections = get_sections(chapter)
    
    content = f'<h2>{chapter_title}</h2>\n'
    content += '<div class="section-list">\n'
    
    for i, section in enumerate(sections, 1):
        section_num = extract_section_number(section.name)
        section_title = clean_title(section.name)
        section_id = f"{tutorial_dir}_{chapter.name}_{section.stem}"
        
        content += f'''<div class="section-item">
    <div class="section-number">{section_num or i}</div>
    <div class="section-title"><a href="{section_id}.html">{section_title}</a></div>
</div>
'''
    
    content += '</div>\n'
    
    chapter_id = f"{tutorial_dir}_{chapter.name}"
    breadcrumb = f'<div class="breadcrumb"><a href="index.html">ホーム</a><span>></span><a href="{tutorial_dir}.html">{info["title"]}</a><span>></span>{chapter_title}</div>'
    sidebar = generate_sidebar(tutorials, tutorial_dir)
    
    html = get_html_template(chapter_title, content, breadcrumb, sidebar)
    
    output_path = OUTPUT_DIR / f"{chapter_id}.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")


def generate_section_page(tutorial_dir, chapter, section, info, tutorials, sections, section_index):
    """セクションページを生成"""
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
        prev_id = f"{tutorial_dir}_{chapter.name}_{prev_section.stem}"
        prev_title = clean_title(prev_section.name)
        content += f'<a href="{prev_id}.html" class="prev">{prev_title}</a>\n'
    else:
        content += '<span></span>\n'
    
    if section_index < len(sections) - 1:
        next_section = sections[section_index + 1]
        next_id = f"{tutorial_dir}_{chapter.name}_{next_section.stem}"
        next_title = clean_title(next_section.name)
        content += f'<a href="{next_id}.html" class="next">{next_title}</a>\n'
    else:
        content += '<span></span>\n'
    
    content += '</div>\n'
    
    chapter_id = f"{tutorial_dir}_{chapter.name}"
    section_id = f"{tutorial_dir}_{chapter.name}_{section.stem}"
    
    breadcrumb = f'<div class="breadcrumb"><a href="index.html">ホーム</a><span>></span><a href="{tutorial_dir}.html">{info["title"]}</a><span>></span><a href="{chapter_id}.html">{chapter_title}</a><span>></span>{section_title}</div>'
    sidebar = generate_sidebar(tutorials, tutorial_dir)
    
    html = get_html_template(section_title, content, breadcrumb, sidebar)
    
    output_path = OUTPUT_DIR / f"{section_id}.html"
    output_path.write_text(html, encoding="utf-8")
    print(f"Generated: {output_path}")


def main():
    """メイン処理"""
    print("静的サイト生成を開始します...")
    
    # 出力ディレクトリを作成
    OUTPUT_DIR.mkdir(exist_ok=True)
    
    # 存在するチュートリアルのみを対象にする
    tutorials = {}
    for tutorial_dir, info in TUTORIAL_INFO.items():
        if (CONTENT_DIR / tutorial_dir).exists():
            tutorials[tutorial_dir] = info
    
    # トップページを生成
    generate_index_page(tutorials)
    
    # 各チュートリアルのページを生成
    for tutorial_dir, info in tutorials.items():
        tutorial_path = CONTENT_DIR / tutorial_dir
        
        # チュートリアルページ（チャプター一覧）
        generate_tutorial_page(tutorial_dir, info, tutorials)
        
        # 各チャプターのページ
        chapters = get_chapters(tutorial_path)
        for chapter in chapters:
            # チャプターページ（セクション一覧）
            generate_chapter_page(tutorial_dir, chapter, info, tutorials)
            
            # 各セクションのページ
            sections = get_sections(chapter)
            for i, section in enumerate(sections):
                generate_section_page(tutorial_dir, chapter, section, info, tutorials, sections, i)
    
    print(f"\n生成完了！出力先: {OUTPUT_DIR}")
    print(f"生成されたHTMLファイル数: {len(list(OUTPUT_DIR.glob('*.html')))}")


if __name__ == "__main__":
    main()
