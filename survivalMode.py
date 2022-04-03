import random

from kivy.uix.widget import Widget
from fuPongObjects import Meteor

from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, ReferenceListProperty

from kivy.clock import Clock


class CountDown(Widget):
    pass


class LifeIcon(Widget):
    pass


class SModeProperties():
    def __init__(self):
        self.ballAccel = 0.02
        self.horizontalAccel = 0

        self.startingLives = 1
        self.lives = []

        self.perCycleInit = 2

        self.scoreNum = 0


class SurvivalMode(Widget):
    gameMode = ObjectProperty(SModeProperties())

    countText = ObjectProperty(None)
    countDownReset = NumericProperty(5)
    countDownNum = NumericProperty(5)

    paddle = ObjectProperty(None)

    numSurvivedCycles = NumericProperty(0)
    numMeteorsCurrent = NumericProperty(0)

    outOfBounds = BooleanProperty(False)

    scoreText = ObjectProperty(None)

    currentlyScheduledGlobal = ReferenceListProperty()

    def initLives(self):
        for lifeNum in range(self.gameMode.startingLives):
            life = LifeIcon()
            self.add_widget(life)
            life.center = self.width - 50 * lifeNum - 50, self.height - 50
            self.gameMode.lives.append(life)

    def initScore(self, dt):
        print("INITIALIZED SCORE")
        self.scoreText.text = "[size=40] SCORE " + str(self.gameMode.scoreNum) + "[/size]"
        scoreSchedule = Clock.schedule_interval(self.incrementScore, 1)
        self.currentlyScheduledGlobal.append(scoreSchedule)

    def incrementScore(self, dt):
        self.gameMode.scoreNum += 1
        self.scoreText.text = "[size=40] SCORE " + str(self.gameMode.scoreNum) + "[/size]"

    def countDown(self, dt):
        if self.countDownNum == 0:
            self.countText.countNum.text = "[size= 130] *bam* [/size]"
            self.countDownNum = self.countDownReset
            Clock.schedule_once(self.clearText, 1)
            return False
        elif self.countDownNum == 1:
            self.countText.countNum.text = "[size= 130] *bam* [/size]"
        else:
            self.countText.countNum.text = "[size= 80]" + str(self.countDownNum) + "[/size]"
        self.countDownNum -= 1

    def clearText(self, dt=None):
        self.countText.countNum.text = ""

    def initMeteor(self, dt=None):
        meteor = Meteor()
        self.add_widget(meteor)
        self.numMeteorsCurrent += 1
        Clock.schedule_interval(meteor.move, 1 / 60)

        meteor.pos = random.randint(100, self.width), random.randint(self.height - 200, self.height)
        meteor.velocity_y = random.randint(1, 5)

        meteor.setPaddle(self.paddle)
        return False

    def mainLoop(self, dt=None):

        print(self.size)

        if self.numSurvivedCycles % self.gameMode.perCycleInit == 0:
            Clock.schedule_interval(self.countDown, 1)
            Clock.schedule_once(self.initMeteor, 5)

        self.numSurvivedCycles += 1

        print(self.numSurvivedCycles)

    def preGameInit(self, dt):
        # We use a very short interval for fear that two balls may fall out of bounds nearly simultaneously
        outOfBounds = Clock.schedule_interval(self.checkOutOfBounds, 0.1)
        self.currentlyScheduledGlobal.append(outOfBounds)

        Clock.schedule_once(self.initScore, 4)
        self.initLives()

    def checkOutOfBounds(self, dt):
        if self.outOfBounds:
            self.remove_widget(self.gameMode.lives.pop())
            self.outOfBounds = False
            if len(self.gameMode.lives) == 0:
                self.cleanUpProcedure()

    def cleanUpProcedure(self):
        self.countText.countNum.text = "[size=400]E[color=#FFFF00]ND[/color][/size]"
        for schedule in self.currentlyScheduledGlobal:
            print(schedule)
            schedule.cancel()


class EndGameException(Exception):
    pass
