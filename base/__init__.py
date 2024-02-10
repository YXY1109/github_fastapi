from utils.config import global_config

mysql_db = global_config.get('MYSQL', 'DB')
mysql_host = global_config.get('MYSQL', 'HOST')
mysql_port = global_config.get('MYSQL', 'PORT')
mysql_user = global_config.get('MYSQL', 'USER')
mysql_password = global_config.get('MYSQL', 'PASSWORD')

MILVUS_HOST = global_config.get('MILVUS', 'HOST')
MILVUS_PORT = global_config.get('MILVUS', 'PORT')
MILVUS_COLLECTION = global_config.get('MILVUS', 'COLLECTION')
