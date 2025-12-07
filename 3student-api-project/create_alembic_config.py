# create_alembic_config.py - 创建正确编码的 alembic.ini 文件
with open('alembic.ini', 'w', encoding='utf-8') as f:
    f.write("""[alembic]
script_location = migrations
sqlalchemy.url = postgresql+asyncpg://student_user:student_password@localhost:5432/student_db

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""")

print("已创建 UTF-8 编码的 alembic.ini 文件")