import boto3
import os
import secrets
from PIL import Image
from django.conf import settings


# amazon s3 で保存
def save_pictures_s3(picture, user_id):
    """
    Amazon S3に写真を保存するメソッド
    """
    aws_access_key_id = settings.AWS_ACCESS_KEY_ID
    aws_secret_access_key = settings.AWS_SECRET_ACCESS_KEY
    s3_bucket = settings.AWS_STORAGE_BUCKET_NAME

    s3 = boto3.client('s3',
                region_name='us-east-1',
                aws_access_key_id=aws_access_key_id,
                aws_secret_access_key=aws_secret_access_key,
                )
                
    picture_fn = str(user_id) + str(picture)
    response = s3.put_object(
            Body=picture,
            Bucket=s3_bucket,
            Key=picture_fn,
            ACL='public-read'
        )
    return f"https://yoshi-quiz-project.s3.amazonaws.com/{picture_fn}"