import re
import base64

# aiogram
from aiogram.filters import Filter
from aiogram.types import Message
from aiogram.utils.deep_linking import decode_payload


# example
# BotDeepLink("id={int}&name={str}"):
class BotDeepLink(Filter):
    """
    A filter for matching messages with a specific deep link pattern.

    Attributes:
        deep_link_pattern (str): The deep link pattern to match against.

    """

    def __init__(self, deep_link_pattern: str):
        """
        Initializes the BotDeepLink filter with the specified deep link pattern.

        Args:
            deep_link_pattern (str): The deep link pattern to match against.
            e.g:-'param1&param2={value_type->str/int}'

        """

        self.deep_link_pattern = deep_link_pattern

    async def __call__(self, message: Message) -> bool:
        """
        Checks if the message matches the defined deep link pattern.

        Args:
            message (Message): The incoming message to check.

        Returns:
            bool: True if the message matches the deep link pattern, False otherwise.

        """

        incoming_deep_link = self._get_deep_link(message.text)

        if incoming_deep_link:
            deep_link_pattern = self.deep_link_pattern

            regex_pattern = deep_link_pattern.replace("{str}", r"\b\w+\b")\
                            .replace("{int}", r"\b\d+\b")
            
            is_matched = re.match(regex_pattern, incoming_deep_link)
            

            if is_matched:
                return True
            else:
                return False

    def _get_deep_link(self, incoming_message_text):
        """
        Extracts the deep link from the message.

        Args:
            incoming_message_text (str): The incoming message text.

        Returns:
            str: The extracted deep link.

        """

        deep_link_match = re.match(r"^\/start\s\w+$", incoming_message_text)

        if deep_link_match:
            deep_link = deep_link_match.group(0)
            deep_link =  decode_payload(deep_link.split()[-1])
        else:
            deep_link = None

        return deep_link
