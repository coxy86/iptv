IPTV M3U8 generator instructions

Requirements

Hardware
Windows laptop 10/11 both tested and working

Software
Git – latest
Python – latest
Google Chrome browser – latest. If running windows 10, have had issues with newer versions of chrome.
Git hub repository

SSH key connected to laptop. This allows the script to upload the M3U8 files to the requested github repo, please see below link for instructions on how to set this up
https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Some handy commands for the above to work.
Generating the SSH key
ssh-keygen -t ed25519 -C your_email@example.com

Verifying SSH key should work
ssh -T git@github.com

Updates to files needed below, only text in bold and underlined needs updating to personal details

'env'
FOXTEL_USERNAME=foxtelemailaddresshere
FOXTEL_PASSWORD=foxtelpasswordhere

'scrape.py'
REPO_URL = os.environ.get("REPO_URL", 'git@github.com:githubuseraccount/reponame.git')

'start.bat'
cd C:\location_of_downloaded_iptv_folder

Running the process once the above has been completed.
For windows:

1. Open a powershell window as Administrator.
2. Change directory to the location where this application is downloaded/extracted.
3. Run `./scripts/windows/start.bat` to start running the scrape.