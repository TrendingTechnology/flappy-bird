# Flappy Bird made by Thuongton999
# Ez-ist mode
import pygame
import os
import sys
import platform
import random

pygame.mixer.init()
pygame.init()

# this use for build .exe file
def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_path, relative_path)

gameDefaultSettings = {
    "WINDOW_WIDTH": 1000,
    "WINDOW_HEIGHT": 600,
    "WINDOW_TITLE": "Flappy Bird (Made by Thuongton999)",
    "BIRD_WIDTH": 70,
    "BIRD_HEIGHT": 50,
    "SPAWN_POSITION": (200, 255),
    "BIRD_SPEED": -8,
    "WINDOW_SPEED": 3,
    "FPS": 60,
    "GRAVITY": 0.5,
    "MIN_COLUMN_HEIGHT": 100,
    "MAX_COLUMN_HEIGHT": 300,
    "COLUMN_SPACING": 200,
    "COLUMNS": 6,
    "DEFAULT_TEXT": pygame.font.Font(resource_path("font/FlappyBirdRegular.ttf"), 48),
    "DEFAULT_HEADER": pygame.font.Font(resource_path("font/FlappyBirdRegular.ttf"), 78),
    "DEFAULT_TITLE": pygame.font.Font(resource_path("font/FlappyBirdRegular.ttf"), 128),
    "COPYRIGHT": pygame.font.Font(resource_path("font/FlappyBirdRegular.ttf"), 42),
    "BIRD_IMAGE": pygame.image.load(resource_path("images/bird.png")),
    "COLUMN_IMAGE": pygame.image.load(resource_path("images/column.png")),
    "ICON": pygame.image.load(resource_path("images/favicon.ico")),
    "BACKGROUND": pygame.image.load(resource_path("images/background.png")),
    "SCOREBOARD": pygame.image.load(resource_path("images/scoreboard.png")),
    "START_BUTTON": pygame.image.load(resource_path("images/start_button.png")),
    "BRONZE_MEDAL": pygame.image.load(resource_path("images/medal_bronze.png")),
    "SILVER_MEDAL": pygame.image.load(resource_path("images/medal_silver.png")),
    "GOLD_MEDAL": pygame.image.load(resource_path("images/medal_gold.png")),
    "PlATINUM_MEDAL": pygame.image.load(resource_path("images/medal_platinum.png")),   
    "MEDAL_HOVER": pygame.image.load(resource_path("images/medal_hover.png")),
    "TAP_SOUND": pygame.mixer.Sound(resource_path("sounds/pop.wav")),
    "GAME_OVER_SOUND": pygame.mixer.Sound(resource_path("sounds/game_over.wav")),
}

colors = {
    "white": (255, 255, 255),
    "black": (0, 0, 0),
    "clotting": (82,58,74),
    "sun": (230, 193, 32),
    "grey": (143, 143, 143),
    "lemon_chiffon": (255, 250, 205),
}

def setKwargsToProps(props, kwargs):
    settings = kwargs.items()
    for setting, value in settings:
        try:
            props[setting] = value
        except KeyError:
            raise "Key setting %s not found" % (setting)

_circle_cache = {}
def _circlepoints(radius):
        radius = int(round(radius))
        if radius in _circle_cache:
            return _circle_cache[radius]
        x, y, e = radius, 0, 1 - radius
        _circle_cache[radius] = points = []
        while x >= y:
            points.append((x, y))
            y += 1
            if e < 0:
                e += 2 * y - 1
            else:
                x -= 1
                e += 2 * (y - x) - 1
        points += [(y, x) for x, y in points if x > y]
        points += [(-x, y) for x, y in points if x]
        points += [(x, -y) for x, y in points if y]
        points.sort()
        return points

def bordered(text, font, gfcolor=pygame.Color('dodgerblue'), ocolor=(255, 255, 255), opx=2):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

