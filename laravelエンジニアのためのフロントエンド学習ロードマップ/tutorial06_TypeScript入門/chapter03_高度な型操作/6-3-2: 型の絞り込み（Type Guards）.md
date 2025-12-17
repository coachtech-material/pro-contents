# 6-3-2: 型の絞り込み（Type Guards）

## 🎯 このセクションで学ぶこと

- Union型を安全に扱うための**型の絞り込み（Type Narrowing）**の必要性を理解する
- `typeof` 演算子を使ったプリミティブ型の絞り込み方法を習得する
- `instanceof` 演算子を使ったクラスインスタンスの絞り込み方法を習得する
- `in` 演算子を使ったオブジェクトのプロパティ存在チェックによる絞り込み方法を習得する

## 導入

前のセクションで、Union型（例: `string | number`）を持つ変数は、どちらの型にも共通するメソッドしか安全に呼び出せないことを学びました。しかし、実際には「この変数が `string` 型なら大文字にしたいし、`number` 型なら小数点以下を切り捨てたい」といった、型に応じた個別の処理を行いたい場面がほとんどです。

このような課題を解決するのが**型の絞り込み（Type Narrowing）**、通称**Type Guards（型ガード）**です。これは、特定のコードブロック内で、変数の型をより具体的な型に「絞り込む」ための仕組みです。TypeScriptは、`if`文などの条件式を解析し、そのブロック内では変数が特定の型であることを保証してくれます。これにより、Union型を安全かつ柔軟に扱うことが可能になります。

## 詳細解説

### 🔑 なぜ型の絞り込みが必要か？

以下のコードは、前のセクションで見たエラーの例です。

```typescript
function printId(id: string | number) {
  // エラー: Property 'toUpperCase' does not exist on type 'string | number'.
  console.log(id.toUpperCase()); 
}
```

TypeScriptは、`id` が `number` である可能性を排除できないため、コンパイルを許可しません。このコードを安全に実行するには、「`id` が `string` の場合のみ `toUpperCase` を呼び出す」というロジックを加え、それをTypeScriptコンパイラに理解させる必要があります。そのための手法がType Guardsです。

### 1. `typeof` による絞り込み

`typeof` 演算子は、JavaScriptの基本的な演算子で、変数のプリミティブな型を文字列で返します（例: `"string"`, `"number"`, `"boolean"`）。TypeScriptは、この `typeof` を使った条件分岐を理解し、型を絞り込みます。

```typescript
function printId(id: string | number) {
  if (typeof id === "string") {
    // このブロック内では、idは `string` 型として扱われる
    console.log(id.toUpperCase()); // OK
  } else {
    // このブロック内では、idは `number` 型として扱われる
    console.log(id.toFixed(2)); // OK
  }
}

printId("hello-world"); // HELLO-WORLD
printId(123.456);     // 123.46
```

`if (typeof id === "string")` という条件式により、`if`ブロック内では `id` が `string` 型であることが保証されます。TypeScriptコンパイラはこの文脈を理解し、`toUpperCase` の呼び出しを許可します。同様に、`else` ブロック内では残りの可能性である `number` 型に絞り込まれます。

### 2. `instanceof` による絞り込み

`instanceof` 演算子は、あるオブジェクトが特定のクラスのインスタンスであるかどうかを判定します。これは、クラスベースのオブジェクト指向プログラミングで特に役立ちます。

```typescript
class User {
  constructor(public name: string) {}
}

class Company {
  constructor(public companyName: string) {}
}

function printEntity(entity: User | Company) {
  if (entity instanceof User) {
    // このブロック内では、entityは `User` 型として扱われる
    console.log(`User: ${entity.name}`); // OK
  } else {
    // このブロック内では、entityは `Company` 型として扱われる
    console.log(`Company: ${entity.companyName}`); // OK
  }
}

printEntity(new User("Taro"));         // User: Taro
printEntity(new Company("Tech Inc.")); // Company: Tech Inc.
```

### 3. `in` 演算子による絞り込み

`in` 演算子は、オブジェクトが特定のプロパティを持っているかどうかをチェックします。これは、同じような構造を持つが、一部のプロパティが異なるオブジェクトの型を区別するのに便利です。

```typescript
interface Fish {
  swim: () => void;
}

interface Bird {
  fly: () => void;
}

function move(animal: Fish | Bird) {
  if ("swim" in animal) {
    // このブロック内では、animalは `Fish` 型として扱われる
    return animal.swim(); // OK
  } 
  // この時点で、animalは `Bird` 型であることが確定する
  return animal.fly(); // OK
}
```

`"swim" in animal` というチェックにより、TypeScriptは「もし `swim` プロパティが存在するなら、この `animal` は `Fish` 型に違いない」と判断します。これにより、`swim` メソッドを安全に呼び出すことができます。

## 💡 TIP

- Type Guardsは、`if`文だけでなく、`switch`文や三項演算子、`while`ループなど、条件分岐を伴う多くの構文で機能します。TypeScriptのフロー解析能力は非常に高く、コードの流れを追って型を特定してくれます。

## ✨ まとめ

- **型の絞り込み（Type Guards）**は、Union型などの広い型を、特定のコードブロック内でより具体的な型に絞り込むための仕組みである。
- **`typeof`** は、`string`や`number`などのプリミティブ型を絞り込むのに使う。
- **`instanceof`** は、クラスのインスタンスを絞り込むのに使う。
- **`in`** は、オブジェクトが特定のプロパティを持つかどうかで型を絞り込むのに使う。
- これらのType Guardsを使いこなすことで、Union型を安全かつ効果的に活用でき、柔軟で堅牢なコードを書くことができる。
