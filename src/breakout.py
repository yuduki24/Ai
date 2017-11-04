import pygame
from pygame.locals import *
import os
import sys
import math
import random

SCR_RECT = Rect(0, 0, 372, 384)

def main():
    pygame.init()
    screen = pygame.display.set_mode(SCR_RECT.size)
    pygame.display.set_caption(u"ブロック崩し")

    # BGMを再生
    # MFP【Marron Fields Production】
    pygame.mixer.music.load("sound/Curious_Boy.mp3")
    pygame.mixer.music.play(-1)

    # スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()  # 描画用グループ
    blocks = pygame.sprite.Group()       # 衝突判定用グループ
    Paddle.containers = all
    Ball.containers = all
    Block.containers = all, blocks
    # サウンドのロード
    Ball.paddle_sound = load_sound("wood00.wav")  # パドルとの衝突音
    Ball.brick_sound = load_sound("chari06.wav")  # ブロックとの衝突音
    Ball.fall_sound = load_sound("fall06.wav")    # ボールを落とした音

    score_board = ScoreBoard()

    # パドルを作成
    paddle = Paddle()
    # ボールを作成するとスプライトグループallに自動的に追加される
    Ball(paddle, blocks, score_board)
    # ブロックを作成
    # 自動的にblocksグループに追加される
    for x in range(1, 11):  # 1列から10列まで
        for y in range(1, 6):  # 1行から5行まで
            Block(x, y)

    clock = pygame.time.Clock()
    while True:
        clock.tick(60)
        screen.fill((0,0,0))
        all.update()
        all.draw(screen)
        score_board.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

class Paddle(pygame.sprite.Sprite):
    """ボールを打つパドル"""
    def __init__(self):
        # containersはmain()でセットされる
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image("paddle.png")
        self.rect.bottom = SCR_RECT.bottom - 10  # パドルは画面の一番下から少し隙間を開けた.
    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]  # パドルの中央のX座標=マウスのX座標
        self.rect.clamp_ip(SCR_RECT)  # SCR_RECT内でしか移動できなくなる

class Ball(pygame.sprite.Sprite):
    """ボール"""
    __speed = 7
    __angle_left = 150
    __angle_right = 30
    __hit = 0
    def __init__(self, paddle, blocks, score_board):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image("ball.png")
        self.dx = self.dy = 0  # ボールの速度
        self.paddle = paddle  # パドルへの参照
        self.blocks = blocks  # blocksへの参照.
        self.score_board = score_board
        self.update = self.start
    def start(self):
        """ボールの位置を初期化"""
        # パドルの中央に配置
        self.rect.centerx = self.paddle.rect.centerx
        self.rect.bottom = self.paddle.rect.top
        # 左クリックで移動開始
        if pygame.mouse.get_pressed()[0] == 1:
            ran = random.randint(45, 135)
            angle = math.radians(ran)
            self.dx = self.__speed * math.cos(angle)  # float
            self.dy = -self.__speed * math.sin(angle) # float
            # update()をmove()に置き換え
            self.update = self.move
    def move(self):
        """ボールの移動"""
        self.rect.centerx += self.dx
        self.rect.centery += self.dy
        # 壁との反射
        if self.rect.left < SCR_RECT.left:  # 左側
            self.rect.left = SCR_RECT.left
            self.dx = -self.dx  # 速度を反転
        if self.rect.right > SCR_RECT.right:  # 右側
            self.rect.right = SCR_RECT.right
            self.dx = -self.dx
        if self.rect.top < SCR_RECT.top:  # 上側
            self.rect.top = SCR_RECT.top
            self.dy = -self.dy
        # パドルとの反射
        if self.rect.colliderect(self.paddle.rect) and self.dy > 0:
            self.__hit = 0  # 連続ヒットを0に戻す
            # パドルの左端に当たったとき135度方向、右端で45度方向とし、
            # その間は線形補間で反射方向を計算
            x1 = self.paddle.rect.left - self.rect.width  # ボールが当たる左端
            y1 = self.__angle_left  # 左端での反射方向（135度）
            x2 = self.paddle.rect.right  # ボールが当たる右端
            y2 = self.__angle_right  # 右端での反射方向（45度）
            m = float(y2-y1) / (x2-x1)  # 直線の傾き
            x = self.rect.left  # ボールが当たった位置
            y = m * (x - x1) + y1
            angle = math.radians(y)
            self.dx = self.__speed * math.cos(angle)  # float
            self.dy = -self.__speed * math.sin(angle) # float
        # ボールを落とした場合
        if self.rect.top > SCR_RECT.bottom:
            self.update = self.start  # ボールを初期状態に
            self.fall_sound.play()
            # ボールを落としたら-30点
            self.__hit = 0
            self.score_board.add_score(-30)

        # ブロックを壊す
        # ボールと衝突したブロックリストを取得
        blocks_collided = pygame.sprite.spritecollide(self, self.blocks, True)
        if blocks_collided:  # 衝突ブロックがある場合
            oldrect = self.rect
            for brick in blocks_collided:  # 各衝突ブロックに対して
                # ボールが左から衝突
                if oldrect.left < brick.rect.left < oldrect.right < brick.rect.right:
                    self.rect.right = brick.rect.left
                    self.dx = -self.dx
                # ボールが右から衝突
                if brick.rect.left < oldrect.left < brick.rect.right < oldrect.right:
                    self.rect.left = brick.rect.right
                    self.dx = -self.dx
                # ボールが上から衝突
                if oldrect.top < brick.rect.top < oldrect.bottom < brick.rect.bottom:
                    self.rect.bottom = brick.rect.top
                    self.dy = -self.dy
                # ボールが下から衝突
                if brick.rect.top < oldrect.top < brick.rect.bottom < oldrect.bottom:
                    self.rect.top = brick.rect.bottom
                    self.dy = -self.dy
                self.brick_sound.play()
                # 点数を追加
                self.__hit += 1
                self.score_board.add_score(self.__hit * 10)

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image("brick.png")
        # ブロックの位置を更新
        self.rect.left = SCR_RECT.left + x * self.rect.width
        self.rect.top = SCR_RECT.top + y * self.rect.height

class ScoreBoard():
    """スコアボード"""
    def __init__(self):
        self.sysfont = pygame.font.SysFont(None, 80)
        self.score = 0
    def draw(self, screen):
        score_img = self.sysfont.render(str(self.score), True, (255,255,0))
        x = (SCR_RECT.size[0] - score_img.get_width()) / 2
        y = (SCR_RECT.size[1] - score_img.get_height()) / 2
        screen.blit(score_img, (x, y))
    def add_score(self, x):
        self.score += x

def load_image(filename, colorkey=None):
    """画像をロードして画像と矩形を返す"""
    filename = os.path.join("img", filename)
    try:
        image = pygame.image.load(filename)
    except pygame.error as message:
        print ("Cannot load image:", filename)
        raise SystemExit(message)
    image = image.convert()
    if colorkey is not None:
        if colorkey is -1:
            colorkey = image.get_at((0,0))
        image.set_colorkey(colorkey, RLEACCEL)
    return image, image.get_rect()

def load_sound(filename):
    filename = os.path.join("sound", filename)
    return pygame.mixer.Sound(filename)

if __name__ == "__main__":
    main()
