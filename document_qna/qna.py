from typing import Any, Dict, List, Optional, Union
import inspect
from openai import OpenAI


# Right now, all additional information/ contexts are performed by "user"  (i.e. The frontend)
# To perform model driven retrieval, we will use function calling from the openAI client, do note that not all openAI endpoints supports function calling


class QnA:
    def __init__(
        self,
        client: OpenAI,
        client_args: Optional[Dict[str, Any]],
        prompt: str,
        additionals: Optional[Dict[str, str]],
        chat_history: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        self.client = client
        self.chat_history = chat_history or list()

        # Both self.prompts and self.default_msg is not nessesary,
        # they are here so that the outer layer can access it
        self.prompt = [self._make_message("system", prompt)]
        self.additionals = additionals or {}
        self.client_args = client_args or {}

    def __call__(
        self, user_msg: Union[str, Dict], stream: bool = False, **call_args
    ) -> Any:
        if isinstance(user_msg, str):
            new_msg = self._make_message("user", user_msg)
        else:
            new_msg = user_msg

        self.chat_history.append(new_msg)

        if stream:
            # Return a generator with state management
            return self._streaming_context(**call_args)
        else:
            assistant_msg = self.get_assistant_response(**call_args)
            self.chat_history.append(assistant_msg)
            return assistant_msg.get("content")

    def _streaming_context(self, **call_args):
        """Creates a generator that streams the result and handles state management."""
        assistant_msg = {"role": "assistant", "content": ""}
        full_call_args = self.client_args | call_args
        
        # Build chat history using list methods instead of concatenation
        chat_history_prepended = []
        
        # Add prompt - handle both dict and list cases
        if isinstance(self.prompt, list):
            chat_history_prepended.extend(self.prompt)
        else:
            chat_history_prepended.append(self.prompt)
        
        # Add additional context messages
        chat_history_prepended.extend(self.additionals_to_messages())
        
        # Add chat history
        chat_history_prepended.extend(self.chat_history)
        
        stream = self.client.chat.completions.create(
            messages=chat_history_prepended, stream=True, **full_call_args
        )
    # Automatically appends assistance response to chat history
    def get_assistant_response(self, **call_args):
        """Obtains the assistant response via stream results"""

        # Ensure prompt is always a list before concatenation
        prompt_as_list = self.prompt if isinstance(self.prompt, list) else [self.prompt]
        chat_history_prepended = (
            prompt_as_list + self.additionals_to_messages() + self.chat_history
        )

        full_call_args = self.client_args | call_args

        new_response = self.client.chat.completions.create(
            messages=chat_history_prepended, **full_call_args
        )
        new_response = self.strip_response_dict(new_response)
        return new_response

    # Index is zero-indexed with regards to chat history
    # i.e. The system message and the default message does not count
    # Not automatically performing inference
    def restart_from_index(self, index: int):
        # OOB check
        if index >= len(self.chat_history) or index < 0:
            raise ValueError(
                f"Index {index} is out of bounds. Valid range is 0 to {len(self.chat_history) - 1}."
            )
        self.chat_history = self.chat_history[:index]
        return

    def append_additional(self, new_addition: Dict[str, str]):
        """Appends additional information/ context from the

        Old keys will get overridden by new keys
        """
        self.additionals.update(new_addition)

    def remove_additional(self, additional_key: str):
        self.additionals.pop(additional_key)

    def additionals_to_messages(self):
        additionals_msg_list = []
        for key, value in self.additionals.items():
            new_msg = self._make_message(
                "assistant", f"Additional information: \n Content: \n {value}"
            )
            additionals_msg_list.append(new_msg)

        return additionals_msg_list

    def serialize_chat(self):
        """Serialize all chats (WIP)

        Returns:
            _type_: _description_
        """
        default_msg = self.default_msg if hasattr(self, 'default_msg') else None
        return self.prompt, default_msg, self.chat_history, self.additionals

    # Removes all unwanted response fields from obtained response
    # Post processing for response dict
    # I love hardcoding ahahahahaha
    @staticmethod
    def strip_response_dict(
        msg: Dict[str, str], keys_to_keep: Optional[List[str]] = None
    ):
        keys_to_keep = keys_to_keep or ["role", "content"]
        return {key: msg[key] for key in keys_to_keep if key in msg}

    # For manually appending bot/ system messages (w/o going through llm)
    # To add user message (and getting an LLM response), use the __call__ method
    def append_message(
        self,
        role: Optional[str] = None,
        content: Optional[str] = None,
        msg_dict: Optional[Dict] = None,
    ):
        if not (role and content) or msg_dict:
            raise ValueError("Must provide either (role & content) or msg_dict")

        if msg_dict:
            self._verify_msg_dict(msg_dict)
            msg = msg_dict
        else:
            msg = self._make_message(role, content)
        self.chat_history.append(msg)

    def _prepended_msgs(self):
        msg = self.prompt.copy()  # Make a copy to avoid modifying the original
        if hasattr(self, 'default_msg') and self.default_msg:
            msg += [self.default_msg]
        return msg

    @staticmethod
    def _make_message(role: str, content: str):
        msg = {"role": role, "content": content}
        return msg

    @staticmethod
    def _verify_msg_dict(usr_msg: Dict):
        required_keys = ["role", "content"]

        # Check existance of required keys
        for key in required_keys:
            if key not in usr_msg.keys():
                raise KeyError(f"Missing Required Key: {key} from User Message dict")
            if not QnA._string_coerce_check(usr_msg[key]):
                raise TypeError(
                    f"Corresponding value for required Key: {key} could not be converted to string"
                )
        return

    @staticmethod
    def _string_coerce_check(value):
        return (
            inspect.getattr_static(value, "__str__", None) is not None
            or inspect.getattr_static(value, "__repr__", None) is not None
        )
