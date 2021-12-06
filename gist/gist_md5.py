#!/usr/bin/env python
# coding=utf-8


import fire
import hashlib
import os,sys
import httpx

def walk_path_parser(path,date_regex_compile,clean,if_filter,pdp_msg,skype_ids):
    if os.path.isdir(path):
        print(f"file_dir: {path}")
        for filename in os.listdir(path):
            walk_path_parser(path=f"{path}/{filename}",date_regex_compile=date_regex_compile,if_filter=if_filter,clean=clean,p
dp_msg=pdp_msg,skype_ids=skype_ids)
    elif os.path.isfile(path):
        pdp_msg_list=pdp_msg.split('|--|')
        print(f"file_path: {path}")
        file_name=path.split("/")[-1]
        mappings_all=mapping2_xlsx2dict(sheet_path="mapping.xlsx",sheet_name="main",file_name=file_name)
        for filename in mappings_all:
            if filename in os.path.basename(path):
                print("*"*50)
                print(f"[html2sqlite]:{file_name}")
                if_html2text=False if "_noh" in file_name else True
                html2sqlite(html_path=path,mapping=mappings_all[filename],date_regex_compile=date_regex_compile,clean=clean,if_filter=if_filter,pdp_msg_list=pdp_msg_list,skype_ids=skype_ids,if_html2text=if_html2text)
                print()
                print()
                print("*"*50)
                print("*"*50)
                return()
    else:
        print(f"{path} is not exist")


def walk_path_parser()
        if os.path.isdir(path):
            for filename in os.listdir(path):

def gist_md5(file_dir="",file_md5="./md5.txt",gist_url=None):
    """
    计算文件的md5值
    """
    if gist_url!=None:


    def md5(file_path):
        """
        计算文件的md5值
        """
        m = hashlib.md5()
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(4096)
                if not data:
                    break
                m.update(data)
        return m.hexdigest()

    fire.Fire(md5)

if __name__ == '__main__':
  fire.Fire(gist_md5)

