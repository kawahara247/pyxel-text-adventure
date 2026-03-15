import pyxel

# シーン定義
# choices がある → 選択肢シーン
# end がある    → エンディングシーン
SCENES = {
    0: {
        "name": "老人",
        "text": ["世界を救ってくれ。", "魔王を倒せるのはあなただけだ。"],
        "choices": ["わかった", "嫌だ"],
        "next": [1, 2],
    },
    1: {
        "name": "魔王",
        "text": ["よく来たな勇者よ。", "覚悟はできているか？"],
        "choices": ["戦う", "逃げる"],
        "next": [3, 4],
    },
    2: {
        "name": None,
        "text": ["老人は悲しそうに", "うつむいた。"],
        "end": "THE END",
    },
    3: {
        "name": None,
        "text": ["勇者は魔王を倒した。", "世界が救われた。"],
        "end": "THE END",
    },
    4: {
        "name": None,
        "text": ["勇者は逃げ出した。", ""],
        "end": "GAME OVER",
    },
}


class Game:
    def __init__(self):
        pyxel.init(160, 120, title="勇者の選択")
        pyxel.sounds[0].set(
            notes="C3E3G3",   # 音階（ドミソ）
            tones="PPP",       # 音色（P=パルス, S=矩形波, T=三角波, N=ノイズ）
            volumes="432",     # 音量（0-7）
            effects="NNF",     # エフェクト（N=なし, F=フェードアウト）
            speed=10          # 再生速度（小さいほど速い）
        )

        self.font = pyxel.Font("misaki_gothic.bdf")
        self.scene = 0
        self.cursor = 0
        self.char_count = 0
        pyxel.run(self.update, self.draw)

    def update(self) -> None:
        """ゲームの状態を更新する関数"""
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
                if "choices" in scene:
                    # 次のシーンに移動
                    self.scene = scene["next"][self.cursor]

                elif "end" in scene:
                    # タイトルに戻る
                    self.scene = 0

                pyxel.play(0, 0)
                self.cursor = 0
                self.char_count = 0
        else:
            if pyxel.frame_count % 3 == 0:
                self.char_count += 1
                if self.char_count > total_char:
                    self.char_count = total_char

    def draw(self) -> None:
        """画面を描画する関数"""
        pyxel.cls(1)
        scene = SCENES[self.scene]
        total_char = self.total_char()

        # ダイアログボックス（下半分）
        pyxel.rect(0, 55, 160, 65, 0)
        pyxel.rectb(3, 57, 154, 61, 7)

        # 名前タグ（名前がある場合のみ）
        name = scene["name"]
        if name:
            pyxel.rect(5, 50, 50, 13, 7)
            pyxel.text(8, 52, name, 0, self.font)

        # 選択肢
        if "choices" in scene:
            if self.is_all_text_shown():
                for i, choice in enumerate(scene["choices"]):
                    col = 10 if i == self.cursor else 7
                    prefix = "> " if i == self.cursor else "  "
                    pyxel.text(15, 93 + i * 13, prefix + choice, col, self.font)

        # エンディング表示
        if "end" in scene:
            if self.is_all_text_shown():
                pyxel.text(8, 93, scene["end"], 9, self.font)
                pyxel.text(8, 106, "ありがとうございました", 6, self.font)

        # セリフ
        remaining = self.char_count
        for i, line in enumerate(scene["text"]):
            # remaining と line の長さ、どちらか小さい方だけ表示
            show = min(remaining, len(line))
            pyxel.text(8, 65 + i * 13, line[:show], 7, self.font)
            # remaining を減らす
            remaining -= show

    def is_all_text_shown(self) -> bool:
        """現在のシーンの全テキストが表示されているか"""
        return self.char_count == self.total_char()

    def total_char(self) -> int:
        """現在のシーンの全テキスト文字数を返す"""
        scene = SCENES[self.scene]
        return sum(len(line) for line in scene["text"])
        
Game()
