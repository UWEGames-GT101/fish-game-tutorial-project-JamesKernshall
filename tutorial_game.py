import datetime
import random
import pyasge
from gamedata import GameData


def isInside(sprite, mouse_x, mouse_y) -> bool:
    bounds = sprite.getWorldBounds()

    if bounds.v1.x < mouse_x < bounds.v2.x and bounds.v1.y < mouse_y < bounds.v3.y:
        return True
    else:
        return False

    pass


class MyASGEGame(pyasge.ASGEGame):
    """
    The main game class
    """

    def __init__(self, settings: pyasge.GameSettings):
        """
        Initialises the game and sets up the shared data.

        Args:
            settings (pyasge.GameSettings): The game settings
        """
        pyasge.ASGEGame.__init__(self, settings)
        self.renderer.setClearColour(pyasge.COLOURS.BLACK)

        # create a game data object, we can store all shared game content here
        self.data = GameData()
        self.data.inputs = self.inputs
        self.data.renderer = self.renderer
        self.data.game_res = [settings.window_width, settings.window_height]

        # register the key and mouse click handlers for this class
        self.key_id = self.data.inputs.addCallback(pyasge.EventType.E_KEY, self.keyHandler)
        self.mouse_id = self.data.inputs.addCallback(pyasge.EventType.E_MOUSE_CLICK, self.clickHandler)

        # set the game to the menu
        self.menu = True
        self.play_option = None
        self.exit_option = None
        self.menu_option = 0

        # This is a comment
        self.data.background = pyasge.Sprite()
        self.initBackground()

        #
        self.menu_text = None
        self.initMenu()

        #
        self.scoreboard = None
        self.multipler_Text = None
        self.initScoreboard()

        self.flickTimer = 0
        self.comboMultipler = 1

        # This is a comment
        self.fishTextures = []
        self.fish = pyasge.Sprite()
        self.initFish()

    def initBackground(self) -> bool:
        if self.data.background.loadTexture("/data/images/background.png"):

            self.data.background.z_order = -100
            return False
        else:
            return False
        pass

    def initFish(self) -> bool:
        if self.fish.loadTexture("/data/images/kenney_fishpack/fishTile_073.png"):
            self.fish.z_order = 1
            self.fish.scale = 1
            self.spawn()
            self.fishTextures.append(self.fish)

        tempFish = pyasge.Sprite()

        self.LoadFish(tempFish, "/data/images/kenney_fishpack/fishTile_075.png")
        self.LoadFish(tempFish, "/data/images/kenney_fishpack/fishTile_077.png")
        self.LoadFish(tempFish, "/data/images/kenney_fishpack/fishTile_079.png")
        self.LoadFish(tempFish, "/data/images/kenney_fishpack/fishTile_081.png")
        pass

    def LoadFish(self, tempFish, fileName):
        if tempFish.loadTexture(fileName):
            tempFish.z_order = 1
            tempFish.scale = 1
            self.fishTextures.append(tempFish)
        pass


    def initScoreboard(self) -> None:
        self.scoreboard = pyasge.Text(self.data.fonts["MainFont"])
        self.scoreboard.string = str(self.data.score).zfill(5)
        self.scoreboard.position = [1300, 75]
        self.scoreboard.colour = pyasge.COLOURS.CORNFLOWER
        
        self.multipler_Text = pyasge.Text(self.data.fonts["MainFont"])
        self.multipler_Text.string = ""
        self.multipler_Text.position = [1300,200]
        self.multipler_Text.colour = pyasge.COLOURS.CORNFLOWER
        pass

    def initMenu(self) -> bool:
        self.data.fonts["MainFont"] = self.data.renderer.loadFont("/data/fonts/KGHAPPY.ttf", 64)
        self.menu_text = pyasge.Text(self.data.fonts["MainFont"])
        self.menu_text.string = "Flicker Fish Star"
        self.menu_text.position = [400,400]
        self.menu_text.colour = pyasge.COLOURS.BLACK

        self.play_option = pyasge.Text(self.data.fonts["MainFont"])
        self.play_option.string = ">PLAY"
        self.play_option.position = [200, 600]
        self.play_option.colour = pyasge.COLOURS.GOLD

        self.exit_option = pyasge.Text(self.data.fonts["MainFont"])
        self.exit_option.string = "EXIT"
        self.exit_option.position = [600, 600]
        self.exit_option.colour = pyasge.COLOURS.GREY

        return True

    def clickHandler(self, event: pyasge.ClickEvent) -> None:
        if event.action == pyasge.MOUSE.BUTTON_PRESSED and event.button == pyasge.MOUSE.MOUSE_BTN1:

            if isInside(self.fish, event.x, event.y):
                self.data.score += int((2 / self.flickTimer) * self.comboMultipler)
                self.flickTimer = 0
                self.scoreboard.string = str(self.data.score).zfill(5)
                self.spawn()
                self.comboMultipler += 0.25
                if (self.comboMultipler >= 1.4):
                    self.multipler_Text.string = str(round(self.comboMultipler, 2)) + "X"
                    

            else:
                self.multipler_Text.string = ""
                self.comboMultipler = 1
        pass

    def keyHandler(self, event: pyasge.KeyEvent) -> None:

        if event.action == pyasge.KEYS.KEY_PRESSED:

            if event.key == pyasge.KEYS.KEY_RIGHT or event.key == pyasge.KEYS.KEY_LEFT:
                self.menu_option = 1 - self.menu_option


                if self.menu_option == 0:
                    self.play_option.string = ">START"
                    self.play_option.colour = pyasge.COLOURS.GOLD
                    self.exit_option.string = " EXIT"
                    self.exit_option.colour = pyasge.COLOURS.GRAY
                else:
                    self.play_option.string = " START"
                    self.play_option.colour = pyasge.COLOURS.GRAY
                    self.exit_option.string = ">EXIT"
                    self.exit_option.colour = pyasge.COLOURS.GOLD

            if event.key == pyasge.KEYS.KEY_ENTER:
                if self.menu_option == 0:
                    self.menu = False
                else:
                    self.signal_Exit()
            if event.key == pyasge.KEYS.KEY_F:
                self.spawn()
        pass

    def spawn(self) -> None:

        #self.fish = self.fishTextures[random.randint(0, len(self.fishTextures))]

        self.fish.x = random.randint(0, self.data.game_res[0] - self.fish.width)
        self.fish.y = random.randint(0, self.data.game_res[1] - self.fish.height)
        self.fish.scale = random.randint(1, 20) * 0.1

        pass

    def update(self, game_time: pyasge.GameTime) -> None:

        if self.menu:
            # update the menu here
            pass
        else:
            # update the game here
            self.flickTimer += game_time.frame_time

            if (self.flickTimer > 2):
                self.comboMultipler = 1
                self.multipler_Text.string = ""
            pass

    def render(self, game_time: pyasge.GameTime) -> None:
        """
        This is the variable time-step function. Use to update
        animations and to render the gam    e-world. The use of
        ``frame_time`` is essential to ensure consistent performance.
        @param game_time: The tick and frame deltas.
        """
        self.data.renderer.render(self.data.background)
        self.data.renderer.render(self.scoreboard)

        if self.menu:
            self.data.renderer.render(self.menu_text)
            self.data.renderer.render(self.play_option)
            self.data.renderer.render(self.exit_option)
            pass
        else:
            # render the game here
            self.data.renderer.render(self.fish)
            self.data.renderer.render(self.multipler_Text)
            pass


def main():
    """
    Creates the game and runs it
    For ASGE Games to run they need settings. These settings
    allow changes to the way the game is presented, its
    simulation speed and also its dimensions. For this project
    the FPS and fixed updates are capped at 60hz and Vsync is
    set to adaptive.
    """
    settings = pyasge.GameSettings()
    settings.window_width = 1600
    settings.window_height = 900
    settings.fixed_ts = 60
    settings.fps_limit = 60
    settings.window_mode = pyasge.WindowMode.BORDERLESS_WINDOW
    settings.vsync = pyasge.Vsync.ADAPTIVE
    game = MyASGEGame(settings)
    game.run()


if __name__ == "__main__":
    main()
