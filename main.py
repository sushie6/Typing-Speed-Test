import tkinter as tk
from tkinter import scrolledtext, messagebox
import time

SAMPLE_TEXT = """
green vines attached to the trunk of the tree had wound themselves toward the top of the canopy ants used the vine as their private highway avoiding all the creases and crags of the bark to freely move at top speed from top to bottom or bottom to top depending on their current chore at least this was the way it was supposed to be something had damaged the vine overnight halfway up the tree leaving a gap in the once pristine ant highway it was a good idea at least they all thought it was a good idea at the time hindsight would reveal that in reality it was an unbelievably terrible idea but it would take another week for them to understand that right now at this very moment they all agreed that it was the perfect course of action for the current situation he slowly poured the drink over a large chunk of ice he had especially chiseled off a larger block he did not particularly like his drinks cold but he knew that the drama of chiseling the ice and then pouring a drink over it looked far more impressive than how he actually liked it it was all about image and he had managed to perfect the image that he wanted to project"""


class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.minsize(600, 450)
        self.start_time = 0.0
        self.typing_started = False
        self.duration = 60
        self.create_widgets()
        self.load_sample_text()

    def create_widgets(self):
        font_style = ("Courier new", 14)
        result_font_style = ("Arial", 18, "bold")
        timer_font_style = ("Courier new", 12)
        button_font_style = ("Courier new", 16)
        text_area_font_style = ("Courier new", 14)
        padding_x =15

        self.sample_label = tk.Label(self.root, text="Sample Text:", font=font_style)
        self.sample_label.pack(pady=10)
        self.sample_text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=7, font=text_area_font_style, state=tk.DISABLED)
        self.sample_text_area.pack(padx=padding_x, pady=10, fill=tk.BOTH, expand=True)
        self.input_label = tk.Label(self.root, text="Your Typing:", font=font_style)
        self.input_label.pack(pady=10)
        self.input_text_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, height=7, font=text_area_font_style)
        self.input_text_area.pack(padx=padding_x, pady=10, fill=tk.BOTH, expand=True)
        self.input_text_area.bind("<KeyRelease>", self.start_timer)
        self.result_wpm_label = tk.Label(self.root, text="", font=result_font_style)
        self.result_wpm_label.pack(pady=5)
        self.result_accuracy_label = tk.Label(self.root, text="", font=result_font_style)
        self.result_accuracy_label.pack(pady=10)
        self.timer_label = tk.Label(self.root, text=f"Time remaining: {self.duration} seconds", font=timer_font_style)
        self.timer_label.pack(pady=10)
        self.try_again_button = tk.Button(self.root, text="Try Again", command=self.reset_test, state=tk.DISABLED, font=button_font_style)
        self.try_again_button.pack(pady=15)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(3, weight=1)

    def load_sample_text(self):
        self.sample_text_area.config(state=tk.NORMAL)
        self.sample_text_area.delete("1.0", tk.END)
        self.sample_text_area.insert(tk.END, SAMPLE_TEXT)
        self.sample_text_area.config(state=tk.DISABLED)

    def start_timer(self, event):
        if not self.typing_started:
            self.typing_started = True
            self.start_time = time.time()
            self.update_timer()
            self.input_text_area.config(state=tk.NORMAL)

    def update_timer(self):
        if self.typing_started:
            elapsed_time = int(time.time() - self.start_time)
            remaining_time = self.duration - elapsed_time
            self.timer_label.config(text=f"Time remaining: {remaining_time} seconds")
            if remaining_time <= 0:
                self.typing_started = False
                self.input_text_area.config(state=tk.DISABLED)
                self.calculate_speed()
                self.try_again_button.config(state=tk.NORMAL)
            else:
                self.root.after(1000, self.update_timer)

    def calculate_speed(self):
        typed_text = self.input_text_area.get("1.0", tk.END).strip()
        sample_words = SAMPLE_TEXT.split()
        typed_words = typed_text.split()
        num_typed_words = len(typed_words)
        correct_words = 0
        for i in range(min(len(sample_words), len(typed_words))):
            if sample_words[i] == typed_words[i]:
                correct_words += 1

        accuracy = 0
        if sample_words:
            accuracy = (correct_words / len(sample_words)) * 100

        minutes = self.duration / 60
        wpm = int(num_typed_words / minutes)
        self.result_wpm_label.config(text=f"Speed: {wpm} WPM")
        self.result_accuracy_label.config(text=f"Accuracy: {accuracy:.2f}%")
        messagebox.showinfo("Test Over", f"Speed: {wpm} WPM\nAccuracy: {accuracy:.2f}%")

    def reset_test(self):
        self.typing_started = False
        self.start_time = 0.0
        self.timer_label.config(text=f"Time remaining: {self.duration} seconds")
        self.result_wpm_label.config(text="")
        self.result_accuracy_label.config(text="")
        self.input_text_area.delete("1.0", tk.END)
        self.input_text_area.config(state=tk.NORMAL)
        self.load_sample_text()
        self.try_again_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    root.mainloop()