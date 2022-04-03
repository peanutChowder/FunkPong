import random

from kivy.uix.widget import Widget


from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, ReferenceListProperty


from kivy.clock import Clock

from fuPongObjects import Meteor


class CountDown(Widget):
    pass


class QModeProperties:
    def __init__(self):
        self.quantityDict = {1: 2, 2: 3, 3: 4, 4: 5, 5: 6, 6: 7, 7: 10, 8: 20}
        self.ballAccel = 0.02
        self.horizontalAccel = 0

        self.currentLevel = 1
        self.numCyclesLvlUp = 6

        self.finalLevel = 8


class QuantityMode(Widget):
    gameMode = ObjectProperty(QModeProperties())
    
    countText = ObjectProperty(None)
    countDownReset = NumericProperty(5)
    countDownNum = NumericProperty(5)

    paddle = ObjectProperty(None)

    numSurvivedCycles = NumericProperty(0)
    numMeteorsCurrent = NumericProperty(0)

    outOfBounds = BooleanProperty(False)    # This is literally only used for survival mode, kinda ugly try to get rid

    currentlyScheduledGlobal = ReferenceListProperty()

    def displayLevel(self):
        if self.gameMode.currentLevel == self.gameMode.finalLevel:
            self.countText.countNum.text = "[size= 130] *FINALLEVEL* [/size]"
        else:
            self.countText.countNum.text = "[size= 130] *LEVEL%d* [/size]" % self.gameMode.currentLevel

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
        if not self.tooManyMeteors():

            countDown = Clock.schedule_interval(self.countDown, 1)
            self.currentlyScheduledGlobal.append(countDown)

            Clock.schedule_once(self.initMeteor, 5)

        self.numSurvivedCycles += 1
        print(self.numSurvivedCycles)

        print(self.width)
        self.checkLevelUp()

    def preGameInit(self, dt):
        # TODO: maybe move some stuff in here so it's tidier?
        pass

    def tooManyMeteors(self):
        if self.numMeteorsCurrent >= self.gameMode.quantityDict[self.gameMode.currentLevel]:
            return True
        else:
            return False

    def checkLevelUp(self):
        if self.gameMode.currentLevel == self.gameMode.finalLevel:
            print("FINAL")

        elif self.numSurvivedCycles >= self.gameMode.numCyclesLvlUp:
            # Above, the second condition ensures this elif branch does not modify anything on the final level
            self.numSurvivedCycles = 0
            self.gameMode.currentLevel += 1
            self.displayLevel()

            if self.gameMode.currentLevel > 4:
                self.paddle.width = self.width / 3
            else:
                self.paddle.width = self.paddle.width + (self.gameMode.currentLevel * 40)
