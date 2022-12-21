import os
import sys
from flashcard_set import FlashcardSet
from game_session import GameSession

DATABASES_PATH = 'flashcard_databases/'


def menu():
    flashcard_set = None
    while True:
        os.system('cls')
        print("Menu")
        if flashcard_set is None:
            print("Data set: None")
        else:
            print("Data set: " + flashcard_set.name)
        print("Press 1 to start a session")
        print("Press 2 to choose existing flashcard set")
        print("Press 3 to create new flashcard set")
        print("Press 4 to add new questions from new_questions.txt to existing flashcard set")
        print("Press q to quit")
        key = input("Choose menu option: ")
        if key == '1':
            print("Session starts...")
            if flashcard_set is None:
                input("First create or choose existing flashcard set! Press enter to continue.")
                continue
            game_session = GameSession(flashcard_set)
            game_session.session_start()
        elif key == '2':
            print("Choosing flashcard set...")
            print("Available flashcard sets:")
            print(os.listdir(DATABASES_PATH))
            name = input("Type name of flashcard set folder: ")
            flashcard_set = FlashcardSet(name)
        elif key == '3':
            print("Creating new flashcard set...")
            name = input("Type name of new flashcard set: ")
            flashcard_set = FlashcardSet(name, "create")
        elif key == '4':
            print("Adding new questions to flashcard set...")
            if flashcard_set is None:
                input("First create or choose existing flashcard set! Press enter to continue.")
                continue
            flashcard_set.add_questions()
        elif key == 'q':
            sys.exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    menu()
