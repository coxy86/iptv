cd C:\location_of_downloaded_iptv_folder

if not exist venv\ (
    py -m venv venv
)

call "venv\scripts\activate"
python -m pip install --upgrade pip
pip install -U pip
pip install -r requirements.txt
py launch.py
deactivate