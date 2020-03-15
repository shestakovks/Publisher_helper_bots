import json
import os

import dialogflow_v2
from dotenv import load_dotenv


def load_intents_from_json(path_to_file):
    with open(path_to_file) as intents_json:
        intents = json.load(intents_json)
    return intents


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow_v2.IntentsClient()

    parent = intents_client.project_agent_path(project_id)
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

    intents_client.create_intent(parent, intent)
    print('Intent created: {}'.format(display_name))


def create_intents(project_id, intents):
    for display_name, intent_body in intents.items():
        training_phrases_parts = intent_body['questions']
        if isinstance(intent_body['answer'], list):
            message_texts = intent_body['answer']
        else:
            message_texts = [intent_body['answer']]

        create_intent(project_id, display_name, training_phrases_parts, message_texts)


def train_agent(project_id):
    client = dialogflow_v2.AgentsClient()
    parent = client.project_path(project_id)
    client.train_agent(parent)


if __name__ == '__main__':
    load_dotenv()
    google_project_id = os.getenv('GOOGLE_PROJECT_ID')

    intents_dict = load_intents_from_json('intent_source.json')
    create_intents(google_project_id, intents_dict)
    train_agent(google_project_id)
