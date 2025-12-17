# 6-3-1: Union型とIntersection型

## 🎯 このセクションで学ぶこと

- 複数の型を許容する**Union型（合併型）**の概念と使い方を理解する
- 複数の型を結合する**Intersection型（交差型）**の概念と使い方を理解する
- これら2つの型をどのような場面で使い分けるべきかの判断基準を習得する

## 導入

TypeScriptの基本的な型（`string`, `number`など）を学びましたが、実際のアプリケーションでは、より柔軟な型定義が必要になる場面が頻繁にあります。例えば、「ユーザーIDは、数値の場合もあれば、UUIDのような文字列の場合もある」「あるオブジェクトは、基本的なユーザー情報と投稿情報の両方を持っている必要がある」といったケースです。

このような要求に応えるための強力な武器が、**Union型 (`|`)** と **Intersection型 (`&`)** です。これらは、既存の型を組み合わせて新しい、より表現力豊かな型を作り出すための基本的なツールです。このセクションでは、これらの高度な型操作をマスターし、TypeScriptの型システムをさらに活用する方法を学びます。

## 詳細解説

### 🔑 Union型 (Union Types): 「または」の型

Union型は、その名の通り「合併」を意味し、「**A または B**」のように、ある変数が複数の型のうちのいずれか一つであることを表現します。型名の間にパイプ `|` を挟んで定義します。

#### 基本的な使い方

```typescript
// `userId` は string または number のどちらかの型を持つことができる
let userId: string | number;

userId = 101;       // OK
userId = "user-abc"; // OK

// userId = true; // エラー: Type 'boolean' is not assignable to type 'string | number'.
```

この `userId` は、数値でも文字列でも受け入れることができる、より柔軟な変数になりました。

#### Union型の注意点

Union型を持つ変数のプロパティやメソッドにアクセスしようとする場合、その操作は**すべての構成要素の型に共通して存在するものでなければなりません**。

```typescript
function printId(id: string | number) {
  console.log(id.toUpperCase()); // エラー: Property 'toUpperCase' does not exist on type 'string | number'.
                                 // Property 'toUpperCase' does not exist on type 'number'.
}
```

この例では、`id` が `number` である可能性もあるため、`string` 型にしか存在しない `toUpperCase` メソッドを直接呼び出すことはできません。このような場合、次のセクションで学ぶ**型の絞り込み（Type Guards）**が必要になります。

### 🔑 Intersection型 (Intersection Types): 「かつ」の型

Intersection型は、「交差」を意味し、「**A かつ B**」のように、複数の型が持つすべてのプロパティを**結合**した新しい型を作ります。型名の間にアンパサンド `&` を挟んで定義します。

#### 基本的な使い方

オブジェクトの型を結合する際によく使われます。

```typescript
// 基本的なユーザー情報を持つ型
interface User {
  id: number;
  name: string;
}

// 連絡先情報を持つ型
interface Contact {
  email: string;
  phone: string;
}

// User型とContact型の両方のプロパティを持つ新しい型を定義
type UserProfile = User & Contact;

const userProfile: UserProfile = {
  id: 1,
  name: "Taro Yamada",
  email: "taro@example.com",
  phone: "090-1234-5678"
};
```

`UserProfile` 型は、`User` 型と `Contact` 型の両方のプロパティをすべて持っている必要があります。一つでも欠けているとエラーになります。

### Union型とIntersection型の比較

| 型 | 記号 | 意味 | ユースケース例 |
|:---|:---:|:---|:---|
| **Union型** | `|` | **または (OR)**<br>複数の型のうち、いずれか1つ。 | - 関数の引数が複数の型を受け入れる場合<br>- APIのレスポンスが成功時と失敗時で異なる構造を持つ場合 |
| **Intersection型** | `&` | **かつ (AND)**<br>複数の型の特徴をすべて併せ持つ。 | - 既存の複数の型を組み合わせて、新しい複合的な型を作りたい場合<br>- Mixin（複数の小さなオブジェクトを合成するパターン）を型で表現する場合 |

## 💡 TIP: Typeエイリアスとの組み合わせ

Union型やIntersection型は、`type` キーワードを使って**Typeエイリアス（型エイリアス）**として定義することで、再利用性が格段に向上します。

```typescript
// Union型のエイリアス
type StringOrNumber = string | number;

// Intersection型のエイリアス
type AdminUser = User & { isAdmin: boolean };

function processId(id: StringOrNumber) { /* ... */ }

const admin: AdminUser = {
  id: 1,
  name: "Admin",
  isAdmin: true
};
```

複雑な型を何度も書く必要がなくなり、コードの可読性が向上します。

## ✨ まとめ

- **Union型 (`|`)** は、「AまたはB」を表現し、変数が複数の型のうちのいずれかであることを許容する。
- **Intersection型 (`&`)** は、「AかつB」を表現し、複数の型のプロパティをすべて併せ持つ新しい型を作成する。
- Union型は型の**選択肢を広げ**、Intersection型は型の**特徴を合成する**と覚えると良い。
- これらの型は、`type` エイリアスと組み合わせることで、よりクリーンで再利用可能なコードを書く助けとなる。
