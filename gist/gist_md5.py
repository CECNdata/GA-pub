#!/usr/bin/env python
# coding=utf-8

import fire
import hashlib
import os,sys
from pprint import pprint

def md5(file_path):
    m = hashlib.md5()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(4096)
            if not data:
                break
            m.update(data)
    return m.hexdigest()


def walk_path_parser(path):
    file_list=[]
    if os.path.isdir(path):
        for filename in os.listdir(path):
            file_list.extend(walk_path_parser(f"{path}/{filename}"))
    elif os.path.isfile(path):
        file_list.extend([[os.path.basename(path),path,md5(path)]])
    return(file_list)


def gist_md5(file_dir="./download",file_md5="./md5.txt"):
    final_file_list=[]
    for f in file_dir.strip().split():
        final_file_list.extend(walk_path_parser(f))
    #pprint(final_file_list)

    content=[]
    if os.path.exists(file_md5):
        with open(file_md5) as f:
            content = f.readlines()
        content = [x.strip() for x in content]
    init_len=len(content)
    
    for final in final_file_list:
        if final[2] in content:
            #print(final[1])
            os.remove(final[1])
        else:
            content=[final[2]]+content

    final_len=len(content)
    print(final_len-init_len)
    content=content[:1000]
    #pprint(content)
    fo = open(file_md5, "w")
    fo.write("\n".join(content))
    fo.close()

if __name__ == '__main__':
  fire.Fire(gist_md5)
