from kivy.app import App
from kivy.config import Config
from kivy.lang import Builder
from kivy.properties import (
    NumericProperty, ReferenceListProperty, ObjectProperty
)
from kivy.uix.widget import Widget

Config.set('graphics', 'resizable', '0')
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '800')
from kivy.vector import Vector
from kivy.clock import Clock


Builder.load_string("""
<PongBall>:
    size: 30, 30
    canvas:
        Ellipse:
            pos: self.pos
            size: self.size

<PongPaddle>:
    size: 100, 15
    canvas:
        Rectangle:
            pos: self.pos
            size: self.size

<PongGame>:
    ball: pong_ball
    player1: player_left
    player2: player_right

    canvas:
        Rectangle:
            pos: 0, 400
            size: 360, 10

    Label:
        font_size: 70
        center_x: root.width / 4
        top: root.top - 50
        text: str(root.player1.score)

    Label:
        font_size: 70
        center_x: root.width / 4
        top: root.top - 450
        text: str(root.player2.score)

    PongBall:
        id: pong_ball
        center: self.parent.center

    PongPaddle:
        id: player_left
        y: root.y
        center_x: root.center_x

    PongPaddle:
        id: player_right
        y: 785
        center_x: root.center_x
""")

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx, vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.y, vel.x + offset


class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self, vel=(0, 4)):
        self.ball.center = self.center
        self.ball.velocity = vel

    def update(self, dt):
        self.ball.move()

        # bounce of paddles
        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        # bounce ball off bottom or top
        if (self.ball.y < self.y):
            self.serve_ball(vel=(0, 2))
            self.player1.score += 1
        if (self.ball.top > self.top):
            self.serve_ball(vel=(0, -2))

            self.player2.score += 1
        # went of to a side to score point?
        if self.ball.x < self.x:
            self.ball.velocity_x *= -1

        if self.ball.right > self.width:
            self.ball.velocity_x *= -1

    def on_touch_move(self, touch):
        if touch.y < self.width / 3:
            self.player1.center_x = touch.x
        if touch.y > self.width - self.width / 3:
            self.player2.center_x = touch.x


class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 120.0)
        return game


if __name__ == '__main__':
    PongApp().run()