"""Основной файл приложения"""
import os

from flask import Flask, request
from werkzeug.exceptions import BadRequest
from utils import build_query
from exceptions import NotBoolConvertedType, NotIntType


app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query", methods=["POST"])
def perform_query():
    # получить параметры query и file_name из request.args, при ошибке вернуть ошибку 400
    # проверить, что файла file_name существует в папке DATA_DIR, при ошибке вернуть ошибку 400
    # с помощью функционального программирования (функций filter, map), итераторов/генераторов сконструировать запрос
    # вернуть пользователю сформированный результат
    data = request.json
    try:
        file_name = data['file_name']
        cmd1 = data['cmd1']
        cmd2 = data['cmd2']
        value1 = data['value1']
        value2 = data['value2']
    except:
        return BadRequest(description=f"Missing one or more arguments")

    path_file = os.path.join(DATA_DIR, file_name)
    if not os.path.exists(path_file):
        raise BadRequest(description=f"File {file_name} was not found")

    with open(path_file) as file:
        try:
            result = build_query(file, cmd1, value1)
            result = build_query(result, cmd2, value2)
            result = '\n'.join(result)
        except NotBoolConvertedType as e:
            return 'Method "sort" require a boolean parametr', 400
        except NotIntType as e:
            return 'Methods "limit" and "map" require a numeric parametr', 400

    return app.response_class(result, status='200 Completed successfully', content_type="text/plain")


if __name__ == '__main__':
    app.run(port=7777)
