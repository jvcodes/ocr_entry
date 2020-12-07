from flask import Flask, render_template, request
import pandas as pd
import os
import json 
import pre_process_cut_Image as pc
app = Flask(__name__)

def insert_at(path, key, value, new = False):
    with open(path) as fr:
        spoint = json.load(fr)
    spoint[key] = value
    if new:
        spoint['pos'] = 0
    with open(path, mode='w') as f:
        f.write(json.dumps(spoint))

@app.route('/fpath', methods=['POST'])
def change_path():
    print(dict(request.form))
    path = request.form['text']
    pc.convert_img(path)
    pc.cut_img(path)
    insert_at(point_file, 'path',path , True)
    return render_template('success.html')

@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'POST':
        print("POST METHOD")
        rvalues  = dict(request.form)
        CsvRow = list(rvalues.values())
        print(CsvRow)
        with open('finall.csv','a') as fd:
            fd.write(','.join(CsvRow[1:]) + '\n')
        insert_at(point_file, 'pos', str(CsvRow[1]))
        index = int(CsvRow[1]) + 1
        path = CsvRow[0]
    if request.method == 'GET':
        if os.path.exists(point_file):
            with open(point_file) as fr:
                spoint = json.load(fr)
                index = int(spoint['pos'])
                path = spoint['path']
    print(index)
    ocr_values = ocr_data[ocr_data.index==index].values[0]
    return render_template('index.html', ocr_values = dict(zip(columns,ocr_values)), path = path)

if __name__ == '__main__':
    ocr_data = pd.read_csv('extracted.csv')
    point_file = 'point_file.json'
    index = 0
    columns = ocr_data.columns 
    if os.path.exists(point_file):
        with open(point_file) as fr:
            spoint = json.load(fr)
            index = int(spoint['pos'])
            path = spoint['path']
    app.run(debug= True)



#mklink /D "C:\Users\arka\Music\anaconda\flask\static\images" "C:\Users\arka\Music\anaconda\exm_10\cutimg"