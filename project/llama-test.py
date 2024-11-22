import ollama
import re
import json
import pandas as pd

def generate_questions_from_transcript(filename, model='llama3.2'):
    task_description = """
        You are an AI tasked with generating multiple-choice questions (MCQs) from a given transcript. 
        Your goal is to:
        1. Identify important concepts, events, or details in the transcript.
        2. Frame a question in a simple and clear manner based on these concepts.
        3. Provide 4 answer options for each question, ensuring one is correct and the others are plausible but incorrect.
        4. Specify the index (0-based) of the correct answer.
        5. Format your response as a JSON list where each entry follows the structure:
        { "question": "<question_text>", "options": ["<option1>", "<option2>", "<option3>", "<option4>"], "correct_answer": <index_of_correct_option> }

        Here is an example:
            {
                "question": "What is the capital of France?",
                "options": ["Berlin", "Madrid", "Paris", "Rome"],
                "correct_answer": 2
            }
        Your input will be a transcript, and you will generate questions based on its content in this exact format.
        """

    # Read the transcript from the file
    with open(filename, 'r') as file:
        transcript = file.read()
    
    # Combine task description and transcript into the prompt
    prompt = task_description +'\n Here is the transcript content: \n' + transcript + 'Generate 1 question in the said json format, { "question": "<question_text>", "options": ["<option1>", "<option2>", "<option3>", "<option4>"], "correct_answer": <index_of_correct_option> } , based on this transcript.'

    # Call Ollama's chat API to generate a response
    response = ollama.generate(model=model, prompt=prompt)
    # Extract JSON from the response using regex
    json_match = re.search(r'\[\s*{.*}\s*\]', response["response"], re.DOTALL)
    if json_match:
        json_string = json_match.group(0)  # Extract matched JSON substring
        try:
            questions_list = json.loads(json_string)
            print(questions_list)
        except json.JSONDecodeError as e:
            print("Error parsing JSON:", e)
            return None
    else:
        print("No valid JSON found in the response.")
        return None
    with open("output.csv", "a") as output:
        try:
            for question in questions_list:
                output.write(f"{question['question']},{question['options'][0]},{question['options'][1]},{question['options'][2]},{question['options'][3]},{question['correct_answer']}\n")
        except Exception as e:
            print("Error writing to CSV:", e)
    return response
    
# Example usage
questions = generate_questions_from_transcript("subtitle.txt")
print(questions)