from flask import Flask, request, render_template_string
import re
import unicodedata

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def index():
    message = ""
    if request.method == "POST":
        message = request.form["message"]
        if re.search("[a-zA-Z]", message):
            message = "한글을 사용합시다!"
        message = unicodedata.normalize("NFKC", message)    # for normalize Windows and Mac Hangul implementation
    return render_template_string('''
        <form method="POST">
            Message: <input type="text" name="message">
            <input type="submit">
        </form>
        <p>Repeat your message:</p>
        <div>%s</div>
    ''' % message)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
