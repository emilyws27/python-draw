#!/usr/bin/python
#JustGotFileStreamToWork.py

from tkinter import *
from tkinter.colorchooser import askcolor as ac
from pyscreenshot import grab
import random
import Pmw

__author__  = "Emily Sheehan - Coder & Procrastinator"
__version__ = 1.0

"""Welcome to my final project. This application contains two main sections: 
   the regular drawing app and the drawing game.
   
   I drew my inspiration from Microsoft Paint, although my app has just a fraction
   of the features and tools. Nonetheless, I created the "inverted infinity" tool. 
   The application uses tkinter for graphics.                                       
"""


class start_up():
    """This is called to initialize the application. It allows user to choose which 
       path they'd like to follow (either game or drawing), and gives instructions."""
    
    def __init__(self):
        self.start = Tk()
        self.start.title("Emily's Final Project - Take 2") #take 2 b/c take1 was a disaster
        self.start.geometry("300x200")
        
        self.msgs = Pmw.Balloon(self.start)
        
        
        self.buttonFrame = Frame(self.start, background="green")
        
        
        self.doodleButton = Button(self.start, text="Doodle", command=self.draw)
        self.doodleButton.pack()
        
        self.msgs.bind(self.doodleButton, "click here to simply draw!")
        
        self.play_game = Button(self.start, text="Play A Game", command=self.play)
        self.play_game.pack()
        self.msgs.bind(self.play_game, "click here for a two person game!")
        
        self.instructions = Label(self.start, text="To simply draw, click 'Doodle'.\n" +
                                                   "\n" +
                                                   "For the game, two players are needed.\n" + 
                                                   "P1 must draw the word \n" +
                                                   " given on the screen in the allotted time. \n" +
                                                   "P2 must then guess correctly the word in time.")
        self.instructions.configure(background="dodger blue", foreground="white")
        self.instructions.pack()
        self.start.mainloop()
        
    def draw(self):
        Painter()           #makes a Paint object
    def play(self):
        Game().start_it() #makes a Game object
        
