import os
import datetime
import boto3
from dotenv import load_dotenv
import tarfile
import argparse

load_dotenv()

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
            return True
        except Exception as e:
            print(f"Error during the file compression: {e}")
            return False
    else:
        raise Exception('Invalid source Path. Try again')
  

# function used to upload the backup on S3 bucket
def s3_upload():    
    print('Uploading on S3')


def main():
    args=get_args()
    source=args.source
    # get the output file clean name
    output=prepare_output_source(args.output)
    # generate the backup tar file
    create_tar_file(source, output)

    # creating tar file

   

    # upload on s3..
    s3_upload()


if __name__ == '__main__':
    main()