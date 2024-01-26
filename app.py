from flask import Flask, render_template, jsonify
from dataAll import utils

app = Flask(__name__)
# Ajax
@app.route('/')
def render():
    return render_template('index.html')


@app.route('/echarts_1')
def get_echarts_1_data():
    data=utils.getTagNum()
    return jsonify({"data": data})


@app.route('/echarts_2')
def get_echarts_2_data():
    data=utils.getAttitudeRatio()
    return jsonify({"data": data})


@app.route('/echarts_3')
def get_echarts_3_data():
    axis,data = utils.getQuestionTimeAndPop()
    return jsonify({"data0":axis,"data1": data['num'].to_list()})


@app.route('/echarts_4')
def get_echarts_4_data():
    year,p,n=utils.getAttitudeWithTime()
    return jsonify({"year": year,"p":p,"n":n})


@app.route('/echarts_5')
def get_echarts_5_data():
    data=utils.getTitleWord()
    return jsonify({"data": data})

@app.route('/echarts_6')
def get_echarts_6_data():
    data=utils.getAttitudeKudo()
    return jsonify({"data": data})

@app.route('/china_map')
def get_china_map_data():
    data=utils.getProvince()
    return jsonify({"data": data})


if __name__ == '__main__':
    app.run(debug=True)