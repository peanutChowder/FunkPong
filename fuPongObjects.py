
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.uix.widget import Widget

class Paddle(Widget):
    pos1 = NumericProperty(0)
    pos2 = NumericProperty(0)
    posList = ReferenceListProperty(pos1, pos2)
    currentPos = NumericProperty(0)
    velocity = NumericProperty(0)

    def on_touch_move(self, touch):
        self.center_x = touch.x
        self.posList[self.currentPos] = touch.pos[0]
        if self.currentPos == 1:
            self.calcVelocity()
        self.changePosRec()

    def calcVelocity(self):
        self.velocity = self.pos2 - self.pos1

    def changePosRec(self):
        if self.currentPos == 0:
            self.currentPos = 1
        else:
            self.currentPos = 0


class Meteor(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)


    def move(self, dt):
        self.pos = Vector(self.velocity) + self.pos
        self.velocity_y -= self.parent.gameMode.ballAccel
        self.velocity_x -= self.parent.gameMode.horizontalAccel
        self.hitPaddle()
        self.hitSide()

        return self.notOutBounds()

    def hitSide(self):
        if (self.center_x < 0) or (self.center_x > self.parent.width):
            self.velocity_x *= -1

    def hitPaddle(self):
        if self.collide_widget(self.paddle):
            self.velocity_y *= -1
            self.velocity_x = (self.paddle.velocity * 0.5)

    def setPaddle(self, paddle):
        self.paddle = paddle

    def notOutBounds(self):
        # TODO: note that this was recently changed from "outOfWindow
        if self.center_y < 0:
            self.parent.numMeteorsCurrent -= 1
            self.parent.numSurvivedCycles = 0
            self.parent.outOfBounds = True      # literally only here for survival mode (actually also fuMode now)
            self.parent.remove_widget(self)
            return False
        return True