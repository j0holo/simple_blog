import logging

logging.basicConfig(format='%(asctime)s %(message)s',
                    level=logging.INFO,
                    filename='blog.log')
logger = logging.getLogger('admin')
logger.setLevel(logging.INFO)
