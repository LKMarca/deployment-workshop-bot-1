from .__init__ import *


# ==========================================================
# Actions CheckN1 - Verifica se algo deu errado no checklist
# ==========================================================
class ActionCheckN1(Action):
    # Nome de actions para o rasa
    def name(self) -> Text:
        return "action_check_n1"

    # Verifica se algo deu errado no checklist
    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        log(tracker.latest_message)

        # fiz isso de forma aleatoria para testes
        data = tracker.get_slot('user_data')
        just_cycle = data['target-cycle']
        just_ct_name = data['test-case']
        all_sites = get_sites()
        all_sites = all_sites[0]['prodlike']
        internet = True
        cycle = False
        site = True
        call_checklist = False
        if just_cycle is None:
            # just_cycle[id-1][0] = {'value': '1007', 'ReferenceValue': 'COT - Esteira 1'}
            cycle = True
            call_checklist = True
        if just_cycle is not None:
            for site in all_sites:
                if site['Name'].lower() in just_ct_name.lower():
                    site = None
                    call_checklist = True
                    break
            if site is not None:
                dispatcher.utter_message('Não consegui detectar o sistema que está sendo executado')
        if 'venda triple' in str(just_ct_name.lower()):
            internet = None
            call_checklist = True

        return [SlotSet('internet', internet), SlotSet('cycle', cycle), SlotSet('site', site), SlotSet('call_form_checklist_n1', call_checklist)]