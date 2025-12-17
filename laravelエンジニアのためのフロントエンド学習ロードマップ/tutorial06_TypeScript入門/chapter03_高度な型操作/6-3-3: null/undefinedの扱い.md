# 6-3-3: null/undefinedの扱い

## 🎯 このセクションで学ぶこと

- JavaScriptにおける `null` と `undefined` の違いを理解する
- TypeScriptの `strictNullChecks` オプションがなぜ重要なのかを説明できるようになる
- Optional Chaining (`?.`) と Nullish Coalescing (`??`) を使って、`null` や `undefined` を安全かつ簡潔に扱う方法を習得する

## 導入

`null` と `undefined` は、JavaScriptにおける「値が存在しないこと」を示すプリミティブ値ですが、多くの開発者にとって混乱の元であり、有名な「ぬるぽ」に代表される `Cannot read property '...' of null` のような実行時エラーの最大の原因です。

TypeScriptは、この問題に対処するための強力な仕組みを提供します。特にコンパイラオプション `strictNullChecks` を有効にすることで、`null` や `undefined` が潜在的に含まれる変数を静的に検出し、より安全なコードを書くことを強制します。このセクションでは、これらの値を安全に扱うためのTypeScriptの機能と、モダンなJavaScriptの構文を学びます。

## 詳細解説

### 🔑 `null` vs `undefined`

まず、JavaScriptにおける2つの値の違いを再確認しましょう。

- **`undefined`**: 変数が宣言されたが、まだ値が代入されていない状態。または、関数が何も返さない場合のデフォルトの戻り値。
- **`null`**: 開発者が意図的に「値がない」ことを明示するために代入する値。

```javascript
let a; // a は undefined

const obj = { b: 1 };
// obj.c は undefined

// 意図的に「空」を示す
let user = null;
```

TypeScriptでは、これらはそれぞれ `undefined` 型と `null` 型として扱われます。

### `strictNullChecks` の重要性

`tsconfig.json` で `"strict": true` を設定すると、その一部である `"strictNullChecks": true` が有効になります。これにより、TypeScriptの型システムは `null` と `undefined` を他の型（`string`や`number`など）とは明確に区別するようになります。

**`strictNullChecks: false` の場合（非推奨）**

```typescript
// strictNullChecks: false
let name: string = null; // エラーにならない！
console.log(name.toUpperCase()); // 実行時エラー！ Cannot read properties of null (reading 'toUpperCase')
```

`null` を `string` 型の変数に代入できてしまうため、実行時エラーのリスクが残ります。

**`strictNullChecks: true` の場合（推奨）**

```typescript
// strictNullChecks: true
let name: string = null; // エラー: Type 'null' is not assignable to type 'string'.
```

コンパイル時点でエラーを検出できるため、実行時エラーを未然に防ぐことができます。`null` や `undefined` を許容したい場合は、Union型を使って明示的に示す必要があります。

```typescript
let nullableName: string | null = null; // OK
```

### 安全な `null`/`undefined` の扱い方

`strictNullChecks` を有効にすると、`null` や `undefined` の可能性がある変数を使おうとするとコンパイルエラーになります。これを解決するためのモダンな構文が2つあります。

#### 1. Optional Chaining (`?.`)

Optional Chaining（オプショナルチェイニング）演算子は、オブジェクトのプロパティにアクセスする際に、そのオブジェクトが `null` または `undefined` であった場合に、エラーを発生させる代わりに `undefined` を返す構文です。

```typescript
interface User {
  name: string;
  address?: { // addressは存在しないかもしれない
    street: string;
  };
}

const user1: User = { name: "Taro" };
const user2: User = { name: "Jiro", address: { street: "Shibuya" } };

// 従来の方法（ネストが深い）
const street1_old = user1.address && user1.address.street;

// Optional Chaining を使った方法
const street1 = user1.address?.street; // user1.address が undefined なので、結果は undefined
const street2 = user2.address?.street; // "Shibuya"

console.log(street1); // undefined
console.log(street2); // "Shibuya"
```

`?.` を使うことで、`if`文のネストを避け、非常に簡潔かつ安全にプロパティにアクセスできます。

#### 2. Nullish Coalescing (`??`)

Nullish Coalescing（null合体）演算子は、左辺の値が `null` または `undefined` の場合にのみ、右辺のデフォルト値を返す演算子です。

```typescript
let userInput = null;
let userName = userInput ?? "Guest"; // userInput が null なので "Guest" が代入される
console.log(userName); // "Guest"

let userAgeInput = 0;
let userAge = userAgeInput ?? 20; // userAgeInput は null/undefined ではないので 0 が代入される
console.log(userAge); // 0
```

**`||` 演算子との違い**

従来の `||` 演算子は、左辺が `0` や `""` (空文字) のような「falsy」な値の場合にも右辺を返してしまいます。`??` は `null` と `undefined` の場合にのみ反応するため、より厳密なデフォルト値の設定が可能です。

```typescript
let volume_or = 0 || 50; // 50 (0がfalsyなため)
let volume_nullish = 0 ?? 50; // 0 (0はnullishではないため)
```

## 💡 TIP

- Optional ChainingとNullish Coalescingを組み合わせることで、非常に強力なフォールバック処理を一行で書くことができます。

```typescript
const streetName = user.address?.street ?? "住所未登録";
```

このコードは、「もし `user.address` が存在し、その中に `street` プロパティがあればその値を、そうでなければ `'住所未登録'` を使う」という意味になります。

## ✨ まとめ

- `strictNullChecks` を有効にすることは、TypeScriptで安全なコードを書くための基本である。
- `null` や `undefined` を許容する場合は、`string | null` のようにUnion型で明示的に示す必要がある。
- **Optional Chaining (`?.`)** は、`null` や `undefined` の可能性があるオブジェクトのプロパティに安全にアクセスするための構文。
- **Nullish Coalescing (`??`)** は、値が `null` または `undefined` の場合にのみデフォルト値を提供するための構文。
- これらの機能を使いこなすことで、`null` や `undefined` に起因する実行時エラーを大幅に削減できる。
