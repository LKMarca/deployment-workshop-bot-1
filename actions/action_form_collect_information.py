from .__init__ import *
from .utils import get_by_id


# ======================================================================================
# Actions validate_collect_fomr - forms to validate ct and generate ect
# ======================================================================================
class ActionsCollectInformation(FormValidationAction):
    def name(self) -> Text:
        return "validate_collect_form"

    def validate_ct(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        data = tracker.get_slot('user_data')
        page = int(tracker.get_slot('page_ct'))
        number = str(filter_entities(tracker.latest_message, 'number', 'value'))
        ordinal = str(filter_entities(tracker.latest_message, 'ordinal', 'value'))
        response = tracker.latest_message['intent']['name']
        user = tracker.get_slot('user_alm_qc')
        all_ct = tracker.get_slot('all_ct')
        ct_name = tracker.get_slot('ct')
        if response == 'view_more_intent':
            page += 1
            if len(all_ct) < page:
                page = 1
            error = '0'
            return{"error_collect": error, 'count_finish': '0', "ct": None, 'page_ct': page}
        if len(all_ct) > 0:
            if ordinal is not None and str(ordinal) <= '3':
                data = all_ct[str(page)][int(ordinal)-1]
                data = get_by_id(user, data['id'])
                if len(data) > 0:
                    return {"error_collect": '0', "ct": data['test-case'], 'id_': data['id'], 'page_ct': 1, 'user_data': data}
            else:
                for x in all_ct:
                    x = all_ct[x]
                    for i in x:

                        if str(number) == str(i['id']) and response == 'informations_intent':
                            data = get_by_id(user, i['id'])
                            if len(data) > 0:
                                return {"error_collect": '0', "ct": data['test-case'], 'id_': data['id'], 'page_ct': 1, 'user_data': data}

                        elif i['test-case'] == ct_name or i['id'] == ct_name:
                            data = get_by_id(user, i['id'])
                            if len(data) > 0:
                                return {"error_collect": '0', "ct": data['test-case'], 'id_': data['id'], 'page_ct': 1, 'user_data': data}

        # fallback
        ct = None
        if error == '0':
            error = '1'
            return{"error_collect": error, "ct": ct}
        elif error == '1':
            error = '2'
            return{"error_collect": error, "ct": ct}
        elif error == '2':
            error = '3'
            return{"error_collect": error, "ct": ct}
        else:
            error = '0'
            return{"error_collect": error}

    def validate_collect(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        response = tracker.latest_message['intent']['name']
        collect = tracker.get_slot('collect')
        informations = tracker.get_slot('informations')
        correct_informations = tracker.get_slot('correct_informations')
        response = tracker.latest_message['intent']['name']
        if response == 'come_back_intent' or response == 'deny_intent':
            return{"ct": None, "id_": None, "error_collect": '0', "collect": None}
        if response == 'affirm_intent':
            collect = True
            informations = True
            correct_informations = True
            return{"error_collect": '0', "collect": collect, "informations": informations, "correct_informations": correct_informations}
        else:
            # fallback
            if error == '0':
                error = '1'
                return{"collect": None, "error_collect": error}
            elif error == '1':
                error = '2'
                return{"collect": None, "error_collect": error}
            elif error == '2':
                error = '3'
                return{"collect": None, "error_collect": error}
            else:
                error = '0'
                return{"error_collect": error}

    def validate_informations(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        response = tracker.latest_message['intent']['name']
        collect = tracker.get_slot('collect')
        response = tracker.latest_message['intent']['name']
        if response == 'come_back_intent' or response == 'deny_intent':
            return{"ct": None, "id_": None, "error_collect": '0', "collect": None, "informations": None}
        if response == 'informations_intent':
            informations = True
            return{"informations": informations, "error_collect": '0'}
        else:
            # fallback
            if error == '0':
                error = '1'
                collect = False
                return{"collect": collect, "informations": None, "error_collect": error}
            elif error == '1':
                error = '2'
                collect = False
                return{"collect": collect, "informations": None, "error_collect": error}
            elif error == '2':
                error = '3'
                collect = False
                return{"collect": collect, "informations": None, "error_collect": error}
            else:
                error = '0'
                return{"error_collect": error}

    def validate_correct_informations(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        log(tracker.latest_message)
        response = tracker.latest_message['intent']['name']
        error = tracker.get_slot('error_collect')
        ct_value = filter_entities(tracker.latest_message, 'ct_entity', 'value')
        id_value = filter_entities(tracker.latest_message, 'id_entity', 'value')
        correct_informations = tracker.get_slot('correct_informations')
        response = tracker.latest_message['intent']['name']
        if response == 'come_back_intent' or response == 'deny_intent':
            return{"ct": None, "id_": None, "error_collect": '0', "collect": None, "informations": None, "correct_informations": None}
        if response == 'informations_intent':
            correct_informations = True
            ct = ct_value
            id_ = id_value
            return{"error_collect": '0', "correct_informations": correct_informations, "ct": ct, "id_": id_}
        else:
            # fallback
            if error == '0':
                error = '1'
                collect = False
                return{"collect": collect, "error_collect": error}
            elif error == '1':
                error = '2'
                collect = False
                return{"collect": collect, "error_collect": error}
            elif error == '2':
                error = '3'
                collect = False
                return{"collect": collect, "error_collect": error}
            else:
                error = '0'
                return{"error_collect": error, "error_collect": error}


# ======================================================================================
# Actions action_ask_ct -  Shows the available CTs to the user
# ======================================================================================
class AskForCT(Action):

    def name(self) -> Text:
        return "action_ask_ct"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        # data = tracker.get_slot('user_data')
        continue_finish = tracker.get_slot('count_finish')
        channel = tracker.get_latest_input_channel()
        # last_event = tracker.get_last_event_for('user', skip=0)
        all_ct = tracker.get_slot('all_ct')
        channel = tracker.get_latest_input_channel()
        page = int(tracker.get_slot('page_ct'))
        prediction = tracker.latest_message
        buttons = []
        # fallback
        if error == '1':
            dispatcher.utter_message(text='Desculpa, não consegui identificar o CT ou o ID que você me informou!')
        elif error == '2':
            dispatcher.utter_message(text='Ainda não consegui identificar o CT ou o ID que você me informou!')
        elif error == '3':
            if channel == 'socketio':
                dispatcher.utter_message(text='Infelizmente não vou conseguir te ajudar a registrar o defeito! ☹️ Nesse caso, você pode abrir o ALM QC e registrá-lo por lá! 😉')
            elif channel == 'telegram':
                dispatcher.utter_message(json_message={'text': 'Infelizmente não vou conseguir te ajudar a registrar o defeito! ☹️\nNesse caso, você pode abrir o ALM QC e registrá-lo por lá! 😉', 'parse_mode': 'HTML'})
            elif channel == 'botframework':
                dispatcher.utter_message(json_message={'text': 'Infelizmente não vou conseguir te ajudar a registrar o defeito! ☹️<br>Nesse caso, você pode abrir o ALM QC e registrá-lo por lá! 😉', 'parse_mode': 'HTML'})
            return[FollowupAction('action_system')]
        # fim fallback
        if prediction['intent']['name'] == 'deny_intent' or prediction['intent']['name'] == 'come_back_intent':
            texto = choice(['Ok!', 'Certo!', 'Tudo bem!'])
            dispatcher.utter_message(f'{texto} Vamos lá novamente! 😊')
        elif prediction['intent']['name'] == 'view_more_intent':
            texto = choice(['Ok!', 'Certo!', 'Tudo bem!'])
            dispatcher.utter_message(f'{texto} Encontrei mais alguns casos de teste para você! 😊')
        if len(all_ct) > 0:
            # botões para webchat
            if channel == 'socketio':
                for i in all_ct[f'{page}']:
                    ct = i
                    button = {'title': ct['test-case'], 'payload': ct['id']}
                    buttons.append(button)
                # caso esxista varios CT, adicionar botão ver mais
                if len(all_ct) > 1:
                    ver_mais = {'title': 'Ver mais', 'payload': 'Ver Mais'}
                    buttons.append(ver_mais)
                if continue_finish == '0':
                    dispatcher.utter_message(text="Agora, selecione o teste que você está executando ou informe o ID! 😉", button_type="vertical", buttons=buttons)
                else:
                    dispatcher.utter_message(text="Caso queira abrir um novo defeito, **selecione o teste que você está executando ou informe o ID!** 😉", button_type="vertical", buttons=buttons)
            # botões para Telegram e Teams
            else:
                for i in all_ct[f'{page}']:

                    ct = i
                    button = {"type": "postBack", 'title': ct['test-case'], 'payload': ct['id']}
                    buttons.append(button)
                if len(all_ct) > 1:
                    ver_mais = {"type": "postBack", 'title': 'Ver mais', 'payload': 'Ver Mais'}
                    buttons.append(ver_mais)

                if continue_finish == '0':
                    dispatcher.utter_message(text="Agora, selecione o teste que você está executando ou informe o ID! 😉", button_type="vertical", buttons=buttons)
                else:
                    if channel == "telegram":
                        dispatcher.utter_message(text="Caso queira abrir um novo defeito, selecione o teste que você está executando ou informe o ID! 😉", button_type="vertical", buttons=buttons)
                    else:
                        dispatcher.utter_message(text="Caso queira abrir um novo defeito, <b>selecione o teste que você está executando ou informe o ID!</b> 😉", button_type="vertical", buttons=buttons)
        return[]


# ======================================================================================
# Actions action_ask_collect -  checks the information with the user
# ======================================================================================
class AskForCollect(Action):
    def name(self) -> Text:
        return "action_ask_collect"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        data = tracker.get_slot('user_data')
        id_ = data['id']
        ct = data['test-case']
        name_run = data['name-run']
        owner_run = data['owner-run']
        origin_system = data['origin-system']
        status_run = data['status-run']
        target_cycle = data['target-cycle']
        channel = tracker.get_latest_input_channel()
        if error == '3':
            dispatcher.utter_message('Desculpe, mas não consegui entender! ☹️')
            return[FollowupAction('action_system')]

        if error == '0':
            dispatcher.utter_message("Certo! Encontrei algumas informações sobre esse teste:")
            channel = tracker.get_latest_input_channel()
            if channel == 'socketio':
                dispatcher.utter_message(f'**Caso de Teste:** {ct}  **ID:** {id_} **Nome do run:** {name_run} **Target Cycle:** {target_cycle} **Dono do run:** {owner_run} **Sistema Origem:** {origin_system} **Status:** {status_run}')
            elif channel == 'cmdline':
                dispatcher.utter_message(f'Caso de Teste: {ct}\n ID: {id_}\n Nome do run: {name_run}\n Target Cycle: {target_cycle}\n Dono do run: {owner_run}\n Sistema Origem: {origin_system}\n Status: {status_run}')
            elif channel == 'telegram':
                dispatcher.utter_message(json_message={'text': f'<b>Caso de Teste:</b> {ct}\n <b>ID:</b> {id_}\n <b>Target Cycle:</b> {target_cycle}\n <b>Nome do run:</b> {name_run}\n <b>Dono do run:</b> {owner_run}\n <b>Sistema Origem:</b> {origin_system}\n <b>Status:</b> {status_run}\n ', 'parse_mode': 'HTML'})
            elif channel == 'botframework':
                dispatcher.utter_message(json_message={'text': f'<b>Caso de Teste:</b> {ct} </br> <b>ID:</b> {id_} </br> <b>Target Cycle:</b> {target_cycle}</br> <b>Nome do run:</b> {name_run}</br> <b>Dono do run:</b> {owner_run}</br> <b>Sistema Origem:</b> {origin_system}</br> <b>Status:</b> {status_run} </br> ', 'parse_mode': 'HTML'})
            else:
                dispatcher.utter_message(json_message={'text': f'<b>Caso de Teste:</b> {ct} \n <b>ID:</b> {id_} \n <b>Target Cycle:</b> {target_cycle}\n <b>Nome do run:</b> {name_run}\n <b>Dono do run:</b> {owner_run}\n <b>Sistema Origem:</b> {origin_system}\n <b>Status:</b> {status_run} \n', 'parse_mode': 'HTML'})
            dispatcher.utter_message(text='Essas informações estão corretas?', buttons=[{"type": "postBack", "title": "Sim, estão corretas", "payload": "Sim, estão corretas"}, {"type": "postBack", "title": "Não estão corretas", "payload": "Não"}, {"type": "postBack", "title": "Voltar", "payload": "voltar"}])
        # fallback
        else:
            if channel == 'socketio':
                dispatcher.utter_message(f'**Caso de Teste:** {ct}  **ID:** {id_} **Nome do run:** {name_run} **Target Cycle:** {target_cycle} **Dono do run:** {owner_run} **Sistema Origem:** {origin_system} **Status:** {status_run}')
            elif channel == 'telegram':
                dispatcher.utter_message(json_message={'text': f'<b>Caso de Teste:</b> {ct}\n <b>ID:</b> {id_}\n <b>Target Cycle:</b> {target_cycle}\n <b>Nome do run:</b> {name_run}\n <b>Dono do run:</b> {owner_run}\n <b>Sistema Origem:</b> {origin_system}\n <b>Status:</b> {status_run}\n ', 'parse_mode': 'HTML'})
            elif channel == 'botframework':
                dispatcher.utter_message(json_message={'text': f'<b>Caso de Teste:</b> {ct} </br> <b>ID:</b> {id_} </br> <b>Target Cycle:</b> {target_cycle}</br> <b>Nome do run:</b> {name_run}</br> <b>Dono do run:</b> {owner_run}</br> <b>Sistema Origem:</b> {origin_system}</br> <b>Status:</b> {status_run} </br> ', 'parse_mode': 'HTML'})
            else:
                dispatcher.utter_message(json_message={'text': f'<b>Caso de Teste:</b> {ct}\n <b>ID:</b> {id_}\n <b>Target Cycle:</b> {target_cycle}\n <b>Nome do run:</b> {name_run}\n <b>Dono do run:</b> {owner_run}\n <b>Sistema Origem:</b> {origin_system}\n <b>Status:</b> {status_run}\n ', 'parse_mode': 'HTML'})
            if channel == 'socketio' or channel == 'cmdline':
                text = choice(['Ops! Não consegui entender! 🤔 ', 'Poxa! Não consegui entender! 🤔 '])
            elif channel == 'telegram':
                text = choice(['Ops! Não consegui entender! 🤔\n', 'Poxa! Não consegui entender! 🤔\n'])
            elif channel == 'botframework':
                text = choice(['Ops! Não consegui entender! 🤔<br>', 'Poxa! Não consegui entender! 🤔<br>'])
            if error == '1':
                if channel == 'socketio' or channel == 'cmdline' :
                    dispatcher.utter_message(text=text)
                elif channel == 'telegram':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
                elif channel == 'botframework':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
                dispatcher.utter_message(text='Essas informações estão corretas?', buttons=[{"type": "postBack", "title": "Sim, estão corretas", "payload": "Sim, estão corretas"}, {"type": "postBack", "title": "Não estão corretas", "payload": "Não"}, {"type": "postBack", "title": "Voltar", "payload": "voltar"}])
            elif error == '2':
                if channel == 'socketio' or channel == 'cmdline':
                    dispatcher.utter_message(text=text)
                elif channel == 'telegram':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
                elif channel == 'botframework':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
                dispatcher.utter_message(text='Essas informações estão corretas?', buttons=[{"type": "postBack", "title": "Sim, estão corretas", "payload": "Sim, estão corretas"}, {"type": "postBack", "title": "Não estão corretas", "payload": "Não"}, {"type": "postBack", "title": "Voltar", "payload": "voltar"}])
        return []


# ======================================================================================
# Actions action_ask_informations -  ask user what information incorrect
# ======================================================================================
class AskForInformations(Action):
    def name(self) -> Text:
        return "action_ask_informations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        collect = tracker.get_slot('collect')
        data = tracker.get_slot('user_data')
        id_ = data['target-cycle']
        ct = data['test-case']
        name_run = data['name-run']
        owner_run = data['owner-run']
        origin_system = data['origin-system']
        status_run = data['status-run']
        if collect:
            return{"informations": True}
        if error == '0':
            dispatcher.utter_message(text='Certo! Nesse caso, me diga quais delas devem ser alteradas e seus valores corretos! 😉', buttons=[{"type": "postBack", "title": f"{ct}", "payload": f"{ct}"}, {"type": "postBack", "title": f"{id_}", "payload": f"{id_}"}, {"type": "postBack", "title": f"{name_run}", "payload": f"{name_run}"}, {"type": "postBack", "title": f"{owner_run}", "payload": f"{owner_run}"}, {"type": "postBack", "title": f"{origin_system}", "payload": f"{origin_system}"}, {"type": "postBack", "title": f"{status_run}", "payload": f"{status_run}"}])
        # fallback
        else:
            text = choice(['Ops! Não consegui entender! 🤔 ', 'Poxa! Não consegui entender!'])
            if error == '1':
                dispatcher.utter_message(text=text)
                dispatcher.utter_message(text='Me diga quais informações devem ser alteradas e seus valores corretos! 😉', buttons=[{"type": "postBack", "title": f"{ct}", "payload": f"{ct}"}, {"type": "postBack", "title": f"{id_}", "payload": f"{id_}"}, {"type": "postBack", "title": f"{name_run}", "payload": f"{name_run}"}, {"type": "postBack", "title": f"{owner_run}", "payload": f"{owner_run}"}, {"type": "postBack", "title": f"{origin_system}", "payload": f"{origin_system}"}, {"type": "postBack", "title": f"{status_run}", "payload": f"{status_run}"}])
            elif error == '2':
                dispatcher.utter_message(text=text)
                dispatcher.utter_message(text='Me diga quais informações devem ser alteradas e seus valores corretos! 😉', buttons=[{"type": "postBack", "title": f"{ct}", "payload": f"{ct}"}, {"type": "postBack", "title": f"{id_}", "payload": f"{id_}"}, {"type": "postBack", "title": f"{name_run}", "payload": f"{name_run}"}, {"type": "postBack", "title": f"{owner_run}", "payload": f"{owner_run}"}, {"type": "postBack", "title": f"{origin_system}", "payload": f"{origin_system}"}, {"type": "postBack", "title": f"{status_run}", "payload": f"{status_run}"}])
            else:
                dispatcher.utter_message('Desculpe, mas não consegui entender! ☹️')
                return[FollowupAction('action_system')]


# ======================================================================================
# Actions action_ask_correct_informations -  ask user what informations for change
# ======================================================================================
class AskForCorrectInformations(Action):
    def name(self) -> Text:
        return "action_ask_correct_informations"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('error_collect')
        channel = tracker.get_latest_input_channel()
        if error == '0':
            dispatcher.utter_message("Entendi! Agora me informe quais seriam as informações corretas, para que eu possa corrigí-las!")
        # fallback
        else:
            if channel == 'socketio':
                text = choice(['Ops! Não consegui entender! 🤔 Me diga quais informações devem ser alteradas e seus valores corretos! 😉', 'Poxa! Não consegui entender! 🤔 Me diga quais informações devem ser alteradas e seus valores corretos! 😉'])
            elif channel == 'telegram':
                text = choice(['Ops! Não consegui entender! 🤔\nMe diga quais informações devem ser alteradas e seus valores corretos! 😉', 'Poxa! Não consegui entender! 🤔\nMe diga quais informações devem ser alteradas e seus valores corretos! 😉'])
            elif channel == 'botframework':
                text = choice(['Ops! Não consegui entender! 🤔<br>Me diga quais informações devem ser alteradas e seus valores corretos! 😉', 'Poxa! Não consegui entender! 🤔<br>Me diga quais informações devem ser alteradas e seus valores corretos! 😉'])
            if error == '1':
                if channel == 'socketio':
                    dispatcher.utter_message(text=text)
                elif channel == 'telegram':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
                elif channel == 'botframework':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
            elif error == '2':
                if channel == 'socketio':
                    dispatcher.utter_message(text=text)
                elif channel == 'telegram':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
                elif channel == 'botframework':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
            else:
                dispatcher.utter_message('Desculpe, mas não consegui entender! ☹️')
                return[FollowupAction('action_system')]


# ======================================================================================
# Actions action_finish_collect -  action with a final message for check informacions
# ======================================================================================
class ActionFinishCollect(Action):
    def name(self) -> Text:
        return "action_finish_collect"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict) -> List[EventType]:
        log(tracker.latest_message)
        dispatcher.utter_message("Ótimo! Já consegui corrigir essas informações para você! 🙂")
        return[FollowupAction("action_check_n1")]