from tkinter import simpledialog, messagebox, ttk
import tkinter as tk
from storage import DictItem
import random
import time


class UI:
    def __init__(self, svc):
        self.svc = svc
        self.root = tk.Tk()
        self.root.title("Words Learning App")
        self.root.geometry("350x320")
        self.main_window()
        self.content = None

    def main_window(self):
        # Header Frame
        self.root.columnconfigure(0, weight=1)
        self.header_frame = tk.Frame(self.root)
        self.header_frame.grid(row=0, column=0, columnspan=2, padx=5, pady=2, sticky="ew")

        words_learned, goal = self.svc.get_progress()

        self.greeting_label = tk.Label(self.header_frame, text="Welcome!")
        self.greeting_label.grid(row=0, column=0, sticky="w")
        self.words_count_label = tk.Label(self.header_frame,
                                          text=f"Words learned: {words_learned}/{goal}")
        self.words_count_label.grid(row=0, column=1, sticky="e")

        # Name Entry
        self.name_entry = tk.Entry(self.header_frame)
        self.name_entry.grid(row=1, column=0, padx=3, pady=3, sticky="ew")
        self.name_entry.insert(0, "What is your name?")
        self.header_frame.columnconfigure(0, weight=1)

        self.ok_button = tk.Button(self.header_frame, text="OK", command=self.set_name)
        self.ok_button.grid(row=1, column=1)
        self.header_frame.columnconfigure(1, weight=0)

        # Buttons Frame
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.new_button = tk.Button(self.buttons_frame, text="New", width=7, command=self.new_word)
        self.practice_button = tk.Button(self.buttons_frame, text="Practice", width=7, command=self.practice)
        self.quiz_button = tk.Button(self.buttons_frame, text="Quiz", width=7, command=self.quiz)
        self.settings_button = tk.Button(self.buttons_frame, text="Settings", width=7, command=self.settings)

        self.new_button.grid(row=0, column=0)
        self.practice_button.grid(row=0, column=1)
        self.quiz_button.grid(row=0, column=2)
        self.settings_button.grid(row=0, column=3)

        # Content Frame
        self.content_frame = tk.Frame(self.root)
        self.content_frame.grid(row=3, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def destroy(self):
        if self.content is not None:
            self.content.destroy()
        self.content = None

    def set_name(self):
        name = self.name_entry.get()
        if name and name != "What is your name?":
            self.svc.username = name
            self.update_words_count_label()

            self.greeting_label.config(text=f"Hi again, {name}!")
            self.name_entry.grid_remove()
            self.ok_button.grid_remove()

            self.destroy()
        else:
            messagebox.showerror("Error", "Please enter your name.")


    def update_words_count_label(self):
        words_learned, goal = self.svc.get_progress()
        self.words_count_label.config(text=f"Words learned: {words_learned}/{goal}")

    def new_word(self):
        self.content = NewWord(self.svc, self.content_frame, self.update_words_count_label)
        self.content.show()

    def practice(self):
        practice = Practice(self.svc, self.content_frame)
        practice.show()

    def quiz(self):
        quiz = Quiz(self.svc, self.content_frame)
        quiz.show()

    def settings(self):
        settings = Settings(self.svc, self.content_frame, self.update_words_count_label)
        settings.show()

    def run(self):
        self.root.mainloop()


class NewWord:
    def __init__(self, svc, frame, update_words_count_label):
        self.svc = svc
        self.frame = frame
        self.pos_entry = None
        self.meaning_entry = None
        self.word_entry = None
        self.topic_entry = None
        self.update_words_count_label = update_words_count_label

    def destroy(self):
        # Clear existing content in the content frame
        for widget in self.frame.winfo_children():
            widget.destroy()

    def show(self):
        self.destroy()

        # Topic
        tk.Label(self.frame, text="Topic:").grid(row=0, column=0, sticky="w")
        self.topic_entry = ttk.Combobox(self.frame)
        self.topic_entry['values'] = self.svc.get_sorted_topics()
        self.topic_entry.grid(row=0, column=1, sticky="ew")

        # New Word
        tk.Label(self.frame, text="New word:").grid(row=1, column=0, sticky="w")
        self.word_entry = tk.Entry(self.frame)
        self.word_entry.grid(row=1, column=1, pady=10, sticky="ew")

        # Meaning
        tk.Label(self.frame, text="Meaning:").grid(row=2, column=0, sticky="w")
        self.meaning_entry = tk.Entry(self.frame)
        self.meaning_entry.grid(row=2, column=1, pady=10, sticky="ew")

        # Part of Speech
        tk.Label(self.frame, text="Part of speech:").grid(row=3, column=0, sticky="w")
        self.pos_entry = ttk.Combobox(self.frame, state="readonly")
        self.pos_entry['values'] = ("noun", "verb", "adjective", "adverb")
        self.pos_entry.set('noun')
        self.pos_entry.grid(row=3, column=1, pady=10, sticky="ew")

        # Save Button
        save_button = tk.Button(self.frame, text="Save", command=self.save_new_word)
        save_button.grid(row=4, column=0, columnspan=2, stick="s", pady=10)

        self.frame.columnconfigure(1, weight=1)

    def reset(self):
        self.word_entry.delete(0, tk.END)
        self.meaning_entry.delete(0, tk.END)
        self.topic_entry['values'] = self.svc.get_sorted_topics()
        self.topic_entry.set('')
        self.update_words_count_label()

    def save_new_word(self):
        try:
            # Get data from entries
            self.svc.add_new_word(
                self.topic_entry.get(),
                self.word_entry.get(),
                self.meaning_entry.get(),
                self.pos_entry.get()
            )

            self.reset()

            messagebox.showinfo("Success", "Word added successfully!")
        except RuntimeError as exc:
            messagebox.showerror("Error", str(exc))


class Practice:
    def __init__(self, svc, frame):
        self.svc = svc
        self.frame = frame

    def show(self):
        # Clear existing content in the content frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Topic Selection
        tk.Label(self.frame, text="Choose topic:").grid(row=0, column=0, sticky="w")
        self.topic_select = ttk.Combobox(self.frame, state="readonly", values=self.svc.get_sorted_topics())
        self.topic_select.grid(row=0, column=1, sticky="ew")
        # Attach an event handler to a widget,(name of the event, function that is called when the event occurs)
        self.topic_select.bind("<<ComboboxSelected>>", self._load_random_meaning)

        # Meaning Display
        self.meaning_label = tk.Label(self.frame, text="", padx=10, pady=10, wraplength=260)
        self.meaning_label.grid(row=1, column=0, columnspan=2)

        # Word Display (initially hidden)
        self.word_label = tk.Label(self.frame, text="", wraplength=260)
        self.word_label.grid(row=2, column=0, columnspan=2)

        # Control Buttons
        next_button = tk.Button(self.frame, text="Next", command=self._load_random_meaning)
        next_button.grid(row=3, column=0, padx=20, pady=20, sticky="ws")

        show_word_button = tk.Button(self.frame, text="Show word", command=self._show_word)
        show_word_button.grid(row=3, column=1, padx=20, pady=20, sticky="es")

    def _load_random_meaning(self, event=None):
        topic = self.topic_select.get()
        words = self.svc.get_words_by_topic(topic)  # DictItem, Words by topic
        if words:
            selected_word = random.choice(words)  # DictItem object
            self.current_word = selected_word.word
            self.meaning_label.config(text=selected_word.meaning)
            self.word_label.config(text="")
            # Start a timer to show the word after 10 seconds
            self.frame.after(10000, self._show_word)

    def _show_word(self):
        self.word_label.config(text=self.current_word)
        self.word_label.grid()


class Quiz:
    def __init__(self, svc, frame):
        self.svc = svc
        self.frame = frame

    def show(self):
        # Clear existing content in the content frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Topic Selection
        tk.Label(self.frame, text="Choose topic:").grid(row=0, column=0, sticky="w")
        self.topic_select = ttk.Combobox(self.frame, state="readonly", values=self.svc.get_sorted_topics())
        self.topic_select.grid(row=0, column=1, sticky="ew")
        self.topic_select.bind("<<ComboboxSelected>>", self.start_quiz)

        # Question Label
        question_label = tk.Label(self.frame, text="What is the word for:", anchor="w")
        question_label.grid(row=1, column=0, pady=5, sticky="we")
        self.meaning_label = tk.Label(self.frame, text="", wraplength=260)
        self.meaning_label.grid(row=2, column=0, columnspan=2, pady=5, sticky="we")

        # Answer Buttons
        self.buttons = []
        for i in range(3):
            choice_button = tk.Button(self.frame, command=lambda b=i: self.check_answer(b))
            choice_button.grid(row=3 + i, column=1, columnspan=2, sticky="ew")
            self.buttons.append(choice_button)
        self.frame.columnconfigure(0, weight=1)

    def start_quiz(self, event=None):
        self.selected_topic = self.topic_select.get()
        self.prepare_question()

    def prepare_question(self):
        words = self.svc.get_words_by_topic(self.selected_topic)
        if len(words) < 3:
            messagebox.showinfo("Error", "Not enough words in the selected topic for a quiz.")
            return

        correct_word = random.choice(words)
        self.correct_answer = correct_word.word
        self.meaning_label.config(text=f"{correct_word.meaning}")

        options = random.sample(words, 3)
        if correct_word not in options:
            options[random.randint(0, 2)] = correct_word

        for i, option in enumerate(options):
            self.buttons[i].config(text=option.word)

    def check_answer(self, button_index):
        selected_option = self.buttons[button_index].cget("text")
        if selected_option == self.correct_answer:
            messagebox.showinfo("Correct!", f"Correct! {self.correct_answer}.")
        else:
            messagebox.showinfo("Incorrect", f"Correct answer: {self.correct_answer}.")
        self.prepare_question()  # Prepare the next question

class Settings:
    def __init__(self, svc, frame, update_label_callback):
        self.svc = svc
        self.frame = frame
        self.update_label_callback = update_label_callback

    def show(self):
        # Clear existing content in the content frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        # Goal Setting
        tk.Label(self.frame, text="Goal:").grid(row=0, column=0, sticky="w")
        self.goal_entry = tk.Entry(self.frame)
        self.goal_entry.grid(row=0, column=1, pady=10, sticky="ew")


        # Update Goal Button
        update_goal_button = tk.Button(self.frame, text="Update goal", command=self.update_goal)
        update_goal_button.grid(row=2, column=0, columnspan=2, sticky="ew", pady=10)

        self.frame.columnconfigure(1, weight=1)

        # Load and display current goal and progress
        self.display_current_goal_and_progress()

    def update_goal(self):
        new_goal = self.goal_entry.get()
        if new_goal.isdigit():
            self.svc.update_goal(int(new_goal))

            self.display_current_goal_and_progress()

            messagebox.showinfo("Success", "Goal updated successfully!")
        else:
            messagebox.showerror("Error", "Please enter a valid number.")

    def display_current_goal_and_progress(self):

        self.update_label_callback()


