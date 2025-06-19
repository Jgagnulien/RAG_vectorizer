import os
from dotenv import load_dotenv
from groq import Groq

def main(user_prompt):
    key = os.getenv("GROQ_API_KEY")

    client = Groq(
        # This is the default and can be omitted
        api_key=key
    )

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": """
                You will be asked for rule suggestions by a fraud decisioning expert working for a bank that needs to improve the existing rules for payments fraud detection. 
                There are two different options on how to proceed and you need to choose one.
                Option 1: The new rule needs to cover a new fraud trend, 
                so he needs to search on the internet for news, blogposts and linkedin posts of that trend.
                The historical bank data may not have examples of this pattern yet, 
                so the ideas needs to come from the internet.
                Option 2: The existing decision engine is underperforming, 
                so he needs to use analytical methods to explore the existing bank data and discover new rules.
                Option 3: It is a known fraud trend and we should have a look at rules that exist in our external DB to suggest to the user. 
                Answer with either "1", "2" or "3" nothing else !
                """
            },
            {
                "role": "user",
                "content": user_prompt,
            }
        ],
        model="llama-3.3-70b-versatile",
    )

    choice = chat_completion.choices[0].message.content

    return choice
