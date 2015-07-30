#######################################################################
###
###     title:      BREAKEOUT
###     author:     deco
###     update:     2015/07/29
###
#######################################################################
from tkinter import *
import random
import time

# Collision Method
def point_collision(a , b):
    cx = ( b[2] - b[0]) / 2
    cy = ( b[3] - b[1]) /2
    r = cx
    #left-top
    dx = cx - a[0]
    dy = cy - a[1]
    p1 = dx**2 + dy**2 < r**2
    #right-top
    dx = cx - a[2]
    dy = cy - a[1]
    p2 = dx**2 + dy**2 < r**2
    #right-bottom
    dx = cx - a[2]
    dy = cy - a[3]
    p3 = dx**2 + dy**2 < r**2
    #left-bottom
    dx = cx - a[0]
    dy = cy - a[3]
    p4 = dx**2 + dy**2 < r**2

    return p1 or p2 or p3 or p4

## Ball Class
class Ball:
    def __init__( self, canvas, paddle, blocks, speed, color):
        self.canvas = canvas
        self.paddle = paddle
        self.speed = speed
        self.blocks = blocks
        self.id = canvas.create_oval( 10, 10, 25, 25, fill=color)
        self.canvas.move( self.id, 245, 300)
        self.x = 0
        self.y = 0
        self.canvas_height = canvas.winfo_height()
        self.canvas_width = canvas.winfo_width()
        self.hit_bottom = False
        # Score text
        self.score = 0
        self.score_text = TextLabel( canvas, 'SCORE:00000', WIDTH, 0, color='blue')
        self.score_text.show()
        self.canvas.bind_all( '<Button-1>', self.gamestart)

    def gamestart( self, evt):
        self.x = -self.speed
        self.y = self.speed

    def hit_paddle( self, pos):
        paddle_pos = self.canvas.coords( self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0] <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def hit_block( self, pos):
        collision_type = 0
        for block in self.blocks:
            block_pos = self.canvas.coords( block.id)
            #circle_collision check
            if point_collision( block_pos, pos):
                collision_type |= 3
            #top check
            if pos[2] >= block_pos[0] and pos[0] <= block_pos[2] and \
                    pos[3] >= block_pos[1] and pos[3] < block_pos[3]:
                collision_type |= 1
            #bottom check
            if pos[2] >= block_pos[0] and pos[0] <= block_pos[2] and \
                    pos[1] > block_pos[1] and pos[1] <= block_pos[3]:
                collision_type |= 1
            #left check
            if pos[3] >= block_pos[1] and pos[1] <= block_pos[3] and \
                    pos[2] >= block_pos[0] and pos[2] < block_pos[2]:
                collision_type |= 2
            #right check
            if pos[3] >= block_pos[1] and pos[1] <= block_pos[3] and \
                    pos[0] > block_pos[0] and pos[0] <= block_pos[2]:
                collision_type |= 2

        if collision_type != 0:
            return ( block, collision_type)
        return ( None, None)

    def draw( self):
        self.canvas.move( self.id, self.x, self.y)
        pos = self.canvas.coords( self.id)
        if pos[1] <= 0:
            self.y *= -1
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
        if self.hit_paddle(pos) == True:
            self.y *= -1
            if self.x > 0:
                self.x += 1
            else:
                self.x -= 1
        if pos[0] <= 0:
            self.x *= -1
        if pos[2] >= self.canvas_width:
            self.x *= -1

        ( target, collision_type) = self.hit_block( pos)
        if target != None:
            target.delete()
            del self.blocks[ self.blocks.index( target)]
            if ( collision_type & 1) != 0:
                self.y *= -1
            if ( collision_type & 2) != 0:
                self.x *= -1
            #Add score
            self.score += 100
            print(self.score)
            print(self.score_text)
            canvas.itemconfig( self.score_text.id, text='Score : {0:05d}'.format( self.score))

## Paddle Class
class Paddle:
    def __init__( self, canvas, speed, color):
        self.canvas = canvas
        self.speed = speed
        self.id = canvas.create_rectangle( 0, 0, 100, 10, fill=color)
        self.canvas.move( self.id, 200, 600)
        self.x = 0
        self.canvas_width = self.canvas.winfo_width()
        self.canvas.bind_all( '<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all( '<KeyPress-Right>', self.turn_right)

    def draw( self):
        self.canvas.move( self.id, self.x, 0)
        pos = self.canvas.coords( self.id)
        if pos[0] <= 0:
            self.x  = 0
        if pos[2] >= self.canvas_width:
            self.x = 0


    def turn_left( self, evt):
        self.x = -self.speed

    def turn_right( self, evt):
        self.x = self.speed

## Block Class
class Block:
    def __init__( self, canvas, x, y, color):
        self.canvas = canvas
        self.pos_x = x
        self.pos_y = y
        self.id = canvas.create_rectangle( 0, 0, 50, 20, fill=color)
        self.canvas.move( self.id, 25 + self.pos_x * 50, 25 + self.pos_y * 20)

    def delete( self):
        self.canvas.delete( self.id)

## GameoverLabel Class
class GameoverLabel:
    def __init__( self, canvas, color):
        self.canvas = canvas
        self.gameover = False
        self.canvas_centerX = canvas.winfo_width()/2
        self.canvas_centerY = canvas.winfo_height()/2
        self.id = canvas.create_text( self.canvas_centerX, self.canvas_centerY, anchor='center', font=( '', 50),
                text='GAME OVER', fill=color, state='hidden')
        def draw( self):
            if self.gameover == False:
                #canvas.itemconfig( self.id, state='normal')
                self.gameover = True

class TextLabel:
    def __init__( self, canvas, text, x, y, fontsize=20, color='black'):
        self.canvas = canvas
        self.id = canvas.create_text( 250, 200, text=text, fill=color,\
            font=('Times', fontsize), state='hidden')

    def show( self):
        self.canvas.itemconfig( self.id, state='normal')

## Main
# config
WIDTH = 500
HEIGHT = 700
FPS = 30
BALL_SPEED = 5
PADDLE_SPEED = 5
COLORS = ( 'red', 'green', 'blue', 'yellow', 'pink')
BLOCK_W = 9
BLOCK_H = 5
BLOCK_LIST = [ 0, 1, 0, 0, 0, 1, 0,
        0, 1, 0, 0, 1, 0, 0, 
        0, 0, 1, 1, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0 ]


# Initialize
tk = Tk()
tk.title( 'Breakeout')
tk.resizable( 0, 0)
tk.wm_attributes( '-topmost', 1)
canvas = Canvas( tk, width=WIDTH, height=HEIGHT, bd=0, highlightthickness=0)
canvas.pack()
tk.update()

# Create objects
blocks = []
for y in range( BLOCK_H):
    for x in range( BLOCK_W):
        blocks.append( Block( canvas, x, y, random.choice( COLORS)))
paddle = Paddle( canvas, PADDLE_SPEED, 'blue')
ball = Ball( canvas, paddle, blocks, BALL_SPEED, 'red')
gameover_text = GameoverLabel( canvas, 'red')

while True:
    if ball.hit_bottom == False:
        print( 'ball.hit_bottom == False')
        ball.draw()
        paddle.draw()
    else:
        print( 'ball.hit_bottom == True')
        gameover_text.draw()
    tk.update_idletasks()
    tk.update()
    time.sleep( 1/FPS)

