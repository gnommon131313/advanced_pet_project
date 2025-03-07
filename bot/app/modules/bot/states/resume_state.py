import telebot, math
from sqlalchemy import distinct
from telebot.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

from modules.db import models
from modules.bot.entities import fsm
from modules.db.db_manager import db
from modules.utils.emojer import Emoji
from modules.utils.llm_responder import llm_responder
from modules.bot.states.base_state import BaseState, MainButton


class ResumeState(BaseState):
  
    def __init__(self, bot, chat_id, username):
        super().__init__(bot, chat_id, username)

        from modules.bot.states import resume_state
        
        self._main_buttons.append(MainButton(state=resume_state.ResumeState, text=f"{Emoji.ARROW_LEFT}Назад"))
  
    def on_enter(self):
        super().on_enter()
        
        self._save_message(self._bot.send_message(
            chat_id=self._chat_id,
            text=f"{Emoji.MESSAGE}Групповые чаты:",
        ))
        
        with db.create_session() as session:
            for chat_id in session.query(distinct(models.Message.chat_id)).all()[0]:
                keyboard = InlineKeyboardMarkup()
                keyboard.row(InlineKeyboardButton(text=f"{Emoji.MARK_BLUE}Резюмировать", callback_data=f"{chat_id}"))
                
                self._save_message(self._bot.send_message(
                    chat_id=self._chat_id,
                    text=f"{self._bot.get_chat(chat_id).title}",
                    reply_markup=keyboard
                ))
                        
    def callback_handler(self, call: CallbackQuery):
        self._drop_saved_messages()
       
        with db.create_session() as session:
            self._save_message(self._bot.send_message(chat_id=self._chat_id, text=f"подождите..."))
            
            messages = session.query(models.Message).filter_by(chat_id=call.data).order_by(models.Message.message_id.desc()).limit(5).all()
            messages = sorted(messages, key=lambda message: message.message_id)
            
            # !ВАЖНО: CallbackQuery имеет срок жизни в 60сек, а получение ответа от llm может быть дольше, тогда будет ошибка, эта ошибка не фатальна, и если модель мощьная то это никогда не поизойдет, т.к. тут эта возможная ошибка просто игнорируеться
            llm_response = llm_responder.query(
                knowledge_base=[message.text for message in messages], 
                question="describe in a few words"
            )
            
            self._drop_saved_messages()
            self._save_message(self._bot.send_message(
                chat_id=self._chat_id,
                text=f"{llm_response['exact']}",
                reply_markup=self._get_main_keyboard()
            ))
            
        return self