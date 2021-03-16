from flask import Flask, jsonify, request
app = Flask(__name__)

STATUS = 'Done'


@app.route('/change')
def change():
    global STATUS
    STATUS = request.args.get('status')
    return STATUS


@app.route('/api/status')
def status():
    return jsonify({'status': STATUS})


@app.route('/api/start')
def start():
    global STATUS
    STATUS = 'Done'
    return 'ok'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
