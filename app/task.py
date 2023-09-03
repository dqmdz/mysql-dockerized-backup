import os
import time
import logging

from dotenv import load_dotenv
from datetime import datetime, timedelta

def make_backup():

    load_dotenv()

    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    days = int(os.getenv('DAYS'))
    backup_path = 'backup/'

    logging.info(f'host={db_host} - user={db_user} - pwd={db_password} - days={days}')

    now = time.strftime('%Y%m%d')

    today = datetime.now()
    delta = timedelta(days=days)
    previous = today - delta
    before = previous.strftime('%Y%m%d')

    file = open("backup/names", 'r')
    count_db = len(file.readlines())
    logging.info(f'count_db={count_db}')
    file.close()
    p = 1
    file = open("backup/names", 'r')
    while p <= count_db:
        db = file.readline()[:-1]
        logging.info(f'backup {db}')
        dumpcmd = "mysqldump -h " + db_host + " -u " + db_user + " -p" + db_password + " " + db + " > " + backup_path + db + now + ".sql"
        logging.info(dumpcmd)
        os.system(dumpcmd)
        dumpcmd = "tar -zcf " + backup_path + db + now + ".tar.gz " + backup_path + db + now + ".sql"
        logging.info(dumpcmd)
        os.system(dumpcmd)
        dumpcmd = "rm " + backup_path + db + now + ".sql"
        logging.info(dumpcmd)
        os.system(dumpcmd)
        dumpcmd = "rm " + backup_path + db + before + ".tar.gz"
        logging.info(dumpcmd)
        os.system(dumpcmd)
    
        p = p + 1
    file.close()