
from random import randint

from kivy.uix.widget import Widget
from kivy.uix.image import Image

from fuPongObjects import Meteor
from fuModeObjects import Shit, InvertedPaddle, Roof

from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, ReferenceListProperty
from kivy.graphics import Ellipse
from kivy.core.window import Window


from kivy.clock import Clock


class Cactus(Image):
    def __init__(self, dashModeObj):
        super(Cactus, self).__init__()
        self.dashModeObj = dashModeObj

    def move(self, dt):
        self.center_x -= self.dashModeObj.realBall.fauxVelocity
        if self.dashModeObj.realBall.collide_widget(self):
            raise EndGameException

        if self.center_x < 0:
            self.dashModeObj.remove_widget(self)
            return False


class DashBall(Widget):
    gravityStrength = NumericProperty(0.5)
    fauxVelocity = NumericProperty(5)
    velocity_y = NumericProperty(0)

    def __init__(self, dashModeObj):
        super(DashBall, self).__init__()
        self.dashModeObj = dashModeObj


    def calcPos(self, dt):
        self.center_y += self.velocity_y
        self.velocity_y -= self.gravityStrength
        if self.center_y < self.dashModeObj.gameMode.floorPos:
            self.velocity_y = 0

    def allowJump(self, dt):
        self.allowJumpBool = True





class DModeProperties:
    def __init__(self, dashModeObject):
        self.dashModeObject = dashModeObject

        self.scoreNum = 0

        self.addedWidgets = []
        self.scheduledObjects = []
        self.floorPos = 120

        self.level = 0
        self.levelList = [self.initCactusCycle, self.speedIncrease, self.speedIncrease] # TODO: what's the third level we could add?

    def initCactusCycle(self):
        cactusSpawnInterval = 1
        Clock.schedule_interval(self.dashModeObject.initCactus, cactusSpawnInterval)

    def speedIncrease(self):
        self.dashModeObject.realBall.fauxVelocity += 2





class DashMode(Widget):
    gameMode = ObjectProperty(None)

    paddle = ObjectProperty(None)

    numSurvivedCycles = NumericProperty(0)

    outOfBounds = BooleanProperty(False)

    scoreText = ObjectProperty(None)

    currentlyScheduledGlobal = ReferenceListProperty()
    # ==================== New Attributes
    realBall = ObjectProperty(None)
    countText = ObjectProperty(None)
    numMeteorsCurrent = NumericProperty(0)

    def __init__(self):
        super(DashMode, self).__init__()
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)

    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        print(self.realBall.center)
        if keycode[1] == "w" and self.realBall.center_y < self.gameMode.floorPos + 5:
            self.realBall.allowJumpBool = False
            print("DOWN")
            self.realBall.velocity_y = 15


    def initScore(self):
        print("INITIALIZED SCORE")
        self.scoreText.text = "[size=40] SCORE " + str(self.gameMode.scoreNum) + "[/size]"
        scoreSchedule = Clock.schedule_interval(self.incrementScore, 1)
        self.currentlyScheduledGlobal.append(scoreSchedule)

    def incrementScore(self, dt):
        self.gameMode.scoreNum += 1
        self.scoreText.text = "[size=40] SCORE " + str(self.gameMode.scoreNum) + "[/size]"




    def mainLoop(self, dt=None):

        self.numSurvivedCycles += 1

        self.checkLevelUp()

    def checkLevelUp(self):
        levelUpNum = 6
        if self.numSurvivedCycles % levelUpNum == 0:
            self.numSurvivedCycles = 0
            self.gameMode.level += 1
            self.gameMode.levelList[self.gameMode.level]()

    def preGameInit(self, dt):
        self.remove_widget(self.paddle)
        self.gameMode = DModeProperties(self)

        self.realBall = DashBall(self)
        self.realBall.center = (self.width / 4), self.gameMode.floorPos + 50

        Clock.schedule_interval(self.realBall.calcPos, 1/60)

        self.realBall.size = 20, 20
        self.add_widget(self.realBall)

        self.gameMode.levelList[self.gameMode.level]()
        self.initScore()


    def initCactus(self, dt=None):
        spawn = randint(0, 1)
        if spawn:           # randomizer
            cactusObj = Cactus(self)
            cactusObj.size = 55, 70
            cactusObj.center = self.width, self.gameMode.floorPos + cactusObj.size[1] / 2
            self.add_widget(cactusObj)
            self.gameMode.addedWidgets.append(cactusObj)

            cactusSchedule = Clock.schedule_interval(cactusObj.move, 1 / 60)
            self.gameMode.scheduledObjects.append(cactusSchedule)



    def clearEventText(self, dt):
        self.countText.countNum.text = ""

    def checkOutOfBounds(self, dt):
        if self.outOfBounds:
            self.cleanUpProcedure()

    def cleanUpProcedure(self):
        self.countText.countNum.text = "[size=400]E[color=#FFFF00]ND[/color][/size]"
        for schedule in self.currentlyScheduledGlobal:
            print(schedule)
            schedule.cancel()

        for schedule in self.gameMode.scheduledObjects:
            print(schedule)
            schedule.cancel()
        for obj in self.gameMode.addedWidgets:
            self.remove_widget(obj)

class EndGameException(Exception):
    pass
