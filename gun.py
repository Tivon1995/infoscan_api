import multiprocessing

bind = '0.0.0.0:5000'
workers = multiprocessing.cpu_count() * 2 + 1
threads = 1 
backlog = 2048
worker_class = "gevent"
worker_connections = 9
daemon = False
debug = True

proc_name = 'app'
pidfile = './app.pid' #gunicorn进程id，kill掉该文件的id，gunicorn就停止
loglevel = 'debug'
logfile = './debug.log' #debug日志
errorlog = './error.log' #错误信息日志
timeout = 3600
keepalive = 5
