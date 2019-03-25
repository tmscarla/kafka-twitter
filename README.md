# Twitter-Kafka Course Project

Private repo for the mandatory project for the 2019 **Middleware Technologies** class.

The purpose of  this project is to implement a simplified version of the Twitter social network using **Apache Kafka** to store tweets. Users interact with Twitter using a client that presents a timeline of tweets and allows users to publish new tweets.</p>

## Data Preprocessing
Even if it was not requested, we wanted to reproduce a real life situation by using
real tweets of real users. To reach this goal, in the <code>data_preprocessing</code>
folder there the scripts used in order to get, clean and prepare the final dataset; in particular:
1. `tweet_api.py`: this was used in order to periodically fetch tweets from the Twitter social network by means of the Twitter API accessed through the [Twython wrapper](https://twython.readthedocs.io/en/latest/).
2. `topic_extraction.py`: this script extracts the topics from the tweets previously gathered, producing an LDA model that will be used in order to assign a topic to each new tweet in the social network. To performa LDA, we used the very cool free python library [gensim](https://radimrehurek.com/gensim/) together with [nltk](https://www.nltk.org/). A detailed and interesting tutorial can be found in [this article](https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21).
3. `categorize_tweets.py`: **(TO BE DONE!!!**) this script assigns to the new tweets a topic based on the previously generated model.
