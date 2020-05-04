import io
import datetime
from flask import Flask, request, send_file
from .screenshot import Screenshot

app = Flask(__name__)


@app.route('/')
def screenshot():
    url = request.args.get('url', None)
    if url:
        s = Screenshot(url)
        png = s.get_image()
        if png:
            name = "%s.png" % str(datetime.datetime.now().time())
            return send_file(io.BytesIO(png), mimetype='image/png', as_attachment=True, attachment_filename=name)

    return 'Error', 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
