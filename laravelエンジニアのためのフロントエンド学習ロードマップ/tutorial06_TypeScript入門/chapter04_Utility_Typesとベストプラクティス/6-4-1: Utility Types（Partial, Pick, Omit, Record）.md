# 6-4-1: Utility Types（Partial, Pick, Omit, Record）

## 🎯 このセクションで学ぶこと

- 既存の型から新しい型を効率的に作成するための**Utility Types**の概念を理解する
- `Partial<T>` を使って、型のすべてのプロパティをオプショナルにする方法を習得する
- `Pick<T, K>` と `Omit<T, K>` を使って、既存の型から特定のプロパティを選択または除外した新しい型を作る方法を習得する
- `Record<K, T>` を使って、キーと値の型が定まったオブジェクト型を動的に作成する方法を学ぶ

## 導入

TypeScriptでアプリケーションを開発していると、「この型と似ているけど、一部だけ違う型が欲しい」という状況が頻繁に発生します。例えば、

- ユーザー情報を更新するAPIでは、全項目ではなく一部の項目だけを送りたい
- ユーザー一覧画面では、全情報ではなくIDと名前だけを表示したい
- 新規ユーザーを作成する際には、サーバーが自動生成する`id`や`createdAt`は不要

これらの要求のために、毎回新しい`interface`をゼロから定義するのは非常に手間がかかり、コードの重複にも繋がります。

このような一般的な型の変換操作を簡単に行うために、TypeScriptには**Utility Types（ユーティリティ型）**という便利なツールが組み込まれています。これらは、既存の型を引数として受け取り、新しい型を返すジェネリクスベースの型です。このセクションでは、実務で特に頻繁に使われる4つの重要なUtility Typeを学びます。

## 詳細解説

以下の解説では、基準となる`User`インターフェースを使用します。

```typescript
interface User {
  id: number;
  name: string;
  email: string;
  isAdmin: boolean;
  createdAt: Date;
}
```

### 1. `Partial<T>`

`Partial<T>`は、型`T`の**すべてのプロパティをオプショナル（`?`を付けた状態）にした新しい型**を構築します。

**ユースケース**: ユーザー情報の一部だけを更新する関数の引数など。

```typescript
// Userのすべてのプロパティがオプショナルになる
// type PartialUser = { 
//   id?: number; 
//   name?: string; 
//   email?: string; 
//   isAdmin?: boolean; 
//   createdAt?: Date; 
// }
type PartialUser = Partial<User>;

function updateUser(id: number, fieldsToUpdate: PartialUser) {
  // ...更新処理
}

// nameとemailだけを更新する
updateUser(1, { name: 'Taro Yamada', email: 'taro@new-example.com' });
```

### 2. `Pick<T, K>`

`Pick<T, K>`は、型`T`から、指定したキー`K`（Union型で複数指定可）の**プロパティだけを選択（Pick）して**新しい型を構築します。

**ユースケース**: ユーザーの一覧表示に必要な、最小限の情報の型を作りたい場合など。

```typescript
// Userからidとnameプロパティだけを抜き出した型
// type UserPreview = { 
//   id: number; 
//   name: string; 
// }
type UserPreview = Pick<User, 'id' | 'name'>;

const user: UserPreview = {
  id: 1,
  name: 'Taro'
};
```

### 3. `Omit<T, K>`

`Omit<T, K>`は`Pick`の逆で、型`T`から、指定したキー`K`の**プロパティを除外（Omit）して**新しい型を構築します。

**ユースケース**: 新規ユーザー作成時に、サーバー側で自動採番される`id`や`createdAt`を除いた型を作りたい場合など。

```typescript
// UserからidとcreatedAtプロパティを除外した型
// type UserCreationPayload = { 
//   name: string; 
//   email: string; 
//   isAdmin: boolean; 
// }
type UserCreationPayload = Omit<User, 'id' | 'createdAt'>;

function createUser(payload: UserCreationPayload) {
  // ...作成処理
}

createUser({ name: 'Jiro', email: 'jiro@example.com', isAdmin: false });
```

### 4. `Record<K, T>`

`Record<K, T>`は、キーの型が`K`、値の型が`T`である**オブジェクト型を構築します**。`K`には通常、`string`や`number`、または具体的な文字列リテラルのUnion型を指定します。

**ユースケース**: 特定のキーを持つことが決まっている設定オブジェクトや、辞書（連想配列）のようなデータ構造を表現したい場合など。

```typescript
// 'home' | 'about' | 'contact' のいずれかをキーに持ち、
// 値として { title: string; path: string } を持つオブジェクトの型
type PageKey = 'home' | 'about' | 'contact';

interface PageInfo {
  title: string;
  path: string;
}

type Pages = Record<PageKey, PageInfo>;

const siteNav: Pages = {
  home: { title: 'Home', path: '/' },
  about: { title: 'About Us', path: '/about' },
  contact: { title: 'Contact', path: '/contact' }
  // 'extra': { title: 'Extra', path: '/extra' } // エラー: 'extra'はPageKeyに含まれない
};
```

## 💡 TIP

- Utility Typesはネストして組み合わせることも可能です。例えば、「ユーザー作成ペイロードだが、すべての項目をオプショナルにしたい」場合は `Partial<Omit<User, 'id' | 'createdAt'>>` のように書くことができます。
- ここで紹介したもの以外にも、`Readonly<T>`（全プロパティを読み取り専用にする）、`Required<T>`（全プロパティを必須にする）、`ReturnType<T>`（関数の戻り値の型を取得する）など、多くの便利なUtility Typeが存在します。

## ✨ まとめ

- **Utility Types**は、既存の型を元に新しい型を効率的に作成するための、TypeScript組み込みの型ツールである。
- **`Partial<T>`**: 型`T`のすべてのプロパティをオプショナルにする。
- **`Pick<T, K>`**: 型`T`から指定したキー`K`のプロパティのみを抽出する。
- **`Omit<T, K>`**: 型`T`から指定したキー`K`のプロパティを除外する。
- **`Record<K, T>`**: キーが`K`型、値が`T`型であるオブジェクト型を生成する。
- これらを活用することで、型の定義をDRY（Don't Repeat Yourself）に保ち、メンテナンス性の高いコードを書くことができる。
