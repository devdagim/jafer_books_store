from aiogram.fsm.storage.base import BaseStorage, StorageKey
from aiogram.fsm.state import State
from telegram_bot.helpers.db import DB
from typing import Any, Dict


class AioMysqlStorage(BaseStorage):
    """
    Mysql based storage for Finite State Machine.

    Intended to replace MemoryStorage for simple cases where you want to keep
    states between bot restarts.
    """

    def __init__(self):
        """
        Initialize the MysqlStorage class.
        """
        self._init_db()

    def _init_db(self):
        """
        Initialize the MySQL database by creating the required tables if they
        don't exist.
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS aiogram_fsm_data (
                user_id BIGINT NOT NULL,
                chat_id BIGINT NOT NULL,
                data_key TEXT NOT NULL,
                data_Value TEXT NOT NULL,
                UNIQUE KEY unique_chat_id (chat_id)
            );
            CREATE TABLE IF NOT EXISTS aiogram_fsm_state (
                user_id BIGINT NOT NULL,
                chat_id BIGINT NOT NULL,
                state TEXT NOT NULL,
                UNIQUE KEY unique_chat_id (chat_id)
            );
        """
        )
        conn.close()

    def _get_connection(self):
        """
        Get the database connection.

        If the connection is not already established, it will connect to the
        database.
        """

        if DB.is_connected():
            return DB
        else:
            DB.connect()
            return DB

    async def set_state(
        self, key: StorageKey, state: str | State | None = None
    ) -> None:
        """
        Set the state for a specific key in the storage.

        Args:
            key: The storage key.
            state: The state to be set.

        Returns:
            None
        """
        conn = self._get_connection()
        cursor = conn.cursor()

        state_value = None

        if state is not None:
            if isinstance(state, str):
                state_value = state
            elif isinstance(state, State):
                # Extract the state name from the State object
                state_value = state.state

            cursor.execute(
                "INSERT INTO aiogram_fsm_state (user_id, chat_id, state) \
                VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE state = \
                VALUES(state)",
                (key.user_id, key.chat_id, state_value),
            )
        else:
            cursor.execute(
                "DELETE FROM aiogram_fsm_state WHERE user_id=%s AND chat_id=%s",
                (key.user_id, key.chat_id),
            )
        conn.commit()

    async def get_state(self, key: StorageKey) -> str | None:
        """
        Get the state associated with a specific key from the storage.

        Args:
            key: The storage key.

        Returns:
            The state associated with the key, or None if not found.
        """

        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT state FROM aiogram_fsm_state WHERE user_id=%s AND chat_id=%s",
            (key.user_id, key.chat_id),
        )
        result = cursor.fetchone()

        return result["state"] if result else None

    async def set_data(self, key: StorageKey, data: Dict[str, Any]) -> None:
        """
        Set data for a specific key in the storage.

        Args:
            key: The storage key.
            data: The data to be set.

        Returns:
            None
        """

        conn = self._get_connection()
        cursor = conn.cursor()
        if data:
            for data_key, data_value in data.items():
                cursor.execute(
                    "INSERT INTO aiogram_fsm_data (user_id, chat_id, \
                    data_key, data_value) VALUES (%s, %s, %s, %s) ON \
                    DUPLICATE KEY UPDATE data_value = VALUES(data_value)",
                    (key.user_id, key.chat_id, data_key, data_value),
                )
        else:
            cursor.execute(
                "DELETE FROM aiogram_fsm_data WHERE user_id=%s AND chat_id=%s",
                (key.user_id, key.chat_id),
            )
        conn.commit()

    async def get_data(self, key: StorageKey) -> Dict[str, Any]:
        """
        Get the data associated with a specific key from the storage.

        Args:
            key: The storage key.

        Returns:
            The data associated with the key as a dictionary.
        """

        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(
            "SELECT data_key, data_value FROM aiogram_fsm_data WHERE \
            user_id=%s AND chat_id=%s",
            (key.user_id, key.chat_id),
        )
        results = cursor.fetchall()

        if results:
            # {'data_key': 'book_code', 'data_value': 'jb_1592'}
            # into {'book_code':"jb_1592"}
            data = {}
            for result in results:
                data_key = result["data_key"]
                data_value = result["data_value"]

                data[data_key] = data_value

            return data
        else:
            return {}

    async def update_data(
        self, key: StorageKey, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update the data associated with a specific key in the storage.

        Args:
            key: The storage key.
            data: The updated data.

        Returns:
            The updated data associated with the key as a dictionary.
        """

        conn = self._get_connection()
        cursor = conn.cursor()
        for data_key, data_value in data.items():
            cursor.execute(
                "UPDATE aiogram_fsm_data data_key=%s,data_value=%s WHERE \
                user_id=%s AND chat_id=%s",
                (data_key, data_value, key.user_id, key.chat_id),
            )
        conn.commit()

        return self.get_data(key=key)

    async def close(self) -> None:
        """
        Close the database connection.
        """

        self._get_connection().close()
