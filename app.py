import os
from flask import Flask, render_template
# from dotenv import load_dotenv
from flask import import_blueprint
from graph import graph_blueprint
from errors import error_pages

# 加载环境变量
# load_dotenv()

# 创建 Flask 应用程序实例
app = Flask(__name__)

# 配置应用程序
app.config.from_object('config.Config')

# 注册蓝图
app.register_blueprint(import_blueprint, url_prefix='/import')
app.register_blueprint(graph_blueprint, url_prefix='/graph')
app.register_blueprint(error_pages)

# 主页路由
@app.route('/')
def index():
    return render_template('index.html')

# 运行应用程序
if __name__ == '__main__':
    app.run(debug=True)