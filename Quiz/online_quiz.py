import tkinter as tk
from tkinter import messagebox, simpledialog

class Quiz:
    def __init__(self, title):
        self.title = title
        self.questions = []

    def add_question(self, question, options, correct_answer):
        self.questions.append({
            'question': question,
            'options': options,
            'correct_answer': correct_answer
        })

class QuizManager:
    def __init__(self):
        self.quizzes = []

    def create_quiz(self, title):
        quiz = Quiz(title)
        self.quizzes.append(quiz)
        return quiz

    def get_quiz(self, title):
        for quiz in self.quizzes:
            if quiz.title == title:
                return quiz
        return None

quiz_manager = QuizManager()

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Platform")
        self.main_menu()

    def main_menu(self):
        self.clear_window()

        title_label = tk.Label(self.root, text="Quiz Platform", font=("Arial", 24))
        title_label.pack(pady=20)

        create_button = tk.Button(self.root, text="Create a new quiz", command=self.create_quiz)
        create_button.pack(pady=10)

        take_button = tk.Button(self.root, text="Take a quiz", command=self.take_quiz)
        take_button.pack(pady=10)

    def create_quiz(self):
        self.clear_window()

        title = simpledialog.askstring("Quiz Title", "Enter the title of the quiz:")
        if not title:
            self.main_menu()
            return

        quiz = quiz_manager.create_quiz(title)

        while True:
            question = simpledialog.askstring("New Question", "Enter a question (or 'done' to finish):")
            if not question or question.lower() == 'done':
                break

            options = []
            for i in range(4):
                option = simpledialog.askstring("Option", f"Enter option {i+1}:")
                if not option:
                    self.main_menu()
                    return
                options.append(option)

            correct_answer = simpledialog.askstring("Correct Answer", "Enter the correct answer:")
            if not correct_answer:
                self.main_menu()
                return

            quiz.add_question(question, options, correct_answer)

        messagebox.showinfo("Quiz Created", f"Quiz '{title}' created successfully!")
        self.main_menu()

    def take_quiz(self):
        self.clear_window()

        title = simpledialog.askstring("Quiz Title", "Enter the title of the quiz you want to take:")
        quiz = quiz_manager.get_quiz(title)
        if not quiz:
            messagebox.showerror("Error", "Quiz not found!")
            self.main_menu()
            return

        self.clear_window()
        quiz_title_label = tk.Label(self.root, text=f"Taking Quiz: {title}", font=("Arial", 20))
        quiz_title_label.pack(pady=20)

        score = 0
        for idx, question_data in enumerate(quiz.questions):
            self.clear_window()
            quiz_title_label = tk.Label(self.root, text=f"Taking Quiz: {title}", font=("Arial", 20))
            quiz_title_label.pack(pady=20)

            question_label = tk.Label(self.root, text=f"Q{idx+1}: {question_data['question']}", font=("Arial", 14))
            question_label.pack(pady=10)

            answer_var = tk.StringVar()
            for i, option in enumerate(question_data['options']):
                tk.Radiobutton(self.root, text=option, variable=answer_var, value=option).pack(anchor='w')

            submit_button = tk.Button(self.root, text="Submit", command=lambda: self.submit_answer(answer_var, question_data['correct_answer']))
            submit_button.pack(pady=20)

            self.root.wait_variable(answer_var)

            if answer_var.get() == question_data['correct_answer']:
                score += 1
                messagebox.showinfo("Correct!", "Correct!")
            else:
                messagebox.showerror("Wrong!", f"Wrong! The correct answer is: {question_data['correct_answer']}")

        messagebox.showinfo("Quiz Completed", f"Your final score is {score}/{len(quiz.questions)}")
        self.main_menu()

    def submit_answer(self, answer_var, correct_answer):
        self.answer = answer_var.get()
        self.root.quit()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


root = tk.Tk()
app = QuizApp(root)
root.mainloop()