from .__init__ import *


# ==================================================================================
# Actions check_slots_form_n1 - Verifica se deve ou não seguir a abertura do defeito
# ==================================================================================
class ActionCheckSlotsFormN1(Action):
    def name(self) -> Text:
        return 'action_check_slots_form_n1'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        log(tracker.latest_message)
        open_bug = tracker.get_slot('open_bug')
    
        # abre o chamado
        if open_bug is True:
            dispatcher.utter_message('Está tudo certo! 😁 Podemos seguir com a abertura do chamado')
            return [SlotSet('test_mass', False), SlotSet('test_run', False), SlotSet('erro_fluxo_try', '0'), SlotSet('open_bug', open_bug)]
        # finaliza a conversa
        elif open_bug is False:
            return [SlotSet('test_mass', False), SlotSet('test_run', False), SlotSet('erro_fluxo_try', '0'), SlotSet('open_bug', open_bug)]