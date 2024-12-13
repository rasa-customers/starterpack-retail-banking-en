from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionCheckBalance(Action):
    def name(self) -> Text:
        return "action_check_balance"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")
        account_number = tracker.get_slot("account")

        db = Database()

        user_query = "SELECT id FROM users WHERE name = ?"
        user_result = db.run_query(user_query, (username,), one_record=True)
        user_id = user_result[0]

        check_balance_query = (
            "SELECT balance FROM accounts WHERE user_id = ? AND number = ?"
        )
        balance_result = db.run_query(
            check_balance_query, (user_id, account_number), one_record=True
        )

        current_balance = float(balance_result[0])

        message = f"The balance is: ${current_balance}"
        return dispatcher.utter_message(text=message)
