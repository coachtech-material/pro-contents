# 6-1-2: 基本的な型と型推論

## Chapter 1: TypeScriptの基礎

### Section 2: 基本的な型と型推論

🎯 **このセクションで学ぶこと**

-   TypeScriptの主要な基本型（`string`, `number`, `boolean`, `null`, `undefined`）の書き方を習得する。
-   配列（`Array`）とオブジェクト（`Object`）の型注釈の方法を習得する。
-   TypeScriptの強力な機能である**型推論**について理解し、型注釈が不要なケースを知る。

--- 

### イントロダクション：変数に「型」というラベルを貼る

TypeScriptでは、変数や定数を宣言する際に、`変数名: 型`という形式で**型注釈（Type Annotation）**を行います。これにより、その変数にどのような種類のデータが入るべきかを明示的に示すことができます。

```typescript
let user: string = "Yamada";
let age: number = 28;
let isAdmin: boolean = true;
```

このセクションでは、JavaScriptでお馴染みのデータ型に、どのように型注釈を与えていくかを学んでいきます。

--- 

### ⚙️ 主要なプリミティブ型

JavaScriptのプリミティブ型は、そのまま型注釈として使えます。型名はすべて**小文字**で書くのがルールです。

| 型 | 説明 | 例 |
|:---|:---|:---|
| `string` | 文字列 | `let name: string = "Alice";` |
| `number` | すべての数値（整数、浮動小数点数） | `let score: number = 95.5;` |
| `boolean` | `true`または`false` | `let isLoggedIn: boolean = false;` |
| `null` | `null`値 | `let data: null = null;` |
| `undefined` | `undefined`値 | `let memo: undefined = undefined;` |

通常、`null`や`undefined`を単独で型注釈することは稀で、後述するユニオン型（例: `string | null`）の一部として使われることがほとんどです。

--- 

### ⚙️ 配列 (Array) の型

配列の型を表現するには、2つの書き方があります。

1.  **`型[]`** （推奨）
2.  **`Array<型>`** （ジェネリクス構文）

どちらを使っても機能は同じですが、一般的には `型[]` の方が簡潔でよく使われます。

```typescript
// string型の要素のみを持つ配列
let fruits: string[] = ["apple", "banana", "cherry"];

// number型の要素のみを持つ配列
let scores: number[] = [88, 92, 76];
// または Array<number> とも書ける
let scores2: Array<number> = [88, 92, 76];

// エラー: number[]型の配列にstringは追加できない
fruits.push(100); 
scores.push("hello");
```

--- 

### ⚙️ オブジェクト (Object) の型

オブジェクトの型は、そのオブジェクトがどのようなプロパティを持つべきかを定義することで表現します。`{}`の中に、`プロパティ名: 型`のリストを記述します。

```typescript
let user: {
  id: number;
  name: string;
  isAdmin: boolean;
};

// 型注釈に合致するオブジェクトは代入可能
user = {
  id: 1,
  name: "Sato",
  isAdmin: true,
};

// エラー: プロパティ'isAdmin'がありません
user = {
  id: 2,
  name: "Suzuki",
};

// エラー: プロパティ'email'は型に存在しません
user = {
  id: 3,
  name: "Tanaka",
  isAdmin: false,
  email: "tanaka@example.com",
};
```

オブジェクトの型定義は長くなりがちなので、通常は後述する`type`エイリアスや`interface`を使って、名前付きの型として再利用できるようにします。

--- 

### 🚀 型推論 (Type Inference) の威力

TypeScriptの非常に賢い点として、多くの場合、我々がわざわざ型注釈を書かなくても、**文脈から自動的に型を推測してくれる**機能があります。これを**型推論**と呼びます。

特に、**変数の宣言と同時に初期値を代入する場合**、TypeScriptは代入された値の型をその変数の型として自動的に推論します。

```typescript
// let message: string = "Hello, World!"; と書くのと同じ
let message = "Hello, World!";

// messageはstring型と推論されているので、数値を代入しようとするとエラーになる
message = 2024;

// --- 他の例 ---

// ageはnumber型と推論される
let age = 30;

// isActiveはboolean型と推論される
const isActive = true;

// itemsはstring[]型と推論される
const items = ["a", "b", "c"];
```

**ベストプラクティス:**
変数の宣言と同時に初期値を代入する場合など、**TypeScriptが正しく型を推論できる場面では、型注釈は省略する**のが一般的です。これにより、コードの冗長性を減らし、スッキリと保つことができます。

型注釈が必須になるのは、主に以下のような場面です。
-   初期値なしで変数を宣言する場合
-   関数の引数
-   より複雑な型を明示したい場合

--- 

✨ **まとめ**

-   TypeScriptの基本的な型は、JavaScriptのプリミティブ型名（小文字）を使って `変数名: 型` のように注釈する。
-   配列の型は `string[]` や `number[]` のように表現する。
-   オブジェクトの型は `{ id: number; name: string; }` のように、プロパティの形状を定義する。
-   **型推論**は、TypeScriptが文脈から自動で型を決定する強力な機能である。
-   変数の宣言と同時に初期化する場合など、型推論が効く場面では、冗長な型注釈は省略するのが良い習慣である。

📝 **学習のポイント**

-   [ ] `let x = 100;` と `let x: number = 100;` の違いは何ですか？ どちらの書き方が推奨されますか？また、それはなぜですか？
-   [ ] ユーザーのリストを表現する配列の型を定義してください。各ユーザーは`id` (数値) と `name` (文字列) を持つオブジェクトです。
-   [ ] `const value;` のように、初期値なしで定数を宣言するとどうなりますか？ TypeScriptではどのようなエラーが出ますか？
