from app import create_app
app = create_app()

#
#  set FLASK_ENV=development  开启调试模式
#  flask run    运行
if __name__ == '__main__':
    app.run(debug=True)
