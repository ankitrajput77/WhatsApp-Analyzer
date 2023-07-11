import re
import pandas as pd
from wordcloud import WordCloud
import emoji
import streamlit as st


# remving word that has only emojis
def remove_emojis(text):
    emoji_pattern = re.compile("["
                               u"\U0001F600-\U0001F64F"  # emoticons
                               u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                               u"\U0001F680-\U0001F6FF"  # transport & map symbols
                               u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                               u"\U00002500-\U00002BEF"  # chinese char
                               u"\U00002702-\U000027B0"
                               u"\U00002702-\U000027B0"
                               u"\U000024C2-\U0001F251"
                               u"\U0001f926-\U0001f937"
                               u"\U00010000-\U0010ffff"
                               u"\u2640-\u2642"
                               u"\u2600-\u2B55"
                               u"\u200d"
                               u"\u23cf"
                               u"\u23e9"
                               u"\u231a"
                               u"\ufe0f"  # dingbats
                               u"\u3030"
                               "]+", flags=re.UNICODE)
    return emoji_pattern.sub(r'', text)



def features(df):
    user = []
    user_msg = []
    for msg in df['message']:
        split_string = re.split(r"\s*:\s*", msg, maxsplit=1)
        if(len(split_string)) > 1 : 
            number = split_string[0]
            message = split_string[1]
            user.append(number)
            user_msg.append(message)
        else :
            user.append('Notification')
            user_msg.append(msg)
    return (
        user,
        user_msg
    )



def all_messages(selected_user, df):
    if selected_user == 'All Users':
        return len(df['Message'])
    else :
        return df[df['User'] == selected_user].shape[0]



def all_words(selected_user, df):
    df = df[df['User'] != 'Notification']
    df = df[df['Message'] != '<Media omitted>\n']
    if selected_user == 'All Users':
        words = []
        for msg in df['Message']:
            words.extend(msg.split())
        list_without_emojis = [remove_emojis(text) for text in words]
        my_list_without_empty = [element for element in list_without_emojis if element != '']
        return my_list_without_empty
    else :
        words = []
        for msg in df[df['User'] == selected_user]['Message']:
            words.extend(msg.split())
        list_without_emojis = [remove_emojis(text) for text in words]
        my_list_without_empty = [element for element in list_without_emojis if element != '']
        return my_list_without_empty



def word_stock(selected_user, df):
    df = df[df['User'] != 'Notification']
    df = df[df['Message'] != '<Media omitted>\n']
    if selected_user == 'All Users' :
        words = []
        for msg in df['Message']:
            words.extend(msg.split())
        list_without_emojis = [remove_emojis(text) for text in words]
        my_list_without_empty = [element for element in list_without_emojis if element != '']
        return len(list(set(my_list_without_empty)))
    else :
        words = []
        for msg in df[df['User'] == selected_user]['Message']:
            words.extend(msg.split())
        list_without_emojis = [remove_emojis(text) for text in words]
        my_list_without_empty = [element for element in list_without_emojis if element != '']
        return len(list(set(my_list_without_empty)))



def total_days(df): 
    start_date = df['date-time'][0]
    end_date = df['date-time'].iloc[-1]
    total_days = (end_date - start_date).days + 1
    return total_days



def total_links(selected_user, df):
    if selected_user == 'All Users':
        return (len(df[df['Message'] == '<Media omitted>\n']) + len(df[df['Message'] == '<Media omitted>']))
    else :
        df_copy = df[df['User'] == selected_user]
        return (len(df_copy[df_copy['Message'] == '<Media omitted>\n']) + len(df[df['Message'] == '<Media omitted>']))



def create_wordcloud(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]
    wc = WordCloud(width=500, height=500, min_font_size=10, background_color='black', colormap='coolwarm_r')
    df_wc = wc.generate(df['Message'].str.cat(sep=" "))

    return df_wc



def week_activity_map(selected_user,df):

    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]

    return df['day_name'].value_counts()



def month_activity_map(selected_user,df):

    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]

    return df['month_name'].value_counts()



def emoji_activity(selected_user, df):
    if selected_user != 'All Users':
        df = df[df['User'] == selected_user]

    emoji_list = []
    for msg in df['Message']:
        emojis = emoji.emoji_list(msg)
        for i in emojis:
            emoji_list.append(i['emoji'])
    return(
        len(emoji_list),
        len(list(set(emoji_list))),
        pd.DataFrame(emoji_list).value_counts()[:5]
    )




def about_me():
        st.title("About the Creator")
        c1, c2 = st.columns([1,1])
        c1.markdown("""Hey! My name is **Ankit Rajput**, Mathematics and Computing student in Indian Institute Of Technology, Guwahati.
                    This app is for Whatsapp chat Analysis, I am updating this app continuously.
                    If you have any Questions or Suggestion about this app and you want to discuss it with me
                    Contact me on rajputankit72106@gmail.com""")
        c1.markdown("If you are interested :")
        c1.markdown("Github : https://github.com/ankitrajput77")
        c1.markdown("LinkedIn : https://www.linkedin.com/in/ankit-rajput892/")

        c2.image('static/Images/me.jpg')
