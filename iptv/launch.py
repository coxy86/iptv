import logging
import os
import subprocess
from proxy.common import utils
from sys import platform
from dotenv import load_dotenv
from scrape import begin_parse, build_file_and_git_push

load_dotenv()

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='%Y-%m-%d:%H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

if __name__ == "__main__":
    proc = None
    try:
        chrome = None
        chrome_path = os.environ["CHROME_PATH"]

        logger.info(f"Running on {platform} with {chrome_path}")
        if platform == "darwin":
            # os.environ["PATH"] = f"{os.environ['PATH']}:{chrome_path}"
            # logger.info(f"PATH: {os.environ["PATH"]}")
            chrome = f"\"Google Chrome\""
        elif platform == "win32":
            os.environ["PATH"] = f"{os.environ['PATH']};{chrome_path}"
            chrome = "chrome.exe"
        else:
            logger.error(f"{platform} is currently unsupported")

        proxy_port = str(utils.get_available_port())
        os.environ["CHROME_PORT"] = proxy_port

        cmd = f"{chrome} --remote-debugging-port={proxy_port} --hide-crash-restore-bubble --user-data-dir=./ChromeProfile"
        logger.info(f"Running {cmd}")
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,)
        logger.info(
            f'Launcher has been started at port {proxy_port}.  Begin parsing.')

        if begin_parse():
            build_file_and_git_push()
            logger.info("File created and published to git")
        else:
            logger.info("No new file published to git")

    except KeyError as e:
        logger.error(f"KeyError: {e}.  Please define missing key.")
    except KeyboardInterrupt:
        logger.info("Launcher cancelled")
    except Exception as e:
        logger.error(f"Error: {type(e)} {e}")
    finally:
        if proc:
            proc.terminate()
            proc.wait()
