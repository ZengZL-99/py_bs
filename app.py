from app import create_app
# from gevent import monkey
# from gevent.pywsgi import WSGIServer
# from multiprocessing import cpu_count, Process

app = create_app()
# monkey.patch_all()
#
#
# def run(MULTI_PROCESS):
#     if MULTI_PROCESS == False:
#         WSGIServer(('0.0.0.0', 8080), app).serve_forever()
#     else:
#         mulserver = WSGIServer(('0.0.0.0', 8080), app)
#         mulserver.start()
#
#         def server_forever():
#             mulserver.start_accepting()
#             mulserver._stop_event.wait()
#
#         for i in range(cpu_count()):
#             p = Process(target=server_forever)
#             p.start()


#  set FLASK_ENV=development  开启调试模式
#  flask run    运行

if __name__ == '__main__':
    # run(True)
    app.run()
    # 单进程 + 协程
    # run(False)
    # 多进程 + 协程
    # run(True)
