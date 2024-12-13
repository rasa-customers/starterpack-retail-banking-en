from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa_sdk.executor import CollectingDispatcher

from actions.database import Database


class ActionUpdateCardStatus(Action):
    def name(self) -> str:
        return "action_update_card_status"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[str, Any]
    ) -> List[Dict[Text, Any]]:
        username = tracker.get_slot("username")
        card_number = tracker.get_slot("card_number")
        new_status = "inactive"

        db = Database()
        update_query = """
            UPDATE cards
            SET status = ?
            WHERE number = ? AND user_id = (
                SELECT id FROM users WHERE name = ?
            )
        """
        db.cursor.execute(update_query, (new_status, card_number, username))
        db.connection.commit()

        return [SlotSet("card_status", new_status)]
