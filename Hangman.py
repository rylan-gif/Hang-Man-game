import tkinter as tk
import sys
import subprocess
import requests
import random
#logic for gathering random words:

word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
response = requests.get(word_site)
WORDS = response.content.splitlines()
# choosing random word
wordSlice = str(random.choice(WORDS))
word = wordSlice[2:-1]


encodedWord = ["_"] * len(word)
polePhase=0

poleStart = ("      - - - - - -\n "
             "      |          |\n"
             "       |\n"
             "       |\n"
             "       |\n"
             "       |\n"
             "- - - - - - -")
pole1 = ("      - - - - - - \n"
         "       |          |\n"
         "       |          O\n"
         "       |\n"
         "       |\n"
         "       |\n"
         "- - - - - - -\n")
pole2 = ("      - - - - - -\n "
         "      |          |\n"
         "       |          O\n"
         "       |          |\n"
         "       |\n"
         "       |\n"
         "- - - - - - -\n")
pole3 = ("      - - - - - - \n"
         "       |          |\n"
         "       |          O\n"
         "       |          |\\\n"
         "       |\n"
         "       |\n"
         "- - - - - - -\n")
pole4 = ("      - - - - - - \n"
         "       |          |\n"
         "       |          O\n"
         "       |         /|\\\n"
         "       |\n"
         "       |\n"
         "- - - - - - -\n")
pole5 = ("      - - - - - - \n"
         "       |          |\n"
         "       |          O\n"
         "       |         /|\\\n"
         "       |           \\\n"
         "       |\n"
         "- - - - - - -\n")
death = ("      - - - - - - \n"
         "      |          |\n"
         "      |          O\n"
         "      |         /|\\\n"
         "      |         / \\\n"
         "      |\n"
         "- - - - - - -\n")
root = tk.Tk()
# create window with base geometry
root.title("Hangman")
root.configure(background="black")
root.minsize(400, 400)
root.maxsize(500, 500)
root.geometry("300x300+50+50")


# create our initial window before game starts
def appendingChars(character):
    current = charList.get()
    # do not want repeats of characters in this
    if character not in current:
        new = current + character
        charList.set(new)

# create labels
tk.Label(root, text="Hangman", fg="white", bg="black").pack()

encoded = tk.Label(root, text=" ".join(encodedWord), bg="black", fg="white")
encoded.place(x=100, y=300)
entry = tk.Entry(root, font=("Helvetica", 14))
entry.pack(pady=20)
exludedBank = tk.Label(root, text="letters: ", bg="black", fg="white")
exludedBank.place(x=300, y=300)
charList = tk.StringVar(value="")  # since no characters were grabbed, this set should be empty
excluded = tk.Label(root, textvariable=charList, bg="black", fg="white")
excluded.place(x=300, y=325)
# actual game time now:


def stop():
    global cont
    cont = False
    root.destroy()


def repeat():
    python = sys.executable
    # uses subprocess.Popen to launch new instance of current script
    # sys.argv contains the script name and any origional CLI arguments
    subprocess.Popen([python] + sys.argv)
    sys.exit(0)


def guess():
    global polePhase
    global encodedWord
    input = entry.get()
    if input == word:
        for widget in root.winfo_children():
            widget.destroy()
        quitButton = tk.Button(root, text="Quit", command=stop)
        quitButton.place(x=300, y=100)
        restart = tk.Button(root, text="Restart!", command=repeat)
        restart.place(x=50, y=100)
        how = tk.Label(root, text="Amazing work! continue?")
        how.place(x=100, y=100)

    else:
        for char in input:
            if char not in word:
                appendingChars(char)
                polePhase += 1
            else:
                if char in word:
                    for index, letter in enumerate(word):
                        if char == letter:
                            encodedWord[index] = char
                    encoded.configure(text=" ".join(encodedWord))

                if ("".join(encodedWord) == word):
                    for widget in root.winfo_children():
                        widget.destroy()
                    quitButton = tk.Button(root, text="Quit", command=stop)
                    quitButton.place(x=300, y=100)
                    restart = tk.Button(root, text="Restart!", command=repeat)
                    restart.place(x=50, y=100)
                    encouragement = tk.Label(root, text="Good job on getting it right!", fg="white", bg="black")
                    encouragement.place(x=100, y=100)
        if polePhase == 1:
            phase.config(text=pole1)
        elif polePhase == 2:
            phase.config(text=pole2)
        elif polePhase == 3:
            phase.config(text=pole3)
        elif polePhase == 4:
            phase.config(text=pole4)
        elif polePhase == 5:
            phase.config(text=pole5)
        if polePhase == 6:
            for widget in root.winfo_children():
                widget.destroy()
            deathScreen = tk.Label(root, text="You Lose, Continue?", fg="white", bg="black")
            deathScreen.place(x=150, y=200)
            quitButton = tk.Button(root, text="Quit", command=stop)
            quitButton.place(x=300, y=100)
            restart = tk.Button(root, text="Restart!", command=repeat)
            restart.place(x=50, y=100)
            DEADMAN = tk.Label(root, text=death, fg="white", bg="black", justify="left")
            DEADMAN.place(x=200, y=200)
            CorrectWord = tk.Label(root, text=f"The correct word was {word}", fg="white", bg="black")
            CorrectWord.place(x=100, y=50)

button = tk.Button(root, text="submit guess", command=guess)
button.place(x=200, y=100)

phase = tk.Label(root, text=poleStart, bg="black", fg="white", justify="left")
phase.place(x=100, y=100)
# create the window
root.mainloop()