import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'hide'
import pygame
import sys
from PlayerTank import PlayerTank
from EnemyTank import EnemyTank
from Sound import Sound
from BrickWall import BrickWall
from StoneWall import StoneWall
from Home import Home

SCREEN_WIDTH = 1100
SCREEN_HEIGHT = 600
BACKGROUND_COLOR = pygame.Color(0, 0, 0)
FONT_COLOR = (255, 255, 255)
PLAYER_TANK_POSITION = (325, 550)

class MainGame:

    playerTankMoveSound = Sound('../Sound/player.move.wav').setVolume()
    startingSound = Sound('../Sound/intro.wav')


    # 窗口Surface对象
    window = None

    # 玩家坦克
    playerTank = None

    # 玩家子弹
    playerBulletList = []
    playerBulletNumber = 3

    # 敌人坦克
    enemyTankList = []
    enemyTankTotalCount = 5
    # 用来给玩家展示坦克的数量
    enemyTankCurrentCount = 5

    # 敌人坦克子弹
    enemyTankBulletList = []

    #爆炸
    explodeList =[]

    brickWallList = []
    stoneWallList=[]


    

    def __init__(self):
        print('请将输入法切换为英文')
        MainGame.home = Home(425, 550)
        # 记录是否输了
        self.isDefeated = False

    def startGame(self):
        # 初始化展示模块
        pygame.display.init()
        # 设置窗口大小
        size = (SCREEN_WIDTH, SCREEN_HEIGHT)
        # 初始化窗口
        MainGame.window = pygame.display.set_mode(size)
        # 设置窗口标题
        pygame.display.set_caption('Tank Battle')

        # 初始化我方坦克
        MainGame.playerTank = PlayerTank(PLAYER_TANK_POSITION[0], PLAYER_TANK_POSITION[1], 1, 1)

        #音乐
        MainGame.startingSound.play()

        # 初始化场景
        self.initBrickWall()
        self.initStoneWall()

        while 1:
            # 设置背景颜色
            MainGame.window.fill(BACKGROUND_COLOR)

            # 检查是否输了
            if self.isDefeated:
                self.defeated()
                break

            # 获取窗口事件
            self.getPlayingModeEvent()

            # 显示物体
            self.drawBrickWall(MainGame.brickWallList)
            self.drawStoneWall(MainGame.stoneWallList)

            # 显示我方坦克
            MainGame.playerTank.draw(MainGame.window, PLAYER_TANK_POSITION[0], PLAYER_TANK_POSITION[1])


            # 我方坦克移动
            if not MainGame.playerTank.stop:
                MainGame.playerTank.move()
                MainGame.playerTank.collideEnemyTank(MainGame.enemyTankList)
                # 不能撞墙
                MainGame.playerTank.collideBrickWall(MainGame.brickWallList)
                MainGame.playerTank.collideStoneWall(MainGame.stoneWallList)

            # 显示我方坦克子弹
            self.drawPlayerBullet(MainGame.playerBulletList)

            # 展示敌方坦克
            self.drawEnemyTank()

            self.drawExplode()

            # 展示敌方坦克子弹
            self.drawEnemyBullet()


            # 更新窗口
            pygame.display.update()
        # 设置背景颜色
        MainGame.window.fill(BACKGROUND_COLOR)

        # 显示字体
        self.drawText('Defeated', 200, 200, 50, MainGame.window)

        # 更新窗口
        pygame.display.update()


    def getPlayingModeEvent(self):
        # 获取所有事件

        eventList = pygame.event.get()

        for event in eventList:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            """
            stop属性用来控制坦克移动, 当键盘按键按下时, 坦克可以移动, 一直按住一直移动, 当按键抬起时, 停止移动
            如果没有该属性, 按一下按键移动一次, 按一下移动一下, 不能一直按住一直移动
            """
            # 函数原型：pygame.key.set_repeat(delay, interval)
            # 第一个参数影响着按键的灵敏度，第二个参数影响着按键的移动时间间隔
            pygame.key.set_repeat(10, 10)

            key_pressed = pygame.key.get_pressed()

            if key_pressed[pygame.K_w]:
                MainGame.playerTankMoveSound.play(-1)
                MainGame.playerTank.direction = 'UP'
                MainGame.playerTank.stop = False
            elif key_pressed[pygame.K_s]:
                MainGame.playerTankMoveSound.play(-1)
                MainGame.playerTank.direction = 'DOWN'
                MainGame.playerTank.stop = False
            elif key_pressed[pygame.K_a]:
                MainGame.playerTankMoveSound.play(-1)
                MainGame.playerTank.direction = 'LEFT'
                MainGame.playerTank.stop = False
            elif key_pressed[pygame.K_d]:
                MainGame.playerTankMoveSound.play(-1)
                MainGame.playerTank.direction = 'RIGHT'
                MainGame.playerTank.stop = False
            elif key_pressed[pygame.K_j]:
                # 判断子弹数量是否超过指定的个数
                if len(MainGame.playerBulletList) < MainGame.playerBulletNumber:
                    print(len(MainGame.playerBulletList))
                    bullet = MainGame.playerTank.shot()
                    MainGame.playerBulletList.append(bullet)
                    Sound('../Sound/shoot.wav').play(0)
            elif key_pressed[pygame.K_r]:
                # 判断子弹数量是否超过指定的个数
                if len(MainGame.playerBulletList) < MainGame.playerBulletNumber:
                    bullet = MainGame.playerTank.shot()
                    MainGame.playerBulletList.append(bullet)
                    Sound('../Sound/shoot.wav').play(0)
            else:
                MainGame.playerTankMoveSound.stop()
                MainGame.playerTank.stop = True




    def drawPlayerBullet(self, playerBulletList):
        # 遍历整个子弹列表，如果是没有被销毁的状态，就把子弹显示出来，否则从列表中删除
        for bullet in playerBulletList:
            if not bullet.isDestroy:
                bullet.draw(MainGame.window)
                bullet.move(MainGame.explodeList)
                bullet.playerBulletCollideEnemyTank(MainGame.enemyTankList, MainGame.explodeList)
                bullet.bulletCollideBrickWall(MainGame.brickWallList, MainGame.explodeList)
                bullet.bulletCollideStoneWall(MainGame.stoneWallList, MainGame.explodeList)
            else:
                playerBulletList.remove(bullet)



    def drawEnemyTank(self):
        # 如果当前坦克为0，那么就该重新生成坦克
        if len(MainGame.enemyTankList) == 0:
            # 一次性产生三个，如果剩余坦克数量超过三，那只能产生三个
            n = min(3, MainGame.enemyTankTotalCount)
            # 如果最小是0，就说明敌人坦克没有了，那么就赢了
            if n == 0:
                print('赢了')
                return
            # 没有赢的话，就产生n个坦克
            self.initEnemyTank(n)
            # 总个数减去产生的个数
            MainGame.enemyTankTotalCount -= n
        # 遍历坦克列表，展示坦克并且移动
        for tank in MainGame.enemyTankList:
            # 坦克还有生命值
            if tank.life > 0:
                tank.draw(MainGame.window)
                tank.move()
                tank.collidePlayerTank(MainGame.playerTank)
                tank.collideEnemyTank(MainGame.enemyTankList)
                # 不能撞墙
                tank.collideBrickWall(MainGame.brickWallList)
                tank.collideStoneWall(MainGame.stoneWallList)
                bullet = tank.shot()
                if bullet is not None:
                    MainGame.enemyTankBulletList.append(bullet)
            # 坦克生命值为0，就从列表中剔除
            else:
                MainGame.enemyTankCurrentCount -= 1
                MainGame.enemyTankList.remove(tank)

    def initEnemyTank(self, number):
        y = 0
        position = [0, 425, 850]
        index = 0
        for i in range(number):
            x = position[index]
            enemyTank = EnemyTank(x, y)
            MainGame.enemyTankList.append(enemyTank)
            index += 1

    def drawEnemyBullet(self):
        for bullet in MainGame.enemyTankBulletList:
            if not bullet.isDestroy:
                bullet.draw(MainGame.window)
                bullet.move(MainGame.explodeList)
                bullet.enemyBulletCollidePlayerTank(MainGame.playerTank, MainGame.explodeList)
                bullet.bulletCollideBrickWall(MainGame.brickWallList, MainGame.explodeList)
                bullet.bulletCollideStoneWall(MainGame.stoneWallList, MainGame.explodeList)
            else:
                bullet.source.bulletCount -= 1
                MainGame.enemyTankBulletList.remove(bullet)




    def drawExplode(self):
        for e in MainGame.explodeList:
            if e.isDestroy:
                MainGame.explodeList.remove(e)
            else:
                e.draw(MainGame.window)
    
    def drawBrickWall(self, brickWallList):
        for brickWall in brickWallList:
            if brickWall.isDestroy:
                brickWallList.remove(brickWall)
            else:
                brickWall.draw(MainGame.window)
                

    def initBrickWall(self):
        for i in range(20):
            MainGame.brickWallList.append(BrickWall(i * 25, 200))
    
    def initStoneWall(self):
        for i in range(20):
            MainGame.stoneWallList.append(StoneWall(i * 25, 400))
        
    def drawStoneWall(self, stoneWallList):
        for stoneWall in stoneWallList:
            if stoneWall.isDestroy:
                stoneWallList.remove(stoneWall)
            else:
                stoneWall.draw(MainGame.window)
    
    def defeated(self):
        # 失败了坦克不能移动了
        MainGame.playerTankMoveSound.stop()
        # 播放失败音乐
        Sound('../Sound/gameOver.wav').play()
        print('游戏结束')
        self.isDefeated = True
    

    def drawText(self, text, x, y, fontSize, window):
    # 初始化字体
        pygame.font.init()
        font = pygame.font.SysFont('georgia', fontSize)
        # 加载文字并设置颜色
        fontColor = pygame.Color(255, 255, 255)
        fontObject = font.render(text, True, fontColor)
        # 展示文字
        window.blit(fontObject, (x, y))






if __name__ == '__main__':
    MainGame().startGame()