from flask import Blueprint, render_template, request

error_pages = Blueprint("error_pages", __name__, template_folder="templates")


@error_pages.app_errorhandler(404)
def page_not_found(error):
    return render_template("errors/404.html"), 404


@error_pages.app_errorhandler(500)
def internal_server_error(error):
    return render_template("errors/500.html"), 500


@error_pages.route("/report_error", methods=["GET", "POST"])
def report_error():
    if request.method == "POST":
        # 处理报告错误表单的逻辑
        email = request.form.get("email")
        message = request.form.get("message")
        # 执行相应的操作,例如发送电子邮件或记录错误信息
        # ...
        return render_template("errors/report_success.html")
    return render_template("errors/report_error.html")
