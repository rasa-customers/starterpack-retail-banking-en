from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionListPayees(Action):
    def name(self) -> Text:
        return "action_list_payees"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")

        db = Database()
        query = """
        SELECT p.id, p.name, p.account_number
        FROM payees p
        JOIN users u ON p.user_id = u.id
        WHERE u.name = ?
        """
        results = db.run_query(query, (username,), one_record=False)

        payee_names = [payee[1] for payee in results]
        if len(payee_names) > 1:
            payees_list = ", ".join(payee_names[:-1]) + " and " + payee_names[-1]
        else:
            payees_list = payee_names[0] if payee_names else ""

        message = f"You are authorised to transfer money to: {payees_list}"
        dispatcher.utter_message(text=message)

        return []
