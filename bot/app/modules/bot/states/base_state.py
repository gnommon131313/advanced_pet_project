import telebot
from pydantic import BaseModel
from abc import ABC, abstractmethod
from typing import List, Dict, Optional, Type
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from modules.db import models
from modules.bot.entities import fsm
from modules.db.db_manager import db
from modules.utils.emojer import Emoji


class BaseState(ABC):
    
    def __init__(self, bot: telebot.TeleBot, chat_id: int | str, username: str): 
        self._bot = bot
        self._chat_id = chat_id
        self._username = username
        self._saved_messages  = []
        self._main_buttons = []
        
    def on_enter(self) -> None:
        pass
    
    def on_exit(self) -> None:
        self._drop_saved_messages()
        
    def message_handler(self, message: Message):
        self._save_message(message=message)
        
        if button := next((button for button in self._main_buttons if button.state and message.text and message.text in button.text), None): 
            return fsm.fsm.change_state (button.state(self._bot, message.from_user.id, message.from_user.username))
        
        return self
        
    def callback_handler(self, call: CallbackQuery):
        return self
    
    def other_handler(self, message: Message):
        self._save_message(self._bot.send_message(chat_id=message.chat.id, text="формат нe ожидался"))
        
        return self
   
    def _get_main_keyboard(self, admin_state=None, admins: list = None) -> ReplyKeyboardMarkup: 
        keyboard = ReplyKeyboardMarkup (resize_keyboard=True)
       
        for button in self._main_buttons:
            if admin_state is None or admins is None or button.state is not admin_state or self._username in admins: 
                keyboard.add(KeyboardButton(text=button.text, request_contact=button.request_contact))
        
        return keyboard
    
    def _save_message(self, message: Message) -> None:
        self._saved_messages.append(message.message_id)
   
    def _drop_saved_messages(self) -> None:
        for message_id in self._saved_messages:
            self._bot.delete_message(chat_id=self._chat_id, message_id=message_id)
        
        self._saved_messages = []
        
class MainButton(BaseModel):
    state: Type[BaseState] = None
    text: str
    request_contact: bool = False
    
    class Config:
        arbitrary_types_allowed = True