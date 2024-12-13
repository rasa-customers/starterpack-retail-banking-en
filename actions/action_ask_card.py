from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionAskCard(Action):
    def name(self) -> Text:
        return "action_ask_card"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")

        db = Database()
        query = """
            SELECT c.user_id, c.number, c.type
            FROM cards c
            JOIN users u ON c.user_id = u.id
            WHERE u.name = ?
        """
        results = db.run_query(query, (username,), one_record=False)

        buttons = [
            {
                "content_type": "text",
                "title": f"{i + 1}: x{account[1][-4:]} ({account[2].title()})",
                "payload": f"/SetSlots(card_selection={str(account[1])})",
            }
            for i, account in enumerate(results)
        ]
        message = "Select the card you require assistance with:"
        dispatcher.utter_message(text=message, buttons=buttons)

        return []