class Painter():
    """This class creates the canvas and controls all of the drawing and artist interaction."""
    
    def __init__(self, gameActive=False):
        
        self.defaultPen = 3.0 
        self.regularCol = 'black'
        
        
        self.root = Tk()
        self.root.title("Emily's Final Project")
        self.root.geometry('%dx%d+%d+%d' % (600, 600, 0, 23)) #positions at these coordinates on the comp. screen
        
        self.picker = Tk()
        self.picker.title("Options")
        self.picker.geometry('%dx%d+%d+%d' % (273, 150, 615, 23))
        self.shapeVar = StringVar(self.root)
        self.shapeVar.set("Line")
        
        #Top frame that contains pen, erase, take pic, color
        self.option_menu_top = Frame(self.picker, width=500, height=100)
        self.option_menu_top.config(background="black", padx=10, pady=10)
        self.option_menu_top.grid(row=0, columnspan=4)
        
        #bottom frame that contains slider and shapes
        self.option_menu_bottom = Frame(self.picker, background="green", width=500, height=100)
        self.option_menu_bottom.grid(row=1, columnspan=4)
                        

        self.pen = Button(self.option_menu_top, text="Pen", command=self.use_pen, cursor="spraycan")
        self.pen.config(padx=5, pady=5)
        self.pen.grid(row=0, column=1)

        self.color = Button(self.option_menu_top, text="Color", command=self.choose_color)
        self.color.config(padx=5, pady=5)
        self.color.grid(row=0, column=2)
        
        self.eraser = Button(self.option_menu_top, text="Eraser", command=self.use_eraser, cursor="cross_reverse")
        self.eraser.config(padx=5, pady=5)        
        self.eraser.grid(row=0, column=3)
        
        self.save = Button(self.option_menu_top, text="Save Drawing", command=self.save_img)
        self.save.config(padx=5, pady=5)
        self.save.grid(row=0, column=4)
        
        self.shapes = ["Choose A Shape", "Line", "Inverted Infinity", "Square", "Circle"]
        self.drawShapes = OptionMenu(self.option_menu_top, self.shapeVar, *self.shapes)
        self.drawShapes.config(padx=5, pady=5)        
        self.drawShapes.grid(row=2, columnspan=4)

        self.penSizeLabel = Label(self.option_menu_bottom, text="Pen Size: ")
        self.penSizeLabel.grid(row=0,columnspan=4)
        
        self.chooseSize = Scale(self.option_menu_bottom, from_=1, to=15, orient=HORIZONTAL)
        self.chooseSize.set(self.defaultPen)
        self.chooseSize.grid(row=1, columnspan=4)

        self.canvasDraw = Canvas(self.root, bg='white', width=600, height=600) #canvas to draw on
        self.canvasDraw.pack()
        
        self.setup() 
        
        if not gameActive:
            self.root.mainloop()

    def setup(self):
        """This method basically just sets everything up for the canvas.
           It sets all of the variables to their default so that the user
           can begin to draw."""
        
        self.lastX = None #none b/c haven't clicked/dragged
        self.lastY = None
        
        #gets all the current presets 
        self.line_width = self.chooseSize.get()
        self.shape = self.shapeVar.get()
        self.color = self.regularCol
        self.eraser_on = False
        self.triggeredB = self.pen #tool in use
        self.canvasDraw.bind('<B1-Motion>', self.paint) #binds mouse motion to paint function
        self.canvasDraw.bind('<ButtonRelease-1>', self.reset) 

    def use_pen(self):
        """Pen tool: calls activate button which initiates drawing with pen"""
        
        self.triggerTool(self.pen)

    def choose_color(self):
        """Opens color dialogue box to choose paint color."""
        
        self.eraser_on = False
        self.color = ac(color=self.color)[1]

    def use_eraser(self):
        """Sets pen tool to white"""
        
        self.triggerTool(self.eraser, erasing=True)
    
    def save_img(self):
        """Takes screenshot of screen at specific coordinates.
           These coordinates are the coordinates where the canvas is 
           placed on the screen."""
        
        im = grab(bbox=(0, 43, 600, 600))
        im.show() #opens it in preview

    def triggerTool(self, toolClicked, erasing=False):
        """Takes button clicked (tool chosen) and sets
           the necessary variables for paint function."""
        
        self.triggeredB.config(relief=RAISED)
        toolClicked.config(relief=SUNKEN)
        self.triggeredB = toolClicked
        self.eraser_on = erasing

    def paint(self, event):
        """Method responsible for the actual "drawing" on the 
           canvas. It uses the variables set in triggeredTool()
           to draw apropriately. """
        
        #print("hi")
        self.line_width = self.chooseSize.get()
        
        if self.eraser_on:
            paint_color = 'white' 
        else:
            paint_color = self.color
            
        if self.lastX and self.lastY:
            
            if self.shapeVar.get() == "Line":
                self.canvasDraw.create_line(self.lastX, self.lastY, event.x, event.y,
                                            width=self.line_width, fill=paint_color,
                                            capstyle=ROUND, smooth=TRUE, splinesteps=30)
                
            if self.shapeVar.get()  == "Square":
                self.canvasDraw.create_rectangle(self.lastX, self.lastY, event.x + self.line_width,
                                                 event.y + self.line_width, fill=paint_color, outline=paint_color)
            if self.shapeVar.get()  == "Circle":
                self.canvasDraw.create_oval(self.lastX, self.lastY, event.x + self.line_width,
                                                 event.y + self.line_width, fill=paint_color, outline=paint_color)
            if self.shapeVar.get()  == "Inverted Infinity":
                self.canvasDraw.create_polygon(self.lastX, self.lastY, 
                                               (event.x + self.line_width)/2, (event.y + self.line_width)/2,
                                               event.x + self.line_width, event.y + self.line_width, fill=paint_color,
                                               outline=paint_color)
            
        self.lastX = event.x
        self.lastY = event.y        

    def reset(self, event):
        self.lastX, self.lastY = None, None

