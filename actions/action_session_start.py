import random
from datetime import datetime
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.events import ActionExecuted, SessionStarted, SlotSet

from actions.database import Database


class ActionSessionStart(Action):
    def name(self) -> Text:
        return "action_session_start"

    def set_current_date(self) -> List[Dict[Text, Any]]:
        current_date = datetime.now().strftime("%d/%m/%Y")
        return [SlotSet("current_date", current_date)]

    def set_user_profile(self, username: str) -> List[Dict[Text, Any]]:
        db = Database()
        query = """
            SELECT name, segment, email, address
            FROM users
            WHERE name = ?
        """
        result = db.run_query(query, (username,), one_record=True)

        if result:
            username, segment, email, address = result
            return [
                SlotSet("username", username),
                SlotSet("segment", segment),
                SlotSet("email_address", email),
                SlotSet("physical_address", address),
            ]
        else:
            return []

    def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        current_date_events = self.set_current_date()
        username = random.choice(["John Smith", "Mary Brown", "Dan Young"])

        user_profile_events = self.set_user_profile(username)

        events = (
            current_date_events
            + user_profile_events
            + [
                ActionExecuted("action_listen"),
            ]
        )

        return events
