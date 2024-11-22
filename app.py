from datetime import datetime, timedelta
from tkinter import N
from tkinter.tix import Control
from copy import deepcopy

from flask import Flask, json, request, g, jsonify, session
from src.middleware.cors import cors
from src.database.database import init_db
from config import config

import src.database.controller as controller

def init_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = config.SECRET_KEY

    # app에 뭔가 더 추가하고 싶은게 있으면 여기에 추가
    cors.init_app(app)

    return app

app = init_app()
engine, get_db = init_db(config.DATABASE_URI)


# 연결이 끊어질때 db close
@app.teardown_appcontext
def teardown_db(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/api/taxi_info/create', methods=['POST'])
def create_taxi_info():
    is_authenticated = bool(session.get('is_authenticated', False))
    if not is_authenticated:
        return jsonify({"msg":"권하없음"}), 403

    data = request.get_json()
    start_position = data.get('start_position', "")
    end_position = data.get('end_position', "")
    total_people = data.get('total_people', "")
    start_time = data.get('start_time', "")

    creator_nickname = session['nickname']
    creator_id = session['user_id']
    new_pool = controller.create_taxi_pool(
        start_position = start_position,
        end_position = end_position,
        total_people = total_people,
        start_time = start_time,
        creator_id = creator_id,
        creator_nickname=creator_nickname
    )
    
    return jsonify({"id" : new_pool.id}),200

@app.route('/api/taxi_info', methods = ['GET'])
def taxi_info():

    db = get_db()
    day = request.args.get('day', "") # yyyy-mm-dd-hh-mm

    start_datetime = datetime.strftime(day, '%Y-%m-%d-%H-%M')
    end_datetime = deepcopy(start_datetime)
    end_datetime.hour = 23
    end_datetime.minute = 59
    taxi_pools = controller.select_taxi_pools_by_day(db, start_datetime, end_datetime)

    if not taxi_pools:
        return jsonify({"msg": "팟이 없어요"}), 404
    
    result = {"taxi_list": [{
        "start_position" : taxi_pool.start_position,
        "end_position" : taxi_pool.end_position,
        "total_people" : taxi_pool.total_people,
        "participation_num" : taxi_pool.participation_num,
        "start_time" : taxi_pool.start_time,
        "creator" : taxi_pool.creator_nickname,
        "day" : taxi_pool.start_time.weekday()
    }for taxi_pool in taxi_pools]}

    return jsonify(result), 200
    #이제 taxi_pools를 돌면서 딕셔너리화하면서 추가하기?
    
@app.route('/api/taxi_info/<id>', methods=['GET'])
def get_taxi_info(id):
    db = get_db()
    taxi_pool = controller.select_taxi_pools_by_id(db, id)
    result = {
        "start_position": taxi_pool.start_position,
        "end_position": taxi_pool.end_position,
        "total_people": taxi_pool.total_people,
        "participation_num": taxi_pool.participation_num,
        "start_time": taxi_pool.start_time,
        "creator": taxi_pool.creator,
        "day" : taxi_pool.start_time.weekday()
    }
    return jsonify(result), 200

@app.route('/api/taxi_info/participate',methods=['POST'])
def p():
    data = request.get_json()
    user_id = data.get('user_id', "")
    taxi_id = data.get('taxi_id', "")
    controller.create_pool_member(taxi_id=taxi_id, user_id=user_id)
    return {},200

@app.route('/api/taxi_info/participate',methods=['GET'])
def q():
    user_id = request.args.get('user_id', "")
    taxi_id = request.args.get('taxi_id', "") 
    pool_member_find = controller.select_pool_member_by_taxi_user_id(
        user_id=user_id,
        taxi_id=taxi_id
    )
    return jsonify({"is_participated":(not pool_member_find==None)}), 200


    


