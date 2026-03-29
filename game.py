import pyxel


# シーン定義
# choices がある → 選択肢シーン
# next がある    → 直線進行シーン
# end がある    → エンディングシーン
SCENES = {
    0: {
        "name": "管理人",
        "text": [
            "......ようこそ。",
            "私はここの管理人です。",
            "唐突ですがこれからあなたにいくつか質問をします。",
            "あなたは選択肢の中から直感で答えてください。",
            "これはただの「ゲーム」なので、自分の選びたいものを素直に選択しても良いし、逆らって真逆の選択をしても良いです。",
            "ただ——あなたの心に従ってください。",
        ],
        "next": 1,
    },
    1: {
        "name": "管理人",
        "text": [
            "ステージ1：宣言",
            "場面描写",
            "静かな通路の先に、固く閉じた扉がある。",
            "あなたは昔、その扉に向かって、",
            "『自分を救ってくれたものに関わる道へ進みたい』とまっすぐ言葉を投げた。",
            "管理人の言葉",
            "「あの時、あなたが口にした願いは何だったのでしょう？」",
        ],
        "choices": ["飾りでない本音だった", "通るために並べた、それらしい言葉だった"],
        "next": [2, 6],
    },
    2: {
        "name": "管理人",
        "text": [
            "ステージ2：避難所",
            "場面描写",
            "色の抜けた部屋。窓の外も、机の上も、気持ちの置き場がない。",
            "けれど、画面の向こうに入ると、そこだけは呼吸のしかたを思い出せた。",
            "管理人の言葉",
            "あの世界は、あなたにとって何でしたか？",
        ],
        "choices": ["息を継ぐための避難所だった", "見たくないものから、ただ逃げただけだった"],
        "next": [3, 6],
    },
    3: {
        "name": "管理人",
        "text": [
            "ステージ3：烙印",
            "場面描写",
            "空から札が降ってくる。",
            "『無駄』『悪い影響』『子どもっぽい』。",
            "その言葉の下でも、手の中の熱だけは確かに残っている。",
            "管理人の言葉",
            "あなたは、どちらを信じますか？",
        ],
        "choices": ["救われた自分の実感", "外から貼られたラベル"],
        "next": [4, 6],
    },
    4: {
        "name": "管理人",
        "text": [
            "お疲れ様でした。",
            "——実は、私は管理人ではなく、",
            "ずっと奥に残っていた",
            "あなた自身の本心です。",
            "ここはずっと、あなたの心の中だったのです。",
            "届かなかった願いも、避難していた時間も、",
            "外の声に傷ついたことも、無駄ではないと思います。",
            "救われた事実は、誰にも取り上げられません。",
            "ゲームが好きで、良かったんです。",
        ],
        "next": 5,
    },
    5: {
        "name": None,
        "text": [
            "あの頃のあなたへ。",
            "君は間違っていない。",
            "ゲームは君を救い続けた。",
        ],
        "end": "THANKS",
    },
    6: {
        "name": None,
        "text": [
            "......そうですか。",
            "外の声が大きいとき、",
            "心の声はすぐ遠のきます。",
            "また聞こえたら来てください。",
            "演出：管理人の声が遠くなっていく。画面が暗くなる。",
            "「心の声を封じました。管理人は、もう話しかけてきません。」",
        ],
        "end": "BAD END",
    },
}


