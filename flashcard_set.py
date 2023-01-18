import os
from collections import OrderedDict
import random


# class representing single set of flashcards
class FlashcardSet:
    # option create will create new set, otherwise we try to get existing one from disc
    def __init__(self, name, gui, option="read"):
        self.gui = gui
        self.separator = "-"
        self.line_separator = ";\n"
        self.piles = []
        self.name = name
        self.path = 'flashcard_databases/' + name
        self.progress = 0
        self.pile_progress = 0
        for i in range(6):
            self.piles.append(OrderedDict())
        if option == "create":
            self.create_dataset()
        elif option == "read":
            self.read_dataset()
            self.read_progress()
            self.read_pile_progress()

    def add_questions(self):
        self.read_file(0, "new_questions.txt")
        self.save_files()

    def add_and_shuffle_questions(self):
        self.read_file(0, "new_questions.txt")
        self.shuffle_pile(0)
        self.save_files()

    def save_files(self):
        for i, pile in enumerate(self.piles):
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            path = self.path + '/pile' + str(i) + '.txt'
            if i == 5:
                path = self.path + '/already_known.txt'
            with open(path, "w", encoding='utf-8') as fp:
                for question, answer in pile.items():
                    fp.write(question + self.separator + answer + self.line_separator)
        with open(self.path + '/progress.txt', "w", encoding='utf-8') as fp:
            fp.write(str(self.progress))

    def get_pile(self, num):
        return self.piles[num]

    def read_file(self, i, path):
        file = open(path, "r", encoding='utf-8')
        flashcards = file.read().split(self.line_separator)
        for flashcard in flashcards:
            if flashcard == "":
                continue
            quest, ans = flashcard.split(self.separator)
            self.piles[i][quest] = ans
        file.close()

    def move_up(self, num, question):
        ans = self.piles[num].pop(question)
        if num < 5:
            self.piles[num+1][question] = ans
        if self.progress >= len(self.piles[num]):
            self.progress = 0
            self.read_pile_progress()
            self.shuffle_pile(self.get_pile_progress())

    def create_dataset(self):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        else:
            ans = self.gui.show_message_yesno("There is already existing flashcard set with that name. Do you want to overwrite it?")
            if ans is False:
                raise Exception("Not overwriting existing database")
        self.add_and_shuffle_questions()

    def read_dataset(self):
        try:
            for i in range(6):
                path = self.path + '/pile' + str(i) + '.txt'
                if i == 5:
                    path = self.path + '/already_known.txt'
                self.read_file(i, path)
        except FileNotFoundError:
            self.gui.show_error("File not found.")
            # print("File not found.")

    def shuffle_pile(self, num):
        items = list(self.piles[num].items())
        random.shuffle(items)
        self.piles[num] = OrderedDict(items)

    def read_progress(self):
        with open(self.path + '/progress.txt', "r", encoding='utf-8') as fp:
            self.progress = int(fp.read())

    def read_pile_progress(self):
        for i, pile in enumerate(self.piles):
            if len(pile) > 0:
                self.pile_progress = i
                return

    def get_progress(self):
        return self.progress

    def set_progress(self, num):
        self.progress = num

    def inc_progress(self):
        self.progress += 1
        if self.progress >= len(self.piles[self.pile_progress]):
            self.progress = 0
            self.read_pile_progress()
            self.shuffle_pile(self.get_pile_progress())

    def get_pile_progress(self):
        return self.pile_progress

    def get_question(self):
        keys = list(self.piles[self.pile_progress].keys())
        key = keys[self.progress]
        return key, self.piles[self.pile_progress][key]

    def get_pile_size(self):
        return len(self.piles[self.pile_progress])

