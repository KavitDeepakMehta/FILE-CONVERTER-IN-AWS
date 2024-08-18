# FILE-CONVERTER-IN-AWS
## Project Description

Building a Web application using AWS EC2, IAM, S3, SQS and Lambda. To deploy a file uploading web application and show converted file in the destination bucket.

## Project Architecture

![File Conversion Web Application](https://github.com/user-attachments/assets/b7c62eea-0878-4eb0-9740-c21582f742ab)

## Steps

1. Create 2 IAM Roles with Permissions
EC2 – AmazonS3FullAccess, AmazonSQSFullAccess, AWSLambda_FullAccess
Lambda – AmazonEC2FullAccess, AmazonS3FullAccess, AmazonSQSFullAccess

2. Create a S3 Bucket (Source Bucket)
Bucket name : source-bucket-ohio
Object Ownership : Disabled
Block Public setting from bucket : Untick All and Acknowlege it
Bucket Versioning : Disable
Encryption Type: SSE-S3
Bucket Key: Disable
Create Bucket
Edit the policy of bucket as mentioned
Save Changes

3. Create a S3 Bucket (Destination Bucket)
Bucket name : destinashun-bucket-ohio
Object Ownership : Disabled
Block Public setting from bucket : Untick All and Acknowlege it
Bucket Versioning : Disable
Encryption Type: SSE-S3
Bucket Key: Disable
Create Bucket
Edit the policy of bucket as mentioned
Save Changes

4. Create a Lambda Function (ConvertingFunction)
Author from scratch 
Function name : ConvertingFunction
Runtime : Python 3.9 
Architecture : x86_64 
Permission : Give the role you made earlier for Lambda
Create Function

5. Create a EC2 Instance (File_Converter)
Name : File_Converter 
AMI : Amazon Linux 2 
Instance Type : t2.micro 
Key pair (login) : OhioKey 
Add SSH, HTTP & HTTPS
Launch Instance
In Actions, Go to Security and click on Modify IAM Role
Select IAM Role you created earlier for EC2
Save Changes

6. Create a SQS Queue (MessageQueue)
Type : Standard
Name : MessageQueue
Encryption : Disabled
Access Policy : Write it as mentioned
Everything else Disabled
Create Queue

7. Go back to your source bucket and in properties create a event notification
Name : Queue_Event
Event Type : PUT
Destination : SQS Queue
Specify SQS Queue : MessageQueue
Save Changes

8. Go back to your Lambda Function and Add Trigger 
Trigger Configuration : SQS
SQS queue : Select YOUR_SQS_QUEUE_ARN
Add

9. Also Write your Conversion Python Code in Lambda Function

10. Finally Connect your EC2 instance and write the commands and Execute the code to see your converted file in your destination bucket

## Documentation Link

https://docs.google.com/document/d/1IMj_fpMHUMw5_wG4YjrBpvDxIKLTzjxoeW0GYzlnB3c/edit?usp=sharing

## Implementation Video Link

https://github.com/user-attachments/assets/7edd733a-78bb-489d-b1c3-4cc78ed107f5

## Expected Outcome

The expected outcome of the project is that users can upload files to the source S3 bucket, which will trigger an SQS message, invoke a Lambda function to convert the files, and automatically place the converted files into the destination S3 bucket. The entire process will be automated and seamless, allowing for efficient file conversion and storage.
