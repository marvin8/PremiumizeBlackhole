#!/usr/bin/python

import glob
import humanize
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

# Read config file
try:
  with open('config', 'r') as config_file:
    config=json.load(config_file)

# If config file can't be read create a new config file with default values
except IOError:
  with open('config', 'w') as config_file:
    json.dump(default_config, config_file, sort_keys = True, indent = 4)
    config = default_config
    print "Default config created. Please check values in 'config' file"


# Load file with Premiumize ID cache
try: 
  with open(config["directories"]["in_progress_hash_cache"] + 'premiumize_id_cache', 'r') as id_cache_file:
    id_cache=json.load(id_cache_file)
    print("ID Cache loaded:")
    print(json.dumps(id_cache, sort_keys = True, indent = 4))

except:
  id_cache={}


print('')
print('Processing .torrent files')
for filename in glob.glob(os.path.join(config["directories"]["torrents"], config["file_types"]["torrents"])):
  torrent = {"src": open(filename, "rb")}
  request_pars = {"customer_id": config["premiumize"]["customer_id"], "pin": config["premiumize"]["pin"], "type": "torrent"}
  request = requests.post("https://www.premiumize.me/api/transfer/create", data=request_pars, files=torrent)
  response=request.json()
  id_cache[response["id"]] =  response["name"]
  print(response["status"] + ": " + response["name"])


print('')
print('Processing .magnet files')
for filename in glob.glob(os.path.join(config["directories"]["magnets"], config["file_types"]["magnets"])):
  with open(filename, 'r') as magnet_file:
    magnet_link=magnet_file.read()
    request_pars = {"customer_id": config["premiumize"]["customer_id"], "pin": config["premiumize"]["pin"], "type": "torrent", "src": magnet_link}
    request = requests.post("https://www.premiumize.me/api/transfer/create", data=request_pars)
    response=request.json()
    id_cache[response["id"]] =  response["name"]
    print(response["status"] + ": " + response["name"])


print('')
print('Processing .nzb files')
for filename in glob.glob(os.path.join(config["directories"]["nzbs"], config["file_types"]["nzbs"])):
  print("NZB files not yet integrated: " + filename)
# NZB processing may be different at Premiumize's end
#  nzb = {"src": open(filename, "rb")}
#  request_pars = {"customer_id": config["premiumize"]["customer_id"], "pin": config["premiumize"]["pin"], "type": "nzb"}
#  request = requests.post("https://www.premiumize.me/api/transfer/create", data=request_pars, files=torrent)
#  print(request.text)


# Check hashes
if len(id_cache) > 0:
  print("")
  print("Check download status")
  hashes_string = ""
  for cache_id, name in id_cache.iteritems():
    hashes_string = hashes_string + "&hashes[]=" + cache_id

  response = requests.get("https://www.premiumize.me/api/torrent/checkhashes?customer_id=" + config["premiumize"]["customer_id"] + "&pin=" + config["premiumize"]["pin"] + hashes_string)
  for hash_id, array in response.json()["hashes"].iteritems():
    print(id_cache[hash_id] + ": " + array["status"])

 
# Check status of each download in Premiumize ID cache
  for cache_id, name in id_cache.iteritems():
    request_pars = {"customer_id": config["premiumize"]["customer_id"], "pin": config["premiumize"]["pin"], "hash": cache_id}
    response = requests.post("https://www.premiumize.me/api/torrent/browse", data=request_pars)
    print("")
    print("Download info for: " + name)
#    print(json.dumps(response.json(), sort_keys = True, indent = 4))
    if response.json()["status"] == "error":
      print("Download still IN PROGRESS")
    else:
      print("Size: " + humanize.naturalsize(response.json()["size"]))
      print(response.json()["zip"])


# Write Premiumize ID cache to file for persistence
  with open(config["directories"]["in_progress_hash_cache"] + 'premiumize_id_cache', 'w') as id_cache_file:
    json.dump(id_cache, id_cache_file, sort_keys = True, indent = 4)

