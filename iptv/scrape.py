from git import Repo
from git.exc import NoSuchPathError
from foxtellib import ScrapeManager
import logging
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

REPO_URL = os.environ.get("REPO_URL", "git@github.com:githubuseraccount/reponame.git")
REPO_DIR = os.environ.get("REPO_DIR", "./gitrepo")
CONFIG = {
    'foxtelnow': {
        "channels": [{ 
            "channel_name": "Foxtel One",
            "url": "https://watch.foxtel.com.au/app/#/live/f1s"
        }, {	
            "channel_name": "UKTV",
            "url": "https://watch.foxtel.com.au/app/#/live/ukt"
        }, {
            "channel_name": "Arena",
            "url": "https://watch.foxtel.com.au/app/#/live/arn"
        }, {
            "channel_name": "Crime",
            "url": "https://watch.foxtel.com.au/app/#/live/ioi"
        }, {	
            "channel_name": "Comedy",
            "url": "https://watch.foxtel.com.au/app/#/live/hit"
        }, {
            "channel_name": "Famous HD",
            "url": "https://watch.foxtel.com.au/app/#/live/har"
        }, {	
            "channel_name": "Classics",
            "url": "https://watch.foxtel.com.au/app/#/live/fkc"
        }, {
            "channel_name": "British",
            "url": "https://watch.foxtel.com.au/app/#/live/fsu"
        }, {
            "channel_name": "DocPlay",
            "url": "https://watch.foxtel.com.au/app/#/live/dps"
        }, {
            "channel_name": "Real Life",
            "url": "https://watch.foxtel.com.au/app/#/live/rls"
        }, {
            "channel_name": "TLC",
            "url": "https://watch.foxtel.com.au/app/#/live/dta"
        }, {
            "channel_name": "LifeStyle Food",
            "url": "https://watch.foxtel.com.au/app/#/live/fod"
        }, {
            "channel_name": "LifeStyle Home",
            "url": "https://watch.foxtel.com.au/app/#/live/lho"
        }, {
            "channel_name": "Movies Summer",
            "url": "https://watch.foxtel.com.au/app/#/live/trs"
        }, {
            "channel_name": "Real History",
            "url": "https://watch.foxtel.com.au/app/#/live/hst"
        }, {
            "channel_name": "Discovery Channel",
            "url": "https://watch.foxtel.com.au/app/#/live/dis"
        }, {
            "channel_name": "Real Crime",
            "url": "https://watch.foxtel.com.au/app/#/live/cin"
        }, {
            "channel_name": "Investigation Discovery",
            "url": "https://watch.foxtel.com.au/app/#/live/did"
        }, {    
            "channel_name": "Animal Planet",
            "url": "https://watch.foxtel.com.au/app/#/live/ani"
        }, {
            "channel_name": "Discovery Turbo",
            "url": "https://watch.foxtel.com.au/app/#/live/dit"
        }, {
            "channel_name": "WWE",
            "url": "https://watch.foxtel.com.au/app/#/live/wws"
        }, {
            "channel_name": "BoxSets",
            "url": "https://watch.foxtel.com.au/app/#/live/bxs"
        }, {
            "channel_name": "TVSN",
            "url": "https://watch.foxtel.com.au/app/#/live/tvs"
        }, {
            "channel_name": "GOOD",
            "url": "https://watch.foxtel.com.au/app/#/live/acc"
        }, {
            "channel_name": "Movies Premiere",
            "url": "https://watch.foxtel.com.au/app/#/live/sho"
        }, {
            "channel_name": "Movies Hits",
            "url": "https://watch.foxtel.com.au/app/#/live/mvs"
        }, {
            "channel_name": "Movies Family",
            "url": "https://watch.foxtel.com.au/app/#/live/shf"
        }, {
            "channel_name": "Movies Action",
            "url": "https://watch.foxtel.com.au/app/#/live/sha"
        }, {
            "channel_name": "Movies Comedy",
            "url": "https://watch.foxtel.com.au/app/#/live/shy"
        }, {
            "channel_name": "Movies Romance",
            "url": "https://watch.foxtel.com.au/app/#/live/shd"
        }, {
            "channel_name": "Movies Drama",
            "url": "https://watch.foxtel.com.au/app/#/live/mo6"
        }, {
            "channel_name": "Movies Greats",
            "url": "https://watch.foxtel.com.au/app/#/live/grr"
        }, {
            "channel_name": "LMN",
            "url": "https://watch.foxtel.com.au/app/#/live/lms"
        }, {
            "channel_name": "FOX SPORTS NEWS",
            "url": "https://watch.foxtel.com.au/app/#/live/fsn"
        }, {
            "channel_name": "FOX CRICKET",
            "url": "https://watch.foxtel.com.au/app/#/live/fs1"
        }, {
            "channel_name": "FOX League",
            "url": "https://watch.foxtel.com.au/app/#/live/sp2"
        }, {
            "channel_name": "Fox Sports 503",
            "url": "https://watch.foxtel.com.au/app/#/live/fs3"
        }, {
            "channel_name": "FOX Footy",
            "url": "https://watch.foxtel.com.au/app/#/live/faf"
        }, {
            "channel_name": "Fox Sports 505",
            "url": "https://watch.foxtel.com.au/app/#/live/fsp"
        }, {
            "channel_name": "Fox Sports 506",
            "url": "https://watch.foxtel.com.au/app/#/live/sps"
        }, {
            "channel_name": "Fox Sports More",
            "url": "https://watch.foxtel.com.au/app/#/live/fss"
        }, {
            "channel_name": "ESPN",
            "url": "https://watch.foxtel.com.au/app/#/live/esp"
        }, {
            "channel_name": "ESPN2",
            "url": "https://watch.foxtel.com.au/app/#/live/es2"
        }, {    
            "channel_name": "Sky Racing 1",
            "url": "https://watch.foxtel.com.au/app/#/live/sra"
        }, {
            "channel_name": "Sky Racing 2",
            "url": "https://watch.foxtel.com.au/app/#/live/sr2"
        }, {
            "channel_name": "Sky Racing Thoroughbred Central",
            "url": "https://watch.foxtel.com.au/app/#/live/srw"
        }, {
            "channel_name": "RACING",
            "url": "https://watch.foxtel.com.au/app/#/live/rtv"
        }, {
            "channel_name": "SKY NEWS",
            "url": "https://watch.foxtel.com.au/app/#/live/sky"
        }, {
            "channel_name": "SKY Weather",
            "url": "https://watch.foxtel.com.au/app/#/live/fxw"
        }, {
            "channel_name": "Sky News Extra",
            "url": "https://watch.foxtel.com.au/app/#/live/asp"
        }, {
            "channel_name": "SKY NEWS UK",
            "url": "https://watch.foxtel.com.au/app/#/live/suk"
        }, {
            "channel_name": "FOX News",
            "url": "https://watch.foxtel.com.au/app/#/live/fnc"
        }, {
            "channel_name": "CNN International",
            "url": "https://watch.foxtel.com.au/app/#/live/cnn"
        }, {
            "channel_name": "MSNBC",
            "url": "https://watch.foxtel.com.au/app/#/live/msn"
        }, {
            "channel_name": "CNBC",
            "url": "https://watch.foxtel.com.au/app/#/live/cnb"
        }, {
            "channel_name": "Bloomberg Television",
            "url": "https://watch.foxtel.com.au/app/#/live/blm"
        }, {
            "channel_name": "NHK World",
            "url": "https://watch.foxtel.com.au/app/#/live/nhk"
        }, {
            "channel_name": "Cartoon Network",
            "url": "https://watch.foxtel.com.au/app/#/live/cne"
        }, {
            "channel_name": "Boomerang",
            "url": "https://watch.foxtel.com.au/app/#/live/boo"
        }, {
            "channel_name": "DreamWorks",
            "url": "https://watch.foxtel.com.au/app/#/live/drm"
        }, {
            "channel_name": "MTV Hits",
            "url": "https://watch.foxtel.com.au/app/#/live/tmf"
        }, {
            "channel_name": "Nick Music",
            "url": "https://watch.foxtel.com.au/app/#/live/nmu"
        }, {
            "channel_name": "Club MTV",
            "url": "https://watch.foxtel.com.au/app/#/live/vh1"
        }, {
            "channel_name": "MTV 80s",
            "url": "https://watch.foxtel.com.au/app/#/live/mtc"
        }, {
            "channel_name": "CMT",
            "url": "https://watch.foxtel.com.au/app/#/live/cmt"
        }]
    }
}


