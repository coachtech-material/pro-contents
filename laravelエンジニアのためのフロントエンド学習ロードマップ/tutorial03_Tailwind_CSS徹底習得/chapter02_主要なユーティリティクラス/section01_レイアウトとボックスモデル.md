# Tutorial 3: Tailwind CSS徹底習得

## Chapter 2: 主要なユーティリティクラス

### Section 1: レイアウトとボックスモデル（余白、サイズ、配置）

🖼️ **完成形のイメージ**

このセクションでは、Tailwind CSSの最も基本的かつ頻繁に使われるユーティリティクラス群、特にレイアウトとボックスモデルに関連するものを集中的に学びます。これらのクラスを組み合わせることで、要素のサイズ、余白、配置をHTML上で直感的にコントロールできるようになります。

*ここにスクリーンショットを挿入: padding (`p-`), margin (`m-`), width (`w-`), height (`h-`), そしてFlexbox (`flex`, `justify-center`, `items-center`) などのクラスを使って構築された、整然と配置されたカードコンポーネントの例*

--- 

🎯 **このセクションで学ぶこと**

このセクションでは、Tailwind CSSを使ってレイアウトを構築するための基本的なビルディングブロックを習得します。このセクションを終えると、あなたは以下のことができるようになります。

-   `p-`, `m-` などのクラスを使って、要素の`padding`と`margin`を直感的に指定できるようになる。
-   `w-`, `h-` などのクラスを使って、要素の`width`と`height`を固定値や割合で指定できるようになる。
-   `flex`, `grid` などのクラスを使って、FlexboxやGridレイアウトを簡単に適用できるようになる。
-   `justify-*`, `items-*` などのクラスを使って、Flexbox/Gridアイテムの配置をコントロールできるようになる。

--- 

### 導入

Tailwind CSSの真価は、その膨大かつ体系的なユーティリティクラス群にあります。CSSプロパティを一つ一つ書く代わりに、用意されたクラスをLEGOブロックのように組み立てていくことで、高速にUIを構築できます。このセクションでは、その中でも最も使用頻度の高い、レイアウトとボックスモデルに関連するクラスをマスターします。これらのクラスを覚えれば、基本的なレイアウトで困ることはほとんどなくなるでしょう。

### 詳細解説

#### 1. 余白 (Margin & Padding)

`margin`と`padding`は、`m-`と`p-`というプレフィックスで始まるクラスで制御します。その後に方向とサイズを指定します。

-   **方向の指定:**
    -   `t`: top (上)
    -   `b`: bottom (下)
    -   `l`: left (左)
    -   `r`: right (右)
    -   `x`: x軸 (左右)
    -   `y`: y軸 (上下)
    -   (なし): 全方向

-   **サイズの指定:**
    -   Tailwindは`0`, `1`, `2`, `3`, `4`, ... といった数値でサイズを定義する「スペーススケール」を持っています。デフォルトでは、`1`が`0.25rem` (4px) に相当します。つまり、`p-4`は`padding: 1rem;` (16px) となります。

-   **コード例:**
    ```html
    <!-- 上下に1rem(16px)のmargin、左右に2rem(32px)のpaddingを持つdiv -->
    <div class="my-4 px-8">...</div>

    <!-- 左に0.5rem(8px)のmarginを持つspan -->
    <span class="ml-2">...</span>
    ```

#### 2. サイズ (Width & Height)

`width`と`height`は、`w-`と`h-`で制御します。固定値、割合、特別なキーワードが用意されています。

-   **固定値:** `w-4` (1rem), `w-16` (4rem) のように、スペーススケールに基づいた固定値を指定します。
-   **割合:** `w-1/2` (50%), `w-1/3`, `w-full` (100%) のように、分数や`full`で割合を指定できます。
-   **画面幅:** `w-screen` (画面幅いっぱい), `h-screen` (画面の高さいっぱい) といった便利なクラスもあります。
-   **任意の値:** `w-[500px]` のように、角括弧`[]`を使えば、定義されていない任意の値を直接指定することも可能です（JITモードの機能）。

-   **コード例:**
    ```html
    <!-- 幅50%のコンテナ -->
    <div class="w-1/2">...</div>

    <!-- 親要素いっぱいに広がる入力欄 -->
    <input class="w-full" type="text">

    <!-- 高さが画面いっぱいのセクション -->
    <section class="h-screen">...</section>
    ```

#### 3. Flexbox & Grid

`display`プロパティは、プロパティ名をそのままクラス名として使います。

-   `flex`: `display: flex;`
-   `grid`: `display: grid;`
-   `block`: `display: block;`
-   `inline-block`: `display: inline-block;`
-   `hidden`: `display: none;` (要素を非表示にする)

FlexboxやGridの関連プロパティも、非常に直感的なクラス名で提供されています。

-   **Flexboxの例:**
    -   `flex-row`, `flex-col`: `flex-direction`の指定
    -   `justify-start`, `justify-end`, `justify-center`, `justify-between`: `justify-content`の指定
    -   `items-start`, `items-end`, `items-center`, `items-stretch`: `align-items`の指定
    -   `flex-wrap`: `flex-wrap: wrap;`
    -   `flex-grow`: `flex-grow: 1;`
    -   `gap-4`: `gap: 1rem;`

-   **Gridの例:**
    -   `grid-cols-3`: 3列のグリッドを作成 (`grid-template-columns: repeat(3, minmax(0, 1fr));`)
    -   `grid-rows-2`: 2行のグリッドを作成
    -   `col-span-2`: `grid-column: span 2 / span 2;` (アイテムを2列分結合)
    -   `gap-x-4`, `gap-y-8`: 列と行の隙間を個別に指定

-   **コード例 (Flexboxで中央揃え):**
    ```html
    <!-- アイテムを天地左右中央に配置 -->
    <div class="flex justify-center items-center h-screen">
      <p>Hello World</p>
    </div>
    ```

### 💡 TIP

-   **ドキュメント検索が最強の味方:** Tailwindのクラスは膨大です。すべてを暗記する必要は全くありません。公式ドキュメントの検索機能は非常に優秀で、CSSプロパティ名（例: `border-radius`）で検索すれば、対応するユーティリティクラス（例: `rounded`）がすぐに見つかります。開発中は常にドキュメントを開いておくことを強くお勧めします。
-   **VSCode拡張機能:** VSCodeに「Tailwind CSS IntelliSense」という拡張機能をインストールすると、クラス名の自動補完や、クラスにマウスオーバーすると対応するCSSが表示されるなど、開発体験が劇的に向上します。

### ✨ まとめ

-   余白は `m-{direction}-{size}` と `p-{direction}-{size}` で指定する。
-   サイズは `w-{size}` と `h-{size}` で指定し、固定値、割合、画面サイズなどが使える。
-   `flex` や `grid` クラスでレイアウトモードを有効にし、`justify-*`, `items-*`, `gap-*` などの関連クラスで配置や間隔を調整する。
-   `[]`を使った任意の値の指定や、VSCode拡張機能などを活用すると、さらに開発がスムーズになる。

### 📝 学習のポイント

-   [ ] `mt-8`が適用するCSSプロパティと値は何か？
-   [ ] 親要素の幅の3分の2の幅を持つ`div`を作成するためのクラスは何か？
-   [ ] Flexboxを使って、3つのアイテムを均等な間隔を空けて横に並べるためのクラス群（親要素に指定）は何か？
