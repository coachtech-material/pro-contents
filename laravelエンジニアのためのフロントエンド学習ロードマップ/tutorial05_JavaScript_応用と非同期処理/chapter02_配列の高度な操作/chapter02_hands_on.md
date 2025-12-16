# Tutorial 5: JavaScript応用と非同期処理

## Chapter 2: 配列の高度な操作

### Chapter 2 ハンズオン: ECサイトの商品一覧を操作する

🎯 **このハンズオンで達成すること**

-   `map`, `filter`を組み合わせたメソッドチェーンを使い、実践的なデータ操作ができるようになる。
-   `find`を使い、IDを指定して特定のオブジェクトを配列から効率的に見つけ出せるようになる。
-   ECサイトの商品一覧のような、実務で頻繁に遭遇するデータ構造を自在に扱えるようになる。

--- 

🖼️ **完成イメージ**

このハンズオンでは、ECサイトの商品データ（オブジェクトの配列）を想定し、配列の高度なメソッドを駆使して様々な要求に応えていきます。最終的に、コンソールに以下のような情報を出力します。

**最終的なコンソール出力のイメージ:**
```
--- 在庫あり商品のリスト ---
- MacBook Pro (¥250000)
- Stand Monitor (¥80000)

--- 10万円以下の商品名リスト ---
- Stand Monitor
- Keyboard

--- IDが3の商品情報 ---
{ id: 3, name: 'Keyboard', price: 20000, inStock: false }

--- 在庫があり、かつ5万円以上の高額商品リスト ---
- MacBook Pro (¥250000)
- Stand Monitor (¥80000)
```

--- 

### 🧠 先輩エンジニアの思考プロセス

「商品データがあるから、これから色々絞り込んだり加工したりしてリスト作って」と頼まれたとき、頭の中ではまず「どんな操作の組み合わせで実現できるか？」を考えます。

| お題 | 思考プロセス |
|:---|:---|
| **1. 在庫あり商品のリスト** | 「在庫あり」で**絞り込んで** (`filter`)、その結果を「名前と価格の文字列」に**変換** (`map`) すれば良さそうだな。 |
| **2. 10万円以下の商品名** | 「10万円以下」で**絞り込んで** (`filter`)、その結果から「名前」だけを**取り出せば** (`map`) OKだな。 |
| **3. IDが3の商品情報** | これは「IDが3」という条件に合う**最初の1個**を見つければいいだけだから、`find`が最適だ。 |
| **4. 在庫あり & 5万円以上** | これは条件が2つあるな。「在庫あり」で**絞り込んで** (`filter`)、その結果をさらに「5万円以上」で**絞り込めば** (`filter`) いける。最後に名前と価格に**変換** (`map`) しよう。 |

💡 **ポイント:** 複雑な要求も、**「絞り込み (`filter`)」**と**「変換 (`map`)」**という単純な操作の組み合わせに分解して考えるのがコツです。メソッドチェーンは、この思考プロセスをそのままコードに落とし込むことができます。

--- 

### 🏃 実践: Step by Stepで商品データを操作しよう

`index.html`に`<script>`タグを用意し、その中にJavaScriptを記述していきます。

#### Step 1: 商品データの準備

まず、アプリケーションの元となる商品データの配列を定義します。

```javascript
// script.js

const products = [
  { id: 1, name: 'MacBook Pro', price: 250000, inStock: true },
  { id: 2, name: 'Stand Monitor', price: 80000, inStock: true },
  { id: 3, name: 'Keyboard', price: 20000, inStock: false },
  { id: 4, name: 'Mouse', price: 15000, inStock: false },
  { id: 5, name: 'Web Camera', price: 18000, inStock: true },
];
```

#### Step 2: 在庫あり商品のリストを作成する (`filter` → `map`)

`filter`で在庫がある商品（`inStock: true`）を絞り込み、その結果を`map`で`"商品名 (¥価格)"`という形式の文字列に変換します。

