import csv
from tkinter import *
import pandas as pd
from random import randint
import time
BACKGROUND_COLOR = "#B1DDC6"
WHITE = '#FFFFFF'

# ---------------------------- Word selector ------------------------------- #

words = pd.read_csv('data/french_words.csv')
num_word = randint(0,len(words['French'])-1)
words_to_learn = pd.DataFrame(columns=['French','English'])
init_word = words['French'][num_word]

# ---------------------------- button functions ------------------------------- #

def get_word(input):
    print(input)
    global num_word, words, flip, words_to_learn
    window.after_cancel(flip)  # cancels flip timer of previous click

    if input:  # Check if got word right, if so drop
        words = words.drop(labels=num_word, axis=0)

    else:  # Else save word to learn file
        if words['French'][num_word] not in words_to_learn.values:
            word_row = words.iloc[[num_word]]
            words_to_learn = pd.concat([words_to_learn, word_row], ignore_index=True)
            words_to_learn.to_csv('data/words_to_learn.csv',index=False)

    print(len(words['French']))
    num_word = randint(0,len(words['French'])-1)
    fr_word = words['French'][num_word]

    canvas.itemconfig(img, image=card_front)
    canvas.itemconfig(word, text=fr_word, fill='black')
    canvas.itemconfig(lang, text='French', fill='black')
    flip = window.after(3000, show_eng)

def show_eng():
    eng_word = words['English'][num_word]
    canvas.itemconfig(img, image=card_back)
    canvas.itemconfig(lang, text='English', fill='white')
    canvas.itemconfig(word, text=eng_word, fill='white')

# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title('Password Generator')
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR) #add padding to window component
flip = window.after(3000, show_eng)

canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file='images/card_front.png')
card_back = PhotoImage(file='images/card_back.png')
img = canvas.create_image(400,263,image=card_front)
canvas.grid(column=1,row=1,columnspan=2)

lang = canvas.create_text(400,150,text='French', font=('Arial',40,'italic'))
word = canvas.create_text(400,263,text=init_word, font=('Arial',60,'bold'))
# get_word(FALSE)

right_image = PhotoImage(file="images/right.png")
right_button = Button(command=lambda: get_word(TRUE), image=right_image, highlightthickness=0, bg=BACKGROUND_COLOR)
right_button.grid(column=2,row=2)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(command=lambda: get_word(FALSE), image=wrong_image, highlightthickness=0, bg=BACKGROUND_COLOR)
wrong_button.grid(column=1,row=2)

window.mainloop()
