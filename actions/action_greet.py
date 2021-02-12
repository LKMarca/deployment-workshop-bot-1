from .__init__ import *


# ======================================================================
# ActionGreet - action responsável por iniciar a conversa com o usuario
# ======================================================================
class ActionGreet(Action):

    def name(self) -> Text:
        return "action_greet"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        if tracker.get_slot('senderid') is None:
            log(tracker.latest_message)
            text = ['Olá! Seja bem-vindo(a), eu sou a assistente virtual da Vivo! 😄', 'Estou aqui para te ajudar na abertura de defeitos! 😉']
            for texto in text:
                dispatcher.utter_message(text=texto)
        else:
            hi_text = choice(['Oie', 'Oi', 'Oii'])
            text = choice(['Bem vindo(a) de volta! 😉 ', 'Que bom que voltou! 😁', 'Que bom te ver novamente! 😁'])
            dispatcher.utter_message(f'{hi_text}! {text}')

        return[FollowupAction('action_check_login')]