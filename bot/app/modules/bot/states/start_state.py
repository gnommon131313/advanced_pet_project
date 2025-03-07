import telebot
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from modules.db import models
from modules.bot.entities import fsm
from modules.db.db_manager import db
from modules.utils.emojer import Emoji
from modules.bot.states.base_state import BaseState, MainButton


class StartState(BaseState):
  
    def __init__(self, bot, chat_id, username):
        super().__init__(bot, chat_id, username)

        from modules.bot.states import resume_state
        
        self._main_buttons.append(MainButton(state=resume_state.ResumeState, text=f"{Emoji.NOTEBOOK}О чем говорили в чатах?"))
  
    def on_enter(self):
        super().on_enter()
        
        self._save_message(self._bot.send_message(
            chat_id=self._chat_id,
            text=f"{Emoji.WELCOME}Добро пожаловать!",
            reply_markup=self._get_main_keyboard()
        ))