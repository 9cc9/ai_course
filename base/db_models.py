# models.py
from peewee import *
import atexit


# 创建数据库连接
db = MySQLDatabase('spring_boot_demo', user='root', password='Gmy900925', host='localhost')

# 定义模型
class AiContext(Model):
    id = AutoField()  # 主键使用 AutoField
    text = TextField()

    class Meta:
        database = db
        table_name = 'ai_context'  # 映射表名

# 确保数据库连接
db.connect()

# 注册程序退出时关闭数据库连接的钩子
atexit.register(lambda: db.close())
