
import pandas as pd
from collections import Counter
from urlextract import URLExtract
from wordcloud import WordCloud
import emoji
extract=URLExtract()

def fetch_stats(selected_user,df):
    if selected_user !='Overall':
        df=df[df['user']==selected_user]
    num_messages=df.shape[0]
    words=[]
    for message in df['message']:
        # print(msg)
        words.extend(message.split())
    num_media_messages=df[df['message'].str.contains('<Media omitted>|Media omitted')].shape[0]
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))




    return num_messages,len(words),num_media_messages,len(links)




def most_active_user(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'Name','user':'Percent'})
    return x,df
def create_wordcloud(selected_user,df):

    f = open('stop_words_english.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)

    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=" "))  # to generte wordcloud as an image
    return df_wc


def most_common_words(selected_user, df):
    f = open('stop_words_english.txt', 'r')
    stop_words = f.read()
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    temp = df[df['user'] != 'group_notification']
    temp = temp[temp['message'] != '<Media omitted>\n']

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


def emoji_helper(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['message']:
        for c in message:
            if emoji.is_emoji(c):
                emojis.append(c)

    # Count the occurrences of each emoji
    emoji_counts = Counter(emojis)
    # Convert Counter to DataFrame
    emoji_df = pd.DataFrame(list(emoji_counts.items()), columns=['Emoji', 'Count'])
    # Sort DataFrame by count in descending order
    emoji_df = emoji_df.sort_values(by='Count', ascending=False)

    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline
def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline

def weekly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['day_name'].value_counts()


def monthly_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    return df['month'].value_counts()
def activity_heatmap(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    user_heatmap=df.pivot_table(index="day_name",columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap