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

#creating the encoded word given to user
encodedWord = ["_"] * len(word)
polePhase=0
#ASCII for hangman pole itself
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


#Function for adding characters that are not within our word
def appendingChars(character):
    current = charList.get()
    # do not want repeats of characters in this
    if character not in current:
        new = current + character
        charList.set(new)

# Title
tk.Label(root, text="Hangman", fg="white", bg="black").pack()
#Encoded word
encoded = tk.Label(root, text=" ".join(encodedWord), bg="black", fg="white")
encoded.place(x=100, y=300)
#entry box that the user types guesses into
entry = tk.Entry(root, font=("Helvetica", 14))
entry.pack(pady=20)
#where the letters that are NOT in the word are displayed
exludedBank = tk.Label(root, text="letters: ", bg="black", fg="white")
exludedBank.place(x=300, y=300)
charList = tk.StringVar(value="")  # since no characters were grabbed, this set should be empty
excluded = tk.Label(root, textvariable=charList, bg="black", fg="white")
excluded.place(x=300, y=325)
# actual game time now:

#when game ends this is function to quit
def stop():
    global cont
    cont = False
    root.destroy()

#when game ends if the user decides to keep playing this function happens
def repeat():
    python = sys.executable
    # uses subprocess.Popen to launch new instance of current script
    # sys.argv contains the script name and any origional CLI arguments
    subprocess.Popen([python] + sys.argv)
    sys.exit(0)

#every time submit guess button is pressed
def guess():
    #initialize global variables
    global polePhase
    global encodedWord
    #grab user input
    input = entry.get()
    #if user just straight up types the encoded word
    if input == word:
        for widget in root.winfo_children():
            widget.destroy()
        quitButton = tk.Button(root, text="Quit", command=stop)
        quitButton.place(x=300, y=100)
        restart = tk.Button(root, text="Restart!", command=repeat)
        restart.place(x=50, y=100)
        how = tk.Label(root, text="Amazing work! continue?", fg="white", bg="black")
        how.place(x=150, y=100)
    #if they place characters instead or just giving which characters in the word the user typed are not contained in the word
    else:
        #iterate over each character in user input
        for char in input:
            #if guessed character is not in the word
            if char not in word:
                #adding characters to excluded list
                appendingChars(char)
                polePhase += 1
            #some character is in the word
            else:
                #for each character in the word
                for index, letter in enumerate(word):
                    #check if character is the letter in the word
                    if char == letter:
                        #switch out the blank for our character
                        encodedWord[index] = char
                #re-create encoded word
                encoded.configure(text=" ".join(encodedWord))
                #check to see if our word is the actual word
                if ("".join(encodedWord) == word):
                    #clear screen and create 2 buttons that we will offer to either restart game, or quit game
                    for widget in root.winfo_children():
                        widget.destroy()
                    quitButton = tk.Button(root, text="Quit", command=stop)
                    quitButton.place(x=300, y=100)
                    restart = tk.Button(root, text="Restart!", command=repeat)
                    restart.place(x=50, y=100)
                    encouragement = tk.Label(root, text="Good job on getting it right!", fg="white", bg="black")
                    encouragement.place(x=150, y=100)
        #logic for setting the pole phases of the game
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
        #user loses
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
#submit guess
button = tk.Button(root, text="submit guess", command=guess)
button.place(x=200, y=100)
#create our phases of our poles
phase = tk.Label(root, text=poleStart, bg="black", fg="white", justify="left")
phase.place(x=100, y=100)
#loop
root.mainloop()
