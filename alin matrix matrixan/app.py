import os
from flask import Flask, render_template, request, jsonify
from matrix_operation import (
    tambah_matrix, kurang_matrix, kali_matrix,
    transpose_matrix, determinan_matrix, invers_matrix
)

app = Flask(__name__)

OPERASI = {'tambah', 'kurang', 'kali'}

OPERASI_MAP = {
    'tambah':     lambda A, B: tambah_matrix(A, B),
    'kurang':     lambda A, B: kurang_matrix(A, B),
    'kali':       lambda A, B: kali_matrix(A, B),
    'transpose':  lambda A, B: transpose_matrix(A),
    'determinan': lambda A, B: determinan_matrix(A),
    'invers':     lambda A, B: invers_matrix(A),
}


def parse_matrix(prefix, rows, cols):
    return [
        [float(request.form[f'{prefix}{i}{j}']) for j in range(cols)]
        for i in range(rows)
    ]


@app.route('/', methods=['GET', 'POST'])
def index():
    hasil = None
    error = None

    if request.method == 'POST':
        try:
            operasi = request.form['operation']
            rowsA = int(request.form['rowsA'])
            colsA = int(request.form['colsA'])
            A = parse_matrix('A', rowsA, colsA)

            B = None
            if operasi in OPERASI:
                rowsB = int(request.form['rowsB'])
                colsB = int(request.form['colsB'])
                B = parse_matrix('B', rowsB, colsB)

            hasil = OPERASI_MAP[operasi](A, B)

        except (ValueError, KeyError) as e:
            error = str(e)

    return render_template('index.html', hasil=hasil, error=error)

if __name__ == '__main__':
    app.run(debug=True)
