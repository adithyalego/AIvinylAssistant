import os
import ollama

print("Vinyl Tape Damage Diagnostic Assistant - AI Edition")
print("Using local LLM (Ollama)")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    image_path = input("Image path (optional, press Enter to skip): ").strip() or None

    # Build prompt for the LLM
    prompt = f"""
You are an expert vinyl wrap and adhesive tape damage diagnostic assistant.
Analyze the user's description and give a clear, helpful response.

User description: {user_input}
"""

    if image_path:
        prompt += f"\nUser also provided an image: {image_path}"

    prompt += """
Please respond in this format:

Problem: [main issue]
Analysis: [short explanation]
Recommended Fixes:
1. ...
2. ...
3. ...

Prevention: [one tip]
"""

    try:
        response = ollama.chat(
            model='llama3.1:8b',        # change if you used a different model
            messages=[{'role': 'user', 'content': prompt}]
        )
        answer = response['message']['content']
        print("\nAssistant:\n" + answer + "\n")

    except Exception as e:
        print("\nAssistant: Ollama is not responding. Make sure Ollama is running.")
        print("Error:", e)
        print("Falling back to basic response...\n")