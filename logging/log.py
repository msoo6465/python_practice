import logging
import os

logger = logging.getLogger()

logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)

os.makedirs('log',exist_ok=True)

file_handler = logging.FileHandler('./log/my.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

for i in range(10):
	logger.info(f'{i}/10 파일 완료')