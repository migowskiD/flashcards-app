import os
from time import sleep

from termcolor import colored


class GameSession:
    def __init__(self, flashcard_set):
        self.flashcard_set = flashcard_set

    def session_start(self):
        counter = 0
        for i in range(5):
            pile = self.flashcard_set.get_pile(i)
            # for j, (question, answer) in enumerate(pile.items()):
            #     os.system('cls')
            #     print("You are in pile " + str(i+1) + "/5")
            #     print("Flashcard num " + str(j+1) + "/" + str(len(pile)))
            #     print(question)
            #     input("Press enter to show answer:")
            #     print(answer)
            #     known = input("Did you answer correctly? Type y if yes and n if no")
            #     if known == "y" or known == "Y" or known == "yes" or known == "Yes" or known == "YES":
            #         pile.pop(question)
            #         # self.flashcard_set.move_up(i, question)
            while len(pile) > 0:
                index = 0
                while index < len(pile):
                    os.system('cls')
                    print("You are in pile " + str(i+1) + "/5")
                    print("Flashcard num " + str(index+1) + "/" + str(len(pile)))
                    keys = list(pile.keys())
                    key = keys[index]
                    print(colored(key, 'yellow'))
                    input("Press enter to show answer:")
                    print(colored(pile[key], 'green'))
                    known = input("Did you answer correctly? Type yes(y) or no(n). If you want to save and quit type q")
                    if known == "y" or known == "Y" or known == "yes" or known == "Yes" or known == "YES":
                        self.flashcard_set.move_up(i, key)
                    elif known == "q" or known == "Q":
                        self.flashcard_set.save_files()
                        return
                    else:
                        index = index + 1
                    counter += 1
                    if counter % 10 == 0:
                        self.flashcard_set.save_files()
        print("You finished all flashcards from this set!")
        sleep(5)
        self.flashcard_set.save_files()

