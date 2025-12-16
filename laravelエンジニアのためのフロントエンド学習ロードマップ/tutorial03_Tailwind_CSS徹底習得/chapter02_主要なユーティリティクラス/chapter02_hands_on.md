# Tutorial 3: Tailwind CSS徹底習得

## Chapter 2: 主要なユーティリティクラス

### Chapter 2 ハンズオン: 主要ユーティリティクラスでコンポーネントを組み立てる

🖼️ **完成形のイメージ**

このハンズオンでは、Chapter 2で学んだ主要なユーティリティクラス（レイアウト、ボックスモデル、タイポグラフィ、背景、状態、レスポンシブ）を総動員して、いくつかの実践的なUIコンポーネントをゼロから組み立てます。具体的には、「レスポンシブ対応のナビゲーションバー」と「ホバーエフェクト付きの製品カード」を作成します。

*ここに完成したコンポーネントのスクリーンショットを挿入: (1)PC表示では横並びのメニュー、スマホ表示ではハンバーガーメニューになるナビゲーションバー (2)マウスを乗せると画像が少し拡大し、影が濃くなる製品カード*

--- 

🎯 **このセクションで学ぶこと**

このハンズオンを終えると、あなたは以下のことができるようになります。

-   ユーティリティクラスをLEGOブロックのように組み合わせて、実践的なUIコンポーネントを構築できるようになる。
-   モバイルファーストのアプローチで、レスポンシブデザインを実装する具体的な手順を理解する。
-   `hover:`や`md:`などのバリアントを組み合わせて、インタラクティブで適応性のあるUIを作成できるようになる。

--- 

### 🏃 実践: 一緒に作ってみましょう！

このハンズオンでは、Chapter 1でセットアップしたTailwindプロジェクトを引き続き使用します。`index.html`の中身を一度空にして、新しいコンポーネントを一つずつ追加していきましょう。

#### 💭 実装の思考プロセス

**このハンズオンのゴール:**

1.  **ナビゲーションバーの構築:**
    -   モバイル画面では「ロゴ」と「ハンバーガーアイコン」のみ表示。
    -   `md`スクリーン以上では、メニュー項目が横に並んで表示される。
    -   Flexboxユーティリティ (`flex`, `justify-between`, `items-center`) を駆使して要素を配置する。
2.  **製品カードの構築:**
    -   画像、製品名、価格、説明文を含むカードを作成する。
    -   `hover:`バリアントを使って、マウスが乗った時に影を濃くし、画像を少しだけ拡大するインタラクションを追加する。
    -   レスポンシブグリッド (`grid`, `grid-cols-*`, `md:grid-cols-*`) を使って、画面サイズに応じてカードの列数を変更する。

💡 **ポイント:** HTMLの構造を考えながら、同時に`class`属性に必要なユーティリティクラスをどんどん追加していく、というTailwindならではの開発フローに慣れていきましょう。完璧を目指さず、まずは形にしてから微調整していくのがコツです。

#### 📝 ステップバイステップで実装

##### Step 1: レスポンシブ対応のナビゲーションバー

まずは、多くのWebサイトで共通して見られるヘッダーのナビゲーションバーを作成します。

1-1. `index.html`の`<body>`内に以下のHTML構造を追加します。

-   **コマンド/コード (index.html):**
    ```html
    <nav class="bg-white shadow-md">
      <div class="max-w-6xl mx-auto px-4">
        <div class="flex justify-between">
          <!-- Logo -->
          <div>
            <a href="#" class="flex items-center py-5 px-2 text-gray-700 hover:text-gray-900">
              <svg class="h-6 w-6 mr-1 text-blue-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" /></svg>
              <span class="font-bold">Pro-Contents</span>
            </a>
          </div>

          <!-- Primary Nav -->
          <div class="hidden md:flex items-center space-x-1">
            <a href="#" class="py-5 px-3 text-gray-700 hover:text-gray-900">Features</a>
            <a href="#" class="py-5 px-3 text-gray-700 hover:text-gray-900">Pricing</a>
            <a href="#" class="py-5 px-3 text-gray-700 hover:text-gray-900">Contact</a>
          </div>

          <!-- Mobile button -->
          <div class="md:hidden flex items-center">
            <button class="mobile-menu-button">
              <svg class="w-6 h-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16m-7 6h7" /></svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Mobile Menu -->
      <div class="hidden mobile-menu">
        <a href="#" class="block py-2 px-4 text-sm hover:bg-gray-200">Features</a>
        <a href="#" class="block py-2 px-4 text-sm hover:bg-gray-200">Pricing</a>
        <a href="#" class="block py-2 px-4 text-sm hover:bg-gray-200">Contact</a>
      </div>
    </nav>
    ```

-   **コードリーディング:**
    -   `hidden md:flex`: この組み合わせがレスポンシブのキモです。通常は`hidden`（非表示）ですが、`md`スクリーン以上になると`flex`（表示）に変わります。これによりPC用のメニューが実現できています。
    -   `md:hidden`: こちらは逆で、通常は表示されていますが、`md`スクリーン以上になると非表示になります。モバイル用のハンバーガーボタンに使われています。
    -   （この時点ではハンバーガーボタンのクリックイベントは実装しません。スタイリングに集中します。）

##### Step 2: ホバーエフェクト付きの製品カード

次に、eコマースサイトなどでよく見かける製品カードを、グリッドレイアウトの中に配置します。

2-1. `index.html`の`<nav>`タグの後に、以下のHTML構造を追加します。

-   **コマンド/コード (index.html):**
    ```html
    <div class="py-10">
      <div class="max-w-6xl mx-auto px-4">
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
          
          <!-- Product Card 1 -->
          <div class="bg-white rounded-lg shadow-lg overflow-hidden transform hover:scale-105 transition-transform duration-300">
            <img src="https://via.placeholder.com/400x300" alt="Product Image" class="w-full h-48 object-cover">
            <div class="p-6">
              <h3 class="text-xl font-semibold text-gray-800 mb-2">高品質ガジェット</h3>
              <p class="text-gray-600 mb-4">最新技術を駆使した、あなたの生活を豊かにする逸品です。</p>
              <div class="flex justify-between items-center">
                <span class="text-2xl font-bold text-gray-900">¥19,800</span>
                <button class="bg-blue-500 text-white py-2 px-4 rounded-full hover:bg-blue-600 transition-colors">カートに追加</button>
              </div>
            </div>
          </div>

          <!-- カードをあと2つ、同様にコピー＆ペースト -->

        </div>
      </div>
    </div>
    ```

-   **コードリーディング:**
    -   `grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8`: レスポンシブグリッドの定義です。モバイルでは1列、`sm`以上で2列、`lg`以上で3列になります。`gap-8`でカード間の隙間を確保しています。
    -   `transform hover:scale-105 transition-transform duration-300`: これがホバーエフェクトの核です。`transform`で変形を有効にし、`hover`時に`scale-105`（1.05倍に拡大）を適用します。`transition-transform`と`duration-300`で、0.3秒かけて滑らかに変化するように指定しています。
    -   `overflow-hidden`: カードのコンテナにこれを指定しないと、拡大した画像がはみ出してしまうので重要です。

#### ✨ 完成！

お疲れ様でした！ブラウザで`index.html`を開き、ウィンドウサイズを変えたり、カードにマウスを乗せたりしてみてください。ユーティリティクラスを組み合わせるだけで、これだけリッチな表現がCSSを一行も書かずに実現できることを実感できたはずです。これがTailwind CSSのパワーです。
