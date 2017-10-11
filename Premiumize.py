#!/usr/bin/python

import glob
import json
import requests
import os
import urllib

default_config = {}
default_config["directories"] = {}
default_config["directories"]["torrents"] = "."
default_config["directories"]["magnets"] = "."
default_config["directories"]["nzbs"] = "."
default_config["directories"]["in_progress_hash_cache"] = "."
default_config["directories"]["complete_downloads"]="."

default_config["file_types"] = {}
default_config["file_types"]["torrents"] = "*.torrent"
default_config["file_types"]["magnets"] = "*.magnet"
default_config["file_types"]["nzbs"] = "*.nzb"

default_config["premiumize"] = {}
default_config["premiumize"]["customer_id"] = "<change this to your premiumize customer_id>"
default_config["premiumize"]["pin"] = "<change this to your premiumize PIN>"

try:
  with open('config', 'r') as config_file:
    config=json.load(config_file)

except IOError:
  with open('config', 'w') as config_file:
    json.dump(default_config, config_file, sort_keys = True, indent = 4)
    config = default_config
    print "Default config created. Please check values in 'config' file"

for filename in glob.glob(os.path.join(config["directories"]["torrents"], config["file_types"]["torrents"])):
  print(filename)
  torrent = {"src": open(filename, "rb")}
  request_pars = {"customer_id": config["premiumize"]["customer_id"], "pin": config["premiumize"]["pin"], "type": "torrent"}
  request = requests.post("https://www.premiumize.me/api/transfer/create", data=request_pars, files=torrent)
  print(request.text)

for filename in glob.glob(os.path.join(config["directories"]["magnets"], config["file_types"]["magnets"])):
  print(filename)
  with open(filename, 'r') as magnet_file:
    magnet_link=magnet_file.read()
    request_pars = {"customer_id": config["premiumize"]["customer_id"], "pin": config["premiumize"]["pin"], "type": "torrent", "src": magnet_link}
    request = requests.post("https://www.premiumize.me/api/transfer/create", data=request_pars)
    print(request.text)

for filename in glob.glob(os.path.join(config["directories"]["nzbs"], config["file_types"]["nzbs"])):
  print(filename)
# NZB processing may be different at Premiumize's end
#  nzb = {"src": open(filename, "rb")}
#  request_pars = {"customer_id": config["premiumize"]["customer_id"], "pin": config["premiumize"]["pin"], "type": "nzb"}
#  request = requests.post("https://www.premiumize.me/api/transfer/create", data=request_pars, files=torrent)
#  print(request.text)

