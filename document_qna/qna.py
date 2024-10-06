from typing import Any, Callable, Dict, List, Optional, Union
import inspect


# Need to Sync the chat history between the outer discord layer and the inner "LLM" layer
# For chat restart functionality (see below)
# Restart: User decided to change their question
# 

class QnA():
    
    def __init__(self, prompt: str, default_msg: Optional[str], response_func: Callable[[str], Dict], chat_history: Optional[List[Dict[str, str]]] = None) -> None:
        self.response_func = response_func
        self.chat_history = chat_history or list()
        
        #Both self.prompts and self.default_msg is not nessesary, 
        # they are here so that the outer layer can access it
        self.prompt = self._make_message("system", prompt)
        self.default_msg = self._make_message("assistant", default_msg) if default_msg else None
        
        # Basically just self.prompt (and self.default_msg if provided)
        self.prepends = self._prepended_msgs() 
    
    def __call__(self, user_msg: Union[str, Dict]) -> Any:
        new_msg = self._process_new_msg(user_msg)
        self.chat_history.append(new_msg)
        assistant_msg = self.get_assistant_response()
        return assistant_msg
    
    # Automatically appends assistance response to chat history  
    def get_assistant_response(self):
        chat_history_prepended = self.prepends + self.chat_history
        new_response = self.response_func(chat_history_prepended)
        new_response = self.strip_response_dict(new_response)
        self.chat_history.append(new_response)
        return new_response["content"]
        
    # Index is zero-indexed with regards to chat history
    # i.e. The system message and the default message does not count
    # Not automatically performing inference
    def restart_from_index(self, index: int):
        # OOB check
        if index >= len(self.chat_history) or index < 0:
            raise ValueError(f"Index {index} is out of bounds. Valid range is 0 to {len(self.chat_history) - 1}.")
        self.chat_history = self.chat_history[:index]
        return
        
    # Removes all unwanted response fields from obtained response
    # Post processing for response dict
    # I love hardcoding ahahahahaha
    @staticmethod
    def strip_response_dict(msg: Dict[str, str], keys_to_keep: Optional[List[str]] = None):
        keys_to_keep = keys_to_keep or ["role", "content"]
        return {key: msg[key] for key in keys_to_keep if key in msg}
        
    
    
    # For manually appending bot/ system messages (w/o going through llm)
    # To add user message (and getting an LLM response), use the __call__ method
    def append_message(self,
                       role: Optional[str] = None, 
                       content:Optional[str] = None, 
                       msg_dict: Optional[Dict] = None):
        
        if not (role and content) or msg_dict:
            raise ValueError("Must provide either (role & content) or msg_dict")
        
        if msg_dict:
            self._verify_msg_dict(msg_dict)
            msg = msg_dict
        else:
            msg = self._make_message(role, content)
        self.chat_history.append(msg)
    
    def _prepended_msgs(self):
        msg = [self.prompt]
        if self.default_msg:
            msg += [self.default_msg]
        return msg
    
    @staticmethod
    def _make_message(role: str, content:str):
        msg = {"role": role, "content": content}
        return msg

    @staticmethod
    def _process_new_msg(user_msg: Union[str, Dict]):
        if isinstance(user_msg, str):
            return QnA._make_message("user", user_msg)
        else: #if isinstance(user_msg, dict):
            QnA._verify_msg_dict(user_msg)
            return user_msg
    
    @staticmethod
    def _verify_msg_dict(usr_msg: Dict):
        required_keys = ["role", "content"]

        # Check existance of required keys
        for key in required_keys:
            if key not in usr_msg.keys():
                raise KeyError(f"Missing Required Key: {key} from User Message dict")
            if not QnA._string_coerce_check(usr_msg[key]):
                raise TypeError(f"Corresponding value for required Key: {key} could not be converted to string")
        return
        
    @staticmethod
    def _string_coerce_check(value):
        return inspect.getattr_static(value, '__str__', None) is not None or inspect.getattr_static(value, '__repr__', None) is not None
        
    