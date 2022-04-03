# TODO: create the score object.
#   - Also find a way for the game's processes to stop but not the App itself
from fuPongObjects import Paddle
from quantityMode import QuantityMode
from survivalMode import SurvivalMode, EndGameException
from fuMode import FuMode
from dashMode import DashMode

from kivy.uix.widget import Widget

from kivy.clock import Clock
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.properties import NumericProperty, ObjectProperty, ReferenceListProperty



class GameModeSelect:
    def __init__(self):
        self.gameModeList = ["QUANTITY", "SURVIVAL", "FU", "DASH"]
        self.descriptionList = ["[size=20]FOR THOSE THAT SUCK. NO ELIMINATION.[/size]",  "[size=20]JUST TRY TO SURVIVE.[/size]", "[size=20]EVENTS.[/size]", "[size=20]OBSTACLES.[/size]"]

class WelcomeScreen(Screen):

    modeIndex = NumericProperty(0)
    selectGameMode = ObjectProperty(GameModeSelect())

    def changeGameMode(self):
        self.modeIndex = (self.modeIndex + 1) % len(self.selectGameMode.gameModeList)
        self.modeText.text = "[size=50][color=#FFFF00]" + self.selectGameMode.gameModeList[self.modeIndex] +"[/color]MODE[/size]"
        self.modeDesc.text = self.selectGameMode.descriptionList[self.modeIndex]

        print("Changed mode-------------")
        print(self.modeIndex)


class WindowManager(ScreenManager):
    pass


class GameScreen(Screen):
    def beginGame(self, modeIndex):
        print("Begin game modeINdex:", modeIndex)
        modes = [QuantityMode, SurvivalMode, FuMode, DashMode]
        print("BEGUN===========================")
        game = modes[modeIndex]()

        game.paddle = Paddle()
        game.add_widget(game.paddle)

        game.paddle.size = 120, 10

        game.mainLoop()

        preGame = Clock.schedule_once(game.preGameInit, 2)
        mainLoop = Clock.schedule_interval(game.mainLoop, 6)

        game.currentlyScheduledGlobal.append(preGame)
        game.currentlyScheduledGlobal.append(mainLoop)


        self.add_widget(game)




class MeteorApp(App):
    def build(self):
        manager = WindowManager()
        return manager


try:
    MeteorApp().run()
except EndGameException: # This is an ugly temporary solution
    print("bub")