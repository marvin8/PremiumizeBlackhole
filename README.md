# PremiumizeBlackhole

This project is currently in the very early stages of conception.   
Currently the idea is to allow interaction with the Premiumize service, .nzb, .torrent, and .magnet files to automate downloading of content.

To use this program have your software save .nzb, .torrent, and/or .magnet files into directories. Change the config file for this project to point to those directories and then run the Premiumize.py programm.   
Premiumize.py will then look for files in the directories listed in the config and add them to the Premiumize download manager. Any files that have been successfully added to Premiumize will then have the corresponding .nzb, .torrent, or .magnet file removed to prevent repeated uploads.  
The programm will also check the progress of the downloads at Premiumize and list the direct download links for any files that have finished downloading at Premiumize.

Premiumize will then also store a file of files added to the Premiumize download manager in the "in_progress_hash_cache" directory so it can check if downloads at Premiumize are finished at the next run of the program.

Got to [www.premiumize.me](https://www.premiumize.me/ref/682309937) for information about the Premiumize service.  
(The link above is a referral link that will give me 15 days of free service with Premiumize for anyone that signs up for a paid account with Premiumize after following my link. The person paying for a Premiumize account will receive a 15 day bonus on top of any paid for period)

# Usage

Add .magnet, .torrent and/or .nzb files to Premiumize download manager by running: `.\Premiumize upload`

Check status of files at Premiumize download manager by running: `.\Premiumize check`

Download files finished downloading at Premiumize by running: `.\Premiumize download`
