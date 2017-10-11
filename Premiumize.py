#!/usr/bin/python

import json
import urllib

default_config = {}
default_config["directories"] = {}
default_config["directories"]["torrents"] = "."
default_config["directories"]["magnets"] = "."
default_config["directories"]["nzbs"] = "."
default_config["directories"]["in_progress_hash_cache"] = "."
default_config["directories"]["complete_downloads"]="."

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


print config["premiumize"]["customer_id"]
