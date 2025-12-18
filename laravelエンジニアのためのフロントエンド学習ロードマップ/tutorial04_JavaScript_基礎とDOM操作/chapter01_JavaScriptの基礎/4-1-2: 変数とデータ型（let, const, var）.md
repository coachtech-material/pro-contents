# 4-1-2: 変数とデータ型（let, const, var）

## 🎯 このセクションで学ぶこと

- JavaScriptの**変数**を使ってデータを保存・管理できるようになる
- `let`、`const`、`var`の違いを理解し、適切に使い分けられるようになる
- JavaScriptの**基本的なデータ型**（文字列、数値、真偽値など）を理解する

## 導入

プログラミングでは、データを一時的に保存して後で使いたい場面が頻繁にあります。例えば、ユーザーが入力した名前を保存しておいて、後で「こんにちは、〇〇さん」と表示したい場合などです。

このような「データを保存する箱」を**変数**と呼びます。変数を使いこなすことは、プログラミングの第一歩です。

## 変数とは

**変数**は、データに名前を付けて保存する仕組みです。

> **💡 比喩で理解:** 変数は「ラベル付きの箱」のようなものです。箱に「名前」というラベルを貼り、中に「田中太郎」というデータを入れます。後で「名前」の箱を開ければ、「田中太郎」を取り出せます。

```javascript
// 「name」という箱に「田中太郎」を入れる
let name = "田中太郎";

// 「name」の箱の中身を表示
console.log(name);  // 出力: 田中太郎
```

## 変数の宣言方法

JavaScriptでは、変数を宣言する方法が3つあります。

| キーワード | 再代入 | 再宣言 | スコープ | 推奨度 |
|:---|:---|:---|:---|:---|
| `const` | ✕ | ✕ | ブロック | ⭐⭐⭐ |
| `let` | ◯ | ✕ | ブロック | ⭐⭐ |
| `var` | ◯ | ◯ | 関数 | ✕（非推奨） |

### const（定数）

`const`は**再代入できない**変数を宣言します。一度値を設定したら、変更できません。

```javascript
const PI = 3.14159;
console.log(PI);  // 出力: 3.14159

PI = 3.14;  // ❌ エラー: Assignment to constant variable.
```

> **💡 TIP:** 実務では**まず`const`を使う**のが基本です。再代入が必要な場合のみ`let`を使います。これにより、意図しない値の変更を防げます。

### let（変数）

`let`は**再代入できる**変数を宣言します。値を後から変更できます。

```javascript
let count = 0;
console.log(count);  // 出力: 0

count = 1;  // ✅ 再代入OK
console.log(count);  // 出力: 1

count = count + 1;  // ✅ 現在の値に1を足す
console.log(count);  // 出力: 2
```

### var（非推奨）

`var`は古い変数宣言方法です。**現代のJavaScriptでは使いません**。

```javascript
var oldVariable = "古い書き方";
```

> **⚠️ 注意:** `var`には「巻き上げ（hoisting）」や「関数スコープ」など、予期しない動作を引き起こす特性があります。新しいコードでは`const`と`let`のみを使いましょう。

## 変数の命名規則

変数名には以下のルールがあります。

### 使える文字

- アルファベット（a-z, A-Z）
- 数字（0-9）※ただし先頭には使えない
- アンダースコア（_）
- ドル記号（$）

```javascript
// ✅ 有効な変数名
let userName = "田中";
let user_name = "田中";
let $element = document.body;
let _private = "内部変数";
let count1 = 0;

// ❌ 無効な変数名
let 1count = 0;      // 数字で始まっている
let user-name = "";  // ハイフンは使えない
let let = "";        // 予約語は使えない
```

### 命名のベストプラクティス

```javascript
// ✅ キャメルケース（推奨）
let firstName = "太郎";
let isLoggedIn = true;
let getUserData = function() {};

// ✅ 定数は大文字スネークケース
const MAX_COUNT = 100;
const API_BASE_URL = "https://api.example.com";
```

> **💡 TIP:** 変数名は**意味が分かる名前**を付けましょう。`x`や`data`ではなく、`userName`や`productList`のように、何が入っているか一目で分かる名前が理想です。

## データ型

JavaScriptには、以下の基本的なデータ型があります。

### 1. 文字列（String）

テキストデータを表します。シングルクォート（`'`）、ダブルクォート（`"`）、バッククォート（`` ` ``）で囲みます。

```javascript
const greeting = "こんにちは";
const name = '田中太郎';