class Game(Painter):
    """This class inherits from the Paint class. In theory, it is supposed to run
    a game like "Draw Something" where one player is given a word to draw within an
    amt. of time and the other player has to guess.
    
    However, this class is not running and if chosen in the start up menu, it will just 
    act like a regular Painter() object.
    
    On paper, I think it works, but there are likely some errors in the code that I am 
    unaware of because it is not running properly. """
    
    def __init__(self):
        Painter.__init__(self, True) #takes everything 
        self.options = ["Dog", "Cat", "Bird", "Giraffe",
                        "Elephant", "Human", "Pencil",
                        "Cheeseburger", "Charlie", "Monkey",
                        "Bagel", "Frog", "Pig", "Apple", 
                        "Strawberry", "Carrot"]
        #possible drawing choices 
        self.countdown_start_time = 30 #time on the clock to draw(seconds)
        self.time_left = 0
        self.user_guess = ""
        
        self.p1_score = 0 #player scores
        self.p2_score = 0
        self.num_rounds = 0 #if even, p1=drawer. if odd, p2 = drawer
        
        self.score_board = Tk() #scoreboard window
        self.score_board.geometry('%dx%d+%d+%d' % (364, 200, 900, 23))
        self.score_board.configure(bg="dodger blue")
        self.score_board.grid_propagate(False)
        
        self.msg = Pmw.Balloon(self.score_board)
        
        
        ###ALL COUNTDOWN RELATED THINGS ARE COMMENTED OUT BC COULDNT GET IT TO WORK###
        #self.countdown_frame = Frame(self.score_board, bg="red", width=80, height=80)
        #self.countdown_frame.
        #self.countdown_label = Label(self.countdown_frame, text ="TIMER", fg="Blue")
        #self.countdown_label.grid(row=0, column=0)
        
        self.word_frame = Frame(self.score_board, width=80, height=80)
        self.word_frame.grid(row=0, column=0, padx=10, pady=10)
        
        self.score_frame = Frame(self.score_board, width=80, height=80)
        self.score_frame.grid(row=0, column=1,padx=10, pady=10)
        
        self.word_label = Label(self.word_frame, text="Current Word: \n")
        self.word_label.grid(row=0, column=0, sticky="nesw")
        
        self.score_p1_label = Label(self.score_frame, fg="black", text= "P1: " + "pts")
        self.score_p1_label.grid(row=0, column=0,padx=10, pady=10)
        
        self.score_p2_label = Label(self.score_frame, fg="black", text="P2: " + str(self.p2_score) + "pts")
        self.score_p2_label.grid(row=0, column=1, padx=10, pady=10) 
        
        self.startButton = Button(self.score_board, text="Let's Begin", command=self.startGame)   
        self.startButton.grid(row=1, columnspan=2, padx=10, pady=10)
        #self.start_it()
        self.msg.bind(self.startButton, "Instructions: to begin, click this button. \n"
                     + "The game requires 2 players. The first player will be given a word \n"
                     + "and must draw this word. The second player will then guess the drawing. \n"
                     + "points will be added for each correct guess")
                     
        
        self.score_board.mainloop()
                
        #print(self.word)
    def startGame(self):
        
        self.startButton.destroy()
        if len(self.options) == 0:
            print('Game Over!\n' +
                  'Final Score: \n' + 
                  'Player 1: ' + str(self.p1_score) + '\n' +
                  'Player 2: ' + str(self.p2_score) + '\n')
        else:   
            self.word  = random.choice(self.options)
            self.options.remove(self.word)
            self.score_p1_label.configure(text= "P1: " + str(self.p1_score) + " pts")
            self.score_p2_label.configure(text="P2: " + str(self.p2_score) + " pts")
            self.word_label.configure(text="Current Word: \n" + self.word)
            
            self.endButton = Button(self.score_board, text="I'm Done Drawing", command=self.get_guess)
            self.endButton.grid(row=1, column=0, padx=10, pady=10)
        #self.countdown(30)
        
    def start_it(self):
        """This method is called immediately when the user chooses to play the game.
        It makes the word visible as well as the scoreboard and clock."""
        pass
        
        #self.countdown(30)
    
        
    def update_score(self):
        """Updates scoreboard after each round of drawing"""
        
        self.score_p1_label.configure(text="P1: " + str(self.p1_score))
        self.score_p2_label.configure(text="P2: " + str(self.p2_score))
        self.num_rounds += 1
        
        self.startGame()
        
    def check_guess(self, guessed_word):
        """Checks player's guess against the actual randomly
        selected word."""
        self.answer_button.destroy()
        self.answer.destroy()
        if self.num_rounds % 2 == 0: #if p1 drawing
            if guessed_word.upper() == self.word.upper():
                self.p1_score += 10
                self.update_score()
            else:
                self.score_p1_label.configure(text="WRONG!")
        else: #if p2 drawing
            if guessed_word.upper() == self.word.upper():
                self.p2_score += 10
                self.update_score()
            else:
                self.score_p1_label.configure(text="WRONG!")
        nextRound = Button(self.score_board, text="Next Round", command=self.nextRound)
        nextRound.grid(row=3, columnspan=3, padx=10, pady=10)
        #self.startGame()
        
    def nextRound(self):
        """calls startGame for subsequent rounds after the first"""
        self.startGame()
        
    def get_guess(self):
        """Gets guess from entry field"""
        self.endButton.destroy()
        
        self.answer = Entry(self.score_board)
        self.answer.grid(row=2, column=0)
        
        self.word_label.configure(text="WORD HIDDEN")
        
        self.answer_button=Button(self.score_board, text="Guess", 
                                  command=lambda:self.check_guess(self.answer.get()))
        self.answer_button.grid(row=3, column=0, padx=10, pady=10)
        
    def countdown(self, count):
        """starts countdown for the drawer. This method was taken from Bryan Oakley
           on stack overflow, and modified by me to update the tkinter GUI.
           
           It does not work which is why it is never used in my code. When I delete the #s, it 
           lags a ton and does not refresh the label to show the countdown ticks, but waits 30 seconds, 
           the proper time nonetheless, until it calls the entry box (which is right, but it never displays
           the countdown)"""
        
        if count > 0:
            count -=1
            #self.countdown_label['text'] = count
            #self.countdown_label.configure(text=count)
            self.countdown_frame.after(1000, self.countdown(count))
        if count == 0:
            self.countdown_label.configure(text="TIME'S UP")
            self.word_label.configure(text="WORD HIDDEN")
            self.get_guess()
                            
        """if remaining is not None:
            remaining = remaining
            self.countdown_label.config(text="%d" % remaining) #%d refers to integer in tupple
        if remaining <= 0:
            
            #self.check_guess(self.user_guess)
        else:
            self.countdown_label.config(text="%d" % remaining)
            remaining -= 1
            self.countdown_frame.after(1000, self.countdown()) #calls to update clock every second (1000 milliseconds)."""