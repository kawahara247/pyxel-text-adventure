import pyxel

MG_TIMER_MAX = 600  # 10秒 × 60fps
MG_PLAY_X_MIN = 9
MG_PLAY_X_MAX = 150
MG_PLAY_Y_MIN = 6
MG_PLAY_Y_MAX = 89
MG_PLAYER_SIZE = 4
MG_MIN_DIST = 32

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
        "minigame": "fragments",
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
        self.next_after_minigame = 0
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """ゲームの状態を更新する関数"""

        # タイトル状態のとき、ENTER を押したらゲーム開始に切り替える
        if self.state == "title":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.state = "game"
            return

        if self.state == "minigame_fragments":
            self.update_minigame_fragments()
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
                    self.advance_scene(scene)
        else:
            if pyxel.frame_count % 3 == 0:
                self.char_count += 1
                if self.char_count > total_char:
                    self.char_count = total_char

    def advance_scene(self, scene) -> None:
        """シーンを次に進める"""
        cursor = self.cursor
        self._reset_scene_state()
        if "choices" in scene:
            next_scene = scene["next"][cursor]
            if "minigame" in scene and cursor == 0:
                self.next_after_minigame = next_scene
                if scene["minigame"] == "fragments":
                    self.start_minigame_fragments()
            else:
                self.scene = next_scene
        elif "next" in scene:
            self.scene = scene["next"]
        elif "end" in scene:
            self.state = "title"
            self.scene = 0

    def draw(self) -> None:
        """画面を描画する関数"""
        if self.state == "title":
            self.draw_title()
        elif self.state == "minigame_fragments":
            self.draw_minigame_fragments()
        else:
            self.draw_game()

    def draw_title(self) -> None:
        """タイトル画面の描画"""
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
            self.draw_centered_text("PRESS ENTER KEY", 82, 10)

    def draw_game(self) -> None:
        """ゲーム画面の描画"""
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
        all_shown = self.is_all_text_shown()

        # 選択肢（最後のページのみ）
        if "choices" in scene and is_last_page and all_shown:
            prefix_w = self.font.text_width("> ")
            choice_lines = [self.wrap_text(c, 146 - prefix_w) for c in scene["choices"]]
            total_h = sum(len(lines) * 8 for lines in choice_lines) + (len(scene["choices"]) - 1) * 2
            num_display_lines = sum(len(wlines) for _, wlines in current_page_entries)
            text_bottom = 50 + (num_display_lines - 1) * 10 + 7
            choice_y = max(text_bottom + 2, 115 - total_h)
            for i, (choice, wrapped) in enumerate(zip(scene["choices"], choice_lines)):
                col = 10 if i == self.cursor else 7
                prefix = "> " if i == self.cursor else "  "
                for j, wline in enumerate(wrapped):
                    indent = prefix if j == 0 else " " * len(prefix)
                    pyxel.text(8, choice_y, indent + wline, col, self.font)
                    choice_y += 8
                if i < len(scene["choices"]) - 1:
                    choice_y += 2

        # エンディング表示（最後のページのみ）
        if "end" in scene and is_last_page and all_shown:
            pyxel.text(8, 94, scene["end"], 9, self.font)
            pyxel.text(8, 106, "ENTERで最初へ戻る", 6, self.font)

        # ページ続行インジケーター
        if not is_last_page and all_shown:
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
                y += 10
                r -= show
            remaining -= chars_in_line
            if remaining <= 0:
                break

    def get_scene_pages(self, scene):
        """シーンのテキストを最大4行ずつページに分割する"""
        MAX_LINES = 4
        pages = []
        current_page = []
        current_count = 0
        for line in scene["text"]:
            wlines = self.wrap_text(line, 146)
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

    def draw_centered_text(self, text, y, col):
        x = (160 - self.font.text_width(text)) // 2
        pyxel.text(x, y, text, col, self.font)

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

    def start_minigame_fragments(self):
        FRAGMENT_TEXTS = ["自分を", "救って", "くれた", "ものに", "進みたい"]

        self.mg_player_x = 76
        self.mg_player_y = 52
        self.mg_timer = MG_TIMER_MAX
        self.mg_result = None
        self.mg_phase = "intro"
        self.mg_collected_order = []
        self.mg_clear_text = None
        self.state = "minigame_fragments"

        placed = []
        self.mg_fragments = []
        for text in FRAGMENT_TEXTS:
            w = self.font.text_width(text)
            placed_this = False
            for _ in range(100):
                x = pyxel.rndi(MG_PLAY_X_MIN, max(MG_PLAY_X_MIN, MG_PLAY_X_MAX - w))
                y = pyxel.rndi(MG_PLAY_Y_MIN, MG_PLAY_Y_MAX)
                ok = True
                for fx, fy in placed:
                    if abs(x - fx) < MG_MIN_DIST and abs(y - fy) < MG_MIN_DIST:
                        ok = False
                        break
                if ok:
                    placed.append((x, y))
                    self.mg_fragments.append({"x": x, "y": y, "text": text, "w": w, "collected": False})
                    placed_this = True
                    break
            if not placed_this:
                x = pyxel.rndi(MG_PLAY_X_MIN, max(MG_PLAY_X_MIN, MG_PLAY_X_MAX - w))
                y = pyxel.rndi(MG_PLAY_Y_MIN, MG_PLAY_Y_MAX)
                self.mg_fragments.append({"x": x, "y": y, "text": text, "w": w, "collected": False})

    def update_minigame_fragments(self):
        if self.mg_phase == "intro":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.mg_phase = "playing"
            return
        if self.mg_result is None:
            if pyxel.btn(pyxel.KEY_LEFT):
                self.mg_player_x = max(MG_PLAY_X_MIN, self.mg_player_x - 2)
            if pyxel.btn(pyxel.KEY_RIGHT):
                self.mg_player_x = min(MG_PLAY_X_MAX - MG_PLAYER_SIZE + 1, self.mg_player_x + 2)
            if pyxel.btn(pyxel.KEY_UP):
                self.mg_player_y = max(MG_PLAY_Y_MIN, self.mg_player_y - 2)
            if pyxel.btn(pyxel.KEY_DOWN):
                self.mg_player_y = min(MG_PLAY_Y_MAX + MG_PLAYER_SIZE + 1, self.mg_player_y + 2)
            self.mg_timer -= 1
            px, py = self.mg_player_x, self.mg_player_y
            for frag in self.mg_fragments:
                if frag["collected"]:
                    continue
                if (px < frag["x"] + frag["w"] and px + MG_PLAYER_SIZE > frag["x"] and
                        py < frag["y"] + 8 and py + MG_PLAYER_SIZE > frag["y"]):
                    frag["collected"] = True
                    self.mg_collected_order.append(frag["text"])
                    pyxel.play(0, 0)
            if len(self.mg_collected_order) >= len(self.mg_fragments):
                self.mg_result = "clear"
                self.mg_clear_text = "".join(frag["text"] for frag in self.mg_fragments)
            elif self.mg_timer <= 0:
                self.mg_result = "fail"
        elif self.mg_result == "clear":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.advance_to_next_after_minigame()
        elif self.mg_result == "fail":
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.start_minigame_fragments()

    def advance_to_next_after_minigame(self):
        self.scene = self.next_after_minigame
        self.state = "game"
        self._reset_scene_state()

    def _reset_scene_state(self):
        self.cursor = 0
        self.char_count = 0
        self.page = 0
        pyxel.play(0, 0)

    def draw_minigame_fragments(self):
        pyxel.cls(1)

        if self.mg_phase == "intro":
            self._draw_minigame_fragments_intro()
            return

        # タイマーバー (y=0〜3)
        if self.mg_result is None:
            bar_w = int(160 * self.mg_timer / MG_TIMER_MAX)
            pyxel.rect(0, 0, bar_w, 4, 9)
        elif self.mg_result == "clear":
            pyxel.rect(0, 0, 160, 4, 10)

        # 残り秒数（右上）
        if self.mg_result is None:
            secs = (self.mg_timer + 59) // 60
            secs_str = str(secs)
            sw = self.font.text_width(secs_str)
            pyxel.text(158 - sw, 0, secs_str, 9, self.font)

        # プレイフィールド境界
        pyxel.rectb(8, 5, 144, 94, 5)

        # 欠片（未収集は点滅）
        for frag in self.mg_fragments:
            if not frag["collected"]:
                if pyxel.frame_count % 30 < 22:
                    pyxel.text(frag["x"], frag["y"], frag["text"], 7, self.font)

        if self.mg_result is None:
            pyxel.rect(self.mg_player_x, self.mg_player_y, MG_PLAYER_SIZE, MG_PLAYER_SIZE, 10)

        # オーバーレイメッセージ
        if self.mg_result == "clear":
            self.draw_centered_text("願いが灯った", 62, 9)
            if pyxel.frame_count % 60 < 30:
                self.draw_centered_text("ENTERで次へ", 76, 7)
        elif self.mg_result == "fail":
            self.draw_centered_text("時間切れ", 62, 8)
            if pyxel.frame_count % 60 < 30:
                self.draw_centered_text("ENTERでリトライ", 76, 7)

        # 下部バー (y=100〜119)
        pyxel.rect(0, 100, 160, 20, 0)
        pyxel.line(0, 100, 159, 100, 5)

        if self.mg_result == "clear":
            self.draw_centered_text(self.mg_clear_text, 107, 10)
        else:
            x = 10
            for text in self.mg_collected_order:
                pyxel.text(x, 107, text, 7, self.font)
                x += self.font.text_width(text) + 2

    def _draw_minigame_fragments_intro(self):
        lines = [
            ("ことば集め", 10),
            ("---", 5),
            ("画面に散った欠片を集め、", 7),
            ("一本の文章として灯せ。", 7),
            ("---", 5),
            ("十字キー：移動", 6),
            (f"制限時間：{MG_TIMER_MAX // 60}秒", 6),
        ]
        total_h = len(lines) * 10
        y = (120 - total_h) // 2 - 4
        for text, col in lines:
            self.draw_centered_text(text, y, col)
            y += 10
        if pyxel.frame_count % 60 < 30:
            self.draw_centered_text("ENTERでスタート", y + 4, 9)


Game()
