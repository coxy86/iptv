# IPTV M3U8 Builder/Generator

You need to have the following installed or configured on your machine:

- Python 3.12+ (latest)
- Git (latest)
- Google Chrome
- Proper github permission to git@github.com:githubuseraccount/reponame.git

### Prep

1. Create (or update the `.env` file) in the directory where this app is installed/
   extracted.
2. In the `.env` file, set the `FOXTEL_USERNAME` and `FOXTEL_PASSWORD` to the
   appropriate values and save the file.
3. Create repo to github in order to save generated M3U8 playlist.
4. After repo created edit the `scrape.py`and instert your repo address `git@github.com:githubuseraccount/reponame.git`
5. In the `start.bat` file, update/modify the path to the extracted iptv folder location

### Setting up permissions to GitHub repo
- SSH generated key is required laptop connection to GitHub repo. 
- This allows the script to upload the M3U8 files to the requested github repo. 
- See below link for instructions on how to set this up.

https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

Some handy commands for the above to work.

### Generating the SSH key
- ssh-keygen -t ed25519 -C your_email@example.com

### Verifying SSH key should work
- ssh -T git@github.com

### Running the scrape

For windows:

1. Open a powershell window as Administrator.
2. Change directory to the location where this application is installed/extracted.
3. Run `./scripts/windows/start.bat` to start running the scrape.

For macOS: Not tested, may not work.

1. Open a terminal window.
2. Change directory to the location where this application is installed/extracted.
3. Run `./scripts/macos/start.sh` to start running the scrape.
