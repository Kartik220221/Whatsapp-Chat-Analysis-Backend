from fastapi import FastAPI,APIRouter,UploadFile,File,Form
from fastapi.middleware.cors import CORSMiddleware
from preprocess import preprocess_data
from typing import Optional
from helper import *
from model import UserResponseModel
app = FastAPI()
router = APIRouter()

df = None

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://whatsapp-chat-analysis-frontend-zvv.vercel.app"],  # You can set specific origins like ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@router.post('/',response_model=UserResponseModel)
async def get_stats(file:Optional[UploadFile]=File(None),user:Optional[str]=Form("Overall")):
    global df
    if file:
        content = await file.read()
        decoded_content = content.decode('utf-8')
        df = preprocess_data(decoded_content)

    if not isinstance(df,pd.DataFrame):
        return {"error":True,"message":"there is some error in the data"}
    
    unique_user_list:list = get_unique_users(df)
    media_count,message_count = get_message_count(df,user)
    word_count:int = get_word_count(df,user)

    message_percentage:dict = get_user_messages_percentage(df)

    month_data:dict = monthly_data(df,user)

    top_words_data:dict = get_top_words(df,user)

    month_message_data = monthly_message_data(df,user)

    emoji_data:dict = get_emoji_count(df,user)

    return UserResponseModel(
        user=user,
        unique_user_list=unique_user_list,
        message_count=message_count,
        word_count=word_count,
        media_count=media_count,
        message_percentage=message_percentage,
        month_data=month_data,
        month_message_data=month_message_data,
        top_words_data=top_words_data,
        emoji_data=emoji_data
    )

app.include_router(router=router)

        
        
