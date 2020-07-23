#!/usr/bin/python
# -*- coding: utf-8 -*-
import io
import os
import sys
import subprocess
import codecs
import json
import requests

requests.packages.urllib3.disable_warnings() 


located_etcds = []





def check_etcd_keys(pass_in):
    print("Attempting to grab etcd keys  from:"+str(len(pass_in))+" ")  
    
    print(pass_in)
    try:
        url = 'http://{}/v2/keys/?recursive=true'.format(pass_in.strip())
        print(url)
        response = requests.get(url,verify=False,timeout=3)
        if response.text:
           print(response.text)
           local_info = {}
           local_info['host'] = pass_in
           local_info['etcd_keys'] = response.text
           located_etcds.append(local_info)
    except Exception as ohshits:
        pass

    
if __name__ == "__main__":
   etcdList = [line.rstrip('\n') for line in open('targs.txt')]
   print(etcdList)
   
   for host in etcdList:
       check_etcd_keys(host)
   for found in located_etcds:
       if found:
          print(type(found))
          r = json.dumps(found)
          loaded_r = json.loads(r)
          split_host = loaded_r['host'].split(":")
          etcd_keys = loaded_r['etcd_keys']
          
          print("etcd FOUND :"+split_host[0])
          
          etcd_outs = open("etcds/"+split_host[0]+".json","w")
          etcd_outs.write(json.dumps(etcd_keys))
          etcd_outs.close()
          
