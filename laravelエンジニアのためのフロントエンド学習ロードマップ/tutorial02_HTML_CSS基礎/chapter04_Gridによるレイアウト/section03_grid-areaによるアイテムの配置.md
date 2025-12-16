# Tutorial 2: HTML/CSS基礎

## Chapter 4: Gridによるレイアウト

### Section 3: grid-areaによるアイテムの配置

🖼️ **完成形のイメージ**

このセクションでは、Gridレイアウトのもう一つの強力な機能である`grid-area`を学びます。`grid-template-areas`でコンテナに「名前付きエリア」を定義し、`grid-area`で各アイテムをその名の付いたエリアに配置することで、まるでパズルのように直感的なレイアウトを実現します。

*ここにスクリーンショットを挿入: ヘッダー、サイドバー、メインコンテンツ、フッターが、コードに書かれたASCIIアートの通りに配置されている様子*

--- 

🎯 **このセクションで学ぶこと**

このセクションでは、Gridのエリアベースの配置方法をマスターします。このセクションを終えると、あなたは以下のことができるようになります。

- `grid-template-areas`を使って、グリッドコンテナにASCIIアートのような形でレイアウトエリアを定義できるようになる。
- `grid-area`を使って、特定のGridアイテムを、名前が付けられたエリアに割り当てることができるようになる。
- 行番号や列番号を使わずに、より宣言的で視覚的に分かりやすい方法でページ全体のレイアウトを構築できるようになる。

--- 

### 導入

前のセクションでは、列と行のサイズを定義して格子を作りました。アイテムはその格子に従って自動的に配置されましたが、特定のアイテムを「2列目から3列目にまたがって配置したい」といった、より複雑な配置も可能です。その方法の一つが、グリッドのライン番号を指定する方法ですが、より直感的で管理しやすいのが、これから学ぶ`grid-area`を使ったエリアベースの配置です。これは、レイアウト構造をCSSで視覚的に表現できるため、特にページ全体の骨格を作る際に絶大な威力を発揮します。

### 概念の説明

`grid-area`を使ったレイアウトは、2つのプロパティの連携によって成り立ちます。

1.  **`grid-template-areas` (親要素に指定):**
    -   Gridコンテナに、どのような名前のエリアが、どのように配置されるかの「地図」を定義します。
    -   文字列をクォーテーションで囲み、スペース区切りでエリア名を並べることで、行と列のレイアウトをASCIIアートのように記述します。
    -   同じ名前を隣接させると、そのエリアが結合（スパン）されます。
    -   エリアを配置しない場所は、ピリオド (`.`) で表現します。

2.  **`grid-area` (子要素に指定):**
    -   Gridアイテムに、`grid-template-areas`で定義されたどの「エリア名」に対応するかを教えます。

**図解：エリアベースの配置**

```css
/* 親要素 (Gridコンテナ) のCSS */
.container {
  display: grid;
  grid-template-columns: 1fr 3fr; /* 2列 */
  grid-template-rows: auto 1fr auto; /* 3行 */
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
}

/* 子要素 (Gridアイテム) のCSS */
.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.footer { grid-area: footer; }
```

このCSSは、以下のようなレイアウトを視覚的に表現しています。

-   全体は2列3行のグリッドである。
-   1行目はすべて`header`エリアが占める。
-   2行目は、1列目が`sidebar`エリア、2列目が`main`エリアになる。
-   3行目はすべて`footer`エリアが占める。

そして、HTML側で`.header`クラスを持つ要素が`header`エリアに、`.sidebar`クラスを持つ要素が`sidebar`エリアに…というように、自動的に配置されていきます。

### 詳細解説

実際に聖杯レイアウト（Holy Grail Layout）と呼ばれる典型的なWebページレイアウトを`grid-area`で作ってみましょう。

- **HTML:**
  ```html
  <div class="holy-grail-container">
    <header>ヘッダー</header>
    <nav>ナビゲーション</nav>
    <main>メインコンテンツ</main>
    <aside>サイドバー</aside>
    <footer>フッター</footer>
  </div>
  ```

- **CSS:**
  ```css
  .holy-grail-container {
    display: grid;
    height: 100vh; /* 画面の高さいっぱいに広げる */
    grid-template-columns: 150px 1fr 150px; /* 3列 */
    grid-template-rows: auto 1fr auto; /* 3行 */
    grid-template-areas:
      "header header header"
      "nav    main   sidebar"
      "footer footer footer";
  }

  /* 各アイテムを対応するエリアに割り当て */
  header { grid-area: header; }
  nav { grid-area: nav; }
  main { grid-area: main; }
  aside { grid-area: sidebar; }
  footer { grid-area: footer; }

  /* 以下、見た目のための装飾 */
  .holy-grail-container > * {
    border: 1px solid #333;
    padding: 10px;
  }
  ```
- **コードリーディング:**
    - `grid-template-areas`のASCIIアートのような記述が、そのままレイアウトに反映されているのが分かります。
    - `header`と`footer`は3つのセルを結合して1行全体を占めています。
    - 2行目は`nav`, `main`, `sidebar`がそれぞれ1セルずつを占めています。
    - HTMLの要素の順番に関係なく、CSSで指定したエリアに配置されるのが大きな特徴です。（例えば、HTMLで`<footer>`を一番上に書いても、表示は一番下にきます）

### 💡 TIP

- **レスポンシブデザインとの相性:** `grid-template-areas`は、メディアクエリと組み合わせることで真価を発揮します。例えば、スマートフォンなどの狭い画面では、`grid-template-areas`を書き換えて、サイドバーをメインコンテンツの下に移動させる、といったレイアウトの組み替えが非常に簡単に行えます。
- **命名規則:** エリア名はCSSの識別子として有効なものであれば何でも構いませんが、そのエリアの役割が分かるような直感的な名前（`header`, `main`, `sidebar`など）を付けるのが一般的です。

### ✨ まとめ

- `grid-template-areas`を使うと、Gridコンテナに名前付きのエリアを定義できる。
- `grid-area`を使うと、Gridアイテムをその名前付きエリアに配置できる。
- この2つを組み合わせることで、HTMLの構造に依存しない、視覚的でメンテナンス性の高いレイアウト定義が可能になる。
- 特にページ全体の骨格を作るようなマクロなレイアウトで非常に強力。

### 📝 学習のポイント

- [ ] `grid-template-areas`と`grid-area`は、それぞれ親要素と子要素のどちらに指定するか説明できるか？
- [ ] `grid-template-areas`で、隣接するセルを結合するにはどうすればよいか？
- [ ] 2列2行のグリッドで、1行目をすべてヘッダー、2行目の左側をメイン、右側をサイドバーとするレイアウトを`grid-template-areas`で定義できるか？
