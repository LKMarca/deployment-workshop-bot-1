from .__init__ import *


# =============================================================
# action_system - action responsável resetar os slots definidos
# =============================================================
class action_system(Action):
    def name(self) -> Text:
        return 'action_system'

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Reseta os SLOTS especificos!!!!
        log(tracker.latest_message)
        user_alm_qc = tracker.get_slot('user_alm_qc')
        count_finish = tracker.get_slot("count_finish")
        senderid = tracker.get_slot('senderid')
        all_ct = tracker.get_slot('all_ct')
        ct = None
        erro = '0'
        data = tracker.get_slot('user_data')

        return [AllSlotsReset(), SlotSet('senderid', senderid), SlotSet('ct', ct), SlotSet('all_ct', all_ct), SlotSet('erro_fluxo_try', erro), SlotSet('error_collect', erro), SlotSet('user_data', data), SlotSet('count_finish', count_finish), SlotSet('user_alm_qc', user_alm_qc)]

        # , ReminderScheduled(intent_name="greet_intent", trigger_date_time=datetime.now() + timedelta(seconds=1), kill_on_user_message=False)