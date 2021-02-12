from .__init__ import *


# ========================================================================
# Actions ComeBack - Mensagem avisando que de certo ponto não para voltar
# ========================================================================
class ActionComeBack(Action):
    # Nome de actions para o rasa
    def name(self) -> Text:
        return "action_come_back"

    # Verifica se algo deu errado no checklist
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        log(tracker.latest_message)
        channel = tracker.get_latest_input_channel()
        error = tracker.latest_message['intent']['name']
        intents = ['come_back_intent']
        if error in intents:
            dispatcher.utter_message('Ops! Infelizmente não é possível retornar antes desse ponto! 😢')
            if channel == 'socketio':
                dispatcher.utter_message(text='Caso queira entrar com outro usuário, a qualquer momento você pode digitar **“encerrar sessão”** 😉')
                dispatcher.utter_message(text='Deseja continuar ou encerrar sessão?', buttons=[{"title": "Sair", "payload": "Sair"}, {"title": "Continuar", "payload": "Continuar"}])
            else:
                dispatcher.utter_message(json_message={'text': 'Caso queira entrar com outro usuário, a qualquer momento você pode digitar <b>“encerrar sessão”</b> 😉', 'parse_mode': 'HTML'})
                if channel == 'botframework':
                    dispatcher.utter_message(text='Deseja continuar ou encerrar sessão?', buttons=[{"type": "postBack", "title": "Sair", "payload": "Sair"}, {"type": "postBack", "title": "Continuar", "payload": "Continuar"}])
                else:
                    dispatcher.utter_message(text='Deseja continuar ou encerrar sessão?', buttons=[{"type": "postBack", "title": "Sair", "payload": "Sair"}, {"type": "postBack", "title": "Continuar", "payload": "Continuar"}])
            return []
        else:
            dispatcher.utter_message(text='Ops! Não entendi o que você quis dizer! 🤔')
            dispatcher.utter_message(text='Deseja continuar ou encerrar sessão?', buttons=[{"type": "postBack", "title": "Sair", "payload": "Sair"}, {"type": "postBack", "title": "Continuar", "payload": "Continuar"}])
            
            return []