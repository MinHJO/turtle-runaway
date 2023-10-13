# This example is not working in Spyder directly (F5 or Run)
# Please type '!python turtle_runaway.py' on IPython console in your Spyder.
import tkinter as tk
import turtle, random, time

class RunawayGame:
    def __init__(self, canvas, runner, chaser, s_runner, catch_radius=50):
        self.canvas = canvas
        self.runner = runner
        self.s_runner = s_runner
        self.chaser = chaser
        self.catch_radius2 = catch_radius**2

        # Initialize 'runner' and 'chaser'
        self.runner.shape('turtle')
        self.runner.color('blue')
        self.runner.penup()

        self.chaser.shape('turtle')
        self.chaser.color('red')
        self.chaser.penup()

        self.s_runner.shape('turtle')
        self.s_runner.color('yellow')
        self.s_runner.penup()

        # Instantiate an another turtle for drawing
        self.drawer = turtle.RawTurtle(canvas)
        self.drawer.hideturtle()
        self.drawer.penup()

    def is_catched(self):
        p = self.runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
    
    def s_is_catched(self):
        p = self.s_runner.pos()
        q = self.chaser.pos()
        dx, dy = p[0] - q[0], p[1] - q[1]
        return dx**2 + dy**2 < self.catch_radius2
    
    # score
    def get_score(self):
        is_catched = self.is_catched()
        s_is_catched = self.s_is_catched()
        global score
        
        if is_catched:
            score += 1
            runner.hideturtle()
            self.runner.setpos((random.randint(-600, 600) / 2, 0))
            self.runner.setheading(random.randint(0, 350))
            runner.showturtle()
        
        # if you catch the intelligent turtle, you get more scores
        if s_is_catched:
            score += 2
            s_runner.hideturtle()
            self.s_runner.setpos((random.randint(-600, 600) / 2, 0))
            self.s_runner.setheading(random.randint(0, 350))
            s_runner.showturtle()
        
    def start(self, init_dist=400, ai_timer_msec=100):
        self.runner.setpos((-init_dist / 2, 0))
        self.runner.setheading(0)
        self.chaser.setpos((+init_dist / 2, 0))
        self.chaser.setheading(180)
        self.s_runner.setpos((0, +init_dist / 2))    
        self.s_runner.setheading(270)

        # TODO) You can do something here and follows.
        self.ai_timer_msec = ai_timer_msec
        self.canvas.ontimer(self.step, ai_timer_msec)
        # end the game after 60 secs
        self.canvas.ontimer(self.end, 5000)

    # if game is over, show the total score
    def end(self):
        global score
        self.canvas.clear()
        self.drawer.clear()
        text = "Game Over" + '\n' + "Score : %d" %score
        self.drawer.setpos(0, 20)
        self.drawer.write(text)
        score = 0        

    def step(self):
        self.runner.run_ai(self.chaser.pos(), self.chaser.heading())
        self.chaser.run_ai(self.runner.pos(), self.runner.heading())
        self.s_runner.s_run_ai(self.s_runner.pos(), self.s_runner.heading())
        
        # TODO) You can do something here and follows.
        global score
        self.drawer.undo()
        self.drawer.penup()
        self.drawer.setpos(-300, 300)
        self.get_score()
        self.drawer.write("Score : %d" %score)
        
        # Note) The following line should be the last of this function to keep the game playing
        self.canvas.ontimer(self.step, self.ai_timer_msec)

class ManualMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

        # Register event handlers
        canvas.onkeypress(lambda: self.forward(self.step_move), 'Up')
        canvas.onkeypress(lambda: self.backward(self.step_move), 'Down')
        canvas.onkeypress(lambda: self.left(self.step_turn), 'Left')
        canvas.onkeypress(lambda: self.right(self.step_turn), 'Right')
        canvas.listen()

    def run_ai(self, opp_pos, opp_heading):
        pass
    def s_run_ai(self, opp_pos, opp_heading):
        pass

class RandomMover(turtle.RawTurtle):
    def __init__(self, canvas, step_move=10, step_turn=10):
        super().__init__(canvas)
        self.step_move = step_move
        self.step_turn = step_turn

    def run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        if mode == 0:
            self.forward(self.step_move)
        elif mode == 1:
            self.left(self.step_turn)
        elif mode == 2:
            self.right(self.step_turn)
    
    # intelligent turtle
    def s_run_ai(self, opp_pos, opp_heading):
        mode = random.randint(0, 2)
        step_move = random.randint(10, 20)
        step_turn = random.randint(10, 20)
        if mode == 0:
            self.forward(step_move)
        elif mode == 1:
            self.left(step_turn)
        elif mode == 2:
            self.right(step_turn)

if __name__ == '__main__':
    # Use 'TurtleScreen' instead of 'Screen' to prevent an exception from the singleton 'Screen'
    root = tk.Tk()
    canvas = tk.Canvas(root, width=700, height=700)
    canvas.pack()
    screen = turtle.TurtleScreen(canvas)

    # TODO) Change the follows to your turtle if necessary
    runner = RandomMover(screen)
    chaser = ManualMover(screen)
    s_runner = RandomMover(screen)
    score = 0

    game = RunawayGame(screen, runner, chaser, s_runner)
    game.start()
    screen.mainloop()