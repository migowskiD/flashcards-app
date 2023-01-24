import os
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from flashcard_set import FlashcardSet

DATABASES_PATH = 'flashcard_databases/'


class Gui:
    def __init__(self):
        self.flashcard_set = None
        self.root = tk.Tk()
        self.root.title("Flashcards App")
        self.font = ('Arial', 18)
        self.font_small = ('Arial', 12)
        self.height = 900
        self.width = 700
        self.inner_height = self.height - 100
        self.inner_width = self.width - 150
        self.fg = "white"
        self.bg = "#6e7b8b"
        # centering window
        x = self.root.winfo_screenwidth() // 2 - self.width // 2
        y = int(self.root.winfo_screenheight() * 0.1)
        self.root.geometry(str(self.width) + 'x' + str(self.height) + '+' + str(x) + '+' + str(y))

        self.frame = tk.Frame(self.root, height=self.height, width=self.width, bg="#003153")
        self.frame.grid(row=0, column=0)
        self.frame.pack_propagate(False)

        self.inner_frame = tk.Frame(self.frame, height=self.inner_height, width=self.inner_width, bg=self.bg)
        self.inner_frame.pack(padx=(self.width-self.inner_width)/2, pady=(self.height-self.inner_height)/2)
        self.inner_frame.pack_propagate(False)

        self.show_flashcard_choose()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def show_flashcard_choose(self):
        self.clear_widgets(self.inner_frame)

        tk.Button(self.inner_frame, text="Choose existing flashcard set", font=self.font, bg=self.bg, fg=self.fg,
                  cursor="hand2", command=self.choose_dataset).pack(padx=10, pady=10)
        tk.Button(self.inner_frame, text="Create new flashcard set", font=self.font, bg=self.bg, fg=self.fg,
                  cursor="hand2", command=self.create_new_dataset).pack(padx=10, pady=10)

    def show_menu(self):
        self.clear_widgets(self.inner_frame)
        text = "Data set: None"
        if self.flashcard_set is not None:
            text = "Data set: " + self.flashcard_set.name

        tk.Label(self.inner_frame, text="Menu", font=self.font, bg=self.bg, fg=self.fg).pack(padx=10)
        tk.Label(self.inner_frame, text=text, font=self.font, bg=self.bg, fg=self.fg).pack(padx=10)

        tk.Button(self.inner_frame, text="Start a session", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",
                  command=self.session_start).pack(padx=10, pady=10)
        tk.Button(self.inner_frame, text="Choose existing flashcard set", font=self.font, bg=self.bg, fg=self.fg,
                  cursor="hand2", command=self.choose_dataset).pack(padx=10, pady=10)
        tk.Button(self.inner_frame, text="Create new flashcard set", font=self.font, bg=self.bg, fg=self.fg,
                  cursor="hand2", command=self.create_new_dataset).pack(padx=10, pady=10)
        # tk.Button(self.inner_frame, text="Add new questions", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",).pack(padx=10, pady=10)

    def show_question(self):
        self.clear_widgets(self.inner_frame)
        pile_num = self.flashcard_set.get_pile_progress()
        q_num = self.flashcard_set.get_progress()
        question, answer = self.flashcard_set.get_question()
        tk.Label(self.inner_frame, text=str(pile_num + 1) + "/5", font=self.font_small, bg=self.bg, fg=self.fg).pack(
            padx=10)
        tk.Label(self.inner_frame, text=str(q_num + 1) + "/" + str(self.flashcard_set.get_pile_size()),
                 font=self.font_small, bg=self.bg, fg=self.fg).pack(padx=10)
        if ".png" in question:
            img = Image.open("images/" + question)
            if img.height > self.inner_height*0.6:
                scale = self.inner_height*0.6/img.height
                img = img.resize((int(img.width*scale), int(img.height*scale)), Image.ANTIALIAS)
            if img.width > self.inner_width:
                scale = self.inner_width/img.width
                img = img.resize((int(img.width * scale), int(img.height * scale)), Image.ANTIALIAS)
            img_tk = ImageTk.PhotoImage(img)
            flag = tk.Label(self.inner_frame, image=img_tk)
            flag.image = img_tk
            flag.pack()
        else:
            tk.Label(self.inner_frame, text=question, font=self.font_small, bg=self.bg, fg=self.fg).pack(padx=10)

        var = tk.IntVar()
        button = tk.Button(self.inner_frame, text="Continue", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",
                           command=lambda: [var.set(1), button.destroy()])
        button.place(relx=.5, rely=.9, anchor="center")
        button.wait_variable(var)
        tk.Label(self.inner_frame, text=answer, font=self.font_small, bg=self.bg, fg=self.fg).pack(padx=10)

        tk.Button(self.inner_frame, text="Hard", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2", command=lambda: [self.flashcard_set.inc_progress(), self.show_question()]).place(relx=.4, rely=.9, anchor="center")
        tk.Button(self.inner_frame, text="Easy", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2", command=lambda: [self.flashcard_set.move_up(self.flashcard_set.get_pile_progress(), question), self.show_question()]).place(relx=.6, rely=.9, anchor="center")

    def session_start(self):
        if self.flashcard_set is None:
            textbox = tk.Text(self.root, height=5, font=self.font)
            messagebox.showerror(title="Error", message="Create or choose existing flashcard set first!")
            return
        self.show_question()

    def choose_dataset(self):
        self.clear_widgets(self.inner_frame)

        tk.Label(self.inner_frame, text="Available flashcard sets:", font=self.font, bg=self.bg, fg=self.fg).pack(
            padx=10)
        tk.Label(self.inner_frame, text=str(os.listdir(DATABASES_PATH)), font=self.font, bg=self.bg, fg=self.fg).pack(
            padx=10)
        tk.Label(self.inner_frame, text="Type name of flashcard set folder:", font=self.font, bg=self.bg,
                 fg=self.fg).pack(padx=10)
        textbox = tk.Text(self.inner_frame, height=1, width=20, font=self.font)
        textbox.pack()
        tk.Button(self.inner_frame, text="Continue", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",
                  command=lambda: self.get_database_name(textbox)).pack(padx=10, pady=10)
        tk.Button(self.inner_frame, text="Back", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",
                  command=self.show_menu).pack(padx=10, pady=10)

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

    def show_message_yesno(self, text, title="Error"):
        ans = messagebox.askyesno(title=title, message=text)
        return ans

    def create_new_dataset(self):
        self.clear_widgets(self.inner_frame)

        tk.Label(self.inner_frame, text="Type name of new flashcard set folder:", font=self.font, bg=self.bg,
                 fg=self.fg).pack(padx=10)
        textbox = tk.Text(self.inner_frame, height=1, width=20, font=self.font)
        textbox.pack()
        tk.Button(self.inner_frame, text="Continue", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",
                  command=lambda: self.get_database_name(textbox, "create")).pack(padx=10, pady=10)
        tk.Button(self.inner_frame, text="Back", font=self.font, bg=self.bg, fg=self.fg, cursor="hand2",
                  command=self.show_menu).pack(padx=10, pady=10)

    def on_closing(self):
        if self.flashcard_set is not None:
            self.flashcard_set.save_files()
        self.root.destroy()
