import os
import tkinter as tk
from tkinter import messagebox

from flashcard_set import FlashcardSet
from game_session import GameSession
DATABASES_PATH = 'flashcard_databases/'


class Gui:
    def __init__(self, flashcard_set):
        self.flashcard_set = flashcard_set
        self.root = tk.Tk()
        self.root.title("Flashcards App")
        self.font = ('Arial', 18)
        self.height = 700
        self.width = 700
        self.fg = "white"
        self.bg = "#6e7b8b"
        # centering window
        x = self.root.winfo_screenwidth() // 2 - self.width // 2
        y = int(self.root.winfo_screenheight()*0.1)
        self.root.geometry(str(self.width) + 'x' + str(self.height) + '+' + str(x) + '+' + str(y))

        self.frame = tk.Frame(self.root, height=self.height, width=self.width, bg="#003153")
        self.frame.grid(row=0, column=0)
        self.frame.pack_propagate(False)

        self.inner_frame = tk.Frame(self.frame, height=self.height-150, width=self.width-150, bg=self.bg)
        self.inner_frame.pack(padx=75, pady=75)
        self.inner_frame.pack_propagate(False)

        self.show_menu()

        self.root.mainloop()

    def show_menu(self):
        self.clear_widgets(self.inner_frame)
        text = "Data set: None"
        if self.flashcard_set is not None:
            text = "Data set: " + self.flashcard_set.name

        tk.Label(self.inner_frame, text="Menu", font=self.font, bg=self.bg, fg=self.fg).pack(padx=10)
        tk.Label(self.inner_frame, text=text, font=self.font, bg=self.bg, fg=self.fg).pack(padx=10)

        tk.Button(self.inner_frame, text="Start a session", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2", command=self.session_start).pack(padx=10, pady=10)
        tk.Button(self.inner_frame, text="Choose existing flashcard set", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2", command=self.choose_dataset).pack(padx=10, pady=10)
        tk.Button(self.inner_frame, text="Create new flashcard set", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2", command=self.create_new_dataset).pack(padx=10, pady=10)
        tk.Button(self.inner_frame, text="Add new questions", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",).pack(padx=10, pady=10)

    def session_start(self):
        if self.flashcard_set is None:
            textbox = tk.Text(self.root, height=5, font=self.font)
            messagebox.showerror(title="Error", message="Create or choose existing flashcard set first!")
            return
        game_session = GameSession(self.flashcard_set, self)
        game_session.session_start()

    def choose_dataset(self):
        self.clear_widgets(self.inner_frame)

        tk.Label(self.inner_frame, text="Available flashcard sets:", font=self.font, bg=self.bg, fg=self.fg).pack(padx=10)
        tk.Label(self.inner_frame, text=str(os.listdir(DATABASES_PATH)), font=self.font, bg=self.bg, fg=self.fg).pack(padx=10)
        tk.Label(self.inner_frame, text="Type name of flashcard set folder:", font=self.font, bg=self.bg, fg=self.fg).pack(padx=10)
        textbox = tk.Text(self.inner_frame, height=1, width=20, font=self.font)
        textbox.pack()
        tk.Button(self.inner_frame, text="Continue", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",
                  command=lambda: self.get_database_name(textbox)).pack(padx=10, pady=10)

    def get_database_name(self, textbox, create=None):
        name = textbox.get('1.0', tk.END)
        name = name.strip('\n')
        if name == "":
            return
        if create is None:
            self.flashcard_set = FlashcardSet(name, self)
        else:
            self.flashcard_set = FlashcardSet(name, self, "create")
        self.show_menu()

    def clear_widgets(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def show_error(self, text):
        messagebox.showerror(title="Error", message=text)

    def show_message_yesno(self, text):
        ans = messagebox.askyesno(title="Error", message=text)
        return ans

    def create_new_dataset(self):
        self.clear_widgets(self.inner_frame)

        tk.Label(self.inner_frame, text="Type name of new flashcard set folder:", font=self.font, bg=self.bg, fg=self.fg).pack(padx=10)
        textbox = tk.Text(self.inner_frame, height=1, width=20, font=self.font)
        textbox.pack()
        tk.Button(self.inner_frame, text="Continue", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",
                  command=lambda: self.get_database_name(textbox, "create")).pack(padx=10, pady=10)

