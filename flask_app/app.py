import sys

from flask import Flask, render_template, request, redirect, flash, url_for

app = Flask(__name__)
app.secret_key = "Sachin"


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        input_code = request.args.get('input_code')
        output_code = request.args.get('output_code')
        return render_template('index.html', input_code=input_code, output_code=output_code)
    elif request.method == 'POST':
        input_code = request.form.get("input_code")
        if input_code == "":
            flash("Код не был введен. Пожалуйста, введите код, сука")
            return redirect(url_for("main_page", input_code=input_code))
        else:
            # TODO: Сюда воткнуть код с обработкой кода)))
            output_code = ""
            return redirect(url_for("main_page", input_code=input_code, output_code=output_code))


if __name__ == '__main__':
    app.run(debug=True)
