import os
import datetime
import boto3
from dotenv import load_dotenv
import tarfile
import argparse

load_dotenv()



def telegram_notify():
    print("Telegram notify for succeded upload on s3 bucket ")
# get arguments from the function
def get_args():
    parser=argparse.ArgumentParser(description="Data")
    parser.add_argument('-s', '--source', help="The path of the source to backup") 
    parser.add_argument('-o', '--output', help="The output file generated")
    return parser.parse_args()

# check the path 
def check_path(source: str) -> bool: 
    return os.path.exists(source)

# preparing the output source
def prepare_output_source(output: str)-> str: 
    current_data = datetime.datetime.now().strftime("%Y_%m_%d_%H-%M")
    if output == None:
        return f"backup_{current_data}.tar.gz"
    if not output.endswith('.tar.gz'):
        output = f"{output}_{current_data}.tar.gz"
    return output

# function used to create a tar file from the source received
def create_tar_file(source: str, target: str):
    # return true or false
    if check_path(source):
        try:
            with tarfile.open(f"./{target}", mode="w:gz") as tar_file:
                tar_file.add(source, arcname=os.path.basename(source))
            return {"status":True, "file": target } 
        except Exception as e:
            print(f"Error during the file compression: {e}")
            return {"status":False}
    else:
        raise Exception('Invalid source Path. Try again')
  

# function used to upload the backup on S3 bucket
def s3_upload(target: str):    
    # primo parametro la variabile, secondo parametro -> default
    bucket = os.getenv("S3_BUCKET_NAME")
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
    region = os.getenv("AWS_REGION","eu-central-1")

    if not all([bucket, access_key, secret_key]):
        return False
    
    s3 = boto3.client("s3", 
                      aws_access_key_id=access_key,
                      aws_secret_access_key=secret_key,
                      region_name=region)
    try: 
        print(f"Upload di {target} su S3 (Bucket: {bucket})...")
        s3.upload_file(target, bucket, target)
        return True
    except Exception as e: 
        print(e+ 'Errore')
        return False



def main():
    args=get_args()
    source=args.source
    if not source: 
        print("You must select  source with -s")
        return

    # get the output file clean name
    output=prepare_output_source(args.output)
    # generate the backup tar file
    tar_res = create_tar_file(source, output)

    if tar_res["status"]:
        file_generato = tar_res["file"]
        if s3_upload(file_generato):
          print(f"Backup of {file_generato} completed and uploaded")
          os.remove(file_generato)
        else:
            print("Failed Upload")
    else:
        print("Compression failed. operation aborted")


if __name__ == '__main__':
    main()