import dialogflow_v2 as dialogflow


class AnsweringMachine(object):
    def __init__(self, project_id, session_id, language_code):

        self.language_code = language_code

        self.session_client = dialogflow.SessionsClient()
        self.session = self.session_client.session_path(project_id, session_id)

    def get_answer(self, message, ignore_unrecognized=False):
        text_input = dialogflow.types.TextInput(
            text=message, language_code=self.language_code)
        query_input = dialogflow.types.QueryInput(text=text_input)
        response = self.session_client.detect_intent(
            session=self.session, query_input=query_input)
        if ignore_unrecognized and response.query_result.intent.is_fallback:
            return
        answer = response.query_result.fulfillment_text
        return answer
