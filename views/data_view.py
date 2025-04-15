from flask import Blueprint
from flask import render_template, redirect
from flask import request

import os
from pathlib import Path

import pandas as pd
data_bp = Blueprint('data', __name__, url_prefix="/data")


@data_bp.route('/init-titanic', methods = ['GET'])
def initialize_cancer():
    pass

@data_bp.rout('/cancer', methods =['GET'])
def show_cancer():
    #파일에서 데이터 읽기 
    bp_path = data_bp.root_path #현재 blueprintpath

    root_path = Path(bp_path).parent
    file_path = os.path.join(root_path, 'data_files', 'titanic_train.csv')
    #return file_path
    df_cancer = pd.read_csv(file_path)
    #템플릿으로 이동 (위에서 읽은 데이터 전달)
    return render_template('data/' , df = df_cancer)
    pass