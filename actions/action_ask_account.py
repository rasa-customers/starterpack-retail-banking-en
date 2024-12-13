from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionAskAccount(Action):
    def name(self) -> Text:
        return "action_ask_account"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")

        db = Database()
        query = """
            SELECT a.user_id, a.number, a.type
            FROM accounts a
            JOIN users u ON a.user_id = u.id
            WHERE u.name = ?
        """
        results = db.run_query(query, (username,), one_record=False)

        buttons = [
            {
                "content_type": "text",
                "title": f"{account[1]} ({account[2].title()})",
                "payload": str(account[1]),
            }
            for account in results
        ]
        message = "Which account would you like the balance for?"
        dispatcher.utter_message(text=message, buttons=buttons)

        selected_account = tracker.get_slot("account")

        return [SlotSet("account", selected_account)]
