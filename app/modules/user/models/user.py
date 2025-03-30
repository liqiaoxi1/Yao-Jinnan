from sqlalchemy import Column, String, Integer, Date, SmallInteger, DateTime
from sqlalchemy.sql import func
from passlib.context import CryptContext

# 创建密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from database.base_class import Base

class User(Base):
    __tablename__ = 'repo_user'  # FIXME 修改为项目简称前缀+user
    __table_args__ = {'comment': '会员表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment='ID')
    uid = Column(String(32), nullable=False, unique=True, server_default="''", comment='用户ID')
    nickname = Column(String(50), nullable=False, server_default="''", comment='昵称')
    email = Column(String(50), nullable=False, server_default="''", comment='邮箱')
    mobile = Column(String(11), nullable=False, server_default="''", comment='手机')
    avatar = Column(String(1024), nullable=False, server_default="''", comment='头像')
    gender = Column(SmallInteger, nullable=False, server_default="0", comment='性别: 0=未知, 1=男, 2=女')
    birthday = Column(Date, comment='生日')
    password = Column(String(255), nullable=False, server_default="''", comment='密码')
    status = Column(String(30), nullable=False, server_default="''", comment='状态')
    last_login_time = Column(DateTime, comment='上次登录时间')
    last_login_ip = Column(String(50), nullable=False, server_default="''", comment='上次登录IP')

    update_time = Column(DateTime, default=func.now(), comment='更新时间')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')

    def set_password(self, password):
        self.password = pwd_context.hash(password)