class Environment:
    def __init__(self, **kwargs):
        properties = {
            "gravity": gameDefaultSettings["GRAVITY"],
            "tap_sound": gameDefaultSettings["TAP_SOUND"],
            "game_over_sound": gameDefaultSettings["GAME_OVER_SOUND"]
        }
        setKwargsToProps(properties, kwargs)
        self.gravity = properties["gravity"]
        self.tapSound = properties["tap_sound"]
        self.gameOverSound = properties["game_over_sound"]

class Bird:
    def __init__(self, **kwargs):
        self.dead = False
        properties = {
            "width": gameDefaultSettings["BIRD_WIDTH"],
            "height": gameDefaultSettings["BIRD_HEIGHT"],
            "spawn_position": gameDefaultSettings["SPAWN_POSITION"],
            "speed": gameDefaultSettings["BIRD_SPEED"],
            "bird_image": gameDefaultSettings["BIRD_IMAGE"],
            "default_speed": gameDefaultSettings["BIRD_SPEED"]
        }
        self.WIDTH = properties["width"]
        self.HEIGHT = properties["height"]
        setKwargsToProps(properties, kwargs)
        self.positionX, self.positionY = properties["spawn_position"]
        self.defaultSpeed = properties["default_speed"]
        self.speed = properties["speed"]
        self.birdDefaultImage = pygame.transform.scale(properties["bird_image"], (self.WIDTH, self.HEIGHT))
        self.birdRotatedImage = self.birdDefaultImage

    def updateBirdSize(self):
        self.WIDTH = self.birdRotatedImage.get_width()
        self.HEIGHT = self.birdRotatedImage.get_height()
    

class Column:
    def __init__(self, **kwargs):
        properties = {
            "min_height": gameDefaultSettings["MIN_COLUMN_HEIGHT"],
            "max_height": gameDefaultSettings["MAX_COLUMN_HEIGHT"], 
            "position_x": gameDefaultSettings["WINDOW_WIDTH"],
            "column_image": gameDefaultSettings["COLUMN_IMAGE"],
            "rotated": False,
            "height": None,
        }
        setKwargsToProps(properties, kwargs)
        self.minHeight = properties["min_height"]
        self.maxHeight = properties["max_height"]
        self.columnImage = properties["column_image"]
        self.positionX = properties["position_x"]
        self.WIDTH = self.columnImage.get_width()
        self.HEIGHT = properties["height"] if properties["height"] else random.randint(self.minHeight, self.maxHeight)
        self.imageHeight = self.columnImage.get_height()
        self.positionY = 0
        self.rotated = properties["rotated"]
        if self.rotated:
            self.positionY = gameDefaultSettings["WINDOW_HEIGHT"] - self.HEIGHT
            self.columnImage = pygame.transform.rotate(self.columnImage, 180)

class Columns:
    def __init__(self, **kwargs):        
        properties = {
            "interface": None,
            "column_spacing": gameDefaultSettings["COLUMN_SPACING"],
            "columns": gameDefaultSettings["COLUMNS"]
        }
        setKwargsToProps(properties, kwargs)
        self.columnSpacing = properties["column_spacing"]
        self.spawns = properties["columns"]
        self.window = properties["interface"]
        newTopColumn = Column()
        newBottomColumn = Column(
            rotated=True,
            height=(self.window.HEIGHT-newTopColumn.HEIGHT-self.columnSpacing)
        )
        self.columns = [[newTopColumn, newBottomColumn, False], ]
        for i in range(self.spawns-1):          
            newColumnPosition = self.columns[-1][0].positionX+self.columns[-1][0].WIDTH+self.columnSpacing  
            newTopColumn = Column(
                position_x=newColumnPosition
            )
            newBottomColumn = Column(
                rotated=True, 
                position_x=newColumnPosition, 
                height=(self.window.HEIGHT-newTopColumn.HEIGHT-self.columnSpacing)
            )
            self.columns.append([newTopColumn, newBottomColumn, False])
    
    def addNewColumn(self):
        newColumnPosition = self.columns[-1][0].positionX+self.columns[-1][0].WIDTH+self.columnSpacing
        newTopColumn = Column(
            position_x=newColumnPosition
        )
        newBottomColumn = Column(
            rotated=True, 
            position_x=newColumnPosition, 
            height=(self.window.HEIGHT-newTopColumn.HEIGHT-self.columnSpacing)
        )
        self.columns.append([newTopColumn, newBottomColumn, False])

