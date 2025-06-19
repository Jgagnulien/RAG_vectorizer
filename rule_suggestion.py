from llama_cpp import Llama

llm = Llama(model_path="C:/Users/jugagn/OneDrive - SAS/Documents/LLM/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

system_prompt = """
You will be asked for rule suggestions by a fraud decisioning expert working for a bank that needs to improve the existing rules for payments fraud detection, 
use the provided rules to inspire yourself to create a single new rule.
"""

def main(user_prompt, system_prompt):

    llm = Llama(model_path="C:/Users/jugagn/OneDrive - SAS/Documents/LLM/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf")

    """input: llm user_prompt system_prompt"""
    response = llm.create_chat_completion(
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=2048
    )

    llm_response = response['choices'][0]['message']['content']

    return llm_response
