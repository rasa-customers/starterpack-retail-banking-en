from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionAddPayee(Action):
    def name(self) -> Text:
        return "action_add_payee"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")
        payee_name = tracker.get_slot("payee_name")
        account_number = tracker.get_slot("account_number")
        sort_code = tracker.get_slot("sort_code")
        payee_type = tracker.get_slot("payee_type")
        reference = tracker.get_slot("reference")

        db = Database()
        user_query = "SELECT id FROM users WHERE name = ?"
        user_result = db.run_query(user_query, (username,), one_record=True)
        user_id = user_result[0]

        insert_query = """
        INSERT INTO payees (user_id, name, sort_code, account_number, type, reference)
        VALUES (?, ?, ?, ?, ?, ?)
        """
        db.run_query(
            insert_query,
            (
                user_id,
                payee_name,
                sort_code,
                account_number,
                payee_type,
                reference,
            ),
            one_record=False,
        )
        db.connection.commit()
        return [SlotSet("payee_added", True)]