def build_file():
    for key in CONFIG:
        with open(f"./gitrepo/{key}.m3u8", "w") as myfile:
            myfile.write(CONFIG[key]['m3u8'])


def build_file_and_git_push():
    '''
    Build m3u8 file and push to github
    :return:
    '''
    try:
        _ = Repo(REPO_DIR).git_dir
    except NoSuchPathError:
        logger.info("Cloning git repo")
        Repo.clone_from(REPO_URL, REPO_DIR)

    repo = Repo(REPO_DIR)
    repo.remotes.origin.pull()

    build_file()

    if repo.index.diff(None, create_patch=True):
        logger.info(f"Files to push to git found")

        try:
            repo.git.add(all=True)
            repo.index.commit(f"Version update {datetime.datetime.now()}")
            origin = repo.remote(name='origin')
            origin.push()
            logger.info(f"Finished pushing files to git")
        except Exception as e:
            logger.error(f"Unable to push change to git: {e}")
            raise(e)


def begin_parse():
    '''
    Fetch urls required to build m3u8
    :return:
    '''
    try:
        scraper = ScrapeManager()
        return scraper.build_m3u8(CONFIG)
    except Exception as e:
        logger.error(e)
        raise(e)


if __name__ == "__main__":
    if begin_parse():
        build_file_and_git_push()
        logger.info("File created and published to git")
    else:
        logger.info("No new file published to git")
