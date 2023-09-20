import re
# aiogram
from aiogram import BaseMiddleware,exceptions
from aiogram.types import Message,InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.deep_linking import decode_payload
from aiogram.enums import ChatMemberStatus
# project
from telegram_bot.bot_instance import Bot
from telegram_bot.helpers.config import CONFIG
from telegram_bot.template.messages import WELCOME_MESSAGE_FOR_NOT_MEMBER,\
    BE_MEMBER_MESSAGE


# example
# ChannelJoinedMiddleware(['command::start','state::state_name',
# 'deep_link::order_now_btn&book_code={str}'])

class ChannelJoinedMiddleware(BaseMiddleware):
    """
    Middleware for checking if a user is a member of a specific channel before allowing access to protected routes.

    Args:
        middleware_protected_routes (list): List of protected routes or states that require membership.

    Attributes:
        protected_routes (list): List of protected routes or states that require membership.
        channel_username (str): Username of the channel to check membership against.

    """

    def __init__(self, middleware_protected_routes):
        self.protected_routes = middleware_protected_routes
        self.channel_username = CONFIG.get("telegram_api","CHANNEL_USERNAME")\
                            .strip('"')

    async def __call__(self, handler, event: Message, data):
            """
            Performs the middleware logic.

            Args:
                handler (function): Handler function for processing the event.
                event (Message): The incoming message event.
                data (dict): Additional data associated with the event.

            Returns:
                The result of the handler if the conditions are met, or an error message if the user is not a member.

            """

            bot = data.get("bot")
            chat_type = event.chat.type
            incoming_text = event.text
            user_id = event.from_user.id

            is_member = await self._is_member(user_id, bot)
            is_command_protected = self._is_command_protected(incoming_text)
            is_deep_link_protected = self._is_deep_link_protected(incoming_text)
            is_state_protected = await self._is_state_protected(data)
            
            is_protected_by_middleware = is_command_protected or \
                                        is_deep_link_protected or \
                                        is_state_protected
            

            if chat_type == "private":
                user_name = event.from_user.first_name

                if incoming_text == '/start' and not is_member:
                    error_text = WELCOME_MESSAGE_FOR_NOT_MEMBER.format(
                        user_name=user_name,
                        bot_name=(await Bot.me()).username
                    )
                    return await self._send_error_message(error_text, event)

                elif is_protected_by_middleware and not is_member:
                    error_text = BE_MEMBER_MESSAGE.format(
                        user_name=user_name
                    )
                    return await self._send_error_message(error_text, event)

                else:
                    return await handler(event, data)

            else:
                print(1,"-",event)
                return await handler(event, data)

    def _get_command(self, incoming_message_text):
        """
        Extracts the command from the message.

        Args:
            incoming_message_text(str): The incoming message.

        Returns:
            str: The extracted command.

        """

        command_match = re.match(r'^/(\w+)$', incoming_message_text)
        
        if command_match:
            command = command_match.group(1)
            command = command.lower()
            
        else:
            command = None
        
        return command
    
    def _get_deep_link(self, incoming_message_text):
        """
        Extracts the deep link from the message.

        Args:
            incoming_message_text: The incoming message text

        Returns:
            str: The extracted deep link.

        """

        deep_link_match = re.match(r"^\/start\s\w+$", incoming_message_text)

        if deep_link_match:
            deep_link = deep_link_match.group(0)
            deep_link = decode_payload(deep_link.split()[-1])
        else:
            deep_link = None

        return deep_link

    async def _join_channel_btn(self):
        """
        Generates an inline keyboard button to join the channel.

        Returns:
            InlineKeyboardMarkup: The inline keyboard markup with the join channel button.

        """

        channel_username = self.channel_username.replace("@","")

        join_channel_btn_builder = InlineKeyboardBuilder()
        join_channel_btn = InlineKeyboardButton(text="➡️ Join Channel",
                            url=f"https://t.me/{channel_username}")
        join_channel_btn_builder.add(join_channel_btn)

        return join_channel_btn_builder.as_markup()

    async def _send_error_message(self, error_text, message):
        """
        Sends an error message to the user.

        Args:
            error_text (str): The error message text.
            message (Message): The incoming message.

        Returns:
            Message: The sent error message.

        """

        join_channel_btn = await self._join_channel_btn()

        return await message.reply(text=error_text,reply_markup=join_channel_btn)

    async def _is_member(self, user_id, bot) -> bool:
        """
        Checks if the user is a member of the specified channel.

        Args:
            user_id (int): ID of the user.
            bot (Bot): The bot instance.

        Returns:
            bool: True if the user is a member, False otherwise.

        """

        channel_username = self.channel_username
        
        try:
            member_info = await bot.get_chat_member(chat_id=channel_username,
                            user_id=user_id)

            if member_info.status == ChatMemberStatus.LEFT:
                return False
            else:
                return True

        except exceptions.TelegramBadRequest as e:
            return False

    def _is_command_protected(self, incoming_message_text):
        """
        Checks if the incoming text contains a protected command.

        Args:
            text (str): The incoming text.

        Returns:
            bool: True if the text contains a protected command, False otherwise.

        """

        protected_routes = self.protected_routes
        incoming_command = self._get_command(incoming_message_text)

        # if not the incoming command is empty
        if incoming_command:
            for protected_route in protected_routes:
                if protected_route.startswith("command::"):
                    protected_command = protected_route.replace("command::","")
                    # if the incoming command is protected by middleware
                    if protected_command == incoming_command:
                        return True
        else:
            return False
        
    def _is_deep_link_protected(self, incoming_message_text):
        """
        Checks if the incoming text contains a protected deep link.

        Args:
            text (str): The incoming text.

        Returns:
            bool: True if the text contains a protected deep link, False otherwise.

        """

        protected_routes = self.protected_routes
        incoming_deep_link = self._get_deep_link(incoming_message_text)

        # if not the incoming command is empty
        if incoming_deep_link:
            for protected_route in protected_routes:
                if protected_route.startswith("deep_link::"):
                    protected_deep_link = protected_route.replace("deep_link::","")
                    # if the incoming command is protected by middleware
                    deep_link_pattern = protected_deep_link
                    regex_pattern = deep_link_pattern.replace("{str}", r"\b\w+\b")\
                            .replace("{int}", r"\b\d+\b")
                    is_matched = re.match(regex_pattern, incoming_deep_link)
                    
                    if is_matched:
                        return True
        else:
            return False
        
    async def _is_state_protected(self, incoming_data):
        """
        Checks if the incoming event is associated with a protected state.

        Args:
            data (dict): Additional data associated with the event.

        Returns:
            bool: True if the event is associated with a protected state, False otherwise.

        """

        protected_routes = self.protected_routes
        incoming_state = await incoming_data.get('state').get_state()

        # if not the incoming command is empty
        if incoming_state:
            for protected_route in protected_routes:
                if protected_route.startswith("state::"):
                    protected_state = protected_route.replace("state::","")
                    # if the incoming command is protected by middleware
                    if protected_state == incoming_state:
                        return True
        else:
            return False