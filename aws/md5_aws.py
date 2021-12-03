#!/usr/bin/env python
# coding=utf-8
import os
import re
import subprocess
import fire
import hashlib
import time
import datetime

def aws_md5_check(files_path=str,clean_day=30):
    s3_root_path      =os.environ.get('action_bucket')
    s3_repository_path=os.environ.get('GITHUB_REPOSITORY')
    s3_workflow_path  =os.environ.get('GITHUB_WORKFLOW').replace(' ','')

    def walk_file(file_dir):
        L=[]
        for root, dirs, files in os.walk(file_dir):
            for file in files:
                L.append(os.path.join(root, file))
        return L

    def md5checksum(file_path):
        with open(file_path, "rb") as afile:
            m = hashlib.md5()
            data = afile.read()
            m.update(data)
        return m.hexdigest()
    
    def check_md5(files_path):
        md5_list=[]
        for f in walk_file(files_path):
            md5=md5checksum(f)
            if md5 not in md5_list: 
                md5_list.append(md5) 
        return md5_list

    def walk_and_run(file_path=str):
        if os.path.isdir(file_path):
            for f in walk_file(file_path):
                walk_and_run(file_path=f)
        elif os.path.isfile(file_path):
            aws_md5_lis=check_md5("aws_tmpfile")
            file_md5   =md5checksum(file_path)
            if file_md5 in aws_md5_lis:
                run_command(f"rm {file_path}")
            else:
                run_command(f"aws s3 cp {file_path} {s3_root_path}/{s3_repository_path}/{s3_workflow_path}/")

    def run_command(command=str):
        run=subprocess.Popen(command, shell=True, stdout=subprocess.PIPE ,stderr=subprocess.PIPE)
        stdout, stderr = run.communicate()

    run_command(f"aws s3 mb {s3_root_path}")
    run_command(f"mkdir aws_tmpfile")
    run_command(f"aws s3 cp {s3_root_path}/{s3_repository_path}/{s3_workflow_path} aws_tmpfile --recursive")

    fina_file_sum=0
    for file_path in files_path.strip().split():
        walk_and_run(file_path)
        fina_file_sum+=len(walk_file(file_path))
    return(fina_file_sum)

if __name__ == '__main__':
    fire.Fire(aws_md5_check)
