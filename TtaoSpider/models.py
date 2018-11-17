import datetime
from sqlalchemy import Column, String, create_engine, Integer, DateTime, TEXT
from sqlalchemy.ext.declarative import declarative_base
from TtaoSpider.settings import db_host, db_user, db_pawd, db_name, db_port

# 创建对象的基类:
Base = declarative_base()


# 淘宝订单
class TbOrderModel(Base):
    # 表的名字:
    __tablename__ = 'taobaov1_tborder'
    # 表的结构:
    rate_id = Column(String(200), unique=True)
    comment_user_nike = Column(String(200), )
    comment_user_vip = Column(String(200), )
    comment_date = Column(String(200), )
    goods_color = Column(String(200), )
    comment_content = Column(String(200), )