// テンプレートリテラル（バッククォート）
const message = `${greeting}、${name}さん`;
console.log(message);  // 出力: こんにちは、田中太郎さん
```

> **💡 TIP:** テンプレートリテラル（バッククォート）を使うと、`${}`の中に変数を埋め込めます。文字列の連結よりも読みやすいコードが書けます。

### 2. 数値（Number）

整数と小数を表します。

```javascript
const age = 25;           // 整数
const price = 1980.5;     // 小数
const negative = -10;     // 負の数

// 計算
const total = price * 2;
console.log(total);  // 出力: 3961
```

### 3. 真偽値（Boolean）

`true`（真）または`false`（偽）の2つの値のみを持ちます。

```javascript
const isLoggedIn = true;
const hasError = false;

// 条件分岐で使用
if (isLoggedIn) {
  console.log("ログイン中です");
}
```

### 4. undefined

変数が宣言されたが、値が代入されていない状態を表します。

```javascript
let notAssigned;
console.log(notAssigned);  // 出力: undefined
```

### 5. null

「値が存在しない」ことを明示的に表します。

```javascript
let user = null;  // ユーザーがいないことを明示
console.log(user);  // 出力: null
```

### 6. 配列（Array）

複数の値をまとめて管理します。

```javascript
const fruits = ["りんご", "バナナ", "オレンジ"];
console.log(fruits[0]);  // 出力: りんご（インデックスは0から始まる）
console.log(fruits.length);  // 出力: 3
```

### 7. オブジェクト（Object）

キーと値のペアでデータを管理します。

```javascript
const user = {
  name: "田中太郎",
  age: 25,
  isAdmin: false
};

console.log(user.name);  // 出力: 田中太郎
console.log(user["age"]);  // 出力: 25
```

## データ型の確認

`typeof`演算子を使うと、データ型を確認できます。

```javascript
console.log(typeof "文字列");    // 出力: string
console.log(typeof 123);         // 出力: number
console.log(typeof true);        // 出力: boolean
console.log(typeof undefined);   // 出力: undefined
console.log(typeof null);        // 出力: object（歴史的な理由による）
console.log(typeof [1, 2, 3]);   // 出力: object
console.log(typeof { a: 1 });    // 出力: object
```

> **💡 TIP:** `typeof null`が`object`を返すのは、JavaScriptの歴史的なバグです。`null`かどうかを確認するには、`value === null`を使いましょう。

## 🏃 実践: 変数を使ってみよう

ブラウザの開発者ツール（F12 → Console）で以下のコードを試してみましょう。

```javascript
// 1. 変数を宣言
const userName = "田中太郎";
let userAge = 25;

// 2. 変数を使って表示
console.log(`名前: ${userName}`);
console.log(`年齢: ${userAge}歳`);

// 3. 再代入（letのみ可能）
userAge = 26;
console.log(`来年の年齢: ${userAge}歳`);

// 4. 配列とオブジェクト
const hobbies = ["読書", "映画鑑賞", "プログラミング"];
const profile = {
  name: userName,
  age: userAge,
  hobbies: hobbies
};

console.log(profile);
```

**実行結果:**
```
名前: 田中太郎
年齢: 25歳
来年の年齢: 26歳
{ name: '田中太郎', age: 26, hobbies: ['読書', '映画鑑賞', 'プログラミング'] }
```

## よくある間違いと対処法

### 1. constに再代入しようとする

```javascript
const name = "田中";
name = "佐藤";  // ❌ エラー

// 対処法: 再代入が必要ならletを使う
let name = "田中";
name = "佐藤";  // ✅ OK
```

### 2. 変数を宣言せずに使う

```javascript
console.log(message);  // ❌ エラー: message is not defined

// 対処法: 使う前に宣言する
const message = "こんにちは";
console.log(message);  // ✅ OK
```

### 3. 文字列と数値の混同

```javascript
const price = "100";  // 文字列
const tax = 10;       // 数値

console.log(price + tax);  // 出力: "10010"（文字列連結になる）

// 対処法: 数値に変換する
console.log(Number(price) + tax);  // 出力: 110
```

## ✨ まとめ

- **変数**はデータに名前を付けて保存する仕組み
- **`const`を優先**して使い、再代入が必要な場合のみ`let`を使う
- **`var`は使わない**（レガシーコードでのみ見かける）
- JavaScriptには**7つの基本データ型**がある（文字列、数値、真偽値、undefined、null、配列、オブジェクト）
- 変数名は**意味が分かる名前**を付ける

## 📝 学習のポイント

- [ ] `const`、`let`、`var`の違いを説明できる
- [ ] 変数の命名規則を理解している
- [ ] 基本的なデータ型を列挙できる
- [ ] `typeof`演算子でデータ型を確認できる
- [ ] テンプレートリテラルを使って文字列を作成できる
