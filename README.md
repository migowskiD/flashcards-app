# Flashcard App
Simple app with Tkinter graphical interface, allows users to add new flashcards in the format of txt file, optionally question can be a .png file.

App uses the Leitner System for flashcards and divides them into 5 piles, at the beginning all flashcards are in the first pile, then after each question we can choose if we are already familiar with it (question pushed to another pile) or not (stays in the same pile). When we finish one pile we move to the next one.

## Before using
Before first use change `new_question.txt` file to your question. If you need image version of questions, you need to put `.png` files inside `images/` directory.

### `new_question.txt` must be formatted as follows:
```
QUESTION--ANSWER;

```
`--` is the question-answer separator and `;\n` is the flashcard separator. Inside `QUESTION` or `ANSWER` spaces ` `, new line signs `\n`, dashes `-`, brackets `()`, commas `,` etc. are allowed. If you use `.png` file as question, `QUESTION` must be name of the file in the `images/` directory for example:
```
example.png--Multi
line example;

```

## First use
You need to select `Create new flashcard set` option and files for new flashcard set will be created from `new_questions.txt`.

## Next uses
If you already have created flashcard sets you can just use `Choose existing flashcard set` option to work with same set and keep your progress.


