import vectorize_documents
import rule_suggestion

# Variables :
user_prompt = "Are there new fraud trends I can investigate and create rules for ?"


def main(user_prompt):
    RAG = vectorize_documents()

    user_prompt = user_prompt + ", ".join(str(x) for x in RAG)

    rule = rule_suggestion(user_prompt)

    return rule