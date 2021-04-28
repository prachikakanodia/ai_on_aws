#!/usr/bin/env python
# coding: utf-8

#Libraries used are opencv-python, boto3 and ipython.
import cv2
import boto3
import IPython

#To capture the live photo.
capture = cv2.VideoCapture(0)
myimg = "i.jpg"
ret, img = capture.read()
cv2.imwrite(myimg, img)
capture.release()

region = "ap-south-1"
bucket = "aionawss3bucket"

#To upload image on s3 bucket. (Set credentials using aws configure)
s3 = boto3.resource('s3')
s3.Bucket(bucket).upload_file(myimg, myimg)

#Connect to Amazon Rekognition for analysis of image.
rek = boto3.client('rekognition', region_name="ap-south-1" )

resfaces=rek.detect_faces(
Image= {
        "S3Object": {
            "Bucket": bucket,
            "Name": myimg
        }
    },
    Attributes= [
        "ALL"
    ]
)   

details = resfaces

#Few Conditions based on analysis from details.
if resfaces['FaceDetails'][0]['Smile']['Value'] == False:
    if resfaces['FaceDetails'][0]['Smile']['Confidence'] > 70:
        x = "Why are you upset, What happend?"
    else:
        x = "You seem just ok."
else:
    x = "So happy, Keep Smiling."

#Initialize polly to speak.
po = boto3.client('polly')

#Save polly output in mp3 format.
res = po.synthesize_speech(Text=x, OutputFormat='mp3', VoiceId='Joanna')
file = open('myaudio.mp3', 'wb')
file.write(res['AudioStream'].read())

#Listen the output.
IPython.display.Audio("myaudio.mp3")

