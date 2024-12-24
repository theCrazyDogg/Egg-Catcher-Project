from itertools import cycle
from random import randrange
from tkinter import PhotoImage, Tk , Canvas , messagebox , font

canvas_width = 800
canvas_height = 400
win = Tk()
c = Canvas(win , width = canvas_width ,  height = canvas_height)
c.pack()
background_image = PhotoImage(file='background.png')
c.create_image(0, 0, image=background_image, anchor ='nw')

color_cycle = cycle(['blue' , 'light pink' , 'light yellow','light green' , 'red', 'blue' , 'green','black', 'white'])
egg_width = 45
egg_height = 55
egg_score = 10
egg_speed = 50
egg_interval = 4000
egg_image = PhotoImage(file='egg.png')
difficulty_factor = 0.95

catcher_width = 100
catcher_height = 100
catcher_image = PhotoImage(file='catcher.png')
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height -catcher_height - 20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

catcher = c.create_image(catcher_start_x, catcher_start_y, image=catcher_image, anchor='nw')

score = 0
score_text = c.create_text(10,10,anchor='nw' , font=('Arial',18,'bold'),fill='white',text='Score : ' + str(score))

lives_remaning = 3
lives_text = c.create_text(canvas_width-10,10,anchor='ne' , font=('Arial',18,'bold'),fill='white',text='Lives : ' + str(lives_remaning))

eggs = []

def create_eggs():
    x = randrange(10,740)
    y = 40
    new_egg = c.create_image(x, y, image=egg_image, anchor='nw')
    eggs.append(new_egg)
    win.after(egg_interval,create_eggs)

def move_eggs():
    for egg in eggs:
        (egg_x,egg_y) = c.coords(egg)
        c.move(egg,0,10)
        if egg_y + egg_height > canvas_height:
            egg_dropped(egg)
    win.after(egg_speed,move_eggs)

def egg_dropped(egg):
    eggs.remove(egg)
    c.delete(egg)
    lose_a_life()
    if lives_remaning == 0:
        f1=open("hii.txt",'r')
        y=(f1.read())
        x=int(y)
        if score>=x:
            x=str(score)
            f1=open("hii.txt",'w')
            f1.write(x)
            messagebox.showinfo("GAME OVER!","NewHighscore : "+" "+str(x))
        else:
            messagebox.showinfo("GAME OVER!","Your Score : "+" "+str(score)+"\n"+"Highest Score : "+" "+str(x))
        win.destroy()

def lose_a_life():
    global lives_remaning
    lives_remaning -= 1
    c.itemconfigure(lives_text , text='Lives : ' + str(lives_remaning))

def catch_check():
    (catcher_x,catcher_y) = c.coords(catcher)
    for egg in eggs:
        (egg_x,egg_y) = c.coords(egg)
        if catcher_x < egg_x < catcher_x + catcher_width and catcher_y < egg_y < catcher_y + catcher_height:
            eggs.remove(egg)
            c.delete(egg)
            increase_score(egg_score)
    win.after(100,catch_check)

def increase_score(points):
    global score , egg_speed , egg_interval
    score += points
    egg_speed = int(egg_speed * difficulty_factor)
    egg_interval = int(egg_interval * difficulty_factor)
    c.itemconfigure(score_text , text='Score : ' + str(score))

def move_left(event):
    (x, y) = c.coords(catcher)
    if x > 0:
        c.move(catcher,-20,0)

def move_right(event):
    (x, y) = c.coords(catcher)
    if x < canvas_width:
        c.move(catcher,20,0)


c.bind('<Left>' , move_left)
c.bind('<Right>' , move_right)
c.focus_set()

win.after(1000,create_eggs)
win.after(1000,move_eggs)
win.after(1000,catch_check)

win.mainloop()
