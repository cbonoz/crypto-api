from flask import Flask
import coin_data as cd

app = Flask(__name__)

@app.route('/coins')
def coins():
    coin_map = cd.get_coin_map()
    return str(coin_map)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8001)
