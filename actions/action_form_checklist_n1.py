from .__init__ import *


# =======================================================================================
# Actions checklist_n1_form - forms responsavel por verificar erros no checklist
# =======================================================================================
class ActionsChecklistN1Form(FormValidationAction):
    def name(self) -> Text:
        return "validate_checklist_n1_form"

    # responsavel por verificar qual foi o problema para que o forms saiba qual slot chamar

    # valida se o test_mass foi feito corretamente de acordo com usuario
    def validate_internet(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        log(tracker.latest_message)
        list_net = ['25', '50', '100']
        prediction = tracker.latest_message
        response = prediction['intent']['name']
        error = tracker.get_slot('erro_fluxo_try')
        internet = tracker.get_slot('internet')
        error = '0'
        number = str(filter_entities(tracker.latest_message, 'number', 'value'))
        if internet != True:
            if number not in list_net:
                dispatcher.utter_message('Não é disponibilizado esse pacote! 🙂 Recomendo que você verifique se todos os passos estão corretos')
                return {'internet': True, 'site': False, "erro_fluxo_try": '0', "test_mass": True, "open_bug": None}
            elif number in list_net:
                dispatcher.utter_message('Detectei que esta tudo certo!')
                return {'internet': number, "erro_fluxo_try": '0', "open_bug": True}

            if error == '0':
                error = '1'
                return{"erro_fluxo_try": error, 'test_mass': None}
            elif error == '1':
                error = '2'
                return{"erro_fluxo_try": error, 'test_mass': None}
            elif error == '2':
                dispatcher.utter_message('Hmm... Realmente não consegui entender como você gostaria de prosseguir 😔')
                dispatcher.utter_message('Infelizmente vou precisar encerrar nossa conversa ')
                return{'internet': False, 'site': True, "erro_fluxo_try": '0', 'open_bug': False}
            
            # Fallback
        else:
            if error == '0':
                return{"erro_fluxo_try": error, 'test_mass': None, "internet": True}
            elif error == '1':
                error = '2'
                return{"erro_fluxo_try": error, 'test_mass': None, "internet": True}
            elif error == '2':
                dispatcher.utter_message('Hmm... Realmente não consegui entender como você gostaria de prosseguir 😔')
                dispatcher.utter_message('Infelizmente vou precisar encerrar nossa conversa ')
                return{'internet': False, 'site': True, "erro_fluxo_try": '0', 'open_bug': False}


    # valida se o test_run foi feito corretamente de acordo com usuario
    def validate_site(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        log(tracker.latest_message)
        prediction = tracker.latest_message
        error = tracker.get_slot('erro_fluxo_try')
        response = prediction['intent']['name']
        data = tracker.get_slot('user_data')
        url = str(filter_entities(tracker.latest_message, 'url', 'value'))
        just_ct_name = data['test-case']
        site = tracker.get_slot('site')
        all_sites = get_sites()
        all_sites = all_sites[0]['prodlike']
        erro = '0'
        if site != True:
            for site in all_sites:

                if site['Name'].lower() in just_ct_name.lower():
                    if site['value'] == url:
                        dispatcher.utter_message('Certo! Me parece que você esta executando no link correto!')
                        return {"site": '1', "test_run": False, "open_bug": True, "erro_fluxo_try": '0'}
                    else:
                        dispatcher.utter_message(f"Parece que seu link não esta correto para este sistema. O correto seria {site['value']}")
                        return {"site": '1', "test_run": True, "open_bug": None, "erro_fluxo_try": '0'}
            dispatcher.utter_message('Desculpe mas não consegui indentificar o sistema em que você esta executando')
            return {"site": '1', "test_run": False, "erro_fluxo_try": '0', "open_bug": True}

            if error == '0':
                error = '1'
                return{"erro_fluxo_try": error, 'site': None}
            elif error == '1':
                error = '2'
                return{"erro_fluxo_try": error, 'site': None}
            elif error == '2':
                dispatcher.utter_message('Hmm... Realmente não consegui entender como você gostaria de prosseguir 😔')
                dispatcher.utter_message('Infelizmente vou precisar encerrar nossa conversa ')
                return{'internet': False, "site": True, "erro_fluxo_try": '0', 'open_bug': False}

        # Fallback
        if error == '0':
            return{"erro_fluxo_try": error, 'site': True}
        elif error == '1':
            error = '2'
            return{"erro_fluxo_try": error, 'site': True}
        elif error == '2':
            dispatcher.utter_message('Hmm... Realmente não consegui entender como você gostaria de prosseguir 😔')
            dispatcher.utter_message('Infelizmente vou precisar encerrar nossa conversa ')
            return{'internet': False, "site": True, "erro_fluxo_try": '0', 'open_bug': False}

    def validate_open_bug(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        log(tracker.latest_message)
        prediction = tracker.latest_message
        response = prediction['intent']['name']
        error = tracker.get_slot('erro_fluxo_try')
        if response == 'continue_intent' or response == 'affirm_intent':
            return {"erro_fluxo_try": '0', 'open_bug': True}
        elif response == 'try_again_intent' or response == 'deny_intent' or response == 'come_back_intent':
            dispatcher.utter_message('Ok! 🙂 Recomendo que você verifique o fluxo de testes que está executando!')
            dispatcher.utter_message('Confere se a massa ou o ambiente de testes estão corretos')
            return {"erro_fluxo_try": '0', 'count_finish': '1', 'open_bug': False}

        if error == '0':
            error = '1'
            dispatcher.utter_message('Desculpa, não entendi.')
            return{"erro_fluxo_try": error, 'open_bug': None}
        elif error == '1':
            error = '2'
            dispatcher.utter_message('Desculpa mas eu ainda não consegui entender.')
            return{"erro_fluxo_try": error, 'open_bug': None}
        elif error == '2':
            dispatcher.utter_message('Hmm... Realmente não consegui entender como você gostaria de prosseguir 😔')
            dispatcher.utter_message('Infelizmente vou precisar encerrar nossa conversa ')
            return{'internet': False, 'site': True, 'count_finish': '1', "erro_fluxo_try": '0', 'open_bug': False}
  
        return{'internet': False, 'site': True, "erro_fluxo_try": '0', 'open_bug': False}

# ======================================================================================
# Actions ask_test_mass -  pergunta ao usuario se ele fez tudo corretamente no test_mass
# ======================================================================================
class ActionAskInternet(Action):
    def name(self) -> Text:
        return "action_ask_internet"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('erro_fluxo_try')
        channel = tracker.get_latest_input_channel()

        if error == '0':
            dispatcher.utter_message('Percebi que você está vendendo pacote de internet.')
            dispatcher.utter_message('Qual a velocidade de internet que você está tentando vender? 🤔')
        elif error == '1':
            dispatcher.utter_message('Desculpa, não entendi!')
        elif error == '2':
            dispatcher.utter_message('Ainda não entendi!')
        
        return []


# ===================================================================================
# Actions ask_test_run - pergunta ao usuario se ele fez tudo corretamente no test_run
# ===================================================================================
class ActionAskSite(Action):
    def name(self) -> Text:
        return "action_ask_site"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('erro_fluxo_try')
        channel = tracker.get_latest_input_channel()
        if error == '0':
            dispatcher.utter_message('Qual o link do sistema que você esta utilizando?')
        elif error == '1':
            dispatcher.utter_message('Desculpa, não entendi!')
        elif error == '2':
            dispatcher.utter_message('Ainda não entendi!')

        return []

class ActionAskOpenBug(Action):
    def name(self) -> Text:
        return "action_ask_open_bug"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        log(tracker.latest_message)
        error = tracker.get_slot('erro_fluxo_try')
        channel = tracker.get_latest_input_channel()
        open_bug = tracker.get_slot('open_bug')
        test_run = tracker.get_slot('test_run')
        test_mass = tracker.get_slot('test_mass')
        test_cycle = tracker.get_slot('cycle')
        channel = tracker.get_latest_input_channel()
        if test_run == True:
            dispatcher.utter_message('Ops! Parece que você está executando o teste em sistema diferente! 🤔')
            dispatcher.utter_message('Confere se a massa ou o ambiente de testes estão corretos')
            if channel == 'socketio':
                dispatcher.utter_message(text='**Recomendo que você tente executar seu teste novamente e volte mais tarde!**')
                dispatcher.utter_message('Caso tenha certeza de que sua execução de testes está correta, podemos continuar')
                dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"title": "Sim", "payload": "Sim"}, {"title": "Não", "payload": "Sim"}])
            elif channel == 'cmdline':
                dispatcher.utter_message(text='Recomendo que você tente executar seu teste novamente e volte mais tarde!')
                dispatcher.utter_message('Caso tenha certeza de que sua execução de testes está correta, podemos continuar')
                dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"title": "Sim", "payload": "Sim"}, {"title": "Não", "payload": "Sim"}]) 
            else:
                dispatcher.utter_message(json_message={'text': '<b>Recomendo que você tente executar seu teste novamente e volte mais tarde!</b>', 'parse_mode': 'HTML'})
                dispatcher.utter_message(json_message={'text': 'Caso tenha certeza de que sua execução de testes está correta, podemos continuar'})
                if channel == 'botframework':
                    dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito??', buttons=[{"type": "postBack", "title": "Sim", "payload": "Sim"}, {"type": "postBack", "title": "Não", "payload": "Não"}])
                else:
                    dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"type": "postBack", "title": "Sim", "payload": "Sim"}, {"type": "postBack", "title": "Não", "payload": "Não"}])
            
        if test_cycle == True:
            dispatcher.utter_message('Ops!  Parece que não foi informado o Target Cycle e por isso não é possível identificar a esteira do teste! 🤔')
            dispatcher.utter_message('Confere se a massa ou o ambiente de testes estão corretos')
            if channel == 'socketio':
                dispatcher.utter_message(text='**Recomendo que você tente executar seu teste novamente e volte mais tarde!**')
                dispatcher.utter_message('Caso tenha certeza de que sua execução de testes está correta, podemos continuar')
                dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"type": "postBack", "title": "Sim", "payload": "Sim"}, {"type": "postBack", "title": "Não", "payload": "Não"}])
            elif channel == 'cmdline':
                dispatcher.utter_message(text='Recomendo que você tente executar seu teste novamente e volte mais tarde!')
                dispatcher.utter_message('Caso tenha certeza de que sua execução de testes está correta, podemos continuar')
                dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"type": "postBack", "title": "Sim", "payload": "Sim"}, {"type": "postBack", "title": "Não", "payload": "Não"}])
            else:
                dispatcher.utter_message(json_message={'text': '<b>Recomendo que você tente executar seu teste novamente e volte mais tarde!</b>', 'parse_mode': 'HTML'})
                dispatcher.utter_message(json_message={'text': 'Caso tenha certeza de que sua execução de testes está correta, podemos continuar'})
                if channel == 'botframework':
                    dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"type": "postBack", "title": "Sim", "payload": "Sim"}, {"type": "postBack", "title": "Não", "payload": "Não"}])
                else:
                    dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"type": "postBack", "title": "Sim", "payload": "Sim"}, {"type": "postBack", "title": "Não", "payload": "Não"}])
            
        elif test_mass == True:
            if channel == 'socketio':
                dispatcher.utter_message(text='**Recomendo que você tente executar seu teste novamente com outra massa e volte mais tarde!**')
                dispatcher.utter_message('Caso tenha certeza de que sua massa de testes está correta, podemos continuar')
                dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"title": "Sim", "payload": "Sim"}, {"title": "Não", "payload": "Não"}])
            elif channel == 'cmdline':
                dispatcher.utter_message(text='Recomendo que você tente executar seu teste novamente com outra massa e volte mais tarde!')
                dispatcher.utter_message('Caso tenha certeza de que sua massa de testes está correta, podemos continuar')
                dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"title": "Sim", "payload": "Sim"}, {"title": "Não", "payload": "Não"}])    
            else:
                dispatcher.utter_message(json_message={'text': '<b>Recomendo que você tente executar seu teste novamente com outra massa e volte mais tarde!</b>', 'parse_mode': 'HTML'})
                dispatcher.utter_message(json_message={'text': 'Caso tenha certeza de que sua massa de testes está correta, podemos continuar'})
                if channel == 'botframework':
                    dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"type": "postBack", "title": "Sim", "payload": "Sim"}, {"type": "postBack", "title": "Não", "payload": "Não"}])
                else:
                    dispatcher.utter_message(text='Você tem certeza que deseja continuar com a abertura do defeito?', buttons=[{"type": "postBack", "title": "Sim", "payload": "Sim"}, {"type": "postBack", "title": "Não", "payload": "Não"}])

        return []