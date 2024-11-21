import ollama
import re
import json
import pandas as pd

def generate_questions_from_transcript(filename, model='llama3.2'):
    task_description = """
    Task Description:
    Based on the above transcript, generate questions that can be used to quiz someone on the content.
    The generated questions should be relevant to the course material and should be easily answerable based on the transcript.
    Return question, list of four options and a correct answer index in a json format. A few examples are given below. Strictly follow json format below.
    {question:'Who won the nobel prize for physics in 2000?', options:['Jack Kilby', 'Albert Einstein', 'Michio Kaku', 'Isaac Newton'], correct_answer: 'Jack Kilby'}
    {question:'Dusra_prashn', options:['Pehlaopshan', 'Dusraoption', 'Theesraopshan', 'Chouthaopshan'], correct_answer: 'Theesraopshan'}
    {question:'What colour is the umbrealla?', options:['Red', 'Blue', 'Green', 'Yellow'], correct_answer: 'Blue'}
    """

    # Read the transcript from the file
    with open(filename, 'r') as file:
        transcript = file.read()
    
    # Combine task description and transcript into the prompt
    prompt = f"Transcript: {transcript} \n \n {task_description}"

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