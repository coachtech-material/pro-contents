# Tutorial 3: Tailwind CSS 徹底習得

## Chapter 2: レスポンシブデザイン

### Chapter 2 ハンズオン: レスポンシブなカードレイアウトを作成する

🎯 **このハンズオンで達成すること**

-   モバイルファーストのアプローチに基づき、レスポンシブなカードコンポーネントを構築できるようになる。
-   Flexboxとブレークポイントを組み合わせ、画面サイズに応じてカード内のレイアウトを変更できるようになる。
-   `grid`とブレークポイントを組み合わせ、カードを並べるグリッドレイアウトをレスポンシブにできるようになる。

--- 

🖼️ **完成イメージ**

このハンズオンでは、以下のようなレスポンシブなカードレイアウトを作成します。

-   **スマートフォン（モバイル）表示:** カードの画像が上、テキストが下に配置された1列のレイアウト。
-   **タブレット（`md`）以上での表示:** 画面左に画像、右にテキストが配置された2カラムのレイアウト。カード自体は2列のグリッドで表示。
-   **ノートPC（`lg`）以上での表示:** カードは3列のグリッドで表示。

*ここにスクリーンショットを挿入: (1) スマホ画面で、画像とテキストが縦に並んだカードが1列で表示されている様子。 (2) タブレット画面で、画像とテキストが横に並んだカードが2列で表示されている様子。 (3) PC画面で、同じく横並びのカードが3列で表示されている様子。*

--- 

### 🧠 先輩エンジニアの思考プロセス

「レスポンシブなカード一覧を作ってください」と頼まれたとき、頭の中では以下のように「モバイルから」考え始めます。

| 手順 | 思考プロセス |
|:---|:---|
| **1. モバイルのカード構造 (HTML)** | まずはスマホでの見た目を考える。画像が上で、その下にタイトルと説明文が来るのが自然だな。HTMLの骨格を作ろう。 |
| **2. モバイルのカードスタイリング** | カード全体に背景色、角丸、影を付けてカードらしくしよう。画像とテキストの間の余白も調整する。 |
| **3. モバイルのグリッドレイアウト** | スマホではカードは1列で縦に並べよう。`grid`と`grid-cols-1`を使う。 |
| **4. タブレットでのカードレイアウト** | 次に`md`サイズ。画面が広くなったから、カードの中は画像とテキストを横並びにしよう。`md:flex`が使えそうだ。 |
| **5. タブレットでのグリッドレイアウト** | カード自体も横に並べられるな。`md:grid-cols-2`で2列にしよう。 |
| **6. PCでのグリッドレイアウト** | さらに広い`lg`サイズなら、`lg:grid-cols-3`で3列にすればもっと見やすいな。 |

💡 **ポイント:** **「コンポーネント単体（カードの中身）」と「コンポーネントの集合（カードの並び）」**のレスポンシブ対応を、それぞれモバイルから順番に考えていくのがコツです。

--- 

### 🏃 実践: Step by Stepでカードレイアウトを作成しよう

`tailwind-handson`プロジェクトの`src/index.html`を編集していきます。

#### Step 1: HTMLの基本構造（モバイルファースト）

まず、`<body>`タグの中身をすべて削除し、カード1つ分のHTML構造を記述します。この時点ではまだレスポンシブ対応は考えず、モバイルでの表示だけを意識します。

```html
<!-- src/index.html -->

<body class="bg-gray-100 p-4 sm:p-6">

  <!-- カードコンテナ -->
  <div class="max-w-sm mx-auto bg-white rounded-lg shadow-md overflow-hidden">
    <!-- カード画像 -->
    <div>
      <img class="w-full h-48 object-cover" src="https://via.placeholder.com/400x250" alt="Card Image">
    </div>
    <!-- カード本文 -->
    <div class="p-6">
      <h2 class="text-xl font-bold text-gray-800 mb-2">カードのタイトル</h2>
      <p class="text-gray-600 text-base">
        ここにカードの詳細な説明文が入ります。モバイルではこのように画像の下にテキストが表示されます。
      </p>
    </div>
  </div>

</body>
```

