from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionAskAccountFrom(Action):
    def name(self) -> Text:
        return "action_ask_account_from"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")

        db = Database()
        query = """
            SELECT a.id, a.type, a.balance, a.number
            FROM accounts a
            JOIN users u ON a.user_id = u.id
            LEFT JOIN cards c ON a.id = c.account_id AND c.type = 'debit'
            WHERE u.name = ?
        """
        results = db.run_query(query, (username,), one_record=False)

        buttons = [
            {
                "content_type": "text",
                "title": f"{account[1].title()} (Balance: ${account[2]:.2f})",
                "payload": str(account[3]),
            }
            for account in results
        ]
        message = "Which account would you like to transfer money from?"
        dispatcher.utter_message(text=message, buttons=buttons)

        return []
