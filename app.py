import pandas as pd
import os
import getch
import random
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# External vocab list
df = pd.read_csv("vocab.csv")

# Clear the terminal screen
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

# Variables
gameInfo = {
    'answer': '',
    'answerColumn': 0,
    'answerRow': 0,
    'history': np.empty((99, 5), dtype=np.dtype('U100')),
    'correct': 0,
    'language': '',
    'notLanguage': '',
    'option': 0,
    'optionMenu': 0,
    'playerAnswer': '',
    'question': 1,
    'questionColumn': 0,
    'questionRow': 0,
    'questions': 20,  # 20 is default
    'word': '',
}

# Reset Variables
def gameReset(gameInfo):
    numQuestions = gameInfo['questions']
    gameInfo.clear()
    gameInfo.update({
        'answer': '',
        'answerColumn': 0,
        'answerRow': 0,
        'history': np.empty((99, 5), dtype=np.dtype('U100')),
        'correct': 0,
        'language': '',
        'notLanguage': '',
        'option': 0,
        'optionMenu': 0,
        'playerAnswer': '',
        'question': 1,
        'questionColumn': 0,
        'questionRow': 0,
        'questions': numQuestions,
        'word': '',
    }
)

# Home Menu
def menu(gameInfo):
    clear_terminal()
    while not (1 <= gameInfo['option'] <= 3):
        print("Select an option:\n1: Start\n2: Options\n3: Exit\n")
        try:
            gameInfo['option'] = int(getch.getch())
            return gameInfo['option']
        except ValueError:
            gameInfo['option'] = 0
        
# Randoms question from external csv
def newQuestion(gameInfo):
    gameInfo['answerColumn'] = random.choice(df.columns)
    if gameInfo['answerColumn'] == 'Japanese':
        gameInfo['language'] = 'Japanese'
        gameInfo['notLanguage'] = 'English'
    elif gameInfo['answerColumn'] == 'English':
        gameInfo['language'] = 'English'
        gameInfo['notLanguage'] = 'Japanese'
    gameInfo['answerRow'] = random.randint(0, len(df) - 1)
    gameInfo['answer'] = df.loc[gameInfo['answerRow'] , gameInfo['answerColumn']]
    gameInfo['word'] = df.loc[gameInfo['answerRow'] , gameInfo['notLanguage']]

# General Question Loop
def gameQuestion(gameInfo):
    #print(f"The answer is {gameInfo['answer']}")
    print(f"Correct: {gameInfo['correct']}")
    gameInfo['playerAnswer'] = input(f"Question {gameInfo['question']} of {gameInfo['questions']}:\n\nWhat is {gameInfo['word']} in {gameInfo['language']}?\n\n\t")

# Checks input against expected answer, tallys correct answers
def checkAnswer(gameInfo):
    gameInfo['history'][gameInfo['question'] - 1][3] = gameInfo['word']
    gameInfo['history'][gameInfo['question'] - 1][4] = gameInfo['language']
    if gameInfo['answer'].lower() in gameInfo['playerAnswer'].lower():
        gameInfo['correct'] += 1
        print("Correct!\n")
        gameInfo['history'][gameInfo['question'] - 1][2] = "O"  # Adjust index to start from 0
        gameInfo['history'][gameInfo['question'] - 1][3] = gameInfo['word']
    else:
        print(f"Incorrect! The answer was {gameInfo['answer']}")  # Use f-string for proper formatting
        gameInfo['history'][gameInfo['question'] - 1][2] = "X"  # Adjust index to start from 0

    gameInfo['history'][gameInfo['question'] - 1][1] = gameInfo['answer']  # Adjust index to start from 0
    gameInfo['history'][gameInfo['question'] - 1][0] = gameInfo['playerAnswer']  # Adjust index to start from 0

# Main script flow
def game(gameInfo):
    while gameInfo['option'] == 1:
        gameInfo['question'] = 1
        for gameInfo['question'] in range(1, gameInfo['questions'] + 1):
            newQuestion(gameInfo)
            gameQuestion(gameInfo)
            clear_terminal()
            checkAnswer(gameInfo)
        results(gameInfo)
        gameInfo['option'] = 0

# Draws Results table then sends users back to home menu
def results(gameInfo):
    clear_terminal()
    data = []

    font_path = 'font.ttf'  # Your font path goes here
    fm.fontManager.addfont(font_path)
    prop = fm.FontProperties(fname=font_path)

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = prop.get_name()

    print(f"\n\n\tYou answered {gameInfo['correct']} questions correctly!\n")

    for gameInfo['question'] in range(0, gameInfo['questions']):
        row_data = []
        row_data.append(str(gameInfo['question'] + 1))# Question Number
        row_data.append(f"{gameInfo['history'][gameInfo['question']][3]}") # Word
        row_data.append(f"{gameInfo['history'][gameInfo['question']][0]}") # Your Answer
        row_data.append(f"{gameInfo['history'][gameInfo['question']][1]}") # Correct Answer
        row_data.append(f"{gameInfo['history'][gameInfo['question']][2]}") # O or X
        data.append(row_data)

    fig, ax = plt.subplots(figsize=(8, (gameInfo['questions'] / 2 - 1)))
    ax.axis('tight')
    ax.axis('off')

    table = ax.table(cellText=data, colLabels=['Q', 'Word', 'Your Answer', 'Correct Answer', 'Correct'],
                    loc='center', cellLoc='center', colColours=['lightblue']*5)
    table.set_fontsize(14)
    table.scale(1, 2)

    plt.show()

    print("\tPress any key to go back to home menu")
    getch.getch()
    gameReset(gameInfo)

# Settings Menu
def settings(gameInfo):
    while gameInfo['option'] == 2:
        print("Select an option:\n1: Number of Questions\n2: Question Types\n3: Back\n")
        try:
            gameInfo['optionMenu'] = int(getch.getch())
        except ValueError:
            gameInfo['optionMenu'] = 0
        if gameInfo['optionMenu'] == 1:
            while True:
                clear_terminal()
                new_questions = input(f"Enter number of questions (default is 20):\nCurrent number: {gameInfo['questions']}\n")
                try:
                    new_questions = int(new_questions)
                    if new_questions > 0:
                        gameInfo['questions'] = new_questions

                        break
                except ValueError:
                    pass
            gameInfo['optionMenu'] = 0
        elif gameInfo['optionMenu'] == 2:
            clear_terminal()
            print("Choose Question types:\n")
            # Code for selecting question types goes here
            gameInfo['optionMenu'] = 0
        elif gameInfo['optionMenu'] == 3:
            gameInfo['option'] = 0
            return gameInfo['option']

# Menu Navigation
while not (gameInfo['option'] == 3):
    if gameInfo['option'] == 0:
        clear_terminal()
        menu(gameInfo)
    elif gameInfo['option'] == 1:
        clear_terminal()
        print('がんばって!')
        game(gameInfo)
    elif gameInfo['option'] == 2:
        clear_terminal()
        settings(gameInfo)
exit

