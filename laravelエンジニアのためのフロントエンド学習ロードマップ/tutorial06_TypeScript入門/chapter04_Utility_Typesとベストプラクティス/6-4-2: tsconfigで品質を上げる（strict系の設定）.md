# 6-4-2: tsconfigで品質を上げる（strict系の設定）

## 🎯 このセクションで学ぶこと

- `tsconfig.json` の `strict` オプションが、単一の設定ではなく、複数の厳格なチェックを有効にするためのメタオプションであることを理解する
- `strict` に含まれる主要なオプション（`noImplicitAny`, `strictNullChecks` など）が、それぞれどのようなコード品質の向上に寄与するのかを説明できるようになる
- なぜ `"strict": true` を設定することが、現代のTypeScript開発においてベストプラクティスとされるのかを学ぶ

## 導入

`tsconfig.json` は、TypeScriptプロジェクトの「憲法」であると学びました。その中でも、**コードの堅牢性と品質に最も大きな影響を与えるのが `"strict": true` という一行です。**

この設定を有効にすると、TypeScriptコンパイラはより厳格なルールセットに基づいてコードをチェックするようになります。これにより、曖昧なコードや潜在的なバグをコンパイル時点で検出し、実行時エラーのリスクを大幅に低減させることができます。

初心者のうちは、この厳格さによってエラーが増え、開発が進めにくく感じるかもしれません。しかし、これらのエラーは「将来バグになる可能性のあるコード」をコンパイラが親切に教えてくれているサインです。このセクションでは、`strict` モードが有効にする主要な設定を一つずつ解き明かし、その恩恵を理解します。

## 詳細解説

`"strict": true` は、以下の主要なオプション（およびその他いくつか）をすべて `true` に設定するのと同じ意味を持つ、包括的な設定です。

```json
{
  "compilerOptions": {
    "strict": true
    // 上記は、以下をすべて有効にすることに相当する
    /*
    "noImplicitAny": true,
    "strictNullChecks": true,
    "strictFunctionTypes": true,
    "strictBindCallApply": true,
    "strictPropertyInitialization": true,
    "noImplicitThis": true,
    "alwaysStrict": true
    */
  }
}
```

ここでは、特に重要なものをいくつか見ていきましょう。

### 1. `noImplicitAny`

**暗黙的な `any` 型を禁止します。**

型が明示的に指定されておらず、TypeScriptが型を推論することもできない場合、その変数は暗黙的に `any` 型になってしまいます。`any` は型チェックを無効にするため、これはバグの温床です。`noImplicitAny` は、そのようなケースをコンパイルエラーにします。

```typescript
// noImplicitAny: false の場合
function log(message) { // message は暗黙的に any 型
  console.log(message.toUpperCase()); // 実行時に message が文字列でないとエラー
}

// noImplicitAny: true の場合
function log(message) { // エラー: Parameter 'message' implicitly has an 'any' type.
  // ...
}

// 修正後
function log(message: string) { // OK: 型を明示的に指定する
  console.log(message.toUpperCase());
}
```

### 2. `strictNullChecks`

**`null` と `undefined` をすべての型から分離します。**

これは `strict` モードの中でも最も影響の大きいオプションの一つです。以前のセクションで学んだ通り、このオプションを有効にすると、`string` 型の変数に `null` を代入するようなコードはコンパイルエラーになります。`null` や `undefined` を許容したい場合は、`string | null` のように明示的にUnion型で示す必要があります。

これにより、`Cannot read property of null` のような実行時エラーを劇的に減らすことができます。

### 3. `strictFunctionTypes`

**関数の引数の型チェックをより厳格にします（反変性/contravarianceを正しくチェックする）。**

これは少し高度なトピックですが、関数の互換性に関するチェックを強化します。特に、コールバック関数などを扱う際に、より安全な型チェックを提供します。

```typescript
function greet(fn: (name: string) => void) {
  fn("world");
}

function print(arg: string | number) {
  console.log(arg);
}

// strictFunctionTypes: false の場合
greet(print); // エラーにならないが、潜在的に危険

// strictFunctionTypes: true の場合
greet(print); // エラー: Argument of type 
              // 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 	 " is not assignable to type 
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																						`parameter of type 
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																					"'(string | number) => void
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																															"'(name: string) => void
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																												
																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																																		

`greet`が要求する関数は `(name: string) => void` ですが、`print` は `(arg: string | number) => void` です。`print` は `string` だけでなく `number` も受け入れてしまうため、`greet` の要求よりも広い型を許容してしまっています。`strictFunctionTypes` はこれを検出し、型安全性を保ちます。

## 💡 TIP: 既存のプロジェクトに `strict` を導入する

すでに進行中の大規模なプロジェクトに `"strict": true` を導入すると、大量のコンパイルエラーが発生して圧倒されることがあります。その場合は、`strict` を構成するオプションを一つずつ（例えば、まずは `noImplicitAny` から）有効にして、段階的にコードベースを改善していくアプローチが有効です。

## ✨ まとめ

- `"strict": true` は、TypeScriptの型チェックを最大限に活用するための、複数の厳格なオプションをまとめた設定である。
- **`noImplicitAny`**: 型が不明な変数をなくし、コードのすべての部分が型チェックの対象となるようにする。
- **`strictNullChecks`**: `null`・`undefined` に起因する実行時エラーをコンパイル時点で防ぐ。
- **`strictFunctionTypes`**: 関数の互換性チェックを強化し、より安全なコールバックを実現する。
- 新規プロジェクトでは、最初から `"strict": true` を設定することが強く推奨される。これにより、開発の初期段階から高品質で堅牢なコードを維持することができる。
