import pyxel
import math

class App:
    def __init__(self):
        pyxel.init(200, 200)
        self.ballx = 100
        self.bally = 160
        self.angle = pyxel.rndi(30, 150)
        self.vx = pyxel.cos(self.angle) * 2
        self.vy = pyxel.sin(self.angle) * 2
        self.paddle_width = 15
        self.padx = 100 - self.paddle_width / 2  # パッドの中心座標
        self.blocks = self.generate_blocks()
        self.game_over = False
        self.remaining_attempts = 4
        self.game_started = False
        self.paddle_hit = False  # パドルに当たった状態を管理

        pyxel.run(self.update, self.draw)

    def generate_blocks(self):
        blocks = []
        for a in range(30):  # ブロックの数を減らす
            blockx = 15 + 15 * (a % 10)  # ブロックの横の間隔を広げる
            blocky = 10 + 15 * int(a / 10)  # ブロックの縦の間隔を広げる
            blocks.append((blockx, blocky, 14, 14))  # ブロックのサイズを大きくする
        return blocks

    def update(self):
        if not self.game_started:
            if pyxel.btnp(pyxel.KEY_SPACE):
                self.game_started = True
        else:
            if not self.game_over:
                self.ballx += self.vx
                self.bally += self.vy

                # ボールの反射
                if self.ballx <= 0 or self.ballx >= 200:
                    self.vx = -self.vx

                if self.bally <= 0:
                    self.vy = -self.vy

                # パドルとの反射
                if (
                    self.bally + 2 >= 195
                    and self.padx <= self.ballx <= self.padx + self.paddle_width
                    and self.vy > 0
                ):
                    if not self.paddle_hit:
                        self.vy = -self.vy
                        self.paddle_hit = True
                        self.bally = 195 - 2  # パドルの上端にボールがくっつかないように位置調整
                else:
                    self.paddle_hit = False

                # ボールが画面外に出たらリセット
                if self.bally >= 200:
                    self.remaining_attempts -= 1
                    if self.remaining_attempts <= 0:
                        self.game_over = True
                    else:
                        self.ballx = pyxel.rndi(0, 199)
                        self.bally = 160  # ボールのy座標をリセット
                        self.vx = pyxel.cos(pyxel.rndi(30, 150)) * 2
                        self.vy = pyxel.sin(pyxel.rndi(30, 150)) * 2
                # ブロックとの反射
                for block in list(self.blocks):
                    if (
                        self.ballx + 2 >= block[0]
                        and self.ballx - 2 <= block[0] + block[2]
                        and self.bally + 2 >= block[1]
                        and self.bally - 2 <= block[1] + block[3]
                    ):
                        # ボールがブロックの上下に接触した場合
                        if (
                            self.ballx + 2 >= block[0]
                            and self.ballx - 2 <= block[0] + block[2]
                        ):
                            self.vy = -self.vy
                        # ボールがブロックの左右に接触した場合
                        elif (
                            self.bally + 2 >= block[1]
                            and self.bally - 2 <= block[1] + block[3]
                        ):
                            self.vx = -self.vx
                            
                        self.blocks.remove(block)


                self.padx = pyxel.mouse_x - self.paddle_width / 2  # パッドの中心座標を更新

               

    def draw(self):
        pyxel.cls(0)

        if not self.game_started:
            pyxel.text(70, 90, "Press SPACE to start", pyxel.frame_count % 16)
        elif not self.game_over:
            pyxel.circ(self.ballx, self.bally, 2, 10)
            pyxel.rect(self.padx, 195, self.paddle_width, 3, 3)

            # ブロックを描画
            for block in self.blocks:
                pyxel.rect(block[0], block[1], block[2], block[3], 1)

            # 残りの回数を表示
            pyxel.text(150, 190, "×" + str(self.remaining_attempts), 7)
        else:
            pyxel.text(50, 80, "Game Over", 8)

App()
