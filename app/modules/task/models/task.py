from sqlalchemy import Column, Integer, String, DateTime, func,ForeignKey
from sqlalchemy.orm import relationship
from database.base_class import Base

class Task(Base):
    __tablename__ = 'repo_task'
    __table_args__ = {'comment': '任务表'}

    id = Column(Integer, primary_key=True, comment='任务ID')
    name = Column(String(255), nullable=False, default='', comment='任务名称')
    description = Column(String(500), nullable=False, default='', comment='任务描述')
    create_time = Column(DateTime, default=func.now(), comment='创建时间')
    update_time = Column(DateTime, default=func.now(), onupdate=func.now(), comment='更新时间') 
    subtask = relationship("SubTask", back_populates="task", uselist=False)

class SubTask(Base):
    __tablename__ = 'repo_subtask'
    __table_args__ = {'comment': '子任务表'}

    id = Column(Integer, primary_key=True, comment='子任务ID')
    title = Column(String(255), nullable=False, default='', comment='子任务标题')
    status = Column(String(50), nullable=False, default='pending', comment='子任务状态')
    
    task_id = Column(Integer, ForeignKey("repo_task.id"), unique=True, nullable=False, comment='关联的任务ID')

    task = relationship("Task", back_populates="subtask")

from sqlalchemy import Column, Integer, Text, Date, DateTime, func
from database.base_class import Base

class DailyReport(Base):
    __tablename__ = "repo_daily_report"
    __table_args__ = {'comment': '日报记录表'}

    id = Column(Integer, primary_key=True, autoincrement=True, comment="日报ID")
    user_id = Column(Integer, nullable=False, comment="用户ID")
    date = Column(Date, nullable=False, comment="日报日期")
    content = Column(Text, nullable=False, comment="日报内容")
    create_time = Column(DateTime, default=func.now(), comment="创建时间")


