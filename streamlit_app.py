import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from nltk import word_tokenize, download
from nltk.probability import FreqDist

from main_functions import get_top_stories, get_most_popular, filter_words

download("stopwords")
st.set_option('deprecation.showPyplotGlobalUse', False)


st.set_page_config(
    page_title="Project 1",
    page_icon="📰",
    layout="centered",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.streamlit.io/library/api-reference',
        'Report a bug': "https://docs.streamlit.io/library/api-reference",
        'About': "# This is Project 1 for COP 4813 - Prof. Gregory Reis"
    })

st.title("Project 1 - News App")

# SIDEBAR WITH DROP BUTTONS

with st.sidebar:
    api_option = st.selectbox(
        'Select An API',
        (
            'Top Stories',
            'Most Popular Articles'
        )
    )

# TOP STORIES

def display_top_stories():
    st.header('Top Stories API')
    st.subheader('I - Wordcloud')

    topic = st.selectbox(
        'Select a topic of your interest',
        ["arts", "automobiles", "books", "business", "fashion", "food", "health", "home", "insider", "magazine",
         "movies", "nyregion", "opinion", "politics", "realestate", "science", "sports", "sundayreview",
         "technology", "theater", "t-magazine", "travel", "upshot", "us", "world"]
    )

    col1, col2 = st.columns(2)

    with col1:
        wordcloud_max_words = st.slider(
            'Choose a maximum number of words to display',
            min_value=1,
            max_value=200,
            value=100
        )

        colormap = st.selectbox(
            'Choose a colormap',
            [
                'prism',
                'viridis',
                'plasma',
                'magma',
                'cividis',
                'cool',
                'spring'
            ]
        )

        background_color = st.color_picker(
            'Choose a background color',
            '#ffffff'
        )

    articles = get_top_stories(topic)

    abstracts = ""

    for result in articles["results"]:
        abstracts = abstracts + result["abstract"]

    words = word_tokenize(abstracts)

    filtered_words = filter_words(words, wordcloud_max_words)

    print(len(filtered_words))

    freq_distribution = FreqDist(filtered_words)

    with col2:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color=background_color,
            colormap=colormap,
        ).generate_from_frequencies(freq_distribution)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        plt.tight_layout(pad=0)
        st.pyplot()

    st.subheader('II - Frequency Distribution')
    should_display_frequency_dist_plot = st.checkbox('Click here to display the frequency distribution plot')

    if should_display_frequency_dist_plot:

        freq_dist_max_words = st.slider(
            'Choose the number of words',
            min_value=5,
            max_value=50
        )

        most_common_words = pd.DataFrame(freq_distribution.most_common(freq_dist_max_words))
        most_common = pd.DataFrame(
            {
                "words": most_common_words[0],
                "count": most_common_words[1]
            }
        )

        most_common_words_fig = px.histogram(most_common, x="words", y="count", title="Most Common Words",
                                             color="words")

        st.plotly_chart(most_common_words_fig)


# MOST POPULAR ARTICLES


def display_most_popular():
    st.header("Most Popular Articles")
    st.subheader('I - Comparing Most Shares, Viewed and Emailed Articles')

    topic = st.selectbox(
        'Select your preferred set of articles',
        [
            'shared',
            'viewed',
            'emailed',
        ]
    )
    age = st.selectbox(
        'Select the age of your articles in days',
        [
            '1',
            '7',
            '30',
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        wordcloud_max_words = st.slider(
            'Choose a maximum number of words to display',
            min_value=1,
            max_value=200,
            value=100
        )
        background_color = st.color_picker(
            'Choose a background color',
            '#ffffff'
        )
        colormap = st.selectbox(
            'Choose a colormap',
            [
                'prism',
                'viridis',
                'plasma',
                'magma',
                'cividis',
                'cool',
                'spring'
            ]
        )

    articles = get_most_popular(topic, age)

    abstracts = ""

    for result in articles["results"]:
        abstracts = abstracts + result["abstract"]

    words = word_tokenize(abstracts)

    filtered_words = filter_words(words, wordcloud_max_words)

    freq_distribution = FreqDist(filtered_words)

    with col2:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color=background_color,
            colormap=colormap,
        ).generate_from_frequencies(freq_distribution)

        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        plt.tight_layout(pad=0)
        st.pyplot()

    st.subheader('II - Frequency Distribution')
    should_display_frequency_dist_plot = st.checkbox('Click here to display the frequency distribution plot')

    if should_display_frequency_dist_plot:

        freq_dist_max_words = st.slider(
            'Choose the number of words',
            min_value=5,
            max_value=50
        )

        most_common_words = pd.DataFrame(freq_distribution.most_common(freq_dist_max_words))
        most_common = pd.DataFrame(
            {
                "words": most_common_words[0],
                "count": most_common_words[1]
            }
        )

        most_common_words_fig = px.histogram(most_common, x="words", y="count", title="Most Common Words",
                                             color="words")

        st.plotly_chart(most_common_words_fig)


if api_option == "Top Stories":
    display_top_stories()
else:
    display_most_popular()