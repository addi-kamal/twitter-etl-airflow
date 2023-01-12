# ETL to Collect, transform and load data to google cloud storage  using Airflow on GCP

In this project, I extracted data using the tweepy API, performed the processing in Python to transform data, 
deployed the pipline on Google Cloud Composer and the final results are loaded onto Google Cloud Storage bucket incrementally using an Airflow workflow.

Airflow is used to programmatically create, schedule and monitor the collection process.

### Prerequisites

* Python version 3.*
* Tweepy API (twitter developer account)
* Apache Airflow
* Google cloud account (GCP)

### Installation and preparation

If you have a GCP account you need to create a Cloud Composer and install tweepy using requirements.txt file. 

If you run the project in your local machine you need to install all the dependencies from the requirements.txt file.

To install tweepy in Google Cloud Composer go to the google shell and run the following command 

```
gcloud composer environments update 'composer_id' --update-pypi-packages-from-file requirements.txt --location us-central1
```
In my case I used us-central1 as location for my project, if you use different location use the same in the above command.


### Deploy Apache Airflow Workflow in Cloud Composer

To schedule the DAG in Cloud Composer, you need to upload etl_pipline.py file to your environment's /dags folder

To upload etl_pipline.py with gcloud, run the following command:
```
gcloud composer environments storage dags import --environment 'composer_id' --location us-central1 --source etl_pipline.py
```
The code is now available on Airflow bucket and runing on Google Cloud Composer.

### Airflow Monitoring

Navigate to Airflow instance in Google Cloud Composer to monitor the collection process.

![image](https://user-images.githubusercontent.com/57157566/212065072-9549d272-9be6-439c-9c53-d1015d962841.png)


Our ETL is now runing on Google Cloud Composer

![image](https://user-images.githubusercontent.com/57157566/212065501-a66e2b8b-f5eb-426c-a6e7-bc708dc94679.png)



