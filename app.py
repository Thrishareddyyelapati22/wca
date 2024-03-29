import streamlit as st
import matplotlib.pyplot as plt
import helper
import preprocessor
import seaborn as sns

st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file=st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_upload=uploaded_file.getvalue()
    data=bytes_upload.decode("utf-8")
    df=preprocessor.preprocess(data)
    #st.dataframe(df)
    #fetch unique users
    user_list=df['user'].unique().tolist()
    user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,"Overall")
    selected_user=st.sidebar.selectbox("Show the analysis",user_list)
    if st.sidebar.button("Show Analysis"):



        num_messages,words,num_media_messages,num_links=helper.fetch_stats(selected_user,df)
        st.title("Top Statistics")
        col1,col2,col3,col4=st.columns(4)
        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links shared")
            st.title(num_links)
        #timeline
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,axis=plt.subplots()
        axis.plot(timeline['time'],timeline['message'],color="green")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)


        #daily timeline
        st.title("Daily Timeline")
        daily_timeline = helper.daily_timeline(selected_user, df)
        fig, axis = plt.subplots()
        axis.plot(daily_timeline['only_date'], daily_timeline['message'], color="black")
        plt.xticks(rotation='vertical')
        st.pyplot(fig)




    #activity map
        st.title("Activity Map")
        col1,col2=st.columns(2)
        with col1:
            st.header("Most busy day")
            busy_day=helper.weekly_activity_map(selected_user,df)
            fig,axis=plt.subplots()
            axis.bar(busy_day.index,busy_day.values)
            st.pyplot(fig)
        with col2:
            st.header("Most busy month")
            busy_month = helper.monthly_activity_map(selected_user, df)
            fig, axis = plt.subplots()
            axis.bar(busy_month.index, busy_month.values,color="pink")
            plt.xticks(rotation='vertical')
            st.pyplot(fig)
        st.title("Weekly activity map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,axis=plt.subplots()
        axis=sns.heatmap(user_heatmap)

        st.pyplot(fig)


        #finding the busiest users in the group
        if selected_user=="Overall":
            st.title("Most active users")
            x,new_df=helper.most_active_user(df)
            fig,axis=plt.subplots()

            col1,col2=st.columns(2)
            with col1:
                axis.bar(x.index, x.values,color="red")
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
            with col2:
                st.dataframe(new_df)


        #Word Cloud
        st.title("WordCloud")
        df_wc=helper.create_wordcloud(selected_user,df)
        fig,axis=plt.subplots()
        axis.imshow(df_wc)
        st.pyplot(fig)

        #most commom words
        most_common_df=helper.most_common_words(selected_user,df)

        fig,axis=plt.subplots()
        axis.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title("Most Common Words")
        st.pyplot(fig)


        #emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")
        col1,col2=st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig,axis=plt.subplots()
            axis.pie(emoji_df['Count'],labels=emoji_df['Emoji'],startangle=90, counterclock=False)
            st.pyplot(fig)














