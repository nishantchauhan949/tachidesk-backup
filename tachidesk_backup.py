from re import findall
from time import sleep

from requests import get

from delete_old_files import main_function
from tachidesk_logger import get_logger

WORK_DIR = '/home/nishant/tachidesk/tachidesk-backups/'


def tachidesk_create_backup():
    logger = get_logger()
    try:
        req = None
        try:
            for i in range(0, 3):
                req = get(url='http://localhost:4567/api/v1/backup/export/file')
                if req.status_code == 200:
                    break
                else:
                    logger.error(f'tachidesk_backup.tachidesk_create_backup() :: {req} Request failed :: {req.content}')
                    sleep(5)
        except Exception as err:
            logger.error(f'tachidesk_backup.tachidesk_create_backup() :: {req} Request failed spectacularly :: {err}')

        content_disposition = req.headers['content-disposition']

        file_name = findall("filename=\"(.+)\"", content_disposition)[0]

        with open(file=f'{WORK_DIR + file_name}', mode='wb+') as tachidesk_backup:
            tachidesk_backup.write(req.content)

        logger.info(
            f'tachidesk_backup.tachidesk_create_backup() :: {file_name} downloaded successfully :: {req.status_code}')

        # calling delete_old_files.main_function
        main_function(path=WORK_DIR, extension='.gz', days='3')

    except Exception as e:
        logger.error(f'tachidesk_backup.tachidesk_create_backup() :: Some unexpected error occurred :: {e}')


if __name__ == '__main__':
    tachidesk_create_backup()