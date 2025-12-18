# 6-3-3: null/undefinedの扱い

## 🎯 この章で学ぶこと

- `null`と`undefined`の違いを理解する
- TypeScriptにおける`null`/`undefined`の型安全な扱い方を学ぶ
- オプショナルチェイニングとNullish Coalescingを使いこなす
- `strictNullChecks`の重要性を理解する

## はじめに

JavaScriptにおいて、`null`と`undefined`は「値がない」ことを表す特殊な値です。しかし、これらの値を適切に扱わないと、実行時に「Cannot read property of undefined」といったエラーが発生し、アプリケーションがクラッシュする原因となります。

TypeScriptは、これらの値を型システムで管理することで、コンパイル時にエラーを検出し、より安全なコードを書くことを可能にします。

## 1. `null`と`undefined`の違い

JavaScriptには「値がない」ことを表す値が2つあります。

| 値 | 意味 | 発生するケース |
|---|---|---|
| `undefined` | 値が定義されていない | 変数を宣言したが値を代入していない、オブジェクトに存在しないプロパティにアクセスした |
| `null` | 値が意図的に空である | 開発者が明示的に「値がない」ことを示すために代入する |

```typescript
let a; // undefined（値が未定義）
let b = null; // null（意図的に空）

const obj = { name: "Taro" };
console.log(obj.age); // undefined（存在しないプロパティ）
```

## 2. `strictNullChecks`オプション

TypeScriptの`tsconfig.json`で`strictNullChecks`を`true`に設定すると（`strict: true`に含まれる）、`null`と`undefined`は明示的に型に含めない限り、他の型に代入できなくなります。

```typescript
// strictNullChecks: false の場合
let name: string = null; // OK（危険！）

// strictNullChecks: true の場合
let name: string = null; // Error: Type 'null' is not assignable to type 'string'.
let name: string | null = null; // OK（Union型で明示的に許可）
```

このオプションを有効にすることで、`null`や`undefined`が混入する可能性のある箇所をコンパイラが検出してくれます。

## 3. オプショナルプロパティとオプショナルパラメータ

オブジェクトのプロパティや関数の引数が省略可能であることを示すには、`?`を使います。

```typescript
// オプショナルプロパティ
interface User {
  name: string;
  age?: number; // number | undefined と同等
}

const user1: User = { name: "Taro" }; // OK
const user2: User = { name: "Hanako", age: 25 }; // OK

// オプショナルパラメータ
function greet(name: string, greeting?: string): string {
  return `${greeting ?? "Hello"}, ${name}!`;
}

greet("Taro"); // "Hello, Taro!"
greet("Taro", "Hi"); // "Hi, Taro!"
```

## 4. オプショナルチェイニング (`?.`)

オプショナルチェイニングを使うと、ネストしたオブジェクトのプロパティに安全にアクセスできます。途中で`null`や`undefined`に遭遇した場合、エラーを投げずに`undefined`を返します。

```typescript
interface Company {
  name: string;
  address?: {
    city: string;
    zipCode?: string;
  };
}

const company: Company = { name: "TechCorp" };

// オプショナルチェイニングなし（危険）
// const city = company.address.city; // Error: Cannot read property 'city' of undefined

// オプショナルチェイニングあり（安全）
const city = company.address?.city; // undefined
const zipCode = company.address?.zipCode; // undefined
```

## 5. Nullish Coalescing (`??`)

Nullish Coalescing演算子は、左辺が`null`または`undefined`の場合にのみ右辺の値を返します。`||`演算子と似ていますが、`0`や空文字列`""`を有効な値として扱う点が異なります。

```typescript
const value1 = null ?? "default"; // "default"
const value2 = undefined ?? "default"; // "default"
const value3 = 0 ?? "default"; // 0（0は有効な値）
const value4 = "" ?? "default"; // ""（空文字列は有効な値）

// || との違い
const value5 = 0 || "default"; // "default"（0はfalsyなので右辺が返る）
const value6 = "" || "default"; // "default"（空文字列はfalsyなので右辺が返る）
```

## 6. 非Nullアサーション演算子 (`!`)

変数の後ろに`!`を付けると、TypeScriptに対して「この値は`null`や`undefined`ではない」と断言できます。ただし、これは型チェックを回避するものであり、実行時の安全性は保証されません。**使用は最小限に留めるべきです。**

```typescript
function getElement(id: string): HTMLElement | null {
  return document.getElementById(id);
}

// 非Nullアサーション（危険な場合がある）
const element = getElement("app")!;
element.innerHTML = "Hello"; // 要素が存在しない場合、実行時エラー

// より安全な方法
const element = getElement("app");
if (element) {
  element.innerHTML = "Hello";
}
```

## ✨ まとめ

- `null`は「意図的に空」、`undefined`は「値が未定義」を表す
- `strictNullChecks`を有効にすることで、`null`/`undefined`に関するバグをコンパイル時に検出できる
- オプショナルチェイニング (`?.`) を使うと、ネストしたプロパティへの安全なアクセスが可能
- Nullish Coalescing (`??`) を使うと、`null`/`undefined`の場合のみデフォルト値を設定できる
- 非Nullアサーション (`!`) は便利だが、実行時の安全性を保証しないため使用は慎重に
