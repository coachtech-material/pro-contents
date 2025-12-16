# Tutorial 6: TypeScript 基礎から実用へ

## Chapter 1: TypeScriptの基礎

### Section 3: 関数の型定義

🎯 **このセクションで学ぶこと**

-   関数の**引数**と**戻り値**に型注釈を付ける方法を習得する。
-   戻り値がない関数を表す`void`型について理解する。
-   アロー関数の型定義の方法を習得する。

--- 

### イントロダクション：関数の「契約」を明確にする

TypeScriptが最も真価を発揮する場面の一つが、関数の型定義です。関数に型を付けることで、その関数が「どのような引数を受け取り、どのような値を返すのか」という**契約（シグネチャ）**をコード上で明確に定義できます。

これにより、関数を間違った方法で使ってしまうことを防ぎ、関数を使う側は、その内部実装を知らなくても、型情報だけで安全に関数を利用できるようになります。

--- 

### ⚙️ 引数と戻り値の型注釈

関数の型定義は、主に2つの部分から成ります。

1.  **引数の型注釈:** 各引数名の直後に型を注釈します。
2.  **戻り値の型注釈:** 引数リストの閉じ括弧 `)` の直後に型を注釈します。

**構文:**
```typescript
function 関数名(引数1: 型1, 引数2: 型2): 戻り値の型 {
  // ...関数の処理...
  return 値;
}
```

**例：2つの数値を受け取って合計を返す関数**
```typescript
function add(a: number, b: number): number {
  return a + b;
}

const sum = add(10, 20); // OK

// コンパイルエラー: 引数の型が合わない
const invalidSum1 = add("10", "20");

// コンパイルエラー: 引数の数が合わない
const invalidSum2 = add(10);
```

-   `a: number`, `b: number`：この関数は、`number`型の引数を2つ受け取ることを示します。
-   `: number`（引数リストの後）：この関数は、`number`型の値を返すことを示します。

このように型を定義することで、`add`関数を間違った引数で呼び出そうとすると、TypeScriptコンパイラが即座にエラーを教えてくれます。

--- 

### ⚙️ 戻り値がない関数：`void`型

関数が何も値を返さない場合（`return`文がない、または`return;`で値を返さない）、その戻り値の型は`void`と注釈します。`void`は「空っぽ」を意味します。

```typescript
function sayHello(name: string): void {
  console.log(`Hello, ${name}!`);
  // この関数は何もreturnしない
}

sayHello("TypeScript"); // OK

// エラー: sayHelloは値を返さない(void型)ので、変数に代入しても意味がない
// (厳密にはundefinedが代入されるが、意図しない使い方としてTypeScriptが警告してくれる)
const message = sayHello("World");
```

**戻り値の型推論:**
関数の戻り値の型も、TypeScriptがある程度推論してくれます。しかし、**関数の戻り値の型は、推論に頼らず明示的に注釈する**ことが、一般的に良い習慣とされています。これにより、関数の意図が明確になり、将来の変更（リファクタリング）にも強くなります。

--- 

### ⚙️ アロー関数の型定義

アロー関数の場合も、型定義のルールは基本的に同じです。

```typescript
const multiply = (a: number, b: number): number => {
  return a * b;
};

// 省略記法の場合
const subtract = (a: number, b: number): number => a - b;
```

--- 

### ⚙️ オプショナルな引数とデフォルト値

JavaScriptと同様に、TypeScriptでも引数を省略可能にしたり、デフォルト値を与えたりできます。

#### オプショナルな引数 `?`

引数名の後ろに`?`を付けると、その引数が省略可能であることを示します。省略された場合、その引数の値は`undefined`になります。

```typescript
function buildName(firstName: string, lastName?: string): string {
  if (lastName) {
    return `${firstName} ${lastName}`;
  } else {
    return firstName;
  }
}

let result1 = buildName("Taro"); // OK: "Taro"
let result2 = buildName("Taro", "Yamada"); // OK: "Taro Yamada"
```

-   `lastName?: string` は、`lastName`が`string`型または`undefined`型であることを意味します（`string | undefined`の糖衣構文）。

#### デフォルト値

引数にデフォルト値を設定すると、引数が省略された場合にその値が使われます。デフォルト値が設定されている引数は、自動的にオプショナルになります。

```typescript
function greet(name: string, message: string = "Hello"): string {
  return `${message}, ${name}!`;
}

greet("Alice"); // "Hello, Alice!"
greet("Bob", "Hi"); // "Hi, Bob!"
```

--- 

✨ **まとめ**

-   関数の型定義は、**引数**と**戻り値**に対して行う。
-   これにより、関数の「契約」が明確になり、安全な呼び出しが保証される。
-   何も値を返さない関数の戻り値の型は`void`と注釈する。
-   引数名の後に`?`を付けると、その引数は**オプショナル**になる。
-   引数に**デフォルト値**を設定すると、型推論が効き、かつ自動的にオプショナルになる。

📝 **学習のポイント**

-   [ ] ユーザーオブジェクト（`{ id: number, name: string }`）を受け取り、`"ID: 1, Name: Yamada"`のような文字列を返す関数`formatUser`を定義してください。
-   [ ] なぜ関数の戻り値の型は、型推論に頼らず明示的に書くことが推奨されるのでしょうか？
-   [ ] 引数として数値の配列(`number[]`)を受け取り、その合計値を返す関数`sumArray`を定義してください。もし配列が空の場合は、0を返すようにします。
