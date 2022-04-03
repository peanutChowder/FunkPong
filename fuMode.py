"""
ball number mechanic:
- in std state have just 1 ball

elimination mechanic gameplay:
- Lives?
- something similar to quantity mode, where you can't be eliminated
    - perhaps have a score that increments for
- no lives, instant elimination but a single ball

score mechanic:
- score increments for number of events survived (or seconds)
-

Ideas for events:
- we can also reuse the shit object w/ 0,0,0 colour to give the impression that the ball is flying randomly
- shit idea
- flip axis: make the "down" on the side of the screen. Put the paddle there, make acceleration go that way, etc.
- ball count increases greatly
- giant ball
- fake balls: make multiple balls that are "bombs". when paddle hits them, game ends.
- free paddle: paddle can be moved freely, no longer bound to a single axis


- Holograph: multiple balls of same size same colour init close to the same position to confuse user. The holo balls
can leave the screen without the game ending, but the og cannot
- """
# TODO: this is just a copy paste. modify it

from random import randint

from kivy.uix.widget import Widget

from fuPongObjects import Meteor
from fuModeObjects import Shit, InvertedPaddle, Roof

from kivy.properties import ObjectProperty, NumericProperty, BooleanProperty, ReferenceListProperty


from kivy.clock import Clock





class FModeProperties:
    def __init__(self, fuModeObject):
        self.fuModeObject = fuModeObject
        self.ballAccel = 0.02
        self.horizontalAccel = 0

        self.scoreNum = 0

        self.beginEvent = False

        self.eventStrList = ["[color=#FFFF00]FLYING[/color]SHIT", "[color=#FFFF00]SWITCH[/color]SIDES", "[color=#FFFF00]HEAVY[/color]BALL", "[color=#FFFF00]ROOF[/color]BALL"]
        self.eventList = [self.flyingShit, self.invertAxis, self.heavyBall, self.roofBall]
        self.eventDurationList = [5, 20]

        self.scheduledObjects = []          # currently not necessary
        self.addedWidgets = []

    def flyingShit(self):
        # TODO:
        #   - init more than one shit object
        #   - create a "base case" or delayed schedule_once that remove_widget the shit objects
        #   - give a randomization factor to the size of the shits during init
        #   -
        numOfShits = 10
        print("EVENT SHIT")
        for shitNum in range(10):
            shit = Shit()
            self.addedWidgets.append(shit)

            shit.pos = self.fuModeObject.width - 20, randint(100, self.fuModeObject.height - 100)
            shit.velocity = (randint(-8, -2), randint(-5, 5))
            shit.size = (randint(20,50), randint(20, 50))

            self.fuModeObject.add_widget(shit)
            shit.setFuMode(self.fuModeObject)

            shitSchedule = Clock.schedule_interval(shit.move, 1/60)            # Note this isn't appended to currentlyScheduledGlobal, depending on it being cancel() via hitting sides of scrn

            self.scheduledObjects.append(shitSchedule)
        Clock.schedule_once(self.removeWidgets, 20)

    def removeWidgets(self, dt=None):

        print("removeWidgets ACTIVATED")
        for schedule in self.scheduledObjects:
            schedule.cancel()
        for widget in self.addedWidgets:
            print(widget)
            self.fuModeObject.remove_widget(widget)
        Clock.schedule_once(self.setBeginEventTrue, 5)         # The delay is so that events are not back to back

    def setBeginEventTrue(self, dt=None):
        self.beginEvent = True

    def beginEventTrue(self, dt=None):
        self.beginEvent = True

    def invertAxis(self):
        # TODO: for each event, make it so that there is an exit point where the above is set to false
        invert = InvertedPaddle()
        self.addedWidgets.append(invert)
        self.fuModeObject.add_widget(invert)

        invert.pos = self.fuModeObject.paddle.pos

        self.fuModeObject.remove_widget(self.fuModeObject.paddle)

        self.fuModeObject.realMeteor.velocity_x = 0
        self.fuModeObject.realMeteor.velocity_y = 0
        self.ballAccel = 0

        invert.initInvert(self.fuModeObject)

    def heavyBall(self):
        self.ballAccel = 0.7
        self.fuModeObject.realMeteor.velocity_y = 5
        self.fuModeObject.realMeteor.size = (100, 100)
        Clock.schedule_once(self.resetBallProp, 10)         # These two
        Clock.schedule_once(self.removeWidgets, 10)         # should be the same time

    def resetBallProp(self, dt):
        self.fuModeObject.realMeteor.velocity_y = 2
        self.ballAccel = 0.02
        self.fuModeObject.realMeteor.size = (20, 20)

    def roofBall(self):
        roof = Roof()
        roof.initRoof(self.fuModeObject)

        self.fuModeObject.realMeteor.velocity_y *= 3

        self.fuModeObject.add_widget(roof)
        self.addedWidgets.append(roof)


        Clock.schedule_once(self.removeWidgets, 10)  # should be the same time


