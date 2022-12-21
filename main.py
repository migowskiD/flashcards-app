import os
import sys
from flashcard_set import FlashcardSet
from game_session import GameSession


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
        print("Press 2 to choose existing cards set")
        print("Press 3 to add new flash cards set")
        print("Press q to quit")
        key = input("Choose menu option: ")
        if key == '1':
            print("Session starts...")
            if flashcard_set is None:
                url = input("Type url of dataset folder: ")
                flashcard_set = FlashcardSet(None, url)
            game_session = GameSession(flashcard_set)
            game_session.session_start()
        elif key == '2':
            print("Choosing flash card set...")
            url = input("Type url of dataset folder: ")
            flashcard_set = FlashcardSet(None, url)
        elif key == '3':
            print("Adding new flash card set...")
            name = input("Type name of new set: ")
            flashcard_set = FlashcardSet(name)
        elif key == 'q':
            sys.exit()


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    menu()
