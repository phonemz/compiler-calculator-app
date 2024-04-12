import tkinter as tk
from tkinter import ttk
from calculator import CalcLexer, CalcParser


class CalculatorApp:
    def __init__(self, master):
        self.master = master
        master.title("Calculator")

        self.lexer = CalcLexer()
        self.parser = CalcParser()

        # Input Box
        self.entry = ttk.Entry(master, width=30)
        self.entry.pack(pady=10)

        # Grid of Numbers, Operators, and Signs
        buttons = [
            ("7",),
            ("8",),
            ("9",),
            ("*",),
            ("4",),
            ("5",),
            ("6",),
            ("+",),
            ("1",),
            ("2",),
            ("3",),
            ("-",),
            ("C",),
            ("0",),
            ("=",),
            ("/",),
        ]

        button_frame = ttk.Frame(master)
        button_frame.pack()

        for (text,) in buttons:
            ttk.Button(
                button_frame, text=text, command=lambda t=text: self.on_button_click(t)
            ).grid(
                row=(buttons.index((text,)) // 4),
                column=(buttons.index((text,)) % 4),
                padx=5,
                pady=5,
            )

        # Calculation Results, Prefix, and Postfix Labels
        self.result_label = ttk.Label(master, text="Result:")
        self.result_label.pack(anchor=tk.W, pady=5)
        self.prefix_label = ttk.Label(master, text="Prefix Notation:")
        self.prefix_label.pack(anchor=tk.W, pady=5)
        self.postfix_label = ttk.Label(master, text="Postfix Notation:")
        self.postfix_label.pack(anchor=tk.W, pady=5)

    def on_button_click(self, value):
        if value == "=":
            expression = self.entry.get()

            result = self.parser.parse(self.lexer.tokenize(expression))
            calculation_result = self.parser.evaluate(result)
            prefix_notation = self.parser.prefix(result)
            postfix_notation = self.parser.postfix(result)

            self.result_label.config(text=f"Result: {calculation_result}")
            self.prefix_label.config(text=f"Prefix Notation: {prefix_notation}")
            self.postfix_label.config(text=f"Postfix Notation: {postfix_notation}")

            self.entry.delete(0, tk.END)
            self.entry.insert(tk.END, str(calculation_result))
        elif value == "C":
            self.entry.delete(0, tk.END)
        else:
            self.entry.insert(tk.END, value)
