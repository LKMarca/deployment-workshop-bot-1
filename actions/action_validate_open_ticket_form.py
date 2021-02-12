from .__init__ import *


# =======================================================================================
# Actions title_form - forms to get and analysis the duplicate titles
# =======================================================================================
class ActionsOpenticketForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_open_ticket_form"

    # valida o titulo colocado pelo usuario
    def validate_title_slot(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        title = tracker.get_slot('title_slot')
        error = tracker.get_slot('error_collect')
        request = ['MAMA MIA', 'ERRO', 'BUG']
        log(tracker.latest_message)
        # response = tracker.latest_message['intent']['name']
        if title in request:
            dispatcher.utter_message('Ops! Parece que já existe um outro chamado com esse mesmo título!')
            return {'title_slot': None, 'duplicate_title_slot': True, "error_collect": '0'}
        # por uma validação de tamanho ou algo especifico
        elif len(title) >= 5 and len(title) <= 50:
            return{"error_collect": '0', 'title_slot': title}
        else:
            # fallback
            if error == '0':
                error = '1'
                return{"error_collect": error, 'title_slot': None}
            elif error == '1':
                error = '2'
                return{"error_collect": error, 'title_slot': None}
            elif error == '2':
                error = '0'
                continue_finish = '1'
                dispatcher.utter_message('Que pena! O título desse defeito ainda está inválido! 😞')
                dispatcher.utter_message('Infelizmente não vou conseguir te ajudar nesse momento! ')
                dispatcher.utter_message('Nesse caso, podemos tentar novamente mais tarde! 😉')
                dispatcher.utter_message('Tenha um ótimo dia! Até mais! 👋')
                return{"error_collect": error, 'title_slot': False, 'count_finish': continue_finish, 'details_slot': False, 'check_details_slot': False}
            else:
                error = '0'
                continue_finish = '1'
                dispatcher.utter_message('Que pena! O título desse defeito ainda está inválido! 😞')
                dispatcher.utter_message('Infelizmente não vou conseguir te ajudar nesse momento! ')
                dispatcher.utter_message('Nesse caso, podemos tentar novamente mais tarde! 😉')
                dispatcher.utter_message('Tenha um ótimo dia! Até mais! 👋')
                return{"error_collect": error, 'title_slot': False, 'count_finish': continue_finish, 'details_slot': False, 'check_details_slot': False}
        return

    # valida a descrição colocado pelo usuario
    def validate_details_slot(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        details = tracker.get_slot('details_slot')
        error = tracker.get_slot('error_collect')
        log(tracker.latest_message)
        if len(details) >= 10 and len(details) <= 80:
            return{"error_collect": '0', "details_slot": details}
        else:
            # fallback
            if error == '0':
                error = '1'
                return{"error_collect": error, "details_slot": None}
            elif error == '1':
                error = '2'
                return{"error_collect": error, "details_slot": None}
            elif error == '2':
                error = '0'
                continue_finish = '1'
                dispatcher.utter_message('Que pena! A descrição desse defeito ainda está inválida! 😞')
                dispatcher.utter_message('Infelizmente não vou conseguir te ajudar nesse momento! ')
                dispatcher.utter_message('Nesse caso, podemos tentar novamente mais tarde! 😉')
                dispatcher.utter_message('Tenha um ótimo dia! Até mais! 👋')
                return{"error_collect": error, 'title_slot': False, 'count_finish': continue_finish, 'details_slot': False, 'check_details_slot': False}
            else:
                error = '0'
                continue_finish = '1'
                dispatcher.utter_message('Que pena! A descrição desse defeito ainda está inválida! 😞')
                dispatcher.utter_message('Infelizmente não vou conseguir te ajudar nesse momento! ')
                dispatcher.utter_message('Nesse caso, podemos tentar novamente mais tarde! 😉')
                dispatcher.utter_message('Tenha um ótimo dia! Até mais! 👋')
                return{"error_collect": error, 'title_slot': False, 'count_finish': continue_finish, 'details_slot': False, 'check_details_slot': False}

# valida os se está tudo certo com o titulo e o detalhes do bug colocado pelo usuario
    def validate_check_details_slot(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        error = tracker.get_slot('error_collect')
        response = tracker.latest_message['intent']['name']
        log(tracker.latest_message)
        if response == 'affirm_intent':
            dispatcher.utter_message('Prontinho! O seu defeito foi aberto com sucesso! 🥳 ')
            dispatcher.utter_message('Nº do defeito: {}{}{}.{}{}{}.{}{}{}'.format(randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 9), randint(0, 100), randint(0, 100), randint(0, 100), randint(0, 9), randint(0, 100)))
            dispatcher.utter_message('Agora é só acompanhar a tratativa! 😉')
            continue_finish = '1'
            return{"error_collect": '0', 'count_finish': continue_finish, "check_details_slot": True}
        elif response == 'deny_intent' or response == 'come_back_intent':
            dispatcher.utter_message('Certo, não se preocupe! 😊  Vou corrigir isso para você!')
            return {'title_slot': None, "details_slot": None, 'error_collect': 'again', 'check_details_slot': None}
        else:
            # fallback
            if error == '0':
                error = '1'
                return{"error_collect": error, "check_details_slot": None}
            elif error == '1':
                error = '2'
                return{"error_collect": error, "check_details_slot": None}
            elif error == '2':
                error = '3'
                return{"error_collect": error, "check_details_slot": None}
            else:
                error = '0'
                return{"error_collect": error, "check_details_slot": None}


# ==================================================================================
# Actions action_ask_title_slot -  action que pergunta sobre o titulo do defeito
# ==================================================================================
class AskForSlotTitleSlot(Action):
    def name(self) -> Text:
        return "action_ask_title_slot"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        channel = tracker.get_latest_input_channel()
        response = tracker.latest_message['intent']['name']
        if error == 'again':
            dispatcher.utter_message('Vamos começar novamente! Me informe um título para adicionar no registro da ocorrência desse defeito')
            return [SlotSet('error_collect', '0'), SlotSet('duplicate_title_slot', False)]
        elif error == '0' and response != 'help_intent':
            if channel == 'socketio':
                dispatcher.utter_message(text='Ok!😊 Agora me **informe um título** para continuarmos com a abertura do defeito!')
                dispatcher.utter_message(text='**Obs: O título deve conter entre 5 à 50 caracteres**')
            elif channel == 'cmdline':
                dispatcher.utter_message(text='Ok!😊 Agora me informe um título para continuarmos com a abertura do defeito!')
                dispatcher.utter_message(text='Obs: O título deve conter entre 5 à 50 caracteres')
            else:
                dispatcher.utter_message(json_message={'text': 'Ok!😊 Agora me <b>informe um título</b> para continuarmos com a abertura do defeito!', 'parse_mode': 'HTML'})
                dispatcher.utter_message(json_message={'text': '<b>Obs: O título deve conter entre 5 à 50 caracteres</b>', 'parse_mode': 'HTML'})
        elif error == '1':
            dispatcher.utter_message('Ops! Infelizmente o título que você me informou é inválido! 😔')
            if channel == 'socketio':
                dispatcher.utter_message('**Lembrando que o título deve conter de 5 à 50 caracteres!** 😉')
                dispatcher.utter_message('Agora, **me informe novamente o título** para esse defeito!')
            else:
                dispatcher.utter_message(json_message={'text': '<b>Lembrando que o título deve conter de 5 à 50 caracteres!</b> 😉', 'parse_mode': 'HTML'})
                dispatcher.utter_message(json_message={'text': 'Agora, <b>me informe novamente o título</b> para esse defeito!', 'parse_mode': 'HTML'})
        elif error == '2':
            dispatcher.utter_message('Poxa! O título que você me informou continua sendo inválido! 😞')
            if channel == 'socketio':
                dispatcher.utter_message('**O título para a abertura de defeito deve ter de 5 à 50 caracteres!** 😉')
                dispatcher.utter_message('Vamos tentar novamente! Me **informe o título** para a abertura do defeito!')
            else:
                dispatcher.utter_message(json_message={'text': '<b>O título para a abertura de defeito deve ter de 5 à 50 caracteres!</b> 😉', 'parse_mode': 'HTML'})
                dispatcher.utter_message(json_message={'text': 'Vamos tentar novamente! Me <b>informe o título</b> para a abertura do defeito!', 'parse_mode': 'HTML'})
        elif error == '3':
            dispatcher.utter_message('Que pena! O título desse defeito ainda está inválido! 😞')
            dispatcher.utter_message('Infelizmente não vou conseguir te ajudar nesse momento! ')
            dispatcher.utter_message('Nesse caso, podemos tentar novamente mais tarde! 😉')

        return []


# ===================================================================================
# Actions action_ask_details_slot -  action que pergunta sobre os detalhes do defeito
# ===================================================================================
class AskForSlotDetailsSlot(Action):
    def name(self) -> Text:
        return "action_ask_details_slot"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        channel = tracker.get_latest_input_channel()
        data = tracker.get_slot('user_data')
        response = tracker.latest_message['intent']['name']
        if error == '0' and response != 'help_intent':
            if data['attachment'] == 'Y':
                dispatcher.utter_message('Ótimo! 😊 Eu gerei o ECT da execução baseado nas evidências que você anexou em cada step da sua execução do teste!')
                dispatcher.utter_message('Esses são os arquivos que eu encontrei:')
                attachments = get_attachment(int(data['id']))
                for i in attachments:
                    attachment_file = i['Fields'][2]['values'][0]['value']
                    dispatcher.utter_message(f'Nome do arquivo: {attachment_file}')
            else:
                dispatcher.utter_message('Infelizmente não encontrei nenhum anexo nos steps da execução desse teste!')
                dispatcher.utter_message('Por conta disso, não vou conseguir gerar o ECT para você 😔')
            if channel == 'socketio':
                dispatcher.utter_message(text='Só mais uma coisa! **Descreva os detalhes** sobre esse defeito!')
                dispatcher.utter_message(text='**Obs: A descrição deve conter entre 10 à 80 caracteres**')
            elif channel == 'cmdline':
                dispatcher.utter_message(text='Só mais uma coisa! Descreva os detalhes sobre esse defeito!')
                dispatcher.utter_message(text='Obs: A descrição deve conter entre 10 à 80 caracteres')
            else:
                dispatcher.utter_message(json_message={'text': 'Só mais uma coisa! <b>Descreva os detalhes</b> sobre esse defeito!', 'parse_mode': 'HTML'})
                dispatcher.utter_message(json_message={'text': '<b>Obs: A descrição deve conter entre 10 à 80 caracteres</b>', 'parse_mode': 'HTML'})
        if error == '1':
            dispatcher.utter_message('Ops! Infelizmente a descrição que você me informou é inválido! 😔')
            if channel == 'socketio':
                dispatcher.utter_message('**Lembrando que a descrição dos detalhes deve conter de 10 à 80 caracteres!** 😉')
                dispatcher.utter_message('Agora, **descreva novamente os detalhes** para esse defeito!')
            else:
                dispatcher.utter_message(json_message={'text': '<b>Lembrando que a descrição dos detalhes deve conter de 10 à 80 caracteres!</b> 😉', 'parse_mode': 'HTML'})
                dispatcher.utter_message(json_message={'text': 'Agora, <b>descreva novamente os detalhes</b> para esse defeito!', 'parse_mode': 'HTML'})
        if error == '2':
            dispatcher.utter_message('Poxa! A descrição que você me informou continua sendo inválido! 😞')
            if channel == 'socketio':
                dispatcher.utter_message('**A descrição dos detalhes sobre o defeito deve ter de 10 à 80 caracteres!** 😉')
                dispatcher.utter_message('Vamos tentar novamente! **Descreva os detalhes** para esse defeito!')
            else:
                dispatcher.utter_message(json_message={'text': '<b>A descrição dos detalhes sobre o defeito deve ter de 10 à 80 caracteres!</b> 😉', 'parse_mode': 'HTML'})
                dispatcher.utter_message(json_message={'text': 'Vamos tentar novamente! <b>Descreva os detalhes</b> para esse defeito!', 'parse_mode': 'HTML'})
        if error == '3':
            dispatcher.utter_message('Que pena! O título desse defeito ainda está inválido! 😞')
            dispatcher.utter_message('Infelizmente não vou conseguir te ajudar nesse momento! ')
            dispatcher.utter_message('Nesse caso, podemos tentar novamente mais tarde! 😉')

        return []


# ========================================================================================================
# Actions action_ask_check_details_slot -  action que pergunta se ta tudo certo com os detalhes do chamado
# ========================================================================================================
class AskForSlotCheckDetailsSlot(Action):
    def name(self) -> Text:
        return "action_ask_check_details_slot"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        title = tracker.get_slot('title_slot')
        details = tracker.get_slot('details_slot')
        if error == '0':
            dispatcher.utter_message(f'Título: {title}')
            dispatcher.utter_message(f'Detalhes: {details}')
            dispatcher.utter_message(text='As informações estão corretas?', buttons=[{'type': 'postBack', "title": "Sim, estão corretas", "payload": "Sim, estão corretas"}, {'type': 'postBack', "title": "Não estão corretas", "payload": "Não"}])
        if error == '1':
            dispatcher.utter_message('Ops! Não consegui entender o que você quis dizer 🤔')
            dispatcher.utter_message('As informações de título e descrição sobre o registro da ocorrência desse defeito estão corretas?')
            dispatcher.utter_message(text='As informações estão corretas?', buttons=[{'type': 'postBack', "title": "Sim, estão corretas", "payload": "sim"}, {'type': 'postBack', "title": "Não estão corretas", "payload": "Não"}])
        if error == '2':
            dispatcher.utter_message('Desculpe, ainda não consegui entender se as informações estão corretas ou não 😔')
            dispatcher.utter_message('Esses são os detalhes sobre o registro da ocorrência desse defeito:')
            dispatcher.utter_message(f'Título: {title}')
            dispatcher.utter_message(f'Detalhes: {details}')
            dispatcher.utter_message(text='As informações estão corretas?', buttons=[{'type': 'postBack', "title": "Sim, estão corretas", "payload": "Sim, estão corretas"}, {'type': 'postBack', "title": "Não estão corretas", "payload": "Não"}])
        return []