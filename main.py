import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt

st.title("sentiment analysis of tweets about us airlines")
st.sidebar.title("sentiment analysis of tweets about us airlines")

st.markdown("this application is streamlit dashboard to analyze the sentiment of twitter Ã°ÂÂÂ¦")
st.sidebar.markdown("this application is streamlit dashboard to analyze the sentiment of twitter Ã°ÂÂÂ¦")

#
data_url=("C:\Users\USER\PycharmProjects\Sentiment Analysis\tweets.csv")
st.cache(persist=1)
def load_data():
    data=pd.read_csv(data_url)
    data['tweet_created'] = pd.to_datetime(data['tweet_created'])
    return data

data= load_data()

st.sidebar.subheader("show random tweet")
random_tweet = st.sidebar.radio('sentiment', ('positive', 'neutral', 'negative'))
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')[["text"]].sample(n=1).iat[0,0])

st.sidebar.markdown("### number of tweets by sentiment")
select = st.sidebar.selectbox('visualization type', ['histogram', 'pie chart'], key = '1')

sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'sentiment': sentiment_count.index, 'tweets': sentiment_count.values})

if not st.sidebar.checkbox("hide", 1):
    st.markdown("### number of tweets by sentiment")
    if select == "histogram":
        fig = px.bar(sentiment_count, x ='sentiment', y="tweets", color = 'tweets', height=500)
        st.plotly_chart(fig)
    else:
        fig = px.pie(sentiment_count, values = 'tweets', names = 'sentiment')
        st.plotly_chart(fig)

st.map(data)

st.sidebar.subheader("when and where are users tweeting from?")
#hour = st.sidebar.number_input("hour of day", min_value=1, max_value=24)
hour = st.sidebar.slider("hour of day", 0,23)
modified_data=data[data['tweet_created'].dt.hour==hour]
if not st.sidebar.checkbox("close", 1, key='1'):
    st.markdown("### tweets locations based on the time of day")
    st.markdown("%i tweets between %i:00 and %i:00" % (len(modified_data), hour, (hour+1)%24))
    st.map(modified_data)
    if st.sidebar.checkbox("show row data", 0):
        st.write(modified_data)

st.sidebar.subheader("breakdown airline tweets by sentiment")

choice = st.sidebar.multiselect('pick airlines', ('US Airways', 'United', 'American','Southwest', 'Delta','Virgin America'),key='0')
if len(choice) > 0:
    choice_data = data[data.airline.isin(choice)]
    fig_choice = px.histogram(choice_data,
    x='airline',
    y='airline_sentiment',
    histfunc='count',
    color='airline_sentiment',
    facet_col='airline_sentiment',
    labels={'airline_sentiment':'tweets'},
    height=600,
    width=800)
    st.plotly_chart(fig_choice)


st.sidebar.header("word cloud")
word_sentiment = st.sidebar.radio('display word cloud for what sentiment?', ('positive', 'neutral', 'negative'))

if not st.sidebar.checkbox("close", 1, key='3'):
    st.header('word cloud for %s sentiment' % (word_sentiment))
    df = data[data['airline_sentiment']==word_sentiment]
    words=' '.join(df['text'])
    processed_words=' '.join([word for word in words.split() if 'http' not in word and not word.startswith('@') and word != 'RT'])
    wordcloud=WordCloud(stopwords=STOPWORDS, background_color='white', height=640, width=800).generate(processed_words)
    plt.imshow(wordcloud)
    plt.xticks([])
    plt.yticks([])
    st.pyplot()

