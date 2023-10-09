import json
from google.cloud import dialogflow_v2 as dialogflow
from environs import Env
import argparse


def create_intent(project_id, intent_name, training_phrases, response_text):
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)

    training_phrases_objects = []
    for phrase in training_phrases:
        part = dialogflow.Intent.TrainingPhrase.Part(text=phrase)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases_objects.append(training_phrase)

    message_text = dialogflow.Intent.Message.Text(text=[response_text])
    message = dialogflow.Intent.Message(text=message_text)

    intent = dialogflow.Intent(
        display_name=intent_name,
        training_phrases=training_phrases_objects,
        messages=[message]
    )

    response = intents_client.create_intent(parent=parent, intent=intent)

    print("Intent created: {}".format(response.name))


def main():
    parser = argparse.ArgumentParser(description='Создание DialogFlow intents.')
    parser.add_argument('--phrases_file', type=str, default='phrases.json', help='Путь к Json файлу с фразами.')
    args = parser.parse_args()

    env = Env()
    env.read_env()
    project_id = env('PROJECT_ID')

    with open(args.phrases_file, 'r', encoding='utf-8') as file:
        intents_data = json.load(file)

    for intent_name, intent_data in intents_data.items():
        questions = intent_data.get('questions', [])
        answer = intent_data.get('answer', '')
        create_intent(project_id, intent_name, questions, answer)

    print("Intents успешно созданы в DialogFlow.")


if __name__ == '__main__':
    main()
