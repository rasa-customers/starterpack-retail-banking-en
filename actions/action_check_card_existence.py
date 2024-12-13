from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionCheckCardExistence(Action):
    def name(self) -> str:
        return "action_check_card_existence"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")
        card_number = tracker.get_slot("card_number")

        # TODO: Maybe these should be buttons?
        db = Database()
        query = """
            SELECT c.number
            FROM cards c
            JOIN users u ON c.user_id = u.id
            WHERE u.name = ?
        """
        card_numbers = db.run_query(query, (username,), one_record=False)
        card_numbers = [row[0] for row in card_numbers]

        if card_number in card_numbers:
            return [SlotSet("card_found", True)]
        else:
            return [SlotSet("card_found", False)]
