# M3U8 Builder

You need to have the following installed or configured on your machine:

- python 3.12+
- Google Chrome
- Proper github permission to git@github.com:coxy86/melbtv.git

### Prep

1. Create (or update the `.env` file) in the directory where this app is installed/
   extracted.
2. Check the path of the Google Chrome binary. On macOs, the binary is
   called `Google Chrome` while in windows, it is called `chrome.exe`.
   Update the `.env` file and set the value of `CHROME_PATH` to the path of the
   Google Chrome binary. Save your changes.
3. In the `.env` file, set the `FOXTEL_USERNAME` and `FOXTEL_PASSWORD` to the
   appropriate values and save the file.

### Running the scrape

For windows:

1. Open a powershell window as Administrator.
2. Change directory to the location where this application is installed/extracted.
3. Run `./scripts/windows/start.bat` to start running the scrape.

For macOS:

1. Open a terminal window.
2. Change directory to the location where this application is installed/extracted.
3. Run `./scripts/macos/start.sh` to start running the scrape.
