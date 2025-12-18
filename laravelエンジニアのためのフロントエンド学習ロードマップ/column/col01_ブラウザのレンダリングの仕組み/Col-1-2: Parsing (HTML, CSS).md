# Col-1-2: Parsing (HTML, CSS)

## 🎯 このセクションで学ぶこと

-   ブラウザがHTMLを解析してDOMツリーを構築するプロセスを理解する。
-   ブラウザがCSSを解析してCSSOMツリーを構築するプロセスを理解する。
-   レンダリングブロッキングリソース（特にCSSとJavaScript）がCRPに与える影響を学ぶ。

## 導入

前のセクションで、クリティカルレンダリングパス（CRP）の概要を学びました。CRPの最初の重要なステップは、HTMLとCSSの**解析（Parsing）**です。ブラウザは、サーバーから受け取ったテキストベースのHTMLとCSSのファイルを、自身が理解できるデータ構造、すなわち**DOMツリー**と**CSSOMツリー**に変換します。このプロセスが、最終的なページの見た目を構築するための基礎となります。

## HTMLの解析とDOMの構築

ブラウザがサーバーからHTMLドキュメントを受け取ると、DOM（Document Object Model）ツリーの構築プロセスが始まります。これは、以下の4つのステップで行われます。[1]

1.  **バイト → 文字**: サーバーから受け取ったHTMLファイルは、まず生のバイトデータとして読み込まれます。ブラウザはファイルのエンコーディング（例: `UTF-8`）に基づいて、これらのバイトを文字に変換します。

2.  **文字 → トークン**: 次に、変換された文字のストリームをW3CのHTML5標準に基づいて**トークン化**します。例えば、`<html>`は「開始タグトークン」、`<body>`は「開始タグトークン」、テキストは「文字トークン」、`</body>`は「終了タグトークン」といった具合に、意味のある単位に分割されます。

3.  **トークン → ノード**: 生成されたトークンは、それぞれが特定のプロパティやルールを持つ「オブジェクト（ノード）」に変換されます。

4.  **ノード → DOMツリー**: HTMLタグの親子関係（入れ子構造）に基づいて、作成されたノードがツリー状のデータ構造にリンクされます。これが**DOMツリー**です。例えば、`<html>`オブジェクトは`<body>`オブジェクトの親であり、`<body>`は`<p>`オブジェクトの親、といった関係が構築されます。

![DOMツリー構築のプロセス](https://raw.githubusercontent.com/coachtech-material/pro-contents/main/laravel%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%95%E3%83%AD%E3%83%B3%E3%83%88%E3%82%A8%E3%83%B3%E3%83%89%E5%AD%A6%E7%BF%92%E3%83%AD%E3%83%BC%E3%83%89%E3%83%9E%E3%83%83%E3%83%97/images/column/dom-construction.png)

この全プロセスは、非常に効率的に行われるように最適化されており、ブラウザはHTMLを**ストリーミング**しながら、つまりドキュメント全体がダウンロードされるのを待たずに、部分的に解析してDOMツリーを構築していくことができます。

## CSSの解析とCSSOMの構築

HTMLの解析中に、ブラウザが`<link rel="stylesheet">`や`<style>`タグに遭遇すると、CSSの解析と**CSSOM（CSS Object Model）**ツリーの構築を開始します。このプロセスもHTMLの解析と似ていますが、重要な違いがあります。

CSSの「C」はCascading（カスケード、滝のように流れる）の略で、スタイルルールが親から子へと継承される性質を持っています。そのため、あるノードの最終的なスタイルを決定するには、そのノード自身に適用されるルールだけでなく、親要素から継承されるスタイルや、より具体的なセレクタによる上書きなど、複数のルールを考慮する必要があります。

> そのため、ブラウザはドキュメント内の他のスタイルルールをブロックして CSS を処理することはできません。つまり、CSSOM を構築する間、他のすべての CSS をダウンロードして処理する必要があるのです。
> --- Google Developers, "Render-Blocking CSS" [2]

この性質のため、CSSは**レンダリングブロッキングリソース**と見なされます。ブラウザは、すべてのCSSを解析し、CSSOMツリー全体を構築し終わるまで、ページのレンダリングを開始できません。もしCSSOMの構築が遅れると、Render Treeの構築も遅れ、結果としてユーザーは何も表示されない白い画面を長く見ることになります。

## JavaScriptと解析のブロッキング

JavaScriptもまた、CRPに大きな影響を与える要因です。

HTMLの解析中に`<script>`タグが見つかると、ブラウザは**DOMの構築を一時停止**し、JavaScriptエンジンに制御を渡してスクリプトをダウンロード・解析・実行します。なぜなら、JavaScriptは`document.write()`のような命令でDOMの構造自体を変更する可能性があるため、ブラウザは安全のためにHTMLの解析を続けられないのです。

```html
<html>
  <head>
    <link href="style.css" rel="stylesheet">
  </head>
  <body>
    <p>Hello, <span>world!</span></p>
    <script src="app.js"></script> <!-- DOM構築がここでブロックされる -->
    <div>...</div>
  </body>
</html>
```

さらに、JavaScriptはCSSOMにアクセスしてスタイル情報を問い合わせることもできます（例: `element.style.width`）。もしブラウザがCSSOMの構築が終わっていない状態でJavaScriptを実行しようとすると、スクリプトは不正確な情報を得てしまうかもしれません。このため、ブラウザは先行するCSSのダウンロードとCSSOMの構築が完了するまで、JavaScriptの実行を待機します。

結果として、**CSSはJavaScriptの実行をブロックし、JavaScriptはDOMの構築をブロックする**という依存関係が生まれます。これが、`<link>`タグを`<head>`内に、`<script>`タグを`<body>`の最後に置くことが推奨される主な理由です。

### ブロッキングを回避する方法

幸い、JavaScriptによるDOM構築のブロッキングは、`async`属性や`defer`属性を使うことで制御できます。

-   **`async`**: HTMLの解析をブロックせず、スクリプトを非同期にダウンロードします。ダウンロードが完了次第、DOM構築を一時停止してスクリプトを実行します。
-   **`defer`**: HTMLの解析をブロックせず、スクリプトを非同期にダウンロードします。スクリプトの実行は、DOM構築が完了した後、`DOMContentLoaded`イベントの前に実行されます。

```html
<script src="app.js" async></script>
<script src="app.js" defer></script>
```

これらの属性を適切に使うことで、JavaScriptによるブロッキングの影響を最小限に抑え、CRPを高速化できます。

## ✨ まとめ

-   ブラウザはHTMLを解析してDOMツリーを、CSSを解析してCSSOMツリーを構築する。
-   CSSはレンダリングブロッキングリソースであり、CSSOMの構築が完了するまでページの描画は始まらない。
-   JavaScriptはDOMの構築をブロックする可能性があり、またCSSOMの完成を待ってから実行される。
-   `<script>`タグに`async`や`defer`属性を使用することで、JavaScriptによるブロッキングを制御し、パフォーマンスを改善できる。

---

## 参考文献

[1] Google Developers. (n.d.). *Constructing the Object Model*. Retrieved from https://developers.google.com/web/fundamentals/performance/critical-rendering-path/constructing-the-object-model

[2] Google Developers. (n.d.). *Render-Blocking CSS*. Retrieved from https://developers.google.com/web/fundamentals/performance/critical-rendering-path/render-blocking-css
