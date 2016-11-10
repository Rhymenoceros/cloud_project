# Amazon Machine Learning without the console


This project is meant to demonstrate the functionality of the Amazon web service SDK for python (Boto). In particular it will show how to use Amazon’s machine learning service and the s3 storage service without logging into the amazon console and using the interface. 


## Setting up

### Configuring credentials

By default, the SDK will look for a credentials file at `~/.aws/credentials` or
`C:\Users\USER_NAME\.aws\credentials` for Windows users.
The file should look like this (without spaces at the beginning of each line):

    [default]
    aws_access_key_id = YOUR_ACCESS_KEY_ID
    aws_secret_access_key = YOUR_SECRET_ACCESS_KEY

## Sample code

There are three different scripts run.py, use_model.py and build_model.py.

build_model.py is used to create an amazon machine learning model. The script has been set up to use the document "bank_datasource.csv" in the datasource directory. The model is also preconfigured to use the schema in provided in the model directory. This function takes two arguments and an optional third argument. The first is the name the model will be named. The second is the name of the s3 url to the datasource. you can optionally provide a third argument, this is the name of a datasource you want to upload to s3 and use. If you provide a third argument, the second argument will be used to decide what the name of the uploaded datasource will be. To run this script:

    `python build_model.py "model name" "s3://cits5503-21328536/bank_datasource.csv"`

or

    '`python build_model.py "model name" "s3://cits5503-21328536/bank_datasource.csv" datasource/bank_datasource`	


use_model.py can be used to produce a set of batch predictions from a model. The first argument is the model ID. The second argument sets the score threshold. The third argument provides the s3 url where the predictions are outputted. 

    `python use_model.py ml-12345678901 0.77 s3://your-bucket/ml-output/`

The third script will upload a batch of predictions to an s3 bucket, run analysis on the predictions and automatically download the predictions and place them in the predictions file. This script has three arguments. The first argument is the id of the model that will be used to make the predictions. The second argument is the batch of predictions you want analysed. The third argument is the name of the s3 bucket where the datasource and predictions will be stored. For example:

     `python run.py "ml-B3DNCK5KPUT" "batch/banking-batch.csv" "cits5503-21328536"`
	   

