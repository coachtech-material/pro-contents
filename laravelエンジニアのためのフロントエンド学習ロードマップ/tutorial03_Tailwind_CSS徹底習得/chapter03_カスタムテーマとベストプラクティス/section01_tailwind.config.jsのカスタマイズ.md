# 3-3-1: tailwind.config.jsのカスタマイズ

## Chapter 3: カスタムテーマとベストプラクティス

### Section 1: tailwind.config.jsのカスタマイズ

🎯 **このセクションで学ぶこと**

-   `tailwind.config.js`の`theme`オブジェクトの役割を理解する。
-   デフォルトのカラーパレットやフォント、スペーシングを拡張（extend）または上書き（override）できるようになる。
-   独自のユーティリティクラスを追加できるようになる。

--- 

### イントロダクション：Tailwindを「自分色」に染める

Tailwind CSSには、非常に優れたデフォルトのデザインシステム（カラースキーム、スペーシング、フォントサイズなど）が用意されています。しかし、実際のプロジェクトでは、ブランドカラーを使ったり、特定のフォントサイズや余白のルールを追加したりと、デザインシステム自体をカスタマイズしたい場面が必ず出てきます。

`tailwind.config.js`ファイルは、そのための「カスタマイズ拠点」です。このファイルを編集することで、Tailwindのデフォルト設定を拡張したり、完全に置き換えたりして、プロジェクト独自の設計思想をTailwindに組み込むことができます。

--- 

### 🔑 `theme`オブジェクトの構造

カスタマイズの中心となるのが、`tailwind.config.js`内の`theme`オブジェクトです。このオブジェクトの中に、色（`colors`）、余白（`spacing`）、フォントサイズ（`fontSize`）など、Tailwindのすべてのデザイン定義が含まれています。

```javascript
// tailwind.config.js
module.exports = {
  content: [/* ... */],
  theme: {
    // ここにデフォルトテーマの上書き設定を記述
    screens: {
      'sm': '640px',
      'md': '768px',
    },
    colors: {
      'blue': '#1fb6ff',
      'pink': '#ff49db',
    },
    // ...
    extend: {
      // ここにデフォルトテーマの拡張設定を記述
      colors: {
        'brand-blue': '#1DA1F2',
      },
      spacing: {
        '128': '32rem',
      }
    }
  },
  plugins: [],
}
```

### ⚙️ `extend` vs 上書き（Override）

カスタマイズには2つの方法があります。`theme`直下に設定を書く**「上書き」**と、`theme.extend`の中に書く**「拡張」**です。この違いを理解することが非常に重要です。

-   **上書き (Override)**
    -   **場所:** `theme`オブジェクトの直下
    -   **動作:** デフォルトのテーマ設定を**完全に置き換え**ます。
    -   **例:** `theme: { colors: { 'red': '#ff0000' } }`と書くと、Tailwindのデフォルトカラーパレット（`blue-500`や`green-300`など）は**すべてなくなり**、`bg-red`や`text-red`しか使えなくなります。
    -   **用途:** プロジェクト独自の厳格なデザインシステムをゼロから構築する場合。

-   **拡張 (Extend)**
    -   **場所:** `theme.extend`オブジェクトの中
    -   **動作:** デフォルトのテーマ設定を**維持したまま、新しい値を追加**します。
    -   **例:** `theme: { extend: { colors: { 'brand-primary': '#007bff' } } }`と書くと、既存の`bg-blue-500`などに加えて、`bg-brand-primary`という新しいクラスが使えるようになります。
    -   **用途:** ほとんどのケースでこちらを使います。デフォルトの便利な設定を活かしつつ、プロジェクト固有の値を追加する場合。

**結論：特別な理由がない限り、常に`theme.extend`を使ってカスタマイズするのが安全で推奨される方法です。**

--- 

### 🏃 実践: Step by Stepでテーマをカスタマイズしよう

#### 1. ブランドカラーの追加

プロジェクトのブランドカラーを追加してみましょう。`tailwind.config.js`を以下のように編集します。

```javascript
// tailwind.config.js
module.exports = {
  // ...
  theme: {
    extend: {
      colors: {
        'laravel-red': '#F05340',
        'vue-green': '#42b883',
      },
    },
  },
  // ...
}
```

これで、`bg-laravel-red`や`text-vue-green`といったクラスが使えるようになります。

#### 2. フォントの追加

Google Fontsなどから読み込んだWebフォントを、Tailwindの`fontFamily`に追加してみましょう。

```javascript
// tailwind.config.js
const defaultTheme = require('tailwindcss/defaultTheme')

module.exports = {
  // ...
  theme: {
    extend: {
      fontFamily: {
        sans: ['Noto Sans JP', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  // ...
}
```

-   **コードリーディング**
    -   `const defaultTheme = require('tailwindcss/defaultTheme')`: Tailwindのデフォルトテーマ設定をインポートします。
    -   `sans: ['Noto Sans JP', ...defaultTheme.fontFamily.sans]`: デフォルトのサンセリフフォント（`font-sans`）の配列の**先頭に**`'Noto Sans JP'`を追加しています。これにより、`Noto Sans JP`が利用可能であればそれが使われ、利用できなければデフォルトのフォントが順番に適用される（フォールバック）ようになります。

#### 3. 独自のユーティリティクラスの追加（上級）

`plugins`機能を使うと、より複雑な独自のユーティリティクラスを追加できます。例えば、テキストを縦書きにする`writing-vertical-rl`というクラスを追加したい場合、以下のように記述します。

```javascript
// tailwind.config.js
const plugin = require('tailwindcss/plugin')

module.exports = {
  // ...
  plugins: [
    plugin(function({ addUtilities }) {
      addUtilities({
        '.writing-vertical-rl': {
          'writing-mode': 'vertical-rl',
        },
      })
    })
  ],
}
```

これで、HTML内で`class="writing-vertical-rl"`と書くだけで、テキストが縦書きになります。

--- 

✨ **まとめ**

-   Tailwind CSSのカスタマイズは`tailwind.config.js`の`theme`オブジェクトで行う。
-   デフォルト設定を活かしつつ値を追加する「拡張（`extend`）」と、完全に置き換える「上書き」がある。
-   特別な理由がない限り、常に`theme.extend`を使用することが推奨される。
-   `colors`, `fontFamily`, `spacing`などを拡張することで、プロジェクト独自のデザインシステムを構築できる。
-   `plugins`機能を使えば、JavaScriptでより動的かつ複雑なカスタムユーティリティを定義できる。

📝 **学習のポイント**

-   [ ] `theme.extend.colors`と`theme.colors`の違いを説明できますか？
-   [ ] あなたの会社のブランドカラーを`brand-main`という名前でTailwindに追加するには、`tailwind.config.js`をどのように編集しますか？
-   [ ] デフォルトの`spacing`（余白）に、`13`というキーで`3.25rem`の値を追加するにはどうすればよいですか？
