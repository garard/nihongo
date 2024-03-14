import pandas as pd
import os
import getch
import random
import numpy as np

# External vocab list
df = pd.read_csv("vocab.csv")


#Prepare array for answer storage in dictionary
answerHistory = np.empty((99, 5), dtype=np.dtype('U100'))


# Clear the terminal screen
def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


# All variables contained here
gameInfo = {
    'answer': '',
    'answerColumn': 0,
    'answerRow': 0,
    'history': answerHistory,
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


# Home Menu
def menu(gameInfo):
    while not (1 <= gameInfo['option'] <= 3):
        print("Current directory:", os.getcwd())
        print("Select an option:\n1: Start\n2: Options\n3: Exit\n")
        try:
            gameInfo['option'] = int(getch.getch())
            return gameInfo['option']
        except ValueError:
            gameInfo['option'] = 0


# Randoms question from external table
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
    if gameInfo['playerAnswer'] == gameInfo['answer']:
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
    gameInfo['question'] = 0
    print(f"\n\tYou answered {gameInfo['correct']} questions correctly!\n")
    print("Q\t|\tWord\t\t|\tYour Answer\t|\tCorrect Answer\t|\tCorrect")
    print("_________________________________________________________________________________________________________")
    for gameInfo['question'] in range(0, gameInfo['questions']):
        print(f"{gameInfo['question']+1}", end='\t|\t')

    # Word
        if gameInfo['history'][gameInfo['question']][4] == 'Japanese':
            if len(gameInfo['history'][gameInfo['question']][3]) < 8:
                print(f"{gameInfo['history'][gameInfo['question']][3]}", end='\t\t|\t')
            else:
                print(f"{gameInfo['history'][gameInfo['question']][3]}", end='\t|\t')
        
        if gameInfo['history'][gameInfo['question']][4] == 'English':
            if len(gameInfo['history'][gameInfo['question']][3]) < 5:
                print(f"{gameInfo['history'][gameInfo['question']][3]}", end='\t\t|\t')
            else:
                print(f"{gameInfo['history'][gameInfo['question']][3]}", end='\t|\t')

    # Your Answer    
        if gameInfo['history'][gameInfo['question']][4] == 'Japanese':
            if len(gameInfo['history'][gameInfo['question']][0]) < 8:
                print(f"{gameInfo['history'][gameInfo['question']][0]}", end='\t\t|\t')
            else:
                print(f"{gameInfo['history'][gameInfo['question']][0]}", end='\t|\t')
        
        if gameInfo['history'][gameInfo['question']][4] == 'English':
            if len(gameInfo['history'][gameInfo['question']][0]) <= 5:
                print(f"{gameInfo['history'][gameInfo['question']][0]}", end='\t\t|\t')
            else:
                print(f"{gameInfo['history'][gameInfo['question']][0]}", end='\t|\t')

    # Correct Answer    
        if gameInfo['history'][gameInfo['question']][4] == 'Japanese':
            if len(gameInfo['history'][gameInfo['question']][1]) <= 5:
                print(f"{gameInfo['history'][gameInfo['question']][1]}", end='\t\t|\t')
            else:
                print(f"{gameInfo['history'][gameInfo['question']][1]}", end='\t|\t')
        
        if gameInfo['history'][gameInfo['question']][4] == 'English':
            if len(gameInfo['history'][gameInfo['question']][3]) <= 5:
                print(f"{gameInfo['history'][gameInfo['question']][1]}", end='\t\t|\t')
            else:
                print(f"{gameInfo['history'][gameInfo['question']][1]}", end='\t|\t')
        print(f"{gameInfo['history'][gameInfo['question']][2]}")
    print("\nPress any key to go back to home menu")
    getch.getch()


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
        gameInfo['option'] = menu(gameInfo)
    elif gameInfo['option'] == 1:
        clear_terminal()
        print('がんばって!')
        gameInfo['option'] = game(gameInfo)
    elif gameInfo['option'] == 2:
        clear_terminal()
        gameInfo['option'] = settings(gameInfo)
    elif gameInfo['option'] == 3:
        exit
    elif gameInfo['option'] == 4:
        pass