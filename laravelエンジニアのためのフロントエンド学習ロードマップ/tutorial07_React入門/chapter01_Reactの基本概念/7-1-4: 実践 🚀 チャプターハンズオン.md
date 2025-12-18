# Tutorial 7: React基礎

## Chapter 1: Reactの基本概念

### Chapter 1 ハンズオン: 初めてのReactコンポーネント作成

🎯 **このハンズオンで達成すること**

-   Reactの開発環境（Vite）をゼロからセットアップできるようになる。
-   関数コンポーネントを自分で作成し、`export`/`import`できるようになる。
-   JSXの基本ルール（単一ルート要素、閉じタグ、`className`）を実践で使えるようになる。
-   作成したコンポーネントを別のコンポーネントで再利用し、コンポーネント指向のメリットを体感する。

--- 

🖼️ **完成イメージ**

`App`というメインコンポーネントの中に、自作の`WelcomeMessage`コンポーネントと`UserProfile`コンポーネントを配置し、簡単な自己紹介ページを作成します。`UserProfile`コンポーネントは複数回再利用します。

![完成イメージ](https://placehold.jp/800x400.png?text=ようこそ、Reactの世界へ！%0A%0A---%0A%0A名前:%20山田%20太郎%0A趣味:%20プログラミング%0A---%0A%0A名前:%20鈴木%20花子%0A趣味:%20読書)

--- 

### 🧠 先輩エンジニアの思考プロセス

「Reactで簡単な自己紹介ページ作ってみて」と言われたら、こう考える。

1.  **環境構築:** まずは開発環境がないと始まらない。今は`Vite`を使うのが一番手軽で高速だ。`npm create vite@latest`コマンド一発で、React + TypeScriptのプロジェクト雛形を作ろう。
2.  **コンポーネントの設計:** ページ全体を見て、どんな「部品」に分割できるか考える。
    -   一番上の「ようこそ、Reactの世界へ！」という見出し。これは`WelcomeMessage`コンポーネントにしよう。
    -   「名前」と「趣味」のセット。これは繰り返し使われそうだから、`UserProfile`コンポーネントとして独立させよう。
    -   そして、これら全体をまとめる親が`App`コンポーネントだな。
3.  **`App`コンポーネントの掃除:** Viteが生成した`App.tsx`にはサンプルコードがたくさん入っている。まずはこれを全部消して、まっさらな状態から始めるのが分かりやすい。
4.  **`WelcomeMessage`コンポーネントの実装:** `components`ディレクトリを作って、その中に`WelcomeMessage.tsx`を作成。`h1`タグを返すだけのシンプルなコンポーネントだ。`export default`を忘れずに。
5.  **`UserProfile`コンポーネントの実装:** 同じく`components/UserProfile.tsx`を作成。`div`で囲んで、中に`p`タグで名前と趣味を表示する。これも`export default`する。
6.  **`App`コンポーネントで組み立て:** `App.tsx`に戻って、作成した2つのコンポーネントを`import`する。そして、JSXの中で`<WelcomeMessage />`と`<UserProfile />`を呼び出す。`UserProfile`は2回呼び出して、再利用性を確認しよう。
7.  **スタイリング:** 最後に、見た目を少し整える。`index.css`に簡単なスタイルを追加し、`UserProfile`コンポーネントのルート`div`に`className`で適用する。これで完成だ。

--- 

### 🏃 実践: Step by Stepで自己紹介ページを作ろう

#### Step 1: ViteによるReactプロジェクトのセットアップ

ターミナルを開き、以下のコマンドを実行します。

```bash
# ターミナル
npm create vite@latest my-react-app -- --template react-ts
```

-   `my-react-app`という名前のディレクトリが作成されます。
-   `--template react-ts`で、React + TypeScriptのテンプレートを指定しています。

プロジェクトディレクトリに移動し、必要なパッケージをインストールして、開発サーバーを起動します。

```bash
# ターミナル
cd my-react-app
npm install
npm run dev
```

ブラウザで `http://localhost:5173` のようなアドレスが開かれ、ViteとReactのロゴが表示されれば成功です。

#### Step 2: プロジェクトの初期化（お掃除）

`src`ディレクトリの中を整理します。

1.  `src/App.tsx`の中身をすべて削除し、以下のシンプルなコンポーネントに書き換えます。
    ```tsx
    // src/App.tsx
    function App() {
      return (
        <div>
          {/* ここにコンポーネントを配置していく */}
        </div>
      );
    }
    export default App;
    ```
2.  `src/App.css`と`src/assets`ディレクトリは不要なので削除します。
3.  `src/main.tsx`で`App.css`をインポートしている行を削除します。

#### Step 3: `WelcomeMessage`コンポーネントの作成

`src`ディレクトリ内に`components`という新しいディレクトリを作成します。その中に`WelcomeMessage.tsx`ファイルを作成します。

```tsx
// src/components/WelcomeMessage.tsx

function WelcomeMessage() {
  return <h1>ようこそ、Reactの世界へ！</h1>;
}

export default WelcomeMessage;
```

#### Step 4: `UserProfile`コンポーネントの作成

同様に、`src/components`ディレクトリに`UserProfile.tsx`ファイルを作成します。

```tsx
// src/components/UserProfile.tsx

function UserProfile() {
  return (
    // ルール1: 単一のルート要素で囲む
    // ルール3: classではなくclassNameを使う
    <div className="user-profile">
      <p>名前: 山田 太郎</p>
      <p>趣味: プログラミング</p>
      {/* ルール2: 閉じタグを忘れない */}
      <hr /> 
    </div>
  );
}

export default UserProfile;
```

#### Step 5: `App`コンポーネントで子コンポーネントを呼び出す

`src/App.tsx`を編集し、作成した2つのコンポーネントをインポートして配置します。

```tsx
// src/App.tsx

// 作成したコンポーネントをインポート
import WelcomeMessage from "./components/WelcomeMessage";
import UserProfile from "./components/UserProfile";

function App() {
  return (
    <>
      <WelcomeMessage />
      
      {/* UserProfileコンポーネントを2回再利用 */}
      <UserProfile />
      <UserProfile />
    </>
  );
}

export default App;
```

この時点でブラウザを確認すると、コンポーネントが表示されているはずです。

#### Step 6: 簡単なスタイリング

`src/index.css`を開き、以下のスタイルを追加します。（既存のスタイルは消してもそのままでもOKです）

```css
/* src/index.css */
.user-profile {
  border: 1px solid #ccc;
  padding: 16px;
  margin-top: 16px;
  border-radius: 8px;
}
```

`UserProfile.tsx`で`className="user-profile"`と指定した`div`に、このスタイルが適用され、カードのような見た目になります。

--- 

✨ **まとめ**

-   `npm create vite@latest`コマンドで、最新のReact開発環境を瞬時に構築できる。
-   UIを意味のある単位でコンポーネントに分割し、それぞれ別のファイルとして管理する（例: `WelcomeMessage.tsx`, `UserProfile.tsx`）。
-   親コンポーネント (`App.tsx`) で子コンポーネントを`import`し、JSXタグとして`<UserProfile />`のように呼び出すことで、UIを組み立てていく。
-   同じコンポーネントを複数回呼び出すことで、コードの再利用がいかに簡単で強力であるかを体験した。

📝 **学習のポイント**

-   [ ] `UserProfile`コンポーネントの`hr`タグを`<hr>`のように閉じ忘れると、どのようなエラーが表示されますか？
-   [ ] `App.tsx`で`UserProfile`コンポーネントをもう一つ追加してみてください。変更が即座にブラウザに反映されることを確認しましょう。
-   [ ] 今回は`UserProfile`の中身が固定でした。これを、呼び出し元から「名前」と「趣味」を渡せるようにするには、どうすればよいでしょうか？（次のChapterで学ぶ`props`の予習です）
