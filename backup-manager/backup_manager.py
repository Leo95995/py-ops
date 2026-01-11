import os
import datetime
import boto3
from dotenv import load_dotenv
import tarfile

load_dotenv()



def create_tar_file():
    print('xx')


def s3_upload():
    print('Uploading on S3')


def main():
    # creating tar file
    create_tar_file()

    # upload on s3..
    s3_upload()


if __name__ == '__main__':
    main()