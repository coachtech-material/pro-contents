# Col-1-1: Critical Rendering Path（クリティカルレンダリングパス）

## 🎯 このセクションで学ぶこと

-   クリティカルレンダリングパス（CRP）の定義と、なぜそれがWebパフォーマンスにとって重要なのかを理解する。
-   CRPを構成する主要なステップ（DOM構築、CSSOM構築、Render Tree構築、Layout、Paint）の概要を学ぶ。
-   CRPの最適化が、体感的なページの読み込み速度にどのように影響するかを理解する。

## 導入

Webサイトのパフォーマンスを語る上で、**クリティカルレンダリングパス（Critical Rendering Path, CRP）**の理解は不可欠です。CRPとは、ブラウザがHTML、CSS、JavaScriptのコードを受け取ってから、それを画面上のピクセルとして描画するまでの一連のステップを指します。[1]

このパスを最適化することは、ページの表示速度を向上させ、ユーザー体験（UX）を改善するために極めて重要です。ユーザーは、ページの読み込みが遅いとすぐに離脱してしまう傾向があります。CRPを理解し、ボトルネックを特定して解消することで、より高速で快適なWebサイトを構築できます。

## CRPの主要なステップ

CRPは、大きく分けて以下のステップで構成されています。

1.  **DOM (Document Object Model) の構築**: ブラウザがHTMLを解析し、DOMツリーを作成する。
2.  **CSSOM (CSS Object Model) の構築**: ブラウザがCSSを解析し、CSSOMツリーを作成する。
3.  **Render Tree の構築**: DOMツリーとCSSOMツリーを組み合わせて、描画に必要な情報だけを持つRender Treeを作成する。
4.  **Layout（または Reflow）**: Render Tree内の各ノードの画面上での正確な位置とサイズを計算する。
5.  **Paint（または Repaint）**: Layoutステップで計算された情報をもとに、各ノードを画面上の実際のピクセルに描画する。
6.  **Composite**: 必要に応じて、複数のレイヤーを正しい順序で画面に合成する。

![クリティカルレンダリングパスの図解](https://raw.githubusercontent.com/coachtech-material/pro-contents/main/laravel%E3%82%A8%E3%83%B3%E3%82%B8%E3%83%8B%E3%82%A2%E3%81%AE%E3%81%9F%E3%82%81%E3%81%AE%E3%83%95%E3%83%AD%E3%83%B3%E3%83%88%E3%82%A8%E3%83%B3%E3%83%89%E5%AD%A6%E7%BF%92%E3%83%AD%E3%83%BC%E3%83%89%E3%83%9E%E3%83%83%E3%83%97/images/column/crp.png)

> DOM ツリーと CSSOM ツリーは、レンダリング ツリーに結合されます。レンダリング ツリーでは、表示される各要素のレイアウトが計算され、ペイント処理で画面にピクセルがレンダリングされます。これらのステップをすべて最適化することが、最適なレンダリング パフォーマンスを実現するために重要です。
> --- Google Developers, "Critical Rendering Path" [1]

### 1. DOMの構築

ブラウザはサーバーから受け取ったHTMLを上から下に1行ずつ解析（Parse）し、タグを「ノード」として認識し、それらの親子関係を元に木構造のデータモデルである**DOMツリー**を構築します。このプロセスは、HTMLのバイトデータを文字に変換し、トークンを生成し、ノードに変換し、最終的にツリーを構築するという流れで行われます。[2]

### 2. CSSOMの構築

HTMLの解析中に`<link rel="stylesheet">`タグや`<style>`タグが見つかると、ブラウザはCSSの解析を開始します。HTMLと同様に、CSSのルールを解析し、**CSSOMツリー**を構築します。CSSOMは、どの要素にどのスタイルが適用されるかの情報を持っています。CSSは子要素が親要素のスタイルを継承する（cascading）性質があるため、CSSOMの構築はDOMよりも複雑で、ツリーの末端から再帰的に計算される必要があります。

### 3. Render Treeの構築

DOMツリーとCSSOMツリーが完成すると、ブラウザはこれら2つを組み合わせて**Render Tree**を構築します。Render Treeは、**実際に画面に表示されるノードだけ**で構成されます。例えば、`display: none;`が適用されたノードや、`<head>`タグのような非表示要素はRender Treeに含まれません。

### 4. Layout

Render Treeが構築されると、次に行われるのが**Layout**（レイアウト）ステップです。このステップでは、ビューポート（ブラウザの表示領域）のサイズを基準として、Render Treeの各ノードが画面上のどこに、どのくらいの大きさで配置されるかを計算します。`width: 50%`のような相対的な単位は、この段階で具体的なピクセル値に変換されます。

### 5. Paint

Layoutステップで各ノードの幾何学的な情報（位置、サイズ）が確定すると、**Paint**（ペイント）ステップに移ります。ここでは、計算された情報をもとに、各ノードの見た目（色、境界線、影など）を画面上のピクセルに実際に描画していきます。このプロセスは、複数のレイヤーに分けて行われることがあります。

## なぜCRPの最適化が重要なのか？

CRPの各ステップは、完了するまでに時間がかかります。特に、CSSやJavaScriptのファイルがレンダリングを「ブロック」することが、パフォーマンスの低下に繋がる大きな原因です。

-   **CSSはレンダリングをブロックする**: ブラウザは、CSSOMツリーが完成するまでRender Treeを構築できず、したがってページの描画を開始できません。そのため、CSSファイルの読み込みや解析が遅れると、ユーザーは白い画面を長く見ることになります。
-   **JavaScriptはDOMの構築をブロックする**: HTMLの解析中に`<script>`タグが見つかると、ブラウザはDOMの構築を一時停止し、JavaScriptの実行を優先します。もしそのJavaScriptがDOMを操作する（例: `document.write`）可能性がある場合、ブラウザは安全のために解析を待機せざるを得ません。これにより、DOMの完成が遅れ、結果的に最初の描画も遅れます。

これらのブロッキングを最小限に抑え、CRPをできるだけ速く完了させることが、Webパフォーマンス最適化の鍵となります。

## ✨ まとめ

-   クリティカルレンダリングパス（CRP）は、ブラウザがコードを画面のピクセルに変換するまでの一連の処理のこと。
-   CRPは、DOM構築 → CSSOM構築 → Render Tree構築 → Layout → Paintという主要なステップで構成される。
-   CSSはCSSOMの構築を、JavaScriptはDOMの構築をブロックする可能性があり、これらがパフォーマンスのボトルネックになりやすい。
-   CRPを最適化することは、ページの表示速度を改善し、ユーザー体験を向上させるために不可欠である。

次のセクションでは、CRPの最初のステップであるDOMとCSSOMの構築について、さらに詳しく見ていきます。

---

## 参考文献

[1] Google Developers. (n.d.). *Critical Rendering Path*. Retrieved from https://developers.google.com/web/fundamentals/performance/critical-rendering-path/render-tree-construction

[2] Google Developers. (n.d.). *Constructing the Object Model*. Retrieved from https://developers.google.com/web/fundamentals/performance/critical-rendering-path/constructing-the-object-model
