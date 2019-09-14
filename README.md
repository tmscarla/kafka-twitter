<p align="center">
<img height=180px src="https://github.com/tmscarla/kafka-twitter/blob/master/logo.jpg?raw=true"/>
</p>

# Kafka Twitter

Repository for the mandatory project for the 2019 **Middleware Technologies** class.

The purpose of  this project is to implement a simplified version of the Twitter social network using **Apache Kafka** to store tweets. Users interact with Twitter using a client that presents a timeline of tweets and allows users to publish new tweets.</p>

## Data Preprocessing
Even if it was not requested, we wanted to reproduce a real life situation by using
real tweets of real users. To reach this goal, in the <code>data_preprocessing</code>
folder there the scripts used in order to get, clean and prepare the final dataset; in particular:
1. `tweet_api.py`: this was used in order to periodically fetch tweets from the Twitter social network by means of the Twitter API accessed through the [Twython wrapper](https://twython.readthedocs.io/en/latest/).
2. `topic_extraction.py`: this script extracts the topics from the tweets previously gathered, producing an LDA model that will be used in order to assign a topic to each new tweet in the social network. To performa LDA, we used the very cool free python library [gensim](https://radimrehurek.com/gensim/) together with [nltk](https://www.nltk.org/). A detailed and interesting tutorial can be found in [this article](https://towardsdatascience.com/topic-modelling-in-python-with-nltk-and-gensim-4ef03213cd21).
3. `categorize_tweets.py`: **(TO BE DONE!!!**) this script assigns to the new tweets a topic based on the previously generated model.

<<<<<<< HEAD
## KafkaTwitter
The scope of the project was to create a dummy version of the popular Twitter social network. In our case, we developed a very simple application that has 3 main components:
1. `Client`: the user will interact with the app through a basic GUI made with Tkinter
2. `Application Server`: this component will receive the REST calls from the client and will forward them to the Kafka Brokers in order to publish or fetch the messages. This component is also responsible for filtering the messages. We used Flask to map the REST API.
3. `Kafka`: we used Apache Kafka to store the tweets. Our specific setup was made of 1 machine running both Zookeeper and Kafka, and 2 machines as additional Kafka brokers.

## Get started with KafkaTwitter!
### Setup Apache Kafka
First of all, you need Apache Kafka. In order to do so, just follow the simple instructions provided on the [Confluent Platform Quick Start](https://docs.confluent.io/current/quickstart/ce-quickstart.html#ce-quickstart) page. In a few minutes you should be able download and setup all you need; at that point just open your favorite terminal and run:
```console
foo@bar:~$ <PATH-TO-CONFLUENT>/bin/confluent local start
```
And that's it with Kafka, as simple as that :-)

This is the basic setup if you want to run the application on a single machine. In this case your machine will host the client, the AppServer and both Kafka and Zookeeper. If you want to run the application in a distributed scenario, jump to the end of this file.
### Run the Application Server
The Application Server will serve all the REST calls of the clients so it's the first thing that has to be started. In order to do so you need:

1. Check the IP set at the end of the `Server.py` file. You should see something like:
```python
if __name__ == '__main__':
    app.run(host='127.0.0.1', port='5000', debug=True)
```
Edit this properties as you please. The parameters name are pretty self-explanatory, but just to be sure...
- fill the `host` with the IP machine that will run your server (note: if you are running the app just on your machine, you can simply leave the localhost).
- Flask typically runs on `port` 5000, but you can change this if you need it.
- `debug` is set to true so you can know what's going on.
2. Now simply go to the project folder run the following line on the shell and you should be good to go:
```console
foo@bar:~$ python3 Server.py
```
After a few seconds your Application Server should be running.
=======
// TODO
>>>>>>> d431a6bec5557e45b4a7c141b23b28d6c0a26675
