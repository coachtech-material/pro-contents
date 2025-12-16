# Tutorial 5: JavaScript応用と非同期処理

## Chapter 2: 配列の高度な操作

### Section 4: find と findIndex メソッド

🎯 **このセクションで学ぶこと**

-   `find`メソッドを使い、配列から条件に最初に一致した**要素そのもの**を取得できるようになる。
-   `findIndex`メソッドを使い、配列から条件に最初に一致した要素の**インデックス番号**を取得できるようになる。
-   `filter`と`find`の違いを理解し、適切に使い分けられるようになる。

--- 

### イントロダクション：配列から「探し物」をする

`filter`は条件に合う要素を**すべて**集めて新しい配列を返しました。しかし、実務では「条件に合う最初の1個だけが欲しい」という場面がよくあります。例えば、

-   IDを指定して、特定のユーザーオブジェクトを1つだけ見つけたい。
-   商品コードを元に、商品マスタの配列から該当する商品データを1つだけ引き当てたい。

このような「探し物」に特化したメソッドが`find`です。`find`は、条件に一致した**最初の要素そのもの**を返します。配列ではなく、単一の要素（または`undefined`）を返すのが`filter`との大きな違いです。

また、その要素が配列の何番目にあるか、という**インデックス番号**が知りたい場合には`findIndex`を使います。

--- 

### ⚙️ `find`メソッド：最初に見つかった要素を返す

`find`も`filter`と同様に、`true`または`false`を返すコールバック関数を引数に取ります。

`find`は配列の先頭から順番に要素をチェックし、コールバック関数が**最初に`true`を返した時点**で、その**要素**を返し、処理を終了します。

もし、最後までループしても`true`になる要素が一つも見つからなかった場合は、`undefined`を返します。

**基本構文:**
```javascript
const foundElement = array.find(コールバック関数);
```

**例：IDが3のユーザーを探す**
```javascript
const users = [
  { id: 1, name: "山田" },
  { id: 2, name: "鈴木" },
  { id: 3, name: "田中" },
  { id: 4, name: "佐藤" },
];

const targetUser = users.find(user => user.id === 3);

console.log(targetUser); // { id: 3, name: "田中" }

const nonExistentUser = users.find(user => user.id === 99);

console.log(nonExistentUser); // undefined
```

### 🤔 `filter` vs `find`：配列か、要素か

`filter`と`find`は似ていますが、戻り値が全く異なります。

-   **`filter`**: 条件に合う要素を**すべて**含む**新しい配列**を返す。見つからなければ**空の配列 `[]`** を返す。
-   **`find`**: 条件に合う**最初の1つの要素**を返す。見つからなければ **`undefined`** を返す。

```javascript
const numbers = [10, 20, 30, 40, 50];

// 25より大きいものを探す

const filtered = numbers.filter(n => n > 25);
console.log(filtered); // [30, 40, 50] (配列)

const found = numbers.find(n => n > 25);
console.log(found);    // 30 (要素そのもの)
```

**使い分け:**
-   条件に合うものが複数存在する可能性があり、その**すべてが必要**な場合は`filter`。
-   IDやユニークなキーで検索するなど、結果が**高々1つ**しかなく、その**要素自体が欲しい**場合は`find`。

### ⚙️ `findIndex`メソッド：最初に見つかった要素のインデックスを返す

`findIndex`の使い方は`find`と全く同じですが、戻り値が要素そのものではなく、その要素が配列の何番目にあったかを示す**インデックス番号**になります。

もし、最後までループしても見つからなかった場合は、**-1** を返します。`undefined`ではない点に注意してください。

**基本構文:**
```javascript
const foundIndex = array.findIndex(コールバック関数);
```

**例：名前が「田中」のユーザーのインデックスを探す**
```javascript
const users = [
  { id: 1, name: "山田" },
  { id: 2, name: "鈴木" },
  { id: 3, name: "田中" },
  { id: 4, name: "佐藤" },
];

const tanakaIndex = users.findIndex(user => user.name === "田中");

console.log(tanakaIndex); // 2

const nonExistentIndex = users.findIndex(user => user.name === "加藤");

console.log(nonExistentIndex); // -1
```

`findIndex`は、特定の要素を配列から削除したり、置き換えたりする際に、その位置を特定するために非常によく使われます。

--- 

✨ **まとめ**

-   `find`は、配列から条件に**最初に**一致した**要素そのもの**を返す。見つからなければ`undefined`を返す。
-   `findIndex`は、配列から条件に**最初に**一致した要素の**インデックス番号**を返す。見つからなければ`-1`を返す。
-   条件に合う要素が複数あっても、`find`と`findIndex`は最初の1つを見つけた時点で処理を終了する。
-   「条件に合うものをすべてリストアップしたい」なら`filter`、「特定の1つを見つけたい」なら`find`、と使い分ける。

📝 **学習のポイント**

-   [ ] 前述の`users`配列から、`name`が「鈴木」であるユーザーオブジェクトを`find`メソッドを使って見つけてください。
-   [ ] `filter`と`find`の主な違いを、戻り値に着目して説明してください。条件に合う要素が見つからなかった場合、それぞれ何を返しますか？
-   [ ] `const products = ["机", "椅子", "本棚", "ベッド"];` という配列があります。`findIndex`を使って、「本棚」が配列の何番目にあるか（インデックス）を調べてください。また、「ソファ」を探した場合は何が返ってくるでしょうか？
