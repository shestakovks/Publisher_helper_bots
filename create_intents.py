import argparse
import json
import os

import dialogflow_v2
from dotenv import load_dotenv


def load_learning_data_from_json(path_to_file):
    with open(path_to_file) as learning_json:
        learning_dict = json.load(learning_json)
    return learning_dict


def create_intent(display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow_v2.types.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow_v2.types.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow_v2.types.Intent.Message.Text(text=message_texts)
    message = dialogflow_v2.types.Intent.Message(text=text)

    intent = dialogflow_v2.types.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message])
    return intent


def create_intents(learning_dict):
    intents = []
    for display_name, intent_body in learning_dict.items():
        if not isinstance(intent_body['answer'], list):
            intent_body['answer'] = [intent_body['answer']]
        intent = create_intent(display_name, intent_body['questions'], intent_body['answer'])
        intents.append(intent)
    return intents


def load_intents(project_id, intents):
    intents_client = dialogflow_v2.IntentsClient()
    parent = intents_client.project_agent_path(project_id)
    for intent in intents:
        intents_client.create_intent(parent, intent)
        print('Intent created: {}'.format(intent.display_name))


def train_agent(project_id):
    client = dialogflow_v2.AgentsClient()
    parent = client.project_path(project_id)
    client.train_agent(parent)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path_to_file', help="Path to file with learning data.", type=str)
    args = parser.parse_args()
    path_to_file = args.path_to_file

    load_dotenv()
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')

    learning_dict = load_learning_data_from_json(path_to_file)
    intents = create_intents(learning_dict)
    load_intents(google_project_id, intents)
    train_agent(google_project_id)
