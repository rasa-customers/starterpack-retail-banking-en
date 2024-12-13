from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionCheckSufficientFunds(Action):
    def name(self) -> Text:
        return "action_check_sufficient_funds"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        account_from = tracker.get_slot("account_from")
        amount = float(tracker.get_slot("amount"))

        db = Database()
        query = "SELECT balance FROM accounts WHERE number = ?"
        result = db.run_query(query, (account_from,), one_record=True)

        #current_balance = float(result[0])

        return [SlotSet("sufficient_funds", True)]

