import pandas as pd

from collections import Counter
import emoji

def get_unique_users(df:pd.DataFrame):
    users = df['user'].unique().tolist()
    users.insert(0,"Overall")
    return users

def get_word_count(df:pd.DataFrame,user:str="Overall"):
    if user=="Overall":
        data = df[df['user']!="Group Notification"]['message']
    else:
        data = df[df['user']==user]['message']
        
    output_list = []
    for i in data:
        i_list = i.split(" ")
        output_list.extend(i_list)
    return int(len(output_list))

def get_message_count(df:pd.DataFrame,user:str):
    if user=="Overall":
        data = df[df['user']!="Group Notification"]['message']
    else:
        data = df[df['user']==user]['message']
    media_count = []
    message_count = []
    for i in data:
        if i.strip()=='<Media omitted>':
            media_count.append(i)
        else:
            message_count.append(i)
    return int(len(media_count)),int(len(message_count))

def get_user_messages_percentage(df:pd.DataFrame):
    stats_dict = {}
    for i in df['user'].unique():
        stats_dict[i]=float(round((get_message_count(df,i)[1])/int(get_message_count(df,'Overall')[1])*100,2))
    return stats_dict

def monthly_data(df:pd.DataFrame,user:str):
    time_data = df['month']+' - '+df['year'].astype(str)
    new_series = pd.Series(time_data)
    new_df = pd.DataFrame(new_series,columns=['Month - Year']).copy()
    df['Month - Year'] = new_df
    if user=='Overall':
        data = df[df['user']!="Group Notification"].copy()
    else:
        data = df[df['user']==user].copy()
    monthly_data_dict = {}
    num_unique_fields = data['Month - Year'].unique()
    for i in num_unique_fields:
        message_series = data[data['Month - Year']==i]['message']
        full_text = " ".join(message_series.dropna().astype(str).tolist())
        if full_text.strip() == '':
            num_words = 0
        else:
            num_words = len(full_text.strip().split())

        monthly_data_dict[i] = num_words
    return monthly_data_dict

def monthly_message_data(df:pd.DataFrame,user:str):
    time_data = df['month']+' - '+df['year'].astype(str)
    new_series = pd.Series(time_data)
    new_df = pd.DataFrame(new_series,columns=['Month - Year'])
    df['Month - Year'] = new_df
    monthly_data_dict = {}

    if user=='Overall':
        data = df[df['user']!="Group Notification"]
    else:
        data = df[df['user']==user]
    
    ordered_month_years = data['Month - Year'].unique()

    # Iterate through these unique month-year combinations in their original order
    for month_year in ordered_month_years:
        # Filter the data for the current month_year
        messages_in_month = data[data['Month - Year'] == month_year]
        
        # Count the number of messages in this filtered subset
        count = messages_in_month['message'].count() # .count() ignores NaN messages
                                                   # If you want to count all rows regardless of message content, use len(messages_in_month)

        monthly_data_dict[month_year] = int(count)

    return monthly_data_dict


def get_top_words(df:pd.DataFrame,user:str):
    if user=='Overall':
        data = df[df['user']!="Group Notification"]['message']
    else:
        data = df[df['user']==user]['message']
    text_list = []
    for i in data:
        i_list = i.split(" ")
        text_list.extend(i_list)
    counter = Counter(text_list)
    most_common = counter.most_common(10)
    most_common_word = [word for word,count in most_common]
    most_common_count = [int(count) for word,count in most_common]
    
    least_common = sorted(counter.items(),key=lambda x:x[1])[:10]
    least_common_word = [word for word,count in least_common]
    least_common_count = [int(count) for word,count in least_common]
    return {"most_common":{"most_common_word":most_common_word,'most_common_count':most_common_count},"least_common":{"least_common_word":least_common_word,'least_common_count':least_common_count}}

def get_emoji_count(df:pd.DataFrame,user:str):
    if user=='Overall':
        data = df[df['user']!="Group Notification"]['message']
    else:
        data = df[df['user']==user]['message']
    text_list = []
    for i in data:
        i_list = i.split(" ")
        text_list.extend(i_list)
    def extract_emoji(text:str):
        return [char for char in text if char in emoji.EMOJI_DATA]
    emoji_list = []
    for emoji_text in text_list:
        emoji_list.extend(extract_emoji(emoji_text))
    emoji_counter = Counter(emoji_list)
    return {
        "total_emoji_count":int(sum(emoji_counter.values())),
        "emoji_counts":{k: int(v) for k, v in emoji_counter.items()},
        "unique_emojis":int(len(set(emoji_list)))
    }