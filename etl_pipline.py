# *************   Twitter ETL Pipeline deployed in GCP Cloud Composer   *************

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago
import tweepy
import pandas as pd 
import re
from datetime import timedelta


# These args will get passed on to each operator
# We can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'email': ['addikamal.ak@gmail.com']
}

# basic processing of a tweet
def preprocess(tweet):

    tweet = re.sub(r"http\S+", "", tweet) # delete urls
    tweet = re.sub(r"@[\w]*", "", tweet) # delete tags
    tweet = re.sub(r"#[\w]*", "", tweet) # delete hashtags
    return " ".join(tweet)

"""
I used a context manager to declare the DAG, In this case, I don't need to add the dag variable as a parameter in each operator. 
it is automatically done by the context manager 
thanks to the "with" statement which manages the instantiation of the DAG class and assigns the object into the variable dag. 
For a better understanding, take a look at what is done from the source code of the class DAG of Apache Airflow.
"""
with DAG(
    'twitter_etl_dag',
    default_args=default_args,
    description='Twitter ETL',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['etl-twitter'],
) as dag:
    dag.doc_md = __doc__
    # extract data from twitter using tweepy API
    def get_data_from_twitter():
        access_key = "" 
        access_secret = "" 
        consumer_key = ""
        consumer_secret = ""

        auth = tweepy.OAuthHandler(access_key, access_secret)   
        auth.set_access_token(consumer_key, consumer_secret) 

        api = tweepy.API(auth)
        tweets = api.user_timeline(screen_name='@elonmusk', 
                                count=10,
                                include_rts = False,
                                tweet_mode = 'extended'
                                )

        list = []
        for tweet in tweets:
            text = tweet._json["full_text"]

            refined_tweet = {"user": tweet.user.screen_name,
                            'text' : text,
                            'favorite_count' : tweet.favorite_count,
                            'retweet_count' : tweet.retweet_count,
                            'created_at' : tweet.created_at}
            
            list.append(refined_tweet)

        df = pd.DataFrame(list)
        return df
    # process the tweets before uploading it to Google storage bucket
    def transform(df):
        df['text'] = df['text'].apply(lambda tweet: preprocess(tweet))
        return df
    # load data into Google storage bucket
    def load(df):
        df.to_csv('gs://ske-de-projects/twitter-data/processed_tweets.csv')
        
    extract_task = PythonOperator(
        task_id='extract',
        python_callable=get_data_from_twitter,
    )
    extract_task.doc_md = """\
#### Extract task
Extract task to get data from twitter so ready for the rest of the data pipeline.
so that it can be processed by the next task.
"""

    transform_task = PythonOperator(
        task_id='transform',
        python_callable=transform,
    )
    transform_task.doc_md = """\
#### Transform task
Transform task which process the content of tweets.
"""

    load_task = PythonOperator(
        task_id='load',
        python_callable=load,
    )
    load_task.doc_md = """\
#### Load task
Load task which takes in the result of the Transform task, and load it to twitter folder in google cloud storage bucket.
"""

    # Setting a task downstream of another
    extract_task >> transform_task >> load_task
