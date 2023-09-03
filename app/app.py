import logging

from flask import Flask
from app.task import make_backup

app = Flask(__name__)

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


@app.route('/backup', methods=['GET'])
def backup():
    make_backup()
    return "Backup finished"


if __name__ == '__main__':
    app.run()
