# 4-1-7: Chapter 1 ハンズオン: 簡単な計算機を作成する

## 🎯 このハンズオンの目的

このハンズオンでは、Chapter 1で学んだ変数、関数、演算子、条件分岐、繰り返し処理を使って、簡単な計算機プログラムを作成します。

## 準備

作業用のHTMLファイルを作成します。

```html
<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>JavaScript 計算機</title>
</head>
<body>
  <h1>JavaScript 計算機</h1>
  <script src="calculator.js"></script>
</body>
</html>
```

## 課題1: 基本的な計算関数を作成する

`calculator.js`ファイルを作成し、四則演算を行う関数を作成してください。

### 要件

1. `add(a, b)` - 足し算
2. `subtract(a, b)` - 引き算
3. `multiply(a, b)` - 掛け算
4. `divide(a, b)` - 割り算（0で割る場合はエラーメッセージを返す）

### 解答例

```javascript
// 足し算
const add = (a, b) => a + b;

// 引き算
const subtract = (a, b) => a - b;

// 掛け算
const multiply = (a, b) => a * b;

// 割り算（0除算チェック付き）
const divide = (a, b) => {
  if (b === 0) {
    return "エラー: 0で割ることはできません";
  }
  return a / b;
};

// テスト
console.log("足し算: 10 + 5 =", add(10, 5));       // 15
console.log("引き算: 10 - 5 =", subtract(10, 5)); // 5
console.log("掛け算: 10 * 5 =", multiply(10, 5)); // 50
console.log("割り算: 10 / 5 =", divide(10, 5));   // 2
console.log("割り算: 10 / 0 =", divide(10, 0));   // エラーメッセージ
```

## 課題2: 計算機関数を作成する

演算子を文字列で受け取り、適切な計算を行う`calculate`関数を作成してください。

### 要件

1. 演算子として `+`, `-`, `*`, `/` を受け取る
2. 不正な演算子の場合はエラーメッセージを返す
3. 課題1で作成した関数を再利用する

### 解答例

```javascript
const calculate = (a, operator, b) => {
  if (operator === "+") {
    return add(a, b);
  } else if (operator === "-") {
    return subtract(a, b);
  } else if (operator === "*") {
    return multiply(a, b);
  } else if (operator === "/") {
    return divide(a, b);
  } else {
    return "エラー: 不正な演算子です";
  }
};

// テスト
console.log("10 + 5 =", calculate(10, "+", 5));  // 15
console.log("10 - 5 =", calculate(10, "-", 5));  // 5
console.log("10 * 5 =", calculate(10, "*", 5));  // 50
console.log("10 / 5 =", calculate(10, "/", 5));  // 2
console.log("10 % 5 =", calculate(10, "%", 5));  // エラーメッセージ
```

## 課題3: 複数の計算を連続で行う

配列に格納された複数の計算式を順番に処理し、結果を表示する機能を作成してください。

### 要件

1. 計算式は `{ a: 数値, operator: 演算子, b: 数値 }` の形式で配列に格納
2. `for...of`を使って配列を順番に処理
3. 各計算結果をコンソールに表示

### 解答例

```javascript
const calculations = [
  { a: 100, operator: "+", b: 50 },
  { a: 100, operator: "-", b: 30 },
  { a: 25, operator: "*", b: 4 },
  { a: 100, operator: "/", b: 5 },
  { a: 10, operator: "/", b: 0 }
];

console.log("=== 計算結果 ===");

for (const calc of calculations) {
  const result = calculate(calc.a, calc.operator, calc.b);
  console.log(`${calc.a} ${calc.operator} ${calc.b} = ${result}`);
}
```

## 課題4: 計算履歴を保存する

計算結果を履歴として保存し、後から確認できる機能を追加してください。

### 要件

1. 計算履歴を配列で管理
2. 計算するたびに履歴に追加
3. 履歴を表示する関数を作成

### 解答例

```javascript
// 計算履歴を保存する配列
const history = [];

// 履歴付き計算関数
const calculateWithHistory = (a, operator, b) => {
  const result = calculate(a, operator, b);
  const record = {
    expression: `${a} ${operator} ${b}`,
    result: result,
    timestamp: new Date().toLocaleString("ja-JP")
  };
  history.push(record);
  return result;
};

// 履歴を表示する関数
const showHistory = () => {
  console.log("=== 計算履歴 ===");
  if (history.length === 0) {
    console.log("履歴がありません");
    return;
  }
  for (let i = 0; i < history.length; i++) {
    const record = history[i];
    console.log(`${i + 1}. ${record.expression} = ${record.result} (${record.timestamp})`);
  }
};

// テスト
calculateWithHistory(100, "+", 200);
calculateWithHistory(50, "*", 3);
calculateWithHistory(100, "/", 4);

showHistory();
```

## ✨ まとめ

このハンズオンでは、以下のことを実践しました。

- 関数を定義して処理を再利用可能にする
- 条件分岐を使ってエラーハンドリングを行う
- 配列と繰り返し処理を組み合わせてデータを処理する
- オブジェクトを使って構造化されたデータを管理する

これらの基礎知識は、今後学ぶReactやNext.jsでも頻繁に使用します。次のチャプターでは、配列とオブジェクトについてより詳しく学んでいきましょう。
