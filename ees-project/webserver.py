from flask import Flask

def webserver():
    server = Flask(__name__)

    @server.route('/')
    def run():
        return 'Running!'
    server.run(host="192.168.1.1", port="3402", debug=False)

webserver()
