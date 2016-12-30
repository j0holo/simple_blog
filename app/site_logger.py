import logging

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                    level=logging.INFO,
                    filename='blog.log')
logger = logging.getLogger('admin')
logger.setLevel(logging.INFO)
