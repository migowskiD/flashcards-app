import os


# class representing single set of flashcards
class FlashcardSet:
    # not providing url will create new set, otherwise we try to get existing one from disc
    def __init__(self, name, url=None):
        self.piles = []
        self.path = 'flashcard_databases/'
        if url is None:
            self.name = name
            self.path += name
            for i in range(6):
                self.piles.append({})
            self.save_files()
            self.add_questions()
        else:
            self.name = url.rsplit('\\', 1)[-1]
            print(self.name)
            self.path = url
            try:
                for i in range(6):
                    self.piles.append({})
                    path = self.path + '/pile' + str(i) + '.txt'
                    if i == 5:
                        path = self.path + '/already_known.txt'
                    self.read_file(i, path)
            except FileNotFoundError:
                print("File not found.")

    def add_questions(self):
        self.read_file(0, "new_questions.txt")
        # print(self.piles[0])
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
                    fp.write(question + "," + answer + "\n")

    def get_pile(self, num):
        return self.piles[num]

    def read_file(self, i, path):
        file = open(path, "r", encoding='utf-8')
        flashcards = file.read().split("\n")
        for flashcard in flashcards:
            if flashcard == "":
                continue
            quest, ans = flashcard.split(",")
            self.piles[i][quest] = ans
        file.close()

    def move_up(self, num, question):
        ans = self.piles[num].pop(question)
        if num < 5:
            self.piles[num+1][question] = ans