class FuMode(Widget):
    gameMode = ObjectProperty(None)

    paddle = ObjectProperty(None)

    numSurvivedCycles = NumericProperty(0)

    outOfBounds = BooleanProperty(False)

    scoreText = ObjectProperty(None)

    currentlyScheduledGlobal = ReferenceListProperty()
    # ==================== New Attributes
    realMeteor = ObjectProperty(None)
    countText = ObjectProperty(None)
    numMeteorsCurrent = NumericProperty(0)

    def initScore(self):
        print("INITIALIZED SCORE")
        self.scoreText.text = "[size=40] SCORE " + str(self.gameMode.scoreNum) + "[/size]"
        scoreSchedule = Clock.schedule_interval(self.incrementScore, 1)
        self.currentlyScheduledGlobal.append(scoreSchedule)

    def incrementScore(self, dt):
        self.gameMode.scoreNum += 1
        self.scoreText.text = "[size=40] SCORE " + str(self.gameMode.scoreNum) + "[/size]"

    def initMeteor(self, dt=None):
        self.numMeteorsCurrent += 1
        self.realMeteor = Meteor()
        self.realMeteor.color = 1, 0, 1
        self.add_widget(self.realMeteor)
        meteorSchedule = Clock.schedule_interval(self.realMeteor.move, 1 / 60)
        self.currentlyScheduledGlobal.append(meteorSchedule)

        self.realMeteor.pos = randint(100, self.width), randint(self.height - 200, self.height)
        self.realMeteor.velocity_y = randint(-5, -1)

        self.realMeteor.setPaddle(self.paddle)


    def mainLoop(self, dt=None):

        if self.numSurvivedCycles == 0:
            self.gameMode = FModeProperties(self)
            Clock.schedule_once(self.initMeteor, 1)

        if self.gameMode.beginEvent:
            self.handleEvent()
            self.gameMode.beginEvent = False

        self.numSurvivedCycles += 1

        print(self.numSurvivedCycles)

    def preGameInit(self, dt):
        # TODO: make this shit
        # We use a very short interval for fear that two balls may fall out of bounds nearly simultaneously

        outOfBoundsSchedule = Clock.schedule_interval(self.checkOutOfBounds, 1/61)
        self.currentlyScheduledGlobal.append(outOfBoundsSchedule)

        Clock.schedule_once(self.gameMode.beginEventTrue, 3)

        self.initScore()

    def handleEvent(self):
        # TODO: TEMPORARY TESTING ZONE
        self.gameMode.beginEvent = False
        # eventIndex = 3

        eventIndex = randint(0, len(self.gameMode.eventStrList) - 1)



        self.countText.countNum.text = "[size=100]" + self.gameMode.eventStrList[eventIndex] + "[/size]"
        Clock.schedule_once(self.clearEventText, 2)
        self.gameMode.eventList[eventIndex]()

        # Clock.schedule_interval(self.gameMode.removeWidgets, 1)    Checking for event over wil be done by event objects

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
