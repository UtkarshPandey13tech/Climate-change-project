from flask import Flask, request, jsonify, send_from_directory
import numpy as np
import os

app = Flask(__name__)


@app.route('/')
def serve_html():
    return send_from_directory(os.getcwd(), 'climate.html')


@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        dates = np.array(data['dates'])
        temps = np.array(data['temps'])
        predict_date = data['predict_date']


        def date_to_num(d):
            return np.datetime64(d).astype('datetime64[D]').astype(int)

        xs = np.array([date_to_num(d) for d in dates])
        ys = temps


        m, b = np.polyfit(xs, ys, 1)
        pred_x = date_to_num(predict_date)
        pred_y = m * pred_x + b

        return jsonify({"prediction": float(pred_y)})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
