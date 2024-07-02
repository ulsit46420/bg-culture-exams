import os
import random
import time
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = "https://openrouter.ai/api/v1"
MODEL_NAME = "openai/gpt-4o"

def init_api_client():
    try:
        from openai import OpenAI
        client = OpenAI(api_key=API_KEY, base_url=BASE_URL)
        return client
    except Exception as exception:
        print("Error in initializing API client:", exception)
        raise

def read_csv_file(file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    return [line.strip().split("__,__") for line in lines]

def get_sample_questions(questions, num_columns, num_samples):
    return random.sample([q for q in questions if len(q) == num_columns], num_samples)

def create_prompt(sample_questions, question):
    prompt = ""
    for sample in sample_questions:
        prompt += format_question(sample)
    prompt += format_question(question, include_answer=False)
    return prompt

def format_question(question, include_answer=True):
    formatted_question = (
        f"{question[5]}\n"
        f"  А. {question[6]}\n"
        f"  Б. {question[7]}\n"
        f"  В. {question[8]}\n"
        f"  Г. {question[9]}\n"
    )
    if include_answer:
        formatted_question += f"GENERATE ANSWER WITHIN ONLY ONE CHARACTER (А,Б,В,Г): {question[10]}\n\n"
    else:
        formatted_question += "GENERATE ANSWER WITHIN ONLY ONE CHARACTER (А,Б,В,Г): "
    return formatted_question

def save_response(file_path, question, model_name, response):
    with open(file_path, "a") as file:
        file.write(f"{'__,__'.join(question)}__,__{model_name}__,__{response}\n")

def generate_response(client, prompt, max_retries=3, retry_delay=10):
    retries = 0
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "Отговори правилно на посочения въпрос, както е посочено в примерите. ГЕНЕРИРАЙ ЕДИН СИМВОЛ на Кирилица с верния отговор – А,Б,В,Г"},
                    {"role": "user", "content": prompt},
                ],
                temperature=0,
                max_tokens=2,
                stream=False
            )
            generated_text = response.choices[0].message.content.strip()
            return generated_text
        except Exception as exception:
            print("Error generating response:", exception)
            if "Error code: 503" in str(exception) or "Error code: 429" in str(exception):
                if retries < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retries += 1
                else:
                    print("Max retries reached. Skipping this request.")
                    return None
            else:
                raise

def run_benchmark(train_dir, test_dir, output_dir):
    client = init_api_client()

    for file_name in os.listdir(test_dir):
        test_file_path = os.path.join(test_dir, file_name)
        train_file_path = os.path.join(train_dir, file_name)
        output_file_path = os.path.join(output_dir, f"{MODEL_NAME}_responses.csv")

        test_questions = read_csv_file(test_file_path)
        train_questions = read_csv_file(train_file_path)

        column_counts = {
            "db": [7, 10, 11],
            "dg": [10, 11],
            "di": [10, 11]
        }[file_name.split(".")[0]]

        for question in test_questions:
            num_columns = len(question)
            if num_columns not in column_counts:
                continue

            sample_questions = get_sample_questions(train_questions, num_columns, 5)
            prompt = create_prompt(sample_questions, question)
            print(prompt)

            model_response = generate_response(client, prompt)
            if model_response is not None:
                save_response(output_file_path, question, MODEL_NAME, model_response)

if __name__ == "__main__":
    train_dir = "../data/train"
    test_dir = "../data/test"
    output_dir = "../responses"

    os.makedirs(output_dir, exist_ok=True)
    run_benchmark(train_dir, test_dir, output_dir)
