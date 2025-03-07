from modules.bot.states.base_state import BaseState


class FSM():
    
    def __init__(self) -> None: 
        self._current_state = None
    
    def change_state(self, state: BaseState)-> BaseState:
        
        if self._current_state:
            self._current_state.on_exit()
            
        self._current_state = state
        self._current_state.on_enter()
       
        return self._current_state
    
    
fsm = FSM()