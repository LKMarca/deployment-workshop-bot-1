from .__init__ import *


# =============================================================
# ActionGoodbye - action in case the user needs help
# =============================================================
class ActionHelp(Action):
    def name(self) -> Text:
        return "action_help"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # channel = tracker.get_latest_input_channel()
        # continue_finish = tracker.get_slot('count_finish')
        error1 = '0'
        error2 = '0'
        log(tracker.latest_message)
        last_slot = tracker.get_slot('requested_slot')
        if last_slot is not None:
            dispatcher.utter_message(text='Não se preocupe, estou aqui para te ajudar! 😉')
        if last_slot == "user_alm_qc":
            dispatcher.utter_message(text='Nesse caso, para iniciarmos a abertura do defeito, primeiro preciso que você me informe o seu usuário do ALM QC.')
            dispatcher.utter_message(text='Caso você não tenha um usuário, você pode abrir o ALM QC e registrar o seu defeito por lá! 😄')
        elif last_slot == "ct":
            dispatcher.utter_message(text='Para continuarmos com a abertura do defeito, preciso que você selecione o CT correspondente ao teste que está executando!')
            dispatcher.utter_message(text='Caso o CT que você queira não esteja entre as 3 opções, você pode clicar em “Ver mais” ou informar o ID! 😄')
        elif last_slot == "collect":
            dispatcher.utter_message(text='Antes de continuarmos, preciso que você confirme para mim se as informações sobre esse teste estão ou não corretas! ')
            dispatcher.utter_message(text='Caso essas informações não estejam corretas, podemos voltar e escolher outro caso de teste! 😀')
        elif last_slot == "title_slot":
            dispatcher.utter_message(text='Para continuarmos, preciso que você me informe um título que esteja relacionado com o motivo da abertura para esse defeito!')
        elif last_slot == "details_slot":
            dispatcher.utter_message(text='Para continuarmos, preciso que você me informe uma descrição relatando todos os detalhes sobre esse defeito!')
        # if channel == 'socketio':
        #     dispatcher.utter_message(text='Estou aqui para te ajudar na abertura de defeitos 😉')
        #     dispatcher.utter_message(text='Para isso, vou precisar que você me diga o teste que está executando e confirme suas informações!')
        #     dispatcher.utter_message(text='Se estiver tudo certo com o seu teste, é só me informar um título e uma descrição para finalizarmos a abertura do defeito!')
        # elif channel == 'telegram':
        #     dispatcher.utter_message(json_message={'text': 'Estou aqui para te ajudar na abertura de defeitos 😉\nPara isso, vou precisar que você me diga o teste que está executando e confirme suas informações!\nSe estiver tudo certo com o seu teste, é só me informar um título e uma descrição para finalizarmos a abertura do defeito!', 'parse_mode': 'HTML'})
        # elif channel == 'botframework':
        #     dispatcher.utter_message(json_message={'text': 'Estou aqui para te ajudar na abertura de defeitos 😉</br>Para isso, vou precisar que você me diga o teste que está executando e confirme suas informações!</br>Se estiver tudo certo com o seu teste, é só me informar um título e uma descrição para finalizarmos a abertura do defeito!', 'parse_mode': 'HTML'})
        # else:
        #     dispatcher.utter_message(json_message={'text': 'Estou aqui para te ajudar na abertura de defeitos 😉\nPara isso, vou precisar que você me diga o teste que está executando e confirme suas informações!\nSe estiver tudo certo com o seu teste, é só me informar um título e uma descrição para finalizarmos a abertura do defeito!', 'parse_mode': 'HTML'})
        return [SlotSet('error_collect', error1), SlotSet('erro_fluxo_try', error2)]