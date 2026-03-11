import logging
import os
import shlex
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv


def make_backup():
    load_dotenv()

    db_host = os.getenv('DB_HOST')
    db_user = os.getenv('DB_USER')
    db_password = os.getenv('DB_PASSWORD')
    days = int(os.getenv('DAYS'))
    backup_path = Path('backup')

    logging.info(f'host={db_host} - user={db_user} - pwd={db_password} - days={days}')

    now = datetime.now()
    before = (now - timedelta(days=days)).strftime('%Y%m%d')
    now_str = now.strftime('%Y%m%d')

    db_names = [line.strip() for line in (backup_path / 'names').read_text().splitlines() if line.strip()]
    logging.info(f'count_db={len(db_names)}')

    for db in db_names:
        logging.info(f'backup {db}')
        
        sql_file = backup_path / f'{db}{now_str}.sql'
        tar_file = backup_path / f'{db}{now_str}.tar.gz'
        old_tar = backup_path / f'{db}{before}.tar.gz'

        dumpcmd = shlex.join([
            'mysqldump',
            '-h', db_host,
            '-u', db_user,
            f'-p{db_password}',
            '--single-transaction',
            '--quick',
            '--skip-lock-tables',
            '--skip-add-locks',
            '--compress',
            db
        ]) + f' > {sql_file}'
        
        logging.info(dumpcmd)
        subprocess.run(dumpcmd, shell=True, check=True)

        tar_cmd = ['tar', '-zcf', str(tar_file), str(sql_file)]
        logging.info(' '.join(tar_cmd))
        subprocess.run(tar_cmd, check=True)

        sql_file.unlink()
        
        if old_tar.exists():
            logging.info(f'removing {old_tar}')
            old_tar.unlink()
            
