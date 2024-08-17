#Python Code for your Web Application
import boto3
from flask import Flask, request, jsonify, send_from_directory

app = Flask(__name__)

# Specify your region here
AWS_REGION = 'us-east-2'  # Change to your region

s3 = boto3.client('s3', region_name=AWS_REGION)
sqs = boto3.client('sqs', region_name=AWS_REGION)

ORIGINAL_BUCKET = 'source-bucket-ohio' #Replace with Actual Source Bucket
CONVERTED_BUCKET = 'destinashun-bucket-ohio' #Replace with Actual Destination Bucket
SQS_QUEUE_URL = 'https://sqs.us-east-2.amazonaws.com/851725375246/MessageQueue' #Replace the Queue URL with your Actual URL

@app.route('/')
def index():
    return '''
    <h1>Upload File</h1>
    <form action="/upload" method="post" enctype="multipart/form-data">
        <input type="file" name="file">
        <input type="submit" value="Upload">
    </form>
    '''

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'})
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'})
    if file:
        s3.upload_fileobj(file, ORIGINAL_BUCKET, file.filename)
        sqs.send_message(
            QueueUrl='https://sqs.us-east-2.amazonaws.com/851725375246/MessageQueue', #Replace the Queue URL with your Actual URL
            MessageBody=file.filename
        )
        return jsonify({'message': 'File uploaded and conversion started'})
    return jsonify({'error': 'File upload failed'})

@app.route('/converted/<filename>', methods=['GET'])
def get_converted_file(filename):
    try:
        s3.download_file(CONVERTED_BUCKET, filename, '/tmp/' + filename)
        return send_from_directory('/tmp', filename)
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)