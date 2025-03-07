import sqlalchemy, os, telebot
import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel
from typing import List, Dict, Optional, Type
from telebot.types import Message, CallbackQuery

from modules.bot.entities.fsm import fsm
from modules.db import models
from modules.db.db_manager import db 
from modules.bot.states.base_state import BaseState
from modules.bot.states.start_state import StartState


class Bot:
    
    class Data (BaseModel):
        
        class User (BaseModel):
            user_id: int
            bot_state: Optional [BaseState] = None
        
            class Config:
                arbitrary_types_allowed = True
                
        users: Dict[int, User]
   
    def __init__(self):
        print(f"-----bot-launched-----")
        # db.create_tables()  # Только в самом начале и для тестов
        self._bot = telebot.TeleBot(os.getenv("PRODUCTION_TOKEN"))
        self._data = self.Data(users={})
    
        # @Logger().error_redirect_message
        # @mock_api
        @self._bot.message_handler(content_types=['text', 'contact', 'photo', 'document'])
        def message_handler(message: Message):
        
            if message.chat.type == "private":
                if message.text:
                    print(f"[MESSAGE]=[{message.from_user.username}]=[{message.text}]")
                   
                    if message.text and "/start" in message.text:
                        start_state = fsm.change_state(StartState(self._bot, message.from_user.id, message.from_user.username))
                        
                        if user_data := self._data.users.get(message.from_user.id):
                             user_data.bot_state = start_state
                       
                        else:
                            self._data.users[message.from_user.id] = Bot.Data.User(user_id=message.from_user.id, bot_state=start_state)
                            
                    else:
                        if user_data := self._data.users.get(message.from_user.id): 
                            user_data.bot_state = user_data.bot_state.message_handler(message)
           
                else:
                    if user_data := self._data.users.get(message.from_user.id):
                        user_data.bot_state = user_data.bot_state.other_handler(message)
            
            elif message.chat.type == 'group' or message.chat.type == 'supergroup':
                if message.from_user.is_bot:
                    return
                
                if text := message.text if message.text else message.caption if message.caption else None: 
                    with db.create_session() as session:
                        moscow_offset = datetime.timezone(datetime.timedelta(hours=3))
                        message_date = datetime.datetime.fromtimestamp(message.date, tz=moscow_offset)
                        
                        session.add(models.Message(
                            date=message_date, 
                            chat_id=str(message.chat.id), 
                            user_chat_id=str(message.from_user.id),
                            text=text
                        ))
                        session.commit()
                        
            else:
                self._bot.reply_to(message, "Невозможно обработать сообщение.")
       
        # @Logger().error_redirect_call
        # @mock_api
        @self._bot.callback_query_handler(func=lambda call: True)
        def callback_handler(call: CallbackQuery):
            print (f'\n[CALLBACK]=[{call.from_user.username}]=[{call.data}]')
            
            if user_data := self._data.users.get(call.from_user.id):
                user_data.bot_state = user_data.bot_state.callback_handler(call)
            
            self._bot.answer_callback_query(call.id, text="")
       
        self._bot.delete_my_commands()
        self._bot.polling(none_stop=True, interval=0)