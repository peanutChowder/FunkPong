from kivy.uix.widget import Widget
from kivy.vector import Vector

from kivy.properties import ObjectProperty, BooleanProperty, NumericProperty, ReferenceListProperty

from kivy.clock import Clock

class Roof(Widget):
    def initRoof(self, fuModeObj):
        self.size = fuModeObj.width, 10
        self.center_y = 200
        self.fuModeObject = fuModeObj

        collideSchedule = Clock.schedule_interval(self.checkRoofCollision, 1/30)
        self.fuModeObject.gameMode.scheduledObjects.append(collideSchedule)

    def checkRoofCollision(self, dt):
        if self.fuModeObject.realMeteor.center_y > self.center_y and self.fuModeObject.realMeteor.velocity_y > 0:
            print(self.fuModeObject.realMeteor.center_y)
            self.fuModeObject.realMeteor.velocity_x *= 3
            self.fuModeObject.realMeteor.velocity_y *= -1

class InvertedPaddle(Widget):
    fuModeObject = ObjectProperty(None)
    paddleMovable = BooleanProperty(False)
    nvrtPaddle = ObjectProperty(None)

    # Paddle velocity calculation stuff
    pos1 = NumericProperty(0)
    pos2 = NumericProperty(0)
    posList = ReferenceListProperty(pos1, pos2)
    currentPos = NumericProperty(0)
    velocity = NumericProperty(0)

    def initInvert(self, fuModeObject):
        # TODO: Note that if the ball is out of screen while this is called, it will never return to screen until event is over
        self.fuModeObject = fuModeObject
        self.pos = self.fuModeObject.paddle.pos
        print("Center set to:", self.center) # TODO: delete me
        self.size = self.fuModeObject.paddle.size


        # TODO: should we somehow add this clock schedule to the scheduledObjects list?
        Clock.schedule_interval(self.shiftPaddleLeft, 1/60)


    def shiftPaddleLeft(self, dt):
        if self.fuModeObject.realMeteor.center_x < self.fuModeObject.width - 210:
            self.fuModeObject.realMeteor.center_x += 5
        elif self.fuModeObject.realMeteor.center_x > self.fuModeObject.width - 200:
            self.fuModeObject.realMeteor.center_x -= 5

        if self.fuModeObject.realMeteor.center_y > self.fuModeObject.height / 2 + 10:
            self.fuModeObject.realMeteor.center_y -= 5
        elif self.fuModeObject.realMeteor.center_y < self.fuModeObject.height / 2 - 10:
            self.fuModeObject.realMeteor.center_y += 5

        if self.center_x > 70:
            self.center_x -= 3
        print(self.center_x)
        if (self.center_x <= 70) and (self.fuModeObject.realMeteor.center_y < self.fuModeObject.height / 2 + 10):
            Clock.schedule_interval(self.morphPaddle, 1/60)
            return False

    def morphPaddle(self, dt):
        if self.size[0] == 10:
            if self.size[1] == 120:
                print("Done moving the fake paddle")
                self.paddleMovable = True
                self.fuModeObject.gameMode.horizontalAccel = 0.02
                self.InitAxisGameplay()
                return False
            else:
                self.size[1]+= 2
        else:
            self.size[0] -= 2

    def on_touch_down(self, touch):
        self.velocity = 0

    def on_touch_move(self, touch):
        if not self.paddleMovable:
            return False

        self.center_y = touch.pos[1]

        self.posList[self.currentPos] = self.center_y
        if self.currentPos == 1:
            self.calcPaddleVelocity()
        self.changePosRec()

    def calcPaddleVelocity(self):
        self.velocity = self.pos2 - self.pos1

    def changePosRec(self):
        if self.currentPos == 0:
            self.currentPos = 1
        else:
            self.currentPos = 0

    def InitAxisGameplay(self):
        self.fuModeObject.gameMode.horizontalAccel = 0.02
        invertSchedule = Clock.schedule_interval(self.meteorMovement, 1/60)
        self.fuModeObject.gameMode.scheduledObjects.append(invertSchedule)
        Clock.schedule_once(self.invertOver, 15)

    def meteorMovement(self, dt):
        """
        Since the default movement borders are as follows: {0, 0, width, height}, we will modify by "distanceFromEdge"
        to create a temporary barrier
        :return:
        """
        # TODO:
        #   - bounce off paddle
        #   - bounce off top and bottom
        #   - endgame when touching left
        distanceFromEdge = 100

        if (self.fuModeObject.realMeteor.center_y > self.fuModeObject.height - distanceFromEdge) or (self.fuModeObject.realMeteor.center_y < distanceFromEdge):
            print("Reversed")
            self.fuModeObject.realMeteor.velocity_y *= -1

        if self.collide_widget(self.fuModeObject.realMeteor):
            self.fuModeObject.realMeteor.velocity_x *= -1
            self.fuModeObject.realMeteor.velocity_y = self.velocity

        if self.fuModeObject.realMeteor.center_x < 5:
            self.fuModeObject.realMeteor.center = (-1, -10)
            return False

    def invertOver(self, dt=None):
        self.fuModeObject.add_widget(self.fuModeObject.paddle)
        self.fuModeObject.gameMode.ballAccel = 0.02
        self.fuModeObject.gameMode.horizontalAccel = 0
        self.fuModeObject.gameMode.removeWidgets()




class Shit(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    fuModeobject = ObjectProperty()

    def setFuMode(self, fuModeObject):
        self.fuModeobject = fuModeObject

    def move(self, dt):
        self.pos = Vector(self.velocity) + self.pos

        if (self.center_x > self.fuModeobject.width) or (self.center_x < 0):
            self.velocity_x *= -1
        if (self.center_y > self.fuModeobject.height) or (self.center_y < 0):
            self.velocity_y *= -1

        self.checkCollide()


        # TODO: implementation of the end of this event: do a delayed schedule_once of notOutOfBounds for the duration of the event
        # return self.notOutBounds()

    def checkCollide(self):
        if self.collide_widget(self.fuModeobject.realMeteor):
            temp_x = self.velocity_x
            temp_y = self.velocity_y

            self.velocity_x -= (self.fuModeobject.realMeteor.velocity_x * 0.3)
            self.velocity_y -= (self.fuModeobject.realMeteor.velocity_y * 0.3)

            self.fuModeobject.realMeteor.velocity_x += (temp_x * 0.3)
            self.fuModeobject.realMeteor.velocity_y += (temp_y * 0.3)

    def notOutBounds(self):
        if self.center_x < 200:
            self.parent.remove_widget(self)
            return False
        return True