```javascript
// script.js (続き)

console.log("--- 在庫あり商品のリスト ---");
const inStockProducts = products
  .filter(product => product.inStock === true)
  .map(product => `- ${product.name} (¥${product.price})`);

inStockProducts.forEach(productInfo => console.log(productInfo));
console.log("\n"); // 見やすくするために改行
```

-   **コードリーディング**
    -   `product.inStock === true` は `product.inStock` と省略できます。
    -   `filter`が返した「在庫あり商品オブジェクトの配列」に対して、`map`が実行されます。
    -   最後に、作成された文字列の配列を`forEach`で1行ずつ表示しています。

#### Step 3: 10万円以下の商品名リストを作成する (`filter` → `map`)

今度は価格で`filter`し、商品名だけを`map`で取り出します。

```javascript
// script.js (続き)

console.log("--- 10万円以下の商品名リスト ---");
const cheapProductNames = products
  .filter(product => product.price <= 100000)
  .map(product => product.name);

cheapProductNames.forEach(name => console.log(`- ${name}`));
console.log("\n");
```

#### Step 4: IDで特定の商品を検索する (`find`)

IDが3の商品オブジェクトを`find`メソッドで効率的に見つけます。

```javascript
// script.js (続き)

console.log("--- IDが3の商品情報 ---");
const productWithId3 = products.find(product => product.id === 3);

if (productWithId3) {
  console.log(productWithId3);
} else {
  console.log("該当する商品が見つかりませんでした。");
}
console.log("\n");
```

-   **コードリーディング**
    -   `find`は見つからない場合に`undefined`を返すため、`if`文で存在チェックをしてから表示するのが安全です。

#### Step 5: 複数の条件で絞り込む（応用）

「在庫があり」かつ「価格が5万円以上」という複数の条件で絞り込みます。`filter`を2回繋げても良いですし、1回の`filter`のコールバック関数内で`&&`（AND）を使っても実現できます。

```javascript
// script.js (続き)

console.log("--- 在庫があり、かつ5万円以上の高額商品リスト ---");

// 方法1: filterを2回使う
const expensiveInStockProducts1 = products
  .filter(p => p.inStock)
  .filter(p => p.price >= 50000)
  .map(p => `- ${p.name} (¥${p.price})`);

// 方法2: 1回のfilterで&&を使う（こちらの方が効率的）
const expensiveInStockProducts2 = products
  .filter(p => p.inStock && p.price >= 50000)
  .map(p => `- ${p.name} (¥${p.price})`);

expensiveInStockProducts2.forEach(info => console.log(info));
```

-   **思考のヒント:** 一般的に、ループの回数は少ない方がパフォーマンスが良いため、方法2のように1回の`filter`で済ませられる場合はそちらの方が効率的です。

--- 

✨ **まとめ**

-   `filter`と`map`をメソッドチェーンで繋ぐことで、**「絞り込んで、変換する」**という一連の操作を流れるように記述できる。
-   IDなどユニークな値で特定の1件を探す場合は、`find`が最もシンプルで効率的である。
-   複雑な条件での絞り込みも、`filter`を複数回繋げたり、コールバック関数内で論理演算子（`&&`, `||`）を使ったりすることで実現できる。

📝 **学習のポイント**

-   [ ] `products`配列から、商品名に「o」（オー）の文字が含まれる商品だけを抽出した新しい配列を作成してみてください。（ヒント: 文字列の`includes`メソッドが使えます）
-   [ ] `products`配列のすべての商品の合計金額はいくらになるでしょうか？（ヒント: `map`で価格の配列を作ってから、ループで合計する？...実は、このような集計には`reduce`というさらに強力なメソッドがあります。興味があれば調べてみましょう！）
-   [ ] `find`と`filter`の使い分けについて、どのような場合にどちらを使うべきか、具体的な例を挙げて説明してください。
