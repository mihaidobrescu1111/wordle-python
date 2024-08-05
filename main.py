from tkinter import *
from tkinter import messagebox
import random

entry_list = []
entry_var_list = []
x = 1
y = 0
ie = 0
word = ""
next_word = 0
game_won = False

with open("score.txt", "r") as file:
    score = int(file.read())

with open("output.txt", "r") as file:
    word_list_final = [line.strip() for line in file]

word_to_guess = random.choice(word_list_final)

screen = Tk()
screen.title("Wordle")
screen.minsize(500, 600)
screen.config(pady=20, padx=50)

score_label = Label(text=f"Score: {score}", font=("Courier", 10, "normal"))
score_label.grid(row=0, column=0)

text = Label(text="Wordle", font=("Courier", 20, "normal"))
text.grid(row=0, column=1, columnspan=3)


def on_entry_change(*args):
    global ie
    if ie < 30:
        if len(entry_var_list[ie].get()) == 1:
            ie += 1
    if ie % 5 != 0:
        entry_list[ie].focus()


def delete():
    global ie
    global next_word
    for index in range(6):
        if ie < 30:
            if entry_list[ie].focus_get() == entry_list[index * 5]:
                return 0
    if ie >= 1:
        if ie % 5 == 0 and len(entry_var_list[ie - 1].get()) == 1:
            entry_var_list[ie - 1].set("")
            ie -= 1
        elif len(entry_var_list[ie].get()) == 0:
            entry_var_list[ie - 1].set("")
            entry_list[ie - 1].focus()
            ie -= 1


def submit_word():
    global word
    global next_word
    word = ""
    for k in range(5):
        word += entry_var_list[5 * next_word + k].get()
    if len(word) == 5:
        if word not in word_list_final:
            messagebox.showinfo(message="Word is not in list")
        else:
            next_word += 1
            if next_word <= 5:
                entry_list[next_word * 5].focus()
            check_word()


def check_word():
    global word_to_guess
    global word
    global next_word
    global score
    global game_won
    if next_word == 6 and game_won is False:
        messagebox.showinfo(message=f"You lost!\nWord was {word_to_guess}")
        new_game()
    if word_to_guess.lower() == word.lower():
        score += 1
        score_label.config(text=f"Score: {score}")
        with open("score.txt", "w") as file1:
            file1.write(str(score))
        game_won = True
        messagebox.showinfo(message=f"You won!\nWord was {word_to_guess}")
        new_game()
    else:
        word_dict = {}
        for char in word_to_guess:
            if char not in word_dict:
                word_dict[char] = 1
            else:
                word_dict[char] += 1
        for j in range(len(word_to_guess)):
            print(word_to_guess[j], word[j])
            if word_to_guess[j] == word[j]:
                entry_list[(next_word - 1) * 5 + j].config(bg="green")
                word_dict[word[j]] -= 1
                print()
        for char in word:
            if char in word_to_guess and word_dict[char] > 0 and entry_list[(next_word - 1) * 5 + j]["background"] != "green":
                idx = word.index(char)
                if 5 > idx > 0:
                    entry_list[(next_word - 1) * 5 + idx].config(bg="yellow")
                    word_dict[char] -= 1


def new_game():
    global word_to_guess
    global ie
    global word
    global next_word
    word_to_guess = random.choice(word_list_final)
    ie = 0
    entry_list[ie].focus()
    for entry1 in entry_list:
        entry1.delete(0, END)
        entry1.config(bg="white")
    next_word = 0
    word = ""


for i in range(30):
    entry_var = StringVar()
    entry_var.trace("w", on_entry_change)
    entry_var_list.append(entry_var)
    entry = Entry(width=2, highlightthickness=10, font=("Courier", 30, "normal"), justify="center",
                  textvariable=entry_var)
    if i % 5 == 0 and i != 0:
        x += 1
        y = 0
    entry.grid(row=x, column=y)
    y += 1
    entry_list.append(entry)

submit = Button(text="Submit", bg="green", width=20, height=1, font=("Courier", 20, "normal"), fg="white",
                highlightthickness=5, command=submit_word)
submit.grid(row=7, column=0, columnspan=5)

backspace = Button(text="⌫", command=delete, width=6)
backspace.grid(row=0, column=4)

entry_list[0].focus()
screen.mainloop()
