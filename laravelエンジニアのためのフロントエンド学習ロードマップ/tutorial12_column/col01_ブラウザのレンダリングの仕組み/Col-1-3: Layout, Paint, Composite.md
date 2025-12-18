# Col-1-3: Layout, Paint, Composite

## 🎯 このセクションで学ぶこと

-   Render Treeが構築された後の、Layout、Paint、Compositeの各ステップの役割を理解する。
-   どのようなCSSプロパティの変更が、どのレンダリングステップを引き起こすかを学ぶ。
-   レンダリングパフォーマンスを最適化するための基本的な考え方（Layout/Reflowの最小化）を理解する。

## 導入

DOMツリーとCSSOMツリーが構築され、それらを元にRender Treeが作成されると、クリティカルレンダリングパス（CRP）は最終段階に入ります。ブラウザは、このRender Treeの情報を使って、実際に画面にピクセルを描画していきます。このプロセスは、主に**Layout**、**Paint**、そして**Composite**という3つのステップに分かれています。[1]

これらのステップを理解することは、スムーズなアニメーションやインタラクションを実現し、パフォーマンスの高いWebサイトを構築するために不可欠です。

## 1. Layout（レイアウト）

**Layout**ステップ（Firefoxでは**Reflow**とも呼ばれます）の役割は、Render Treeの各ノードの**幾何学的な情報**、つまり画面上での正確な位置とサイズを計算することです。

Render Treeは、どのノードが表示されるかと、それらにどんなスタイルが適用されるかという情報しか持っていません。`width: 50%`や`font-size: 2em`といった相対的な値が、このLayoutステップで初めて、ビューポートのサイズや親要素のサイズに基づいて具体的なピクセル値に変換されます。

ブラウザは、Render Treeのルートから始まり、各ノードを順番に処理して、ページ全体のレイアウトを決定します。ある要素の位置やサイズが変わると、その後続の要素の位置も再計算する必要があるかもしれません。例えば、`<body>`の幅が変われば、その中のすべての子孫要素のレイアウトに影響が及びます。このように、Layoutはコストの高い処理になる可能性があります。

### Layoutを引き起こす操作

以下のような操作は、Layout（またはReflow）をトリガーします。

-   DOM要素の追加、削除、または変更
-   `width`, `height`, `margin`, `padding`, `border`, `top`, `left`など、要素のジオメトリ（形状や位置）に影響を与えるCSSプロパティの変更
-   ブラウザウィンドウのリサイズ
-   `offsetHeight`や`scrollTop`のような、要素のレイアウト情報を問い合わせるJavaScriptのプロパティの読み取り（ブラウザは正確な値を返すために、保留中のレイアウト計算を強制的に実行する必要があります）

## 2. Paint（ペイント）

**Paint**ステップ（**Repaint**とも呼ばれます）では、Layoutステップで計算された各ノードのジオメトリ情報をもとに、テキスト、色、画像、境界線、影といった**見た目の部分**をピクセルに変換していきます。

この描画処理は、パフォーマンスを最適化するために、複数の**レイヤー（Layers）**に分けて行われることがあります。例えば、`transform`や`opacity`、`will-change`といった特定のCSSプロパティを持つ要素は、他の要素とは別のレイヤーに描画されることがあります。これにより、その要素が変化しても、他のレイヤーを再描画する必要がなくなります。

### Paintを引き起こす操作

Layoutに影響を与えないが、見た目には影響を与えるCSSプロパティの変更は、Paintのみを引き起こします。

-   `background-color`, `color`, `visibility`, `box-shadow`など。

## 3. Composite（コンポジット）

**Composite**（合成）ステップは、Paintステップで描画された複数のレイヤーを、正しい順序で重ね合わせて、最終的な1枚の画面イメージを生成するプロセスです。

ページがスクロールされたり、特定のレイヤーがアニメーションで動いたりする場合を考えてみましょう。もしページ全体が1枚のレイヤーで描画されていたら、スクロールするたびにページ全体を再Paintする必要があります。しかし、ページが複数のレイヤーに分かれていれば、ブラウザは既存のレイヤーを再利用し、それらを正しい位置に動かして再合成（Re-Composite）するだけで済みます。Paint処理は不要です。

このComposite処理は、CPUではなく**GPU（Graphics Processing Unit）**によって高速に実行されます。そのため、LayoutやPaintをスキップしてCompositeのみをトリガーするような変更は、非常に高速に処理できます。

### Compositeのみを引き起こす操作

LayoutもPaintも引き起こさず、Compositeのみをトリガーするプロパティは、アニメーションのパフォーマンスを最適化する上で最も効率的です。

-   `transform`（`translate`, `scale`, `rotate`など）
-   `opacity`

これらのプロパティを変更しても、要素のレイアウト上の位置や他の要素への影響は変わらないため、ブラウザは再Layoutや再Paintを省略し、GPU上でレイヤーを動かしたり透明度を変えたりするだけで済みます。

## パフォーマンス最適化の観点から

レンダリングのパフォーマンスを最適化するということは、これらのLayout、Paint、Compositeの処理、特にコストの高いLayoutとPaintをできるだけ避けることを意味します。

| 変更するプロパティ | Layout | Paint | Composite |
| :--- | :---: | :---: | :---: |
| `width`, `height`, `top`, `left` | ✅ | ✅ | ✅ |
| `background-color`, `color` | ❌ | ✅ | ✅ |
| `transform`, `opacity` | ❌ | ❌ | ✅ |

アニメーションやインタラクションを実装する際は、`top`や`left`で位置を動かすのではなく、`transform: translate()`を使うように心がけるだけで、パフォーマンスは劇的に向上します。[2]

> アニメーションの場合、`transform` と `opacity` プロパティを変更するのが最適です。どちらのプロパティもブラウザのレンダリング パイプラインの合成ステップで処理されるため、最もコストが低くなります。
> --- Google Developers, "Rendering Performance" [1]

## ✨ まとめ

-   CRPの最終段階は、Layout、Paint、Compositeの3ステップで構成される。
-   **Layout**: 要素のサイズと位置を計算する。コストが高い処理。
-   **Paint**: 要素の見た目をピクセルに描画する。複数のレイヤーに分けて行われることがある。
-   **Composite**: 複数のレイヤーをGPU上で合成し、最終的な画面を生成する。
-   パフォーマンスを最適化するには、LayoutとPaintを避け、Compositeのみをトリガーする`transform`や`opacity`プロパティを積極的に利用することが重要である。

---

## 参考文献

[1] Google Developers. (n.d.). *Rendering Performance*. Retrieved from https://developers.google.com/web/fundamentals/performance/rendering

[2] Paul, Lewis., & Smashing Magazine. (2012, June 6). *Why Moving Elements With Translate() Is Better For Performance Than Pos:abs Top/left*. Retrieved from https://www.paulirish.com/2012/why-moving-elements-with-translate-is-better-for-performance-than-posabs-topleft/
