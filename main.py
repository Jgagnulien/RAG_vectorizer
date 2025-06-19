import vectorize_documents
import rule_suggestion

def main(user_prompt):
    RAG = vectorize_documents.main(user_prompt)

    user_prompt = user_prompt + ", ".join(str(x) for x in RAG)

    rule = rule_suggestion.main(user_prompt)

    print(rule)
    return rule

import tkinter as tk
from tkinter import scrolledtext

def on_submit():
    prompt = prompt_entry.get("1.0", tk.END).strip()
    if prompt:
        result = main(prompt)
        response_display.delete("1.0", tk.END)
        response_display.insert(tk.END, result)

# Create the window
root = tk.Tk()
root.title("Rule suggestion GUI")

# Prompt input
tk.Label(root, text="Enter your prompt:").pack()
prompt_entry = scrolledtext.ScrolledText(root, height=5, width=80)
prompt_entry.pack(padx=10, pady=5)

# Submit button
submit_button = tk.Button(root, text="Submit", command=on_submit)
submit_button.pack(pady=5)

# Response output
tk.Label(root, text="Model response:").pack()
response_display = scrolledtext.ScrolledText(root, height=10, width=80)
response_display.pack(padx=10, pady=5)

# Run the GUI
root.mainloop()