from flask import Flask, jsonify
import requests
import time
from collections import deque

app = Flask(__name__)
s = deque(maxlen=10)

@app.route('/numbers/<string:nid>', methods=['GET'])
def get_numbers(nid):
    e = {'f': '/fibo', 'e': '/even'}
    if nid not in e:
        return jsonify({"error": "Invalid number ID"}), 400

    start = time.time()
    try:
        r = requests.get(f"http://20.244.56.144/evaluation-service{e[nid]}", timeout=0.5)
        r.raise_for_status()
        nums = r.json().get('numbers', [])
    except:
        return jsonify({"error": "Failed to fetch numbers"}), 500

    for n in nums:
        if n not in s:
            s.append(n)

    avg = round(sum(s) / len(s), 2) if s else 0.0
    if time.time() - start > 0.5:
        return jsonify({"error": "Response time exceeded limit"}), 500

    return jsonify({
        "windowPrevState": list(s),
        "windowCurrState": list(s),
        "numbers": nums,
        "avg": avg
    })

if __name__ == '__main__':
    app.run(port=9876)
