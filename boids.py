import random
import math
from tkinter import *

WIDTH = 800
HEIGHT = 600
BOIDS = 20
WALL = 100
WALL_FORCE = 10
SPEED_LIMIT = 500
BOID_RADIUS = 8
OFFSET_START = 20


def main():
    initialise()
    mainloop()


def initialise():
    build_boids()
    build_graph()

def build_graph():
    global graph
    root = Tk()
    root.overrideredirect(True)
    root.geometry('%dx%d+%d+%d' % (
    WIDTH, HEIGHT, (root.winfo_screenwidth() - WIDTH) / 2, (root.winfo_screenheight() - HEIGHT) / 2))
    root.bind_all('<Escape>', lambda event: event.widget.quit())
    graph = Canvas(root, width=WIDTH, height=HEIGHT, background='black')
    graph.after(40, update)
    graph.pack()


def update():
    draw()
    move()
    graph.after(40, update)


def draw():
    graph.delete(ALL)
    for boid in boids:
        x1 = boid.position.x - BOID_RADIUS
        y1 = boid.position.y - BOID_RADIUS
        x2 = boid.position.x + BOID_RADIUS
        y2 = boid.position.y + BOID_RADIUS

        graph.create_oval((x1, y1, x2, y2), fill='white')
    graph.update()


def move():
    for boid in boids:
        simulate_wall(boid)
    for boid in boids:
        boid.update_velocity(boids)
    for boid in boids:
        boid.move()


def simulate_wall(boid):
    if boid.position.x < WALL:
        boid.velocity.x += WALL_FORCE
    elif boid.position.x > WIDTH - WALL:
        boid.velocity.x -= WALL_FORCE
    if boid.position.y < WALL:
        boid.velocity.y += WALL_FORCE
    elif boid.position.y > HEIGHT - WALL:
        boid.velocity.y -= WALL_FORCE


def limit_speed(boid):
    if boid.velocity.mag() > SPEED_LIMIT:
        boid.velocity /= boid.velocity.mag() / SPEED_LIMIT


def build_boids():
    global boids
    boids = tuple(Boid(WIDTH, HEIGHT, OFFSET_START) for boid in range(BOIDS))


class TwoD:

    def __init__(self, x, y):
        self.x = float(x)
        self.y = float(y)

    def __repr__(self):
        return 'TwoD(%s, %s)' % (self.x, self.y)

    def __add__(self, other):
        return TwoD(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return TwoD(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return TwoD(self.x * other, self.y * other)

    def __truediv__(self, other):
        return TwoD(self.x / other, self.y / other)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __isub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __idiv__(self, other):
        if isinstance(other, TwoD):
            self.x /= other.x if other.x else 1
            self.y /= other.y if other.y else 1
        else:
            self.x /= other
            self.y /= other
        return self

    def mag(self):
        return math.sqrt((self.x ** 2) + (self.y ** 2))



class Boid:

    def __init__(self, width, height, offset):
        self.velocity = TwoD(400, 300)
        self.position = TwoD(*self.random_start(width, height, offset))
        self.viewrange = 30

    def difference(self, other):
        return math.sqrt((other.position.x - self.position.x) ** 2 + (other.position.y - self.position.y) ** 2)


    def random_start(self, width, height, offset):
        if random.randint(0, 1):
            y = random.randint(1, height)
            if random.randint(0, 1):
                x = -offset
            else:
                x = width + offset
        else:
            x = random.randint(1, width)
            if random.randint(0, 1):
                y = -offset
            else:
                y = height + offset
        return x, y

    def update_velocity(self, boids):
        v1 = self.rule1(boids)
        v2 = self.rule2(boids)
        v3 = self.rule2(boids)
        self.temp = v1 + v2 + v3

    def move(self):
        self.velocity += self.temp
        limit_speed(self)
        self.position += self.velocity / 100

    def rule1(self, boids):
        # clumping
        vector = TwoD(0, 0)
        N = 2
        for boid in boids:
            if boid is not self:
                vector += boid.position
                N += 1
        vector /= N-1
        return (vector - self.position) / 90

    def rule2(self, boids):
        # avoidance
        vector = TwoD(0, 0)
        for boid in boids:
            if boid is not self and self.difference(boid) <= self.viewrange:
                if (self.position - boid.position).mag() < self.viewrange:
                    vector -= (boid.position - self.position)
        return vector / 2

    def rule3(self, boids):
        # schooling
        vector = TwoD(0, 0)
        N = 2
        for boid in boids:
            if boid is not self and self.difference(boid) <= self.viewrange:
                vector += boid.velocity
        vector /= N-1
        return (vector - self.velocity) / 8


if __name__ == '__main__':
    main()
