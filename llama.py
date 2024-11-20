import ollama
import re
import json
import pandas as pd

def generate_questions_from_transcript(filename, model='llama3.2'):
    task_description = """
    Given the following transcript, generate questions that can be used to quiz someone on the content.
    The generated questions should be relevant to the course material and should be easily answerable based on the transcript.
    Return question, list of four options and a correct answer index in a json format. Strictly follow json format provided.
    {question:"question", options:['option1', 'option2', 'option3', 'option4'], correct_answer: 'question2'}
    """

    # Read the transcript from the file
    with open(filename, 'r') as file:
        transcript = file.read()
    
    # Combine task description and transcript into the prompt
    prompt = f"{task_description} \n {transcript}"

    # Call Ollama's chat API to generate a response
    response = ollama.generate(model=model, prompt=prompt)

    print(response["response"])

    # # Extract JSON from the response using regex
    # json_match = re.search(r'\[\s*{.*}\s*\]', response["response"], re.DOTALL)
    # if json_match:
    #     json_string = json_match.group(0)  # Extract matched JSON substring
    #     try:
    #         questions_list = json.loads(json_string)
    #         print(questions_list)
    #     except json.JSONDecodeError as e:
    #         print("Error parsing JSON:", e)
    #         return None
    # else:
    #     print("No valid JSON found in the response.")
    #     return None
    
# Example usage
questions = generate_questions_from_transcript("subtitle.txt")
print(questions)