import sys

from flask import Flask, render_template, request, redirect, flash, url_for
from main import get_code

app = Flask(__name__)
app.secret_key = "Kakoy-to secret key"


@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        input_code = request.args.get('input_code').replace("\r", "")
        output_code = request.args.get('output_code')
        return render_template('index.html', input_code=input_code, output_code=output_code)
    elif request.method == 'POST':
        input_code = request.form.get("input_code")
        if input_code == "":
            flash("Код не был введен. Пожалуйста, введите код.")
            return redirect(url_for("main_page", input_code=input_code))
        else:
            with open("test.cpp", "w", encoding="UTF-8") as file:
                file.write(input_code)

            output_code = get_code()
            if isinstance(output_code, tuple):
                for error in output_code[1]:
                    flash(str(error))
            return redirect(url_for("main_page", input_code=input_code, output_code=output_code, download="ok"))


if __name__ == '__main__':
    app.run(debug=True)
