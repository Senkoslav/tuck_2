from flask import Flask
import redis

app = Flask(__name__)

cache = redis.Redis(host='redis', port=6379, decode_responses=True)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1

@app.route('/count')
def count():
    count = get_hit_count()
    return f'Количество посещений: {count}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
