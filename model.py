from pydantic import BaseModel,Field
from typing import Optional
from fastapi import UploadFile
class UserResponseModel(BaseModel):
    user:str
    unique_user_list:list
    message_count:int
    word_count:int
    media_count:int
    message_percentage:dict
    month_data:dict
    month_message_data:dict
    top_words_data:dict
    emoji_data:dict

    

