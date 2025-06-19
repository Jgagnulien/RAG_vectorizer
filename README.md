# 🧠 RAG-Enabled Rule Suggestion Engine

This project is a GUI-based interface for an **LLM-powered rule suggestion system**, enhanced with **Retrieval-Augmented Generation (RAG)**. It helps generate fraud detection rules based on past rule data and current user prompts.

## 🚀 Features

- 🧾 Takes a natural language prompt from the user (e.g., "Are there new fraud trends I can investigate?")
- 🔍 Uses RAG to retrieve relevant rules from a vectorized document base
- 🤖 Passes enriched context to a local or remote LLM to suggest new rules
- 🖥️ Simple desktop GUI using `tkinter`

---

## 🛠️ How It Works

1. **Input Prompt**  
   User enters a question or idea related to fraud detection.

2. **RAG Phase**  
   `vectorize_documents.main(user_prompt)` retrieves relevant historical rules or context.

3. **LLM Phase**  
   The enriched prompt is passed to `rule_suggestion.main(...)`, which returns a new rule suggestion.

4. **Output Display**  
   The generated rule is shown in a scrollable text window.

---

## 🧩 Project Structure

```plaintext
├── vectorize_documents.py     # Handles vector search logic (RAG)
├── rule_suggestion.py         # Handles interaction with the LLM
├── gui_rule_suggester.py      # Main GUI entry point
├── README.md

---

## 📝 License

MIT License. Feel free to use, modify, and contribute.
