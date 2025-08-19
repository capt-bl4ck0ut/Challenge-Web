from flask import Flask, request, render_template, url_for, redirect
from urllib.request import urlopen
import base64, os

app = Flask(__name__)
app.secret_key = os.urandom(32)

mini_database = []


@app.route('/')
def index():
    return redirect(url_for('view'))


@app.route('/request')
def url_request():
    url = request.args.get('url', '').lower()
    title = request.args.get('title', '')
    if url == '' or url.startswith("file://") or "flag" in url or title == '':
        return render_template('request.html')

    try:
        data = urlopen(url).read()
        mini_database.append({title: base64.b64encode(data).decode('utf-8')})
        return redirect(url_for('view'))
    except:
        return render_template("request.html")


@app.route('/view')
def view():
    return render_template('view.html', img_list=mini_database)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        title = request.form.get('title', '')
        if not f or title == '':
            return render_template('upload.html')

        en_data = base64.b64encode(f.read()).decode('utf-8')
        mini_database.append({title: en_data})
        return redirect(url_for('view'))
    else:
        return render_template('upload.html')


if __name__ == "__main__":
    img_list = [
        {'초록색 선글라스': "static/assetA#03.jpg"}, 
        {'분홍색 선글라스': "static/assetB#03.jpg"},
        {'보라색 선글라스': "static/assetC#03.jpg"}, 
        {'파란색 선글라스': "static/assetD#03.jpg"}
    ]
    for img in img_list:
        for k, v in img.items():
            data = open(v, 'rb').read()
            mini_database.append({k: base64.b64encode(data).decode('utf-8')})
    
    app.run(host="0.0.0.0", port=80, debug=False)

