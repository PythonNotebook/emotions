import logging

import pymysqlpool as pymysqlpool
import pymysql.err
from pymysql import cursors


logger = logging.getLogger(__name__)

config = {
    'pool_name': 'pool',
    'host': 'localhost',
    'port': 3306,
    'user': 'emoji',
    'password': 'wLcJSBkrpHAztBxG',
    'database': 'emoji',
    'autocommit': True,
    "max_pool_size": 16,
    "charset": "utf8mb4"
}
pool = pymysqlpool.ConnectionPool(**config)

"""
数据表 image 字段:
    id: 自增，主键，唯一
    image_id: 图片ID，varchar(64)，索引，非空，唯一
    path: 图片相对路径，varchar(255)，非空
    i_character: 对应的角色，varchar(32)，非空，索引
    emotion: 情绪描述，varchar(32)，非空，索引
    is_official: 属于官方图(0)/二次创作(1)，bool，非空，默认为0，索引
"""


def init_db():
    # 初始化数据库
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("CREATE TABLE IF NOT EXISTS image ("
                           "id INT AUTO_INCREMENT PRIMARY KEY,"
                           "image_id VARCHAR(64) UNIQUE NOT NULL,"
                           "path VARCHAR(255) NOT NULL,"
                           "i_character VARCHAR(32) NOT NULL,"
                           "emotion VARCHAR(32) NOT NULL,"
                           "is_official BOOL NOT NULL DEFAULT 0,"
                           "INDEX (i_character),"
                           "INDEX (emotion),"
                           "INDEX (is_official)"
                           ")")

def list_emojis_all(limit: int = 32, offset: int = 0) -> list[dict]:
    with pool.connection() as conn:
        with conn.cursor(cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM image LIMIT %s OFFSET %s", (limit, offset))
            return cursor.fetchall()

def list_emojis_by_character(i_character: str, limit: int = 32, offset: int = 0) -> list[dict]:
    with pool.connection() as conn:
        with conn.cursor(cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM image WHERE i_character = %s LIMIT %s OFFSET %s", (i_character, limit, offset))
            return cursor.fetchall()

def get_image_path_by_id(image_id: str) -> str:
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute("SELECT path FROM image WHERE image_id = %s", (image_id,))
            return cursor.fetchone().get('path')


init_db()
