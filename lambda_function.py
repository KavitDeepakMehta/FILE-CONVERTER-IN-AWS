import boto3  
import os  
import uuid  
from botocore.exceptions import NoCredentialsError, PartialCredentialsError  

s3 = boto3.client('s3')  
sqs = boto3.client('sqs')  

ORIGINAL_BUCKET = 'source-bucket-ohio' #Replace with Actual Source Bucket
CONVERTED_BUCKET = 'destinashun-bucket-ohio' #Replace with Actual Destination Bucket
QUEUE_URL = 'https://sqs.us-east-2.amazonaws.com/851725375246/MessageQueue' #Replace the Queue URL with your Actual URL

def lambda_handler(event, context):  
    for record in event['Records']:  
        receipt_handle = record['receiptHandle']  
        try:  
            # Get the object from the S3 bucket  
            file_key = record['body']  
            download_path = f'/tmp/{uuid.uuid4()}_{file_key}'  
            s3.download_file(ORIGINAL_BUCKET, file_key, download_path)  

            # Perform the document conversion (example: converting .docx to .pdf)  
            converted_path = convert_document(download_path)  

            # Upload the converted file back to S3  
            converted_key = f'converted/{os.path.basename(converted_path)}'  
            s3.upload_file(converted_path, CONVERTED_BUCKET, converted_key)  
 
            # Delete the message from the queue  
            sqs.delete_message(QueueUrl=QUEUE_URL, ReceiptHandle=receipt_handle)  

        except NoCredentialsError:  
            print("Error: Credentials not available")  

        except PartialCredentialsError:  
            print("Error: Incomplete credentials")  

        except Exception as e:  
            print(f"Error processing {file_key}: {str(e)}")  
 

def convert_document(input_path):  
    # Example conversion logic  
    output_path = input_path.replace('.docx', '.pdf')  
    # Use a library like python-docx or other to perform actual conversion  
    # Here we simply rename the file for demonstration  
    os.rename(input_path, output_path)  
    return output_path