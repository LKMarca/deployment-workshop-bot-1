from .__init__ import *


# =============================================================
# ActionGoodbye - action responsavel pela despedida do usuário
# =============================================================
class ActionGoodbye(Action):
    def name(self) -> Text:
        return "action_goodbye"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        log(tracker.latest_message)
        dismiss = choice(['Até logo! 👋', 'Até mais! 👋', 'Até breve! 👋'])
        texto = choice(['Tenha um ótimo dia! 🌞', 'Quando precisar, é só chamar! 😀'])
        dispatcher.utter_message(f'{texto} {dismiss}')
        last_event = tracker.get_last_event_for('user', skip=0)
        last_intent = last_event['parse_data']['intent']['name'] if last_event else None
        if last_intent == 'goodbye_intent':
            user_finish = None
            return [SlotSet('user_alm_qc', user_finish), SlotSet('count_finish', '0')]
        return []