-   **コードリーディング**
    -   `max-w-sm mx-auto`: カードの最大幅を`sm`（Tailwindのサイズ単位）に制限し、中央に配置します。
    -   `overflow-hidden`: カードの角丸に合わせて、中身（特に画像）がはみ出ないようにします。
    -   `w-full h-48 object-cover`: 画像が親要素の幅いっぱいに広がり、高さは`h-48`に固定されます。`object-cover`は、アスペクト比を保ったまま要素を埋め尽くすように画像をリサイズしてくれます。

この時点でブラウザを見ると、モバイル表示を想定した縦積みのカードが1つ表示されます。

#### Step 2: カードレイアウトのレスポンシブ対応

次に、`md`ブレークポイント以上で、カード内のレイアウトが「画像が左、テキストが右」になるように変更します。

```html
<!-- 変更前 -->
<div class="max-w-sm mx-auto bg-white rounded-lg shadow-md overflow-hidden">

<!-- 変更後 -->
<div class="max-w-sm md:max-w-2xl mx-auto bg-white rounded-lg shadow-md overflow-hidden md:flex">
```

カードの親コンテナに`md:flex`を追加し、最大幅も`md:max-w-2xl`に広げます。さらに、画像と本文のコンテナの幅を調整します。

```html
<!-- src/index.html -->

<body class="bg-gray-100 p-4 sm:p-6">

  <!-- カードコンテナ -->
  <div class="max-w-sm md:max-w-2xl mx-auto bg-white rounded-lg shadow-md overflow-hidden md:flex">
    <!-- カード画像 -->
    <div class="md:w-1/3">
      <img class="w-full h-full object-cover" src="https://via.placeholder.com/400x250" alt="Card Image">
    </div>
    <!-- カード本文 -->
    <div class="p-6 md:w-2/3">
      <h2 class="text-xl font-bold text-gray-800 mb-2">カードのタイトル</h2>
      <p class="text-gray-600 text-base">
        ここにカードの詳細な説明文が入ります。モバイルではこのように画像の下にテキストが表示されます。
      </p>
    </div>
  </div>

</body>
```

-   **コードリーディング**
    -   `md:flex`: `md`以上でカードコンテナをFlexboxにします。
    -   `md:w-1/3`: `md`以上で画像コンテナの幅を1/3にします。
    -   `md:w-2/3`: `md`以上で本文コンテナの幅を2/3にします。
    -   画像の`h-48`を`h-full`に変更し、Flexアイテムとして高さいっぱいに広がるようにします。

ブラウザのウィンドウ幅を広げたり狭めたりして、768pxを境にカードのレイアウトが変わることを確認してください。

#### Step 3: グリッドレイアウトの作成とレスポンシブ対応

最後に、このカードを複数並べ、グリッドレイアウトをレスポンシブにします。

まず、`<body>`タグの直下にグリッドコンテナを配置し、先ほど作ったカードのHTMLをその中にコピー＆ペーストして3つに増やします。

```html
<!-- src/index.html -->

<body class="bg-gray-100 p-4 sm:p-6">

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">

    <!-- カード1 -->
    <div class="max-w-sm md:max-w-none mx-auto bg-white rounded-lg shadow-md overflow-hidden md:flex md:flex-col">
      <!-- カード画像 -->
      <div class="md:h-48">
        <img class="w-full h-full object-cover" src="https://via.placeholder.com/400x250" alt="Card Image">
      </div>
      <!-- カード本文 -->
      <div class="p-6 flex-1">
        <h2 class="text-xl font-bold text-gray-800 mb-2">カードのタイトル 1</h2>
        <p class="text-gray-600 text-base">
          ここにカードの詳細な説明文が入ります。
        </p>
      </div>
    </div>

    <!-- カード2 (カード1と同じ内容をコピー) -->
    <!-- ... -->

    <!-- カード3 (カード1と同じ内容をコピー) -->
    <!-- ... -->

  </div>

</body>
```

