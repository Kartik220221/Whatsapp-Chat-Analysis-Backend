import re
import pandas as pd
from datetime import datetime

def preprocess_data(data:str):
    # Combined pattern for both formats
    pattern = r'(\d{1,2}/\d{1,2}/(\d{2,4})),\s(\d{1,2}:\d{2})(?:\s([ap]m))?\s-\s'

    # Convert to 24-hour format
    def convert_to_24hr(match):
        date_part = match.group(1)
        year = match.group(2)
        time_part = match.group(3)
        am_pm = match.group(4)

        try:
            if len(year) == 2 and am_pm:  # 12-hour format
                full_str = f"{date_part}, {time_part} {am_pm}"
                dt = datetime.strptime(full_str, "%d/%m/%y, %I:%M %p")
            else:  # 24-hour format
                full_str = f"{date_part}, {time_part}"
                dt = datetime.strptime(full_str, "%d/%m/%Y, %H:%M")
            return dt.strftime("%d/%m/%Y, %H:%M - ")
        except Exception as e:
            print("Failed at:", match.group(0))
            raise e

    # Apply conversion
    converted_data = re.sub(pattern, convert_to_24hr, data)

    # Extract messages and timestamps
    split_pattern = r'\d{1,2}/\d{1,2}/\d{4},\s\d{1,2}:\d{2}\s-\s'
    messages = re.split(split_pattern, converted_data)[1:]
    timestamps = re.findall(split_pattern, converted_data)

    # Build DataFrame
    df = pd.DataFrame({'user_message': messages, 'message_date': timestamps})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%d/%m/%Y, %H:%M - ")

    df.rename(columns={'message_date':'date'},inplace=True)

    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['hour'] = df['date'].dt.hour
    df['minute']=df['date'].dt.minute

    df.drop(['date'],axis=1,inplace=True)

    def get_user(raw_message):
        cleaned_message = raw_message.replace('\n', ' ')
        user=cleaned_message.split(":",1)
        if len(user)==2:
            return pd.Series([user[0],user[1].strip()])
        else:
            return pd.Series(["System Message",user[0].strip()])

    df[['user','message']] = df['user_message'].apply(get_user)

    return df
