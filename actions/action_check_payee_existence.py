from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionCheckPayeeExistence(Action):
    def name(self) -> Text:
        return "action_check_payee_existence"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")
        payee_name = tracker.get_slot("payee_name")

        db = Database()
        user_query = "SELECT id FROM users WHERE name = ?"
        user_result = db.run_query(user_query, (username,), one_record=True)
        user_id = user_result[0]

        check_payee_query = "SELECT id FROM payees WHERE user_id = ? AND name = ?"
        payee_result = db.run_query(
            check_payee_query, (user_id, payee_name), one_record=True
        )

        if payee_result:
            return [SlotSet("payee_exists", True)]

        dispatcher.utter_message(
            f"{payee_name} is not an authorised payee. Let's add them!"
        )
        return [SlotSet("payee_exists", False)]
