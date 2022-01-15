

from baopig import *
import pygame
# pyapp.set_inapp_debugging()


class TimesUpScene(Scene):
    def __init__(self):

        Scene.__init__(self, app)

        Text(
            parent=self,
            text="The end !",
            pos=(0, -100),
            sticky="center",
            height=500,
            font_height=50
        )

        pygame.mixer.init()
        self.beep = pygame.mixer.Sound("turn-off-sound.mp3")  # TODO : fix sound not played

        Button(
            parent=self,
            text="Silence",
            pos=(-100, 0),
            sticky="center",
            command=pygame.mixer.stop
        )

        def restart():
            pygame.mixer.stop()
            self.app.mainscene.countdown.start()
            self.app.open("MainScene")
        Button(
            parent=self,
            text="Restart",
            pos=(100, 0),
            sticky="center",
            command=restart
        )

    def close(self):

        app.set_display_mode(0)

    def open(self):

        app.set_display_mode(pygame.FULLSCREEN)
        self.beep.play(loops=20)

    def receive(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                app.set_display_mode(pygame.FULLSCREEN)
            if event.key == pygame.K_g:
                app.set_display_mode(0)
            if event.key == pygame.K_SPACE:
                # app.mainscene.countdown.start()
                app.open("MainScene")


class MainScene(Scene):
    def __init__(self):

        app.set_caption("Programmer Countdown")

        Scene.__init__(
            self,
            app,
            background_color=(170, 170, 170)
        )

        h = 50

        def handle_enter(text):

            self.countdown.cancel()
            self.countdown.set_interval(float(text))
            self.countdown.start()

        def end():
            app.open("TimesUpScene")
            print("YO")
        self.countdown = Timer(
            1,
            # PrefilledFunction(print, "End of countdown"),
            # display.enter_fullscreen_mode,
            PrefilledFunction(app.open, "TimesUpScene"))

        self.pause_button = Button(
            parent=self,
            text="PAUSE",
            pos=(10, self.bottom - 40 - 10),
            command=self.countdown.pause
        )
        self.resume_button = Button(
            parent=self,
            text="RESUME",
            pos=(self.pause_button.right + 10, self.pause_button.top),
            command=self.countdown.resume
        )

        self.hide_button = Button(
            parent=self,
            text="Hide",
            pos=(self.width - 10, self.pause_button.top),
            pos_location="topright",
            command=pygame.display.iconify
        )

        def get_time_left():
            return format_time(float(self.countdown.get_time_left()))
        self.time_left = DynamicText(
            parent=self,
            get_text=get_time_left,
            pos=(10, 65),
            # pos=(0, 0),
            # h=h,
            font_height=h,
            # text_location="right",
            # pos_location="midright",
            # background_color=(240, 30, 30),
        )
        # self.time_left.right = self.right - 10

        self.input_box = NumEntry(
            parent=self,
            text=str(self.countdown.interval),
            pos=(10, 10),
            size=(self.w - 20, 40),
            command=handle_enter,
            # presentation_text="Entrez un temps en secondes",
            name="timeinput"
        )

    def close(self):

        if self.countdown.is_running:
            self.countdown.cancel()

    def receive(self, event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_f:
                app.set_display_mode(pygame.FULLSCREEN)
            if event.key == pygame.K_g:
                app.set_display_mode(0)
            if event.key == pygame.K_SPACE:
                if self.countdown.is_running:
                    self.countdown.pause()
                else:
                    self.countdown.resume()


app = Application()
app.set_style_for(Button, height=40)
app.mainscene = MainScene()
app.timesupscene = TimesUpScene()

keep_going = True
while keep_going:

    keep_going = False
    app.launch()

    if keep_going:
        i = input("Type something to restart the UI : ")