おや？少しレイアウトが崩れてしまいました。グリッドの子要素になったことで、カードのレイアウトを少し調整する必要があります。カードコンテナのクラスを以下のように修正します。

-   `max-w-sm md:max-w-2xl` → `w-full` (グリッドセルいっぱいに広がるように)
-   `md:flex` → `md:block` (カードの中は常に縦積みでOK)

最終的なコードは以下のようになります。

```html
<!-- src/index.html -->
<body class="bg-gray-100 p-4 sm:p-6">
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <!-- カード1 -->
    <div class="w-full bg-white rounded-lg shadow-md overflow-hidden">
      <img class="w-full h-48 object-cover" src="https://via.placeholder.com/400x250/8b5cf6/ffffff" alt="Card 1">
      <div class="p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-2">カードタイトル 1</h2>
        <p class="text-gray-600 text-base">モバイルでは1列、タブレットでは2列、PCでは3列で表示されます。</p>
      </div>
    </div>
    <!-- カード2 -->
    <div class="w-full bg-white rounded-lg shadow-md overflow-hidden">
      <img class="w-full h-48 object-cover" src="https://via.placeholder.com/400x250/ec4899/ffffff" alt="Card 2">
      <div class="p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-2">カードタイトル 2</h2>
        <p class="text-gray-600 text-base">ウィンドウ幅を変えて、レイアウトの変化を確認してください。</p>
      </div>
    </div>
    <!-- カード3 -->
    <div class="w-full bg-white rounded-lg shadow-md overflow-hidden">
      <img class="w-full h-48 object-cover" src="https://via.placeholder.com/400x250/10b981/ffffff" alt="Card 3">
      <div class="p-6">
        <h2 class="text-xl font-bold text-gray-800 mb-2">カードタイトル 3</h2>
        <p class="text-gray-600 text-base">モバイルファーストでスタイルを組み立てるのがコツです。</p>
      </div>
    </div>
  </div>
</body>
```

-   **コードリーディング**
    -   `grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6`: グリッドコンテナ。画面幅に応じてカラム数を変更し、アイテム間の隙間を`gap-6`に設定します。
    -   カード自体のクラスはシンプルになりました。`w-full`でグリッドセルいっぱいに広がり、`md:flex`などのレスポンシブクラスは不要です。なぜなら、カードの中身は常に「画像が上、テキストが下」のままで、カード自体の並び方だけがレスポンシブに変化するからです。

ブラウザで確認し、ウィンドウ幅を変えながら、カードの列数が`1 -> 2 -> 3`と変化することを確認してください。

--- 

✨ **まとめ**

-   モバイルファーストで、まず最小画面でのコンポーネントの見た目とレイアウトを完成させることが重要である。
-   ブレークポイントプレフィックスを使い、画面が大きくなるにつれてスタイルを「追加」または「上書き」していく。
-   「コンポーネント単体」のレスポンシブと、「コンポーネントの集合（グリッドなど）」のレスポンシブを分けて考えると、複雑なレイアウトも整理しやすい。

📝 **学習のポイント**

-   [ ] なぜ最初のステップで`md:flex`を使ったカードレイアウトが、グリッドの子要素になったときにうまく機能しなかったのでしょうか？（ヒント: グリッドとFlexboxの特性の違い）
-   [ ] このハンズオンで作成したカードの画像とテキストの比率を、`md`サイズで「画像が1/4、テキストが3/4」に変更するには、どのクラスを修正すればよいですか？
-   [ ] もし4列目のブレークポイント`xl:grid-cols-4`を追加した場合、どのような画面サイズでレイアウトが変化しますか？
