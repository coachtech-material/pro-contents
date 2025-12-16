# 2-4-3: 実務でよく使うGridパターン

## 🎯 このセクションで学ぶこと

- `grid-template-areas` を使った直感的なレイアウトができるようになる
- `fr` 単位を使った柔軟なカラム幅の指定ができるようになる
- `repeat()` 関数を使った効率的なグリッド定義ができるようになる

## 🖼️ 完成イメージ

このセクションでは、Webサイトでよく使われる聖杯レイアウト（Holy Grail Layout）をGridを使って作成します。

## 導入

Grid Layoutは非常に高機能ですが、実務でよく使われるパターンは限られています。このセクションでは、特に頻出する3つのパターンを学び、Gridをより実践的に使いこなせるようになりましょう。

## 詳細解説

### 1. 聖杯レイアウト（Holy Grail Layout）

ヘッダー、フッター、メインコンテンツ、左右のサイドバーで構成されるレイアウトです。`grid-template-areas` を使うと、アスキーアートのように直感的にレイアウトを定義できます。

```css
.container {
  display: grid;
  grid-template-areas:
    "header header header"
    "nav    main   aside"
    "footer footer footer";
  grid-template-columns: 1fr 3fr 1fr;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
}

.header { grid-area: header; }
.nav    { grid-area: nav; }
.main   { grid-area: main; }
.aside  { grid-area: aside; }
.footer { grid-area: footer; }
```

### 2. `fr` 単位と `repeat()` 関数

- **`fr` 単位**: 利用可能なスペースを分割してカラムに割り当てます。レスポンシブデザインに非常に便利です。
- **`repeat()` 関数**: 同じ定義を繰り返す場合にコードを簡潔にできます。

```css
.grid-container {
  display: grid;
  /* 12カラムのグリッドシステム */
  grid-template-columns: repeat(12, 1fr);
  gap: 20px;
}

.item-4-cols {
  /* 4カラム分の幅を占める */
  grid-column: span 4;
}
```

### 3. `minmax()` 関数

カラムや行の最小値と最大値を指定できます。レスポンシブなカードレイアウトなどで威力を発揮します。

```css
.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 1rem;
}
```

`auto-fit` と `minmax()` を組み合わせることで、コンテナの幅に応じてカードの列数が自動的に調整されます。

## 💡 TIP

- GridとFlexboxは競合するものではなく、併用することでより複雑なレイアウトも実現できます。一般的に、ページ全体の大きなレイアウトはGrid、コンポーネント内の細かいレイアウトはFlexboxが向いています。

## 🏃 実践

前のセクションで作成したギャラリーレイアウトを、`minmax()` を使ってレスポンシブにしてみましょう。

## ✨ まとめ

- `grid-template-areas` で直感的なレイアウト定義が可能
- `fr` 単位と `repeat()` 関数で効率的なグリッド作成
- `minmax()` と `auto-fit` でレスポンシブなレイアウトを実現
