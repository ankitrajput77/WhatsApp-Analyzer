import streamlit as st
import components.data_ingestion as data_ingestion
import components.utils as utils
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import emoji

# Title of the project
st.sidebar.title('Whatsapp Chat Analyzer')

# About button
if st.sidebar.button('About Creator'):
    utils.about_me()

# file uploader 
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
        
        bytes_data = uploaded_file.getvalue()
        data = bytes_data.decode('utf-8')
        df = data_ingestion.preprocessor(data)


        # fetching unique user names
        users = df['User'].unique().tolist()
        users.remove('Notification')
        users.sort()
        users.insert(0,'All Users')
        selected_user = st.sidebar.selectbox('Members', users)


        if st.sidebar.button('Show Analysis'):

            messages = utils.all_messages(selected_user, df)
            words = utils.all_words(selected_user, df)
            avg_word = round(len(words) / messages )
            wordstock = utils.word_stock(selected_user, df)
            total_days = utils.total_days(df)
            media_shared = utils.total_links(selected_user, df)

            with st.container():
                title = f"**{selected_user}'s Analysis** 🌟"
                st.markdown(title, unsafe_allow_html=True)
                if selected_user == 'All Users':
                    days_title = 'Total Days : ' + str(total_days)
                    st.info(days_title)
                
                msg_title = 'Total Messages : ' + str(messages)
                st.success(msg_title, icon='💬')

                word_title = 'Total Words : ' + str(len(words))
                st.warning(word_title, icon= '🔤')

                avg_word_title = 'Average Words Per Msg : ' + str(avg_word)
                st.error(avg_word_title, icon='📨')

                word_stock_title = 'WordStock : ' + str(wordstock)
                st.info(word_stock_title, icon='📧')

                media_title = 'Total Media Shared : ' + str(media_shared)
                st.success(media_title, icon='📷')

            # line plot 
            st.title('Chat Timeline')
            st.text('X : Dates')
            st.text('Y : Messages')
            if selected_user == 'All Users':
                st.line_chart(data=df['date'].value_counts())
            else :
                st.line_chart(data = df[df['User'] == selected_user]['date'].value_counts())

            # Busy bar plot 
            if selected_user == 'All Users':
                st.title('Who is Most busy ? ')
                plt.figure(figsize=(15, 10))
                sns.set_style("darkgrid")
                sns.set_palette("dark")
                df_cpy = df[df['User'] != 'Notification']
                user_counts = df_cpy['User'].value_counts()
                x = user_counts.index.tolist()[:10]
                most_busy = x[0]
                y = user_counts.tolist()[:10]
                plot = sns.barplot(x=x, y=y)
                plt.xlabel('User')
                plt.ylabel('Count')
                plt.title('Messages Count')
                plot.set_facecolor('black')
                st.pyplot(plot.figure)
                st.success('It Seems that ' + most_busy + ' is most busy.')


            st.title('Time Of The Day')

            # Time bar plot 
           if selected_user == 'All Users': 
                hour_user_counts = df.groupby(['hour', 'User']).size().reset_index(name='MessageCount')
                # Pivot the data to create a wide-form DataFrame
                pivot_df = hour_user_counts.pivot(index='hour', columns='User', values='MessageCount')
                # Create the grouped bar plot
                plt.figure(figsize=(15,10))
                sns.set_style('white')
                sns.set_palette("dark")  # Set the color palette
                plot = pivot_df.plot(kind='bar', stacked=True)
                plt.xlabel('Hour')
                plt.ylabel('Number of Messages')
                plot.set_facecolor('black')
                plt.legend(title='User')
                st.pyplot(plot.figure)
                st.success("**This is the bar graph where you can see how many messages are contributed by each User in each Hour.**")
            else :
                df_copy = df[df['User'] == selected_user]
                plt.figure(figsize=(15, 10))  # Set the figure size
                user_counts = df_copy['hour'].value_counts()
                x = user_counts.index.tolist()
                y = user_counts.tolist()
                plot = sns.barplot(x=x, y=y)
                plt.xlabel('Hours')
                plt.ylabel('Count')
                plt.title('User Counts')
                st.pyplot(plot.figure)

            # word cloud plot
            st.title('Word Cloud')
            df_wc = utils.create_wordcloud(selected_user, df)
            fig, ax = plt.subplots()
            ax.imshow(df_wc)
            st.pyplot(fig)
            st.info("**Vibrant visual representation of words, displaying prominent words in varying sizes to highlight their frequency and importance. Provides a quick snapshot of key themes and concepts within a chats.**")
            

            # activity map
            st.title('Activity Map')
            col1,col2 = st.columns(2)
            with col1:
                st.success("Most Busy Day")
                busy_day = utils.week_activity_map(selected_user,df)
                fig,ax = plt.subplots()
                ax.bar(busy_day.index,busy_day.values,color='purple')
                plt.xticks(rotation='vertical')
                st.pyplot(fig)
                Active_day = busy_day.index[0]
                st.success('Most Active Day is : ' + str(Active_day))

            with col2:
                st.success("Most Busy Month")
                busy_month = utils.month_activity_map(selected_user, df)
                fig, ax = plt.subplots()
                ax.bar(busy_month.index, busy_month.values,color='orange')
                plt.xticks(rotation='vertical')
                Active_month = busy_month.index[0]
                st.pyplot(fig)
                st.success('Most Active Month is : ' + str(Active_month))


            # most word plot 
            st.title('Most Used Words')
            counts = pd.Series(words).value_counts()[:20]
            plot = sns.barplot(x=counts.index, y=counts.values)
            st.pyplot(plot.figure)

            # emoji Analysis
            total_emojis, distinct_emojis, top_emojis = utils.emoji_activity(selected_user, df)
            st.title('Emoji Analysis')
            with st.container():
                st.success('Total Emojis Used : ' + str(total_emojis))
                st.info('Distinct Emojis Used : ' + str(distinct_emojis))
                i = top_emojis.index.tolist()[:5]
                top_emo = f"Top Emojis are : {i}"
                st.error(top_emo)


         
