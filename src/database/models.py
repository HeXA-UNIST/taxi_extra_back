from sqlalchemy import Integer, String, DateTime, Boolean
from sqlalchemy.sql.schema import Column
from sqlalchemy.sql.functions import current_timestamp
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.schema import ForeignKey

Base = declarative_base()

class TaxiPool(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement= True)  # 기본 키
    start_position = db.Column(db.String(30), nullable=False)  # 출발 위치
    end_position = db.Column(db.String(30), nullable=False)  # 도착 위치
    total_people = db.Column(db.Integer, nullable=False)  # 모집 인원
    start_time = db.Column(db.DateTime, nullable=False)  # 출발 시간
    creator_id = db.Column(db.String(30), nullable=False)  # 생성자
    creator_nickname = db.Column(db.String(30), nullable=False)  # 생성자
    created_at = db.Column(db.DateTime, nullable=False) # 생성시간

class PoolMember(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement= True)  # 기본 키
    taxi_id = db.Column(db.String(30), nullable=False)  # 출발 위치
    user_id = db.Column(db.String(30), nullable=False)  # 도착 위치
    created_at = db.Column(db.DateTime, nullable=False)  # 출발 시간
    

# 데이터베이스 생성
Base.metadata.create_all()