class Score:
    def __init__(self, **kwargs):
        properties = {
            "interface": None,
            "font": gameDefaultSettings["DEFAULT_HEADER"],
            "text_color": colors["white"],
            "border_color": colors["clotting"]
        }
        setKwargsToProps(properties, kwargs)
        self.interface = properties["interface"]
        self.font = properties["font"]
        self.color = properties["text_color"]
        self.borderColor = properties["border_color"]
        self.points = 0
    
    def render(self):
        scoredRendered = bordered(str(self.points), self.font, gfcolor=self.color, ocolor=self.borderColor)
        self.interface.interface.blit(scoredRendered, (self.interface.WIDTH//2 - scoredRendered.get_width()//2, 50))

class ScoreBoard():   
    def __init__(self, **kwargs):
        properties = {
            "points": 0,
            "position_x": 0,
            "position_y": 0,
            "width": 350,
            "height": 175,
            "interface": None,
            "board_image": gameDefaultSettings["SCOREBOARD"],
            "medal_hover": gameDefaultSettings["MEDAL_HOVER"],
            "medal_size": 80,
            "medals": {
                "bronze": gameDefaultSettings["BRONZE_MEDAL"],
                "silver": gameDefaultSettings["SILVER_MEDAL"],
                "gold": gameDefaultSettings["GOLD_MEDAL"],
                "platinum": gameDefaultSettings["PlATINUM_MEDAL"],
                "hover": gameDefaultSettings["MEDAL_HOVER"]
            }
        }
        setKwargsToProps(properties, kwargs)
        self.marginLeft = 30
        self.marginRight = 30
        self.marginTop = 20
        self.marginBottom = 20
        self.points = properties["points"]
        self.interface = properties["interface"]
        self.WIDTH = properties["width"]
        self.HEIGHT = properties["height"]
        self.positionX = properties["position_x"] if properties["position_x"] else self.interface.WIDTH//2-self.WIDTH//2
        self.positionY = properties["position_y"] if properties["position_y"] else self.interface.HEIGHT//2-self.HEIGHT//2
        self.medalSize = properties["medal_size"]
        self.medalPositionX = self.positionX + self.marginLeft
        self.medalPositionY = self.positionY + self.HEIGHT//2 - self.marginBottom
        self.medalHoverSize = self.medalSize + 6
        self.scoreBoardImage = pygame.transform.scale(properties["board_image"], (self.WIDTH, self.HEIGHT))
        self.medals = {
            "bronze": pygame.transform.scale(properties["medals"]["bronze"], (self.medalSize, self.medalSize)),
            "silver": pygame.transform.scale(properties["medals"]["silver"], (self.medalSize, self.medalSize)),
            "gold": pygame.transform.scale(properties["medals"]["gold"], (self.medalSize, self.medalSize)),
            "platinum": pygame.transform.scale(properties["medals"]["platinum"], (self.medalSize, self.medalSize)),
            "hover": pygame.transform.scale(properties["medals"]["hover"], (self.medalHoverSize, self.medalHoverSize))
        }
        self.medalReached = None
    
    def renderScoreBoard(self):
        self.interface.interface.blit(self.scoreBoardImage, (self.positionX, self.positionY))
        if self.points >= 5:
            self.medalReached = self.medals["bronze"]
            if self.points >= 10:
                self.medalReached = self.medals["silver"]
                if self.points >= 20:
                    self.medalReached = self.medals["gold"]
                    if self.points >= 40:
                        self.medalReached = self.medals["platinum"]
        medalTextRendered = bordered(
            "MEDAL",
            gameDefaultSettings["DEFAULT_TEXT"],
            gfcolor=colors["clotting"],
            ocolor=colors["lemon_chiffon"],
            opx=3
        )
        self.interface.interface.blit(
            medalTextRendered, 
            (
                self.positionX+self.marginLeft, 
                self.positionY+self.marginTop
            )
        )
        self.interface.interface.blit(self.medals["hover"], (self.medalPositionX, self.medalPositionY))
        if self.medalReached:
            self.interface.interface.blit(
                self.medalReached, 
                (
                    self.medalPositionX+(self.medalHoverSize-self.medalSize)//2, 
                    self.medalPositionY+(self.medalHoverSize-self.medalSize)//2
                )
            )
        scoreTextRendered = bordered(
            "SCORES",
            gameDefaultSettings["DEFAULT_TEXT"],
            gfcolor=colors["clotting"],
            ocolor=colors["lemon_chiffon"],
            opx=3
        )
        scoreTextRenderedWidth, scoreTextRenderedHeight = scoreTextRendered.get_size()
        scorePointsRendered = bordered(
            str(self.points),
            gameDefaultSettings["DEFAULT_HEADER"],
            gfcolor=colors["clotting"],
            ocolor=colors["lemon_chiffon"],
            opx=3
        )
        scorePointsRenderedWidth, scorePointsRenderedHeight = scorePointsRendered.get_size()        
        
        self.interface.interface.blit(
            scoreTextRendered,
            (
                self.positionX+self.WIDTH-self.marginRight-scoreTextRenderedWidth,
                self.positionY+self.marginTop
            )
        )
        self.interface.interface.blit(
            scorePointsRendered, 
            (
                self.positionX+self.WIDTH-self.marginRight-scoreTextRenderedWidth+(scoreTextRenderedWidth-scorePointsRenderedWidth)//2, 
                self.positionY+self.marginTop+scoreTextRenderedHeight+(self.medalHoverSize-scorePointsRenderedHeight)//2
            )
        )

class Button:
    def __init__(self, **kwargs):
        properties = {
            "button_image": gameDefaultSettings["START_BUTTON"],
            "button_width": 100,
            "button_height": 60,
            "position_x": 100,
            "position_y": 100,
        }
        setKwargsToProps(properties, kwargs)
        self.WIDTH, self.HEIGHT = properties["button_width"], properties["button_height"]
        self.positionX, self.positionY = properties["position_x"], properties["position_y"]
        self.buttonImage = pygame.transform.scale(properties["button_image"], (self.WIDTH, self.HEIGHT))
    
    def onClick(self, **mouse):
        if mouse["clicked"]:
            return (
                self.positionX <= mouse["mousePosX"] <= self.positionX + self.WIDTH and
                self.positionY <= mouse["mousePosY"] <= self.positionY + self.HEIGHT
            )
        return False

class Window:
    def __init__(self, **kwargs):
        self.frame = pygame.time.Clock()
        properties = {
            "width": gameDefaultSettings["WINDOW_WIDTH"],
            "height": gameDefaultSettings["WINDOW_HEIGHT"],
            "fps": gameDefaultSettings["FPS"],
            "title": gameDefaultSettings["WINDOW_TITLE"],
            "icon": gameDefaultSettings["ICON"],
            "background": gameDefaultSettings["BACKGROUND"],
            "speed": gameDefaultSettings["WINDOW_SPEED"]
        }
        setKwargsToProps(properties, kwargs)
        self.WIDTH = properties["width"]
        self.HEIGHT = properties["height"]
        self.title = properties["title"]
        self.FPS = properties["fps"]
        self.icon = properties["icon"]
        self.background = properties["background"]
        self.backgroundPosX = 0
        self.speed = properties["speed"]

        pygame.display.set_icon(self.icon)
        pygame.display.set_caption(self.title)

        self.interface = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.background = pygame.transform.scale(self.background, (self.WIDTH, self.HEIGHT))

def birdCollision(bird, column):
    return (
        bird.positionX < column.positionX + column.WIDTH and 
        bird.positionX + bird.WIDTH > column.positionX and 
        bird.positionY < column.positionY + column.HEIGHT and 
        bird.positionY + bird.HEIGHT > column.positionY
    )

window = Window()
bird = Bird()
environment = Environment()
columns = Columns(interface=window)
score = Score(interface=window)

def gameQuit():
    os.sys.exit("You dont want to play this game? Fvck you!")
    pygame.quit()

def gameStartScreen():
    startGame = False
    startButton = Button(
        position_x=window.WIDTH//2, 
        position_y=window.HEIGHT//2, 
        button_width=150, button_height=90
    )
    startButton.positionX -= startButton.WIDTH//2
    startButton.positionY -= startButton.HEIGHT//2
    while not startGame:
        window.interface.blit(window.background, (window.backgroundPosX, 0))
        window.interface.blit(window.background, (window.backgroundPosX+window.WIDTH, 0))
        window.backgroundPosX -= window.speed if window.backgroundPosX + window.WIDTH > 0 else -window.WIDTH
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()

        marginTop = 20
        marginBottom = 10
        titleRendered = bordered(
            "Flappy Bird", 
            gameDefaultSettings["DEFAULT_TITLE"], 
            gfcolor=colors["white"], 
            ocolor=colors["clotting"],
            opx=5
        )
        header2Rendered = bordered(
            "thuongton999 code this, ya :))",
            gameDefaultSettings["DEFAULT_TEXT"],
            gfcolor=colors["sun"],
            ocolor=colors["white"],
            opx=3
        )
        copyrightRendered = bordered(
            "Copyright by thuongton999",
            gameDefaultSettings["COPYRIGHT"],
            gfcolor=colors["sun"],
            ocolor=colors["white"],
            opx=3
        )
        window.interface.blit(titleRendered, (window.WIDTH//2-titleRendered.get_width()//2, marginTop))
        window.interface.blit(header2Rendered, (window.WIDTH//2-header2Rendered.get_width()//2, marginTop*2+titleRendered.get_height()))
        window.interface.blit(
            copyrightRendered, 
            (window.WIDTH//2-copyrightRendered.get_width()//2, window.HEIGHT-marginBottom-copyrightRendered.get_height())
        )
        window.interface.blit(startButton.buttonImage, (startButton.positionX, startButton.positionY))
        mousePosX, mousePosY = pygame.mouse.get_pos()
        mouseButtonPressed = pygame.mouse.get_pressed(3)
        if startButton.onClick(mousePosX=mousePosX, mousePosY=mousePosY, clicked=mouseButtonPressed[0]):
            startGame = True
            break
        pygame.display.update()
        window.frame.tick(window.FPS)
    while startGame:
        bird.__init__()
        columns.__init__(interface=window)
        score.__init__(interface=window)

        getReady()
        gamePlay()
        startGame = gameOver()
    return startGame

def getReady():
    ready = False
    while not ready:
        window.interface.blit(window.background, (window.backgroundPosX, 0))
        window.interface.blit(window.background, (window.backgroundPosX+window.WIDTH, 0))
        window.backgroundPosX -= window.speed if window.backgroundPosX + window.WIDTH > 0 else -window.WIDTH
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            elif event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                return

        marginLeft = 50
        getReadyTextRendered = bordered(
            "Get ready? Tap or press any key",
            gameDefaultSettings["DEFAULT_TEXT"],
            gfcolor=colors["grey"],
            ocolor=colors["white"],
            opx=3
        )
        window.interface.blit(bird.birdRotatedImage, (bird.positionX, bird.positionY))
        window.interface.blit(getReadyTextRendered, (bird.positionX+bird.WIDTH+marginLeft, bird.positionY))

        pygame.display.update()
        window.frame.tick(window.FPS)

def gamePlay():
    while not bird.dead:
        window.interface.blit(window.background, (window.backgroundPosX, 0))
        window.interface.blit(window.background, (window.backgroundPosX+window.WIDTH, 0))
        window.backgroundPosX -= window.speed if window.backgroundPosX + window.WIDTH > 0 else -window.WIDTH

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                environment.tapSound.play()
                bird.positionY -= bird.speed if bird.positionY >= 0 else 0
                bird.speed = bird.defaultSpeed
                            
        for topColumn, bottomColumn, passed in columns.columns:
            topColumn.positionX -= window.speed
            bottomColumn.positionX -= window.speed
            window.interface.blit(topColumn.columnImage, (topColumn.positionX, -(topColumn.imageHeight - topColumn.HEIGHT))) 
            window.interface.blit(bottomColumn.columnImage, (bottomColumn.positionX, bottomColumn.positionY))
            if birdCollision(bird, topColumn) or birdCollision(bird, bottomColumn):
                bird.dead = True
                break
        if columns.columns[0][0].positionX + columns.columns[0][0].WIDTH < bird.positionX and not columns.columns[0][2]:
            columns.columns[0][2] = True
            score.points += 1
        if columns.columns[0][0].positionX + columns.columns[0][0].WIDTH < 0:
            columns.columns.pop(0)
            columns.addNewColumn()

        bird.positionY += bird.speed + 0.5*environment.gravity
        bird.speed += environment.gravity
        bird.birdRotatedImage = pygame.transform.rotate(bird.birdDefaultImage, -bird.speed*2)
        
        bird.updateBirdSize()

        window.interface.blit(bird.birdRotatedImage, (bird.positionX, bird.positionY))
        score.render()

        if not (0 <= bird.positionY <= window.HEIGHT - bird.HEIGHT):
            bird.dead = True
  
        pygame.display.update()
        window.frame.tick(window.FPS)

def gameOver():
    environment.gameOverSound.play()
    scoreBoard = ScoreBoard(points=score.points, interface=window)
    titleRendered = bordered(
        "GAME OVER", 
        gameDefaultSettings["DEFAULT_TITLE"], 
        gfcolor=colors["white"], 
        ocolor=colors["clotting"],
        opx=5
    )
    notificationRendered = bordered(
        "Press SPACE to play again or ESC to go back to Menu",
        gameDefaultSettings["DEFAULT_TEXT"],
        gfcolor=colors["lemon_chiffon"],
        ocolor=colors["sun"],
        opx=3
    )
    titleDropDownSpeed = 6
    titlePositionX = window.WIDTH//2-titleRendered.get_width()//2
    titlePositionY = -titleRendered.get_height()
    marginBottom = 20
    marginTop = 20
    notificationPositionX = window.WIDTH//2-notificationRendered.get_width()//2
    notificationPositionY = scoreBoard.positionY+scoreBoard.HEIGHT+marginTop
    
    playAgain = False
    while not playAgain:
        window.interface.blit(window.background, (window.backgroundPosX, 0))
        window.interface.blit(window.background, (window.backgroundPosX+window.WIDTH, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameQuit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return True
                elif event.key == pygame.K_ESCAPE:
                    return False

        titlePositionY += titleDropDownSpeed if titlePositionY+titleRendered.get_height()+marginBottom < scoreBoard.positionY else 0
        
        window.interface.blit(notificationRendered, (notificationPositionX,notificationPositionY))
        window.interface.blit(titleRendered, (titlePositionX, titlePositionY))
        scoreBoard.renderScoreBoard()

        pygame.display.update()
        window.frame.tick(window.FPS)
    return playAgain
    

if __name__ == "__main__":
    command = {
        "clearConsoleLog": {
            "Windows": "cls",
            "Linux": "clear",
            "Darwin": "clear"
        }
    }
    currentOS = platform.system()
    os.system(command["clearConsoleLog"][currentOS])

    home = True
    while home:
        gameStartScreen()
    
    