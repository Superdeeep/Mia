import json
import os
import ollama


def query_ollama(prompt, model='openhermes:7b-mistral-v2.5-q6_K', context=''):
    response = ollama.generate(
        model=model,
        prompt=context + prompt)
    return response['response'].strip()


def create_valid_file():
    if not os.path.exists('train.jsonl'):
        die('No train.jsonl file found!')

    with open('train.jsonl', 'r') as file:
        train_lines = file.read().splitlines()

    total_lines = len(train_lines)
    twenty_percent = round(total_lines * 0.2)

    val_lines = train_lines[:twenty_percent]
    train_lines = train_lines[twenty_percent:]

    with open('train.jsonl', 'w') as file:
        file.write('\n'.join(train_lines))

    with open('valid.jsonl', 'w') as file:
        file.write('\n'.join(val_lines))


def die(message):
    raise Exception(message)


def main():
    if not os.path.exists('instructions.json'):
        topic = input("What is the topic of this training dataset? ")
        prompt = f"""Please list in JSON format 10 frequently asked questions about {topic} from all levels of users  
        f"working on it.  The questions should start with any of the following: 'Where do I' 
        f"'Is it okay to',  'Can you help me', 'I need to', 'Is there a', 'Do you know', 'Where is the', 
        f"'Can you tell me', 'Can I change', 'What are the', 'How do I', 'When is it', 'Does WordPress have'
        f"'How to', 'What is the difference', 'Can users', 'Can I', 'What is' 
        f"You do not need to provide an answer, or category to each question. The list should be 
        f"a single dimension array of only questions."""
        instructions = query_ollama(prompt)
        with open('instructions.json', 'w') as file:
            file.write(instructions)

    with open('instructions.json', 'r') as file:
        instructions = json.load(file)

    total = len(instructions)

    print("------------------------------")
    for i, instruction in enumerate(instructions):
        print(f"({i + 1}/{total}) {instruction}")
        print("------------------------------")

        answer = query_ollama(instruction)
        print(answer)  # for terminal output

        result = {'text': f'<s>[INST] {instruction}[/INST] {answer}</s>'}
        output = json.dumps(result) + "\n"
        output = output.replace('[\/INST]', "[/INST]").replace('<\/s>', "</s>")

        print("\n\n------------------------------\n")

        with open('train.jsonl', 'a') as file:
            file.write(output)

    create_valid_file()

    print("Done! Training and validation JSONL files created.")


if __name__ == "__main__":
    main()
