from .__init__ import *


# ============================================================================
# ActionForceReset - action responsável por reiniciar a conversa com o usuario
# ============================================================================
class ActionForceReset(Action):

    def name(self) -> Text:
        return "action_force_reset"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        log(tracker.latest_message)
        return [AllSlotsReset()]