class Game:
    def __init__(self):
        pyxel.init(160, 120, title="Thanks")
        pyxel.sounds[0].set(
            notes="C3E3G3",   # 音階（ドミソ）
            tones="PPP",       # 音色（P=パルス, S=矩形波, T=三角波, N=ノイズ）
            volumes="432",     # 音量（0-7）
            effects="NNF",     # エフェクト（N=なし, F=フェードアウト）
            speed=10          # 再生速度（小さいほど速い）
        )

        self.font = pyxel.Font("misaki_gothic.bdf")
        self.state = "title"
        self.scene = 0
        self.cursor = 0
        self.char_count = 0
        self.page = 0
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """ゲームの状態を更新する関数"""

        # タイトル状態のとき、ENTER を押したらゲーム開始に切り替える
        if self.state == "title":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.state = "game"
            return

        scene = SCENES[self.scene]
        total_char = self.total_char()

        # 選択肢の操作
        if "choices" in scene:
            if pyxel.btnp(pyxel.KEY_UP):
                self.cursor = 0
            if pyxel.btnp(pyxel.KEY_DOWN):
                self.cursor = 1
    
        # テキストのタイプライター演出
        if pyxel.btnp(pyxel.KEY_RETURN):
            if self.char_count < total_char:
                # テキスト一気に表示
                self.char_count = total_char
            else:
                pages = self.get_scene_pages(scene)
                if self.page < len(pages) - 1:
                    # 次のページへ
                    self.page += 1
                    self.char_count = 0
                    pyxel.play(0, 0)
                else:
                    if "choices" in scene:
                        # 次のシーンに移動
                        self.scene = scene["next"][self.cursor]

                    elif "next" in scene:
                        # 次のシーンに移動
                        self.scene = scene["next"]

                    elif "end" in scene:
                        # タイトルに戻る
                        self.state = "title"
                        self.scene = 0

                    pyxel.play(0, 0)
                    self.cursor = 0
                    self.char_count = 0
                    self.page = 0
        else:
            if pyxel.frame_count % 3 == 0:
                self.char_count += 1
                if self.char_count > total_char:
                    self.char_count = total_char

    def draw(self) -> None:
        """画面を描画する関数"""

        # タイトル画面の描画
        if self.state == "title":
            pyxel.cls(0)

            # 多重枠（高さを60pxに拡大）
            pyxel.rectb(2,  4, 156, 60, 1)
            pyxel.rectb(3,  5, 154, 58, 12)
            pyxel.rectb(4,  6, 152, 56, 13)
            pyxel.rectb(5,  7, 150, 54, 7)
            pyxel.rectb(6,  8, 148, 52, 11)
            pyxel.rectb(7,  9, 146, 50, 3)

            # タイトル文字（4倍拡大 + グラデーション + ドロップシャドウ）
            title = "THANKS"
            tw = self.font.text_width(title)
            scale = 4
            pyxel.image(1).cls(0)
            pyxel.image(1).text(0, 0, title, 1, self.font)
            sx = (160 - tw * scale) // 2
            sy = 10 + (48 - 8 * scale) // 2 + 1  # 枠内（y=10〜57）の縦中央（1px下げて視覚調整）
            # 行ごとのグラデーション色（上: 明るいオレンジ → 下: 暗いオレンジ）
            row_colors = [10, 10, 9, 9, 9, 9, 8, 8]
            for row in range(8):
                for col in range(tw):
                    if pyxel.image(1).pget(col, row) != 0:
                        # ドロップシャドウ（1px 右下にずれた黒）
                        pyxel.rect(sx + col * scale + 2, sy + row * scale + 2, scale, scale, 1)
                        # 本体（グラデーション色）
                        pyxel.rect(sx + col * scale, sy + row * scale, scale, scale, row_colors[row])

            # 点滅する PRESS ENTER KEY
            if pyxel.frame_count % 60 < 30:
                enter_text = "PRESS ENTER KEY"
                ex = (160 - self.font.text_width(enter_text)) // 2
                pyxel.text(ex, 82, enter_text, 10, self.font)

            return
        
        pyxel.cls(1)
        scene = SCENES[self.scene]

        # ダイアログボックス
        pyxel.rect(0, 40, 160, 80, 0)
        pyxel.rectb(3, 42, 154, 75, 7)

        # 名前タグ（名前がある場合のみ）
        name = scene["name"]
        if name:
            pyxel.rect(5, 34, 44, 13, 7)
            pyxel.text(8, 36, name, 0, self.font)

        pages = self.get_scene_pages(scene)
        is_last_page = (self.page == len(pages) - 1)
        current_page_entries = pages[self.page] if self.page < len(pages) else []

        # 選択肢（最後のページのみ）
        if "choices" in scene and is_last_page:
            if self.is_all_text_shown():
                prefix_w = self.font.text_width("> ")
                choice_y = 94
                for i, choice in enumerate(scene["choices"]):
                    col = 10 if i == self.cursor else 7
                    prefix = "> " if i == self.cursor else "  "
                    wrapped = self.wrap_text(choice, 146 - prefix_w)
                    for j, wline in enumerate(wrapped):
                        indent = prefix if j == 0 else " " * len(prefix)
                        pyxel.text(8, choice_y, indent + wline, col, self.font)
                        choice_y += 10
                    choice_y += 2

        # エンディング表示（最後のページのみ）
        if "end" in scene and is_last_page:
            if self.is_all_text_shown():
                pyxel.text(8, 94, scene["end"], 9, self.font)
                pyxel.text(8, 106, "ENTERで最初へ戻る", 6, self.font)

        # ページ続行インジケーター
        if not is_last_page and self.is_all_text_shown():
            pyxel.text(148, 108, "v", 7, self.font)

        # セリフ
        remaining = self.char_count
        y = 50
        for line, wlines in current_page_entries:
            chars_in_line = min(remaining, len(line))
            r = chars_in_line
            for wline in wlines:
                if r <= 0:
                    break
                show = min(r, len(wline))
                pyxel.text(8, y, wline[:show], 7, self.font)
                y += 12
                r -= show
            remaining -= chars_in_line
            if remaining <= 0:
                break

    def get_scene_pages(self, scene):
        """シーンのテキストを最大4行ずつページに分割する"""
        MAX_LINES = 4
        wrapped_by_line = [self.wrap_text(line, 146) for line in scene["text"]]
        pages = []
        current_page = []
        current_count = 0
        for line, wlines in zip(scene["text"], wrapped_by_line):
            if current_count + len(wlines) > MAX_LINES and current_page:
                pages.append(current_page)
                current_page = [(line, wlines)]
                current_count = len(wlines)
            else:
                current_page.append((line, wlines))
                current_count += len(wlines)
        if current_page:
            pages.append(current_page)
        return pages

    def wrap_text(self, text, max_width):
        """テキストを最大幅で折り返す"""
        lines = []
        current = ""
        for char in text:
            if self.font.text_width(current + char) > max_width:
                lines.append(current)
                current = char
            else:
                current += char
        if current:
            lines.append(current)
        return lines

    def is_all_text_shown(self) -> bool:
        """現在のシーンの全テキストが表示されているか"""
        return self.char_count == self.total_char()

    def total_char(self) -> int:
        """現在のページのテキスト文字数を返す"""
        scene = SCENES[self.scene]
        pages = self.get_scene_pages(scene)
        if self.page >= len(pages):
            return 0
        return sum(len(line) for line, _ in pages[self.page])
        
Game()
