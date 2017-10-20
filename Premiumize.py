#!/usr/bin/python

import glob
import json
import requests
import os
import sys
import urllib
import zipfile

# Check for command line options
command = ""
if len(sys.argv) != 2:
  print "Please specifiy what you'd like " + sys.argv[0] + " to do"
  print "Valid options are, 'upload', 'check', and 'download'"
  exit()
else:
  command = sys.argv[1]



class Premiumize:

  def __init__(self, customer_id, pin):
    self.customer_id = customer_id
    self.pin = pin


  def loadIdCache(self, id_cache_file_name):
    try: 
      with open(id_cache_file_name, 'r') as id_cache_file:
        self.id_cache=json.load(id_cache_file)
    except:
        self.id_cache={}


  def saveIdCache(self, id_cache_name):
    with open(id_cache_name, 'w') as id_cache_file:
      json.dump(self.id_cache, id_cache_file, sort_keys = True, indent = 4)

    
  def add2DownloadManager(self, fileName, fileType):
    _response = {}
    if fileType == "magnet":
      with open(fileName, 'r') as _magnet_file:
        _magnet_link = _magnet_file.read()
      _request_pars = {"customer_id": self.customer_id, "pin": self.pin, "type": "torrent", "src": _magnet_link}
      _response = requests.post("https://www.premiumize.me/api/transfer/create", data=_request_pars)
    else:
      _request_pars = {"customer_id": self.customer_id, "pin": self.pin, "type": fileType}
      _filePar = {"src": open(fileName, "rb")}
      _response = requests.post("https://www.premiumize.me/api/transfer/create", data=_request_pars, files=_filePar)

    _responseArr = _response.json()
    self.id_cache[_responseArr["id"]] = _responseArr["name"]
    _addMsg = " "
    if _responseArr["status"] == "success":
      os.remove(fileName)
    _addMsg = " - " + fileType + " file removed"

    print("Premiumize - add to download manager: " + _responseArr["status"] + _addMsg +" - " + _responseArr["name"])


  def checkProgress(self):
    for cache_id, name in self.id_cache.iteritems():
      request_pars = {"customer_id": self.customer_id, "pin": self.pin, "hash": cache_id}
      response = requests.post("https://www.premiumize.me/api/torrent/browse", data=request_pars)
      print("")
      print("Download info for: " + name)
      if response.json()["status"] == "error":
        print("Download still IN PROGRESS")
      else:
        print("Size: " + format(response.json()["size"], ","))
        print(response.json()["zip"])


  def downloadCompleted(self, path):
    request_pars = {"customer_id": self.customer_id, "pin": self.pin}
    response = requests.post("https://www.premiumize.me/api/transfer/clearfinished", data=request_pars)
    for cache_id, name in self.id_cache.items():
      request_pars = {"customer_id": self.customer_id, "pin": self.pin, "hash": cache_id}
      response = requests.post("https://www.premiumize.me/api/torrent/browse", data=request_pars)
      if response.json()["status"] == "error":
        print(name + " - Download still IN PROGRESS")
      else:
        print("Donwloading: " + name)
        urllib.urlretrieve (response.json()["zip"], path + name + ".zip")
        with zipfile.ZipFile(path + name + ".zip", "r") as zipref:
          zipref.extractall(path + name)
        os.remove(path + name + ".zip")
        del id_cache[cache_id]

    

# Read config file
try:
  with open('config', 'r') as config_file:
    config=json.load(config_file)

# If config file can't be read create a new config file with default values
except IOError:
  sys.exit("Config file not found!")


premiumize = Premiumize(config["premiumize"]["customer_id"], config["premiumize"]["pin"])
premiumize.loadIdCache(config["directories"]["in_progress_hash_cache"] + 'premiumize_id_cache')

if command == "upload":
  print("")
  print("Uploading reference files")
  for filename in glob.glob(os.path.join(config["directories"]["torrents"], config["file_types"]["torrents"])):
    premiumize.add2DownloadManager(filename, "torrent")
  for filename in glob.glob(os.path.join(config["directories"]["magnets"], config["file_types"]["magnets"])):
    premiumize.add2DownloadManager(filename, "magnet")
  for filename in glob.glob(os.path.join(config["directories"]["nzbs"], config["file_types"]["nzbs"])):
    premiumize.add2DownloadManager(filename, "nzb")

elif command == "check":
  premiumize.checkProgress()

elif command == "download":
  premiumize.downloadCompleted(config["directories"]["complete_downloads"])      

premiumize.saveIdCache(config["directories"]["in_progress_hash_cache"] + 'premiumize_id_cache')
