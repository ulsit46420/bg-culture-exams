import os
from itertools import chain

from openai import OpenAI
from dotenv import load_dotenv
import time


def read_file(filename):
    with open(f"{filename}", 'r') as f:
        content = f.read()
    return content


def init_api_keys():
    try:
        load_dotenv()
        api_key = os.getenv("DEEPSEEK_API_KEY")
        client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
        return client
    except Exception as exception:
        print("Error in initializing API keys:", exception)
        raise


def generate_response(client, prompt: str, filename: str, number: int, max_retries: int = 3, retry_delay: int = 10):
    retries = 0
    while retries < max_retries:
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "You are generating a dataset from unstructured data"},
                    {"role": "user", "content": prompt},
                ],
                stream=False
            )
            generated_text = response.choices[0].message.content
            print(generated_text)
            with open("generated/deepseek/db/inputs-segmented.txt", "a") as f1, open(
                    "generated/deepseek/db/outputs-segmented.txt",
                    "a") as f2:
                f1.write(prompt + "\n")
                f2.write(filename + "__,__" + str(number) + "__,__" + generated_text + "\n")
            return
        except Exception as exception:
            print("Error generating response:", exception)
            if "Error code: 503" in str(exception) or "Error code: 429" in str(exception):
                if retries < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retries += 1
                else:
                    print("Max retries reached. Skipping this request.")
                    return
            else:
                raise


def get_range(from_number, to_number):
    return range(from_number, to_number + 1)


def get_prompt(document_text: str, examples: str, task_for_number_text: str) -> str:
    return f"""# Document

{document_text}

# Examples

{examples}

# Task

{task_for_number_text}"""


client = init_api_keys()


def getTasksFromFile(filename, range):
    if filename.endswith(".md"):
        # Construct the full file path
        file_path = os.path.join(folder_path, filename)

        # Extract text and associate with filename
        document_text = read_file(file_path)
        examples = read_file("files/formatted_examples-db.md")
        print(file_path)

        for number in range:
            task_for_number_text = \
                (f"Find problem number {number} from the Document and find the matching answer for it in the "
                 f"Document. Generate one row - structured csv for problem number {number}, following the Examples."
                 )
            task_number_prompt = (get_prompt(document_text, examples, task_for_number_text))
            generate_response(client, task_number_prompt, filename, number)


# Specify the folder path
folder_path = 'files/md/bg-sorted/1-7,24-34'

# Iterate through files in the folder
for filename in os.listdir(folder_path):
    getTasksFromFile(filename, chain(range(1, 7), range(24, 34)))

folder_path = 'files/md/bg-sorted/1-22'

for filename in os.listdir(folder_path):
    getTasksFromFile(filename, get_range(1, 22))

folder_path = 'files/md/bg-sorted/1-27'

for filename in os.listdir(folder_path):
    getTasksFromFile(filename, get_range(1, 27))

folder_path = 'files/md/bg-sorted/6,7,9-12,14-16,18-23,26,28-38,40'

for filename in os.listdir(folder_path):
    getTasksFromFile(filename,
                     chain(range(6, 7), range(9, 12), range(14, 16), range(18, 23), [26], range(28, 38), [40]))

folder_path = 'files/md/bg-sorted/7,9-23,26-28,30-38,40'

for filename in os.listdir(folder_path):
    getTasksFromFile(filename, chain([7], range(9, 23), range(26, 28), range(30, 38), [40]))
