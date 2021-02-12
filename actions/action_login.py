from .__init__ import *
from .utils import check_login, get_all_ct, get_ect


# =====================================
# ValidationLoginForm - forms de login
# =====================================
class ValidationLoginForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_login_form"

    def validate_user_alm_qc(self, slot_value: Any, dispatcher: CollectingDispatcher, tracker: Tracker, domain: DomainDict) -> Dict[Text, Any]:
        log(tracker.latest_message)
        # user_alm_qc = slot_value.lower()
        user_alm_qc = str(filter_entities(tracker.latest_message, 'login_entity', 'value'))
        # sender_id = tracker.get_slot("senderid")
        # user_alm_qc = tracker.get_slot("user_alm_qc")
        erro_fluxo_try = tracker.get_slot("erro_fluxo_try")
        if check_login(user_alm_qc.lower()) == 'Approved':
            salutation = choice(['Ótimo', 'Perfeito', 'Certo', 'Ok'])
            dispatcher.utter_message(f'{salutation}! 😄 Já consegui identificar o seu usuário!')
            user_data = get_ect(user_alm_qc)
            all_ct = get_all_ct(user_alm_qc)
            return {"user_alm_qc": user_alm_qc, "erro_fluxo_try": "0", "user_data": user_data, 'all_ct': all_ct, "senderid": tracker.sender_id}
        else:
            if erro_fluxo_try == "0":
                erro_fluxo_try = "1"
                return {"erro_fluxo_try": erro_fluxo_try, "user_alm_qc": None}
            elif erro_fluxo_try == "1":
                erro_fluxo_try = "2"
                return {"erro_fluxo_try": erro_fluxo_try, "user_alm_qc": None}
            elif erro_fluxo_try == "2":
                erro_fluxo_try = "3"
                return {"erro_fluxo_try": erro_fluxo_try, "user_alm_qc": None}
            else:
                erro_fluxo_try = "0"
                return {"erro_fluxo_try": erro_fluxo_try, "user_alm_qc": None}


# ===================================================================================
# ActionUserAlmQC - action de pergunta o usuario do cliente e preenche o slot ou não
# ===================================================================================
class ActionUserAlmQC(Action):
    def name(self) -> Text:
        return "action_ask_user_alm_qc"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        log(tracker.latest_message)
        erro_fluxo_try = tracker.get_slot("erro_fluxo_try")
        channel = tracker.get_latest_input_channel()
        last_event = tracker.get_last_event_for('user', skip=0)
        last_intent = last_event['parse_data']['intent']['name'] if last_event else None
        response = tracker.latest_message['intent']['name']
        if erro_fluxo_try == "0" and response != 'help_intent':
            if last_intent == "greet_intent" or last_intent == "start" or last_intent == "help_intent" or last_intent == "reset_intent":
                if channel == 'socketio':
                    dispatcher.utter_message(text='Primeiro, me **informe o seu usuário do ALM QC** para continuarmos')
                elif channel == 'cmdliactivate rasane':
                    dispatcher.utter_message(text='Primeiro, me informe o seu usuário do ALM QC para continuarmos')
                else:
                    dispatcher.utter_message(json_message={'text': 'Primeiro, me <b>informe o seu usuário do ALM QC</b> para continuarmos', 'parse_mode': 'HTML'})
            else:
                if channel == 'socketio':
                    dispatcher.utter_message(text='Caso queira abrir um novo defeito, é so me **informar o seu usuário** do ALM QC 😀')
                elif channel == 'cmdline':
                    dispatcher.utter_message(text='Caso queira abrir um novo defeito, é so me informar o seu usuário do ALM QC 😀')
                else:
                    dispatcher.utter_message(json_message={'text': 'Caso queira abrir um novo defeito, é so me <b>informar o seu usuário</b> do ALM QC 😀', 'parse_mode': 'HTML'})
        # fallback
        else:
            if channel == 'socketio':
                text = choice(['Ops! Não consegui identificar o usuário! 🤔 Tente me informar novamente, por favor!', 'Poxa! Não encontrei o seu usuário! 🤔 Tente me informar novamente, por favor!', 'Desculpe, mas não consegui validar o seu usuário! 🤔 Tente me informar novamente, por favor!'])
            elif channel == 'telegram':
                text = choice(['Ops! Não consegui identificar o usuário! 🤔\nTente me informar novamente, por favor!', 'Poxa! Não encontrei o seu usuário! 🤔\nTente me informar novamente, por favor!', 'Desculpe, mas não consegui validar o seu usuário! 🤔\nTente me informar novamente, por favor!'])
            else:
                text = choice(['Ops! Não consegui identificar o usuário! 🤔<br>Tente me informar novamente, por favor!', 'Poxa! Não encontrei o seu usuário! 🤔<br>Tente me informar novamente, por favor!', 'Desculpe, mas não consegui validar o seu usuário! 🤔<br>Tente me informar novamente, por favor!'])

            if erro_fluxo_try == "1":
                if channel == 'socketio':
                    dispatcher.utter_message(text=text)
                elif channel == 'telegram':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
                else:
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})

            elif erro_fluxo_try == "2":
                if channel == 'socketio':
                    dispatcher.utter_message(text=text)
                elif channel == 'telegram':
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
                else:
                    dispatcher.utter_message(json_message={'text': text, 'parse_mode': 'HTML'})
            else:
                if channel == 'socketio':
                    dispatcher.utter_message(text='Hmm... Realmente não pude identificar o seu usuário! ☹️ Infelizmente não vou conseguir te ajudar a registrar o defeito! Nesse caso, você pode abrir o ALM QC e registrá-lo por lá! 😉')
                elif channel == 'telegram':
                    dispatcher.utter_message(json_message={'text': 'Hmm... Realmente não pude identificar o seu usuário! ☹️\nInfelizmente não vou conseguir te ajudar a registrar o defeito!\nNesse caso, você pode abrir o ALM QC e registrá-lo por lá! 😉', 'parse_mode': 'HTML'})
                else:
                    dispatcher.utter_message(json_message={'text': 'Hmm... Realmente não pude identificar o seu usuário! ☹️<br>Infelizmente não vou conseguir te ajudar a registrar o defeito!<br>Nesse caso, você pode abrir o ALM QC e registrá-lo por lá! 😉', 'parse_mode': 'HTML'})
                return[SlotSet("user_alm_qc", None), SlotSet("erro_fluxo_try", "0"), FollowupAction('action_goodbye')]
        return []


# ===========================================================================================
# ActionCheckLogin - action responsavel por verificar se o usuario ja está logado no sistema
# ===========================================================================================
class ActionCheckLogin(Action):
    def name(self) -> Text:
        return "action_check_login"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        log(tracker.latest_message)
        user_alm_qc = tracker.get_slot("user_alm_qc")
        # if user_alm_qc is not None:
        if user_alm_qc is not None:
            if user_alm_qc is not False:
                return [FollowupAction("collect_form")]
            else:
                return [FollowupAction("login_form")]
        else:
            return [FollowupAction("login_form")]