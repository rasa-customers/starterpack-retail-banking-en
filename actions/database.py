import json
import logging
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union


class Database:
    table_definitions = {
        "users": {
            "create_statement": """
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    address TEXT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    segment TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """,
            "insert_statement": "INSERT INTO users (name, email, phone, address, username, password, segment) VALUES (?, ?, ?, ?, ?, ?, ?)",
        },
        "accounts": {
            "create_statement": """
                CREATE TABLE IF NOT EXISTS accounts (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    balance REAL,
                    type TEXT,
                    number TEXT,
                    sort_code TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """,
            "insert_statement": "INSERT INTO accounts (user_id, balance, type, number, sort_code) VALUES (?, ?, ?, ?, ?)",
        },
        "transactions": {
            "create_statement": """
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY,
                    account_id INTEGER,
                    amount REAL,
                    datetime DATETIME,
                    description TEXT,
                    payment_method TEXT,
                    payee TEXT,
                    FOREIGN KEY(account_id) REFERENCES accounts(id)
                )
            """,
            "insert_statement": """
                INSERT INTO transactions (account_id, amount, datetime, description, payment_method, payee)
                VALUES (
                    ?,
                    ?,
                    datetime('now', '-' || (ABS(random()) % 90) || ' days',
                                    '-' || (ABS(random()) % 24) || ' hours',
                                    '-' || (ABS(random()) % 60) || ' minutes',
                                    '-' || (ABS(random()) % 60) || ' seconds'),
                    ?,
                    ?,
                    ?
                )
            """,
        },
        "payees": {
            "create_statement": """
                CREATE TABLE IF NOT EXISTS payees (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    name TEXT,
                    sort_code TEXT,
                    account_number TEXT,
                    type TEXT,
                    reference TEXT,
                    added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id)
                )
            """,
            "insert_statement": "INSERT INTO payees (user_id, name, sort_code, account_number, type, reference) VALUES (?, ?, ?, ?, ?, ?)",
        },
        "cards": {
            "create_statement": """
                CREATE TABLE IF NOT EXISTS cards (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    account_id INTEGER,
                    number TEXT UNIQUE,
                    type TEXT,
                    status TEXT,
                    issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(id),
                    FOREIGN KEY(account_id) REFERENCES accounts(id)
                )
            """,
            "insert_statement": "INSERT INTO cards (user_id, account_id, number, type, status) VALUES (?, ?, ?, ?, ?)",
        },
        "branches": {
            "create_statement": """
                CREATE TABLE IF NOT EXISTS branches (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    address TEXT NOT NULL,
                    distance_km REAL
                )
            """,
            "insert_statement": "INSERT INTO branches (name, address, distance_km) VALUES (?, ?, ?)",
        },
        "advisors": {
            "create_statement": """
                CREATE TABLE IF NOT EXISTS advisors (
                    id INTEGER PRIMARY KEY,
                    branch_id INTEGER,
                    name TEXT,
                    email TEXT,
                    phone TEXT,
                    position TEXT,
                    FOREIGN KEY(branch_id) REFERENCES branches(id)
                )
            """,
            "insert_statement": "INSERT INTO advisors (branch_id, name, email, phone, position) VALUES (?, ?, ?, ?, ?)",
        },
        "appointments": {
            "create_statement": """
                CREATE TABLE IF NOT EXISTS appointments (
                    id INTEGER PRIMARY KEY,
                    advisor_id INTEGER,
                    date DATE,
                    start_time TIME,
                    end_time TIME,
                    status TEXT,
                    FOREIGN KEY(advisor_id) REFERENCES advisors(id)
                )
            """,
            "insert_statement": "INSERT INTO appointments (advisor_id, date, start_time, end_time, status) VALUES (?, ?, ?, ?, ?)",
        },
    }

    def __init__(self, database_path: Optional[Path] = None) -> None:
        """Initialise the database, creating or loading the schema and data as necessary."""
        self.project_root_path = Path(__file__).resolve().parent.parent
        self.database_path = (
            database_path or self.project_root_path / "data" / "banking.db"
        )
        self.source_data_path = self.project_root_path / "data" / "source"

        self.logger = self.setup_logger()

        try:
            if self.database_path.exists():
                self.logger.info(f"Loading existing database '{self.database_path}'")
                self.connection = sqlite3.connect(str(self.database_path))
            else:
                self.logger.info(f"Creating new in-memory database")
                self.connection = sqlite3.connect(":memory:")
                self.create_schema()
                self.load_data()
                self.save_to_disk()

            self.cursor = self.connection.cursor()

        except sqlite3.Error as e:
            self.logger.error(f"Error initialising database: {e}")
            raise

    def setup_logger(self) -> logging.Logger:
        """Set up logging configuration."""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s %(levelname)8s %(name)s  - %(message)s"
        )

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        return logger

    def create_schema(self) -> None:
        """Create the database schema."""
        try:
            for table, definition in self.table_definitions.items():
                self.logger.debug(f"Creating table '{table}'")
                self.connection.execute(definition["create_statement"])

            self.connection.commit()
            self.logger.info("Database schema created")
        except sqlite3.Error as e:
            self.logger.error(f"Error creating schema: {e}")
            raise

    def load_data(self) -> None:
        """Load data from JSON files into the database."""
        for source_file in self.source_data_path.glob("*.json"):
            with open(source_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                table_name = source_file.stem.lower()
                self.logger.info(
                    f"Attempting to load data for table '{table_name}' from {source_file}"
                )
                if table_name in self.table_definitions:
                    self.insert_data(table_name, data)
                else:
                    self.logger.warning(f"Skipping unknown table '{table_name}'")

    def insert_data(self, table_name: str, data: List[Dict[str, Any]]) -> None:
        """Insert data into the specified table."""
        if table_name not in self.table_definitions:
            self.logger.error(f"Unknown table: {table_name}")
            raise ValueError(f"Unknown table: {table_name}")

        insert_statement = self.table_definitions[table_name]["insert_statement"]
        try:
            for row in data:
                self.connection.execute(insert_statement, tuple(row.values()))

            self.connection.commit()
            self.logger.info(f"Inserted {len(data)} records into table '{table_name}'")
        except sqlite3.Error as e:
            self.logger.error(f"Error inserting data into table '{table_name}': {e}")
            raise

    def save_to_disk(self) -> None:
        """Save the in-memory database to disk."""
        try:
            with sqlite3.connect(str(self.database_path)) as backup_db:
                self.connection.backup(backup_db)
            self.logger.info(f"Database saved to {self.database_path}")
        except sqlite3.Error as e:
            self.logger.error(f"Error saving database to disk: {e}")
            raise

    def run_query(
        self, query: str, parameters: Tuple = (), one_record: bool = True
    ) -> Union[Tuple, List[Tuple]]:
        """Run a query with the given parameters and return the result."""
        try:
            self.cursor.execute(query, parameters)

            if one_record:
                return self.cursor.fetchone()
            else:
                return self.cursor.fetchall()
        except sqlite3.Error as e:
            self.logger.error(f"Error running query: {e}")
            raise

    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context related to this object."""
        self.connection.close()
        self.logger.info("Database connection closed")
