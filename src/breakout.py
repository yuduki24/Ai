import pygame
from pygame.locals import *
import sys
import breakout_obj
import loader

SCR_RECT = Rect(0, 0, 372, 384)
START, PLAY, GAMEOVER = (0, 1, 2)  # ゲーム状態

def main():
    pygame.init()
    pygame.display.set_caption(u"ブロック崩し")
    screen = pygame.display.set_mode(SCR_RECT.size)
    while True:
        initView(screen)
        breakout(screen)
        gameoverView(screen)

def gameoverView(screen):
    screen.fill((0,0,0))
    sysfont = pygame.font.SysFont(None, 80)
    score_img = sysfont.render("GAME OVER", True, (255,255,0))
    x = (SCR_RECT.size[0] - score_img.get_width()) / 2
    y = (SCR_RECT.size[1] - score_img.get_height()) / 2
    screen.blit(score_img, (x, y))
    pygame.display.update()
    while breakout_obj.game_state == GAMEOVER:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                breakout_obj.game_state = START

def initView(screen):
    title, title_rect = loader.load_image("title.png")
    screen.blit(title, (0, 0))
    pygame.display.update()
    while breakout_obj.game_state == START:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                breakout_obj.game_state = PLAY
    
def breakout(screen):
    # BGMを再生
    # MFP【Marron Fields Production】
    loader.play_sound("Curious_Boy.mp3", -1)
    # スプライトグループを作成して登録
    all = pygame.sprite.RenderUpdates()  # 描画用グループ
    blocks = pygame.sprite.Group()       # 衝突判定用グループ
    breakout_obj.Paddle.containers = all
    breakout_obj.Ball.containers = all
    breakout_obj.Block.containers = all, blocks

    score_board = breakout_obj.ScoreBoard()

    # サウンドのロード
    breakout_obj.Ball.paddle_sound = loader.load_sound("wood00.wav")  # パドルとの衝突音
    breakout_obj.Ball.brick_sound = loader.load_sound("chari06.wav")  # ブロックとの衝突音
    breakout_obj.Ball.fall_sound = loader.load_sound("fall06.wav")    # ボールを落とした音

    # パドルを作成
    paddle = breakout_obj.Paddle()
    # ボールを作成するとスプライトグループallに自動的に追加される
    breakout_obj.Ball(paddle, blocks, score_board)
    # ブロックを作成
    # 自動的にblocksグループに追加される
    for x in range(1, 11):  # 1列から10列まで
        for y in range(1, 6):  # 1行から5行まで
            breakout_obj.Block(x, y)

    breakout_obj.life = 3
    clock = pygame.time.Clock()
    while breakout_obj.game_state == PLAY:
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

if __name__ == "__main__":
    main()
