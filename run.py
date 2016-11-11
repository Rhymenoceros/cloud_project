
"""
Useage:
    python run.py ml_model_id batchfilepath s3BucketName

For example:
    python run.py "ml-B3DNCK5KPUT" "batch/banking-batch.csv" "cits5503-21328536"
"""
import boto3
import use_model
import sys
import os

# The URL of the sample data in S3
#S3_URL = "s3://cits5503-21328536/"
#bucket = 'cits5503-21328536'

def upload_to_s3(uploadfile, newFileName, bucket):
    s3 = boto3.client('s3')
    s3.upload_file(uploadfile, bucket, newFileName)

def download_from_s3(s3file, newFileName, bucket):
    s3 = boto3.client('s3')
    s3.download_file(bucket, s3file, newFileName)

def wait_for_ml_model(mlname):
    client = boto3.client('machinelearning')
    waiter = client.get_waiter("ml_model_available")
    print("waiting for model to be created")
    waiter.wait(FilterVariable = "Name", EQ = mlname)

def wait_for_batch_prediction(bpname):
    client = boto3.client('machinelearning')
    waiter = client.get_waiter("batch_prediction_available")
    print("waiting for batch prediction to complete")
    waiter.wait(FilterVariable = "Name", EQ = bpname)

def wait_for_s3(bucket, objectkey):
    client = boto3.client('s3')
    waiter = client.get_waiter('object_exists')
    print("waiting for file to be uploaded")
    waiter.wait(Bucket = bucket, Key = objectkey)

if __name__ == "__main__":
    #"s3://cits5503-21328536/b"
    try:
        model_id = sys.argv[1]
        #threshold = float(sys.argv[2])
        batchfile = sys.argv[2]
        bucket = sys.argv[3]
        filename = os.path.basename(os.path.normpath(batchfile))
        url = 's3://' + bucket
        upload_to_s3(batchfile, batchfile, bucket) #upload our batch of preditions to s3 bucket
        wait_for_s3(bucket, batchfile) #wait for upload to complete
        predictionName = filename
        bp = use_model.use_model(model_id, 0.77, "schemas/predictionSchema.csv.schema",url, url +'/'+ batchfile, predictionName)
        wait_for_batch_prediction(predictionName)
        results = url+"/batch-prediction/result/"+ bp +"-" + filename + ".gz"
        print(results)
        download_from_s3("batch-prediction/result/"+ bp +"-"+filename+".gz", "prediction/"+bp+".csv.gz", bucket)
    except IndexError:
        print(__doc__)
        sys.exit(-1)
    except:
        print(__doc__)
        raise
