# Tutorial 6: TypeScript 基礎から実用へ

## Chapter 1: TypeScriptの基礎

### Chapter 1 ハンズオン: 簡単な計算アプリを型安全にする

🎯 **このハンズオンで達成すること**

-   既存のJavaScriptコードにTypeScriptの型を適用するプロセスを体験する。
-   変数、関数の引数、関数の戻り値に基本的な型注釈を行えるようになる。
-   TypeScriptを導入することで、どのようにバグを未然に防げるかを実感する。

--- 

🖼️ **完成イメージ**

四則演算を行うシンプルな関数群と、それらを使って計算結果をコンソールに出力するJavaScriptコードがあります。このコードをTypeScriptにリファクタリングし、型安全性を確保します。リファクタリングの過程で、意図的に型エラーを発生させ、TypeScriptがどのようにエラーを検知するかを確認します。

**最終的なコンソール出力:**
```
Addition: 30
Subtraction: -10
Multiplication: 200
Division: 0.5
--- Error Cases ---
Error: Division by zero is not allowed.
```

--- 

### 🧠 先輩エンジニアの思考プロセス

「このJSコード、なんかバグりそうだからTypeScriptで安全にしておいて」と頼まれたら、まずどこから手をつけるか？

1.  **ファイル拡張子の変更:** まずは話の始まり。`.js`を`.ts`に変える。これでTypeScriptコンパイラの監視対象になる。
2.  **変数と定数のチェック:** コード全体を見渡して、変数や定数に型を付けていく。`let`や`const`で初期値が代入されているものは、ほとんど型推論に任せられるな。OK。
3.  **関数のシグネチャ定義（最重要）:** 次に関数。これが一番大事。一つ一つの関数について、「こいつは何を受け取って（引数）、何を返す（戻り値）んだ？」を明確にしていく。
    -   `add(a, b)`: `a`と`b`は明らかに数値(`number`)。足し算の結果も数値(`number`)だな。→ `(a: number, b: number): number`
    -   `subtract`, `multiply`も同じだな。
    -   `divide(a, b)`: これも基本は`number`だけど...おっと、`b`が`0`だとマズい。これは型だけじゃなくて、ロジックの修正も必要だな。0で割ろうとしたらエラーを投げるようにしよう。戻り値は成功すれば`number`だ。
4.  **エラーハンドリング:** `divide`でエラーを投げるようにしたから、呼び出し元で`try...catch`を使ってちゃんとエラーを捕まえてあげないと、プログラムがクラッシュしちゃうな。これも追加しよう。
5.  **型エラーのシミュレーション:** 最後に、わざと間違った使い方をしてみる。`add("1", "2")`みたいに。これでエディタやコンパイラがちゃんと怒ってくれれば、リファクタリング成功だ。

--- 

### 🏃 実践: Step by Stepで型安全なコードへ

`index.ts`というファイル名で作業を始めます。（TypeScript Playgroundのようなオンライン環境で試すのも良いでしょう）

#### Step 1: 元となるJavaScriptコード

まずは、リファクタリング対象のJavaScriptコードです。

```javascript
// index.js (リファクタリング前)

const add = (a, b) => a + b;
const subtract = (a, b) => a - b;
const multiply = (a, b) => a * b;
const divide = (a, b) => a / b;

const num1 = 10;
const num2 = 20;

console.log("Addition:", add(num1, num2));
console.log("Subtraction:", subtract(num1, num2));
console.log("Multiplication:", multiply(num1, num2));
console.log("Division:", divide(num1, num2));

// 問題のある呼び出し
console.log(add("5", "10")); // "510" になってしまう！
```

#### Step 2: 関数の型定義を追加する

各関数に、引数と戻り値の型注釈を追加します。これがTypeScript化の核となる作業です。

```typescript
// index.ts

const add = (a: number, b: number): number => a + b;
const subtract = (a: number, b: number): number => a - b;
const multiply = (a: number, b: number): number => a * b;

// divide関数は0で割るケースを考慮する
const divide = (a: number, b: number): number => {
  if (b === 0) {
    throw new Error("Division by zero is not allowed.");
  }
  return a / b;
};

const num1 = 10; // 型推論により number
const num2 = 20; // 型推論により number

console.log("Addition:", add(num1, num2));
console.log("Subtraction:", subtract(num1, num2));
console.log("Multiplication:", multiply(num1, num2));

// divideはエラーを投げる可能性があるので、try...catchで囲む
try {
  console.log("Division:", divide(num1, num2));
} catch (error) {
  // errorがErrorオブジェクトかチェックするのがより丁寧
  if (error instanceof Error) {
    console.error("Error:", error.message);
  }
}
```

#### Step 3: 型エラーを体験する

型定義を追加したことで、JavaScriptでは素通りしてしまっていた問題のあるコードが、コンパイルエラーとして検出されることを確認します。

```typescript
// index.ts (続き)

// コンパイルエラー！
// Argument of type 'string' is not assignable to parameter of type 'number'.
console.log(add("5", "10")); 
```

このコードをエディタに貼り付けると、`add("5", "10")`の部分に赤い波線が表示され、ホバーすると上記のようなエラーメッセージが表示されるはずです。これにより、意図しない文字列結合(`"510"`)のようなバグを、実行前に完全に防ぐことができます。

#### Step 4: エラーハンドリングをテストする

`divide`関数で`0`による除算を試み、`try...catch`が正しく機能することを確認します。

```typescript
// index.ts (続き)

console.log("--- Error Cases ---");
try {
  // 0で割ってみる
  divide(10, 0);
} catch (error) {
  if (error instanceof Error) {
    console.error("Error:", error.message);
  }
}
```

これを実行すると、コンソールに`Error: Division by zero is not allowed.`と表示され、プログラムがクラッシュすることなく、エラーが適切に処理されたことがわかります。

--- 

✨ **まとめ**

-   既存のJavaScriptコードをTypeScript化する第一歩は、関数のシグネチャ（引数と戻り値）に型を定義することである。
-   型定義を行うことで、間違った型の引数を渡すといった単純なミスを、コード実行前に100%検出できるようになった。
-   型安全性は、単にエラーを防ぐだけでなく、`divide`関数の例のように、コードのロジック（「0では割れない」など）をより堅牢にするきっかけも与えてくれる。
-   `try...catch`構文は、TypeScriptにおいてもエラーハンドリングの重要な役割を担う。

📝 **学習のポイント**

-   [ ] `multiply`関数に、文字列の引数を渡してみてください。どのようなエラーメッセージが表示されますか？
-   [ ] `num1`と`num2`の宣言で、`const num1: number = 10;`のように型注釈をあえて書かなかったのはなぜですか？
-   [ ] ユーザー情報（`name`と`age`を持つオブジェクト）を受け取り、`"Name: Alice, Age: 30"`のような文字列を返す関数`formatUser`を、このハンズオンのスタイルで型定義してみてください。
