import datetime
import random

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import String, Column, DateTime, Integer, ForeignKey, SmallInteger

from base.dababase import get_session_2, get_engine

Base = declarative_base()
now = datetime.datetime.now
my_engine = get_engine()
my_session = get_session_2().__next__()


class BaseTime(Base):
    __abstract__ = True
    update_time = Column(DateTime, default=now, comment="更新时间", onupdate=now)
    create_time = Column(DateTime, default=now, comment="创建时间")


class Video(BaseTime):
    __tablename__ = 'video'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键，自增")
    title = Column(String(50), default="", comment="标题")
    description = Column(String(500), default="", comment="描述")
    year = Column(SmallInteger, default=0, comment="年代")
    director = Column(String(50), default="", comment="导演")
    type = Column(SmallInteger, default=0, comment="类型:电视剧=0，电影=1")
    cover = Column(String(255), default="", comment="封面")
    path = Column(String(255), default="", comment="视频路径")
    duration = Column(SmallInteger, default=3600, comment="时长")
    label = Column(String(50), default="战争/历史", comment="标签，可搜索")
    status = Column(SmallInteger, default=0, comment="0=开启 1=关闭")

    def __repr__(self):
        # 媒资表
        return f"媒资表：{self.title}"


class Behavior(BaseTime):
    __tablename__ = 'behavior'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键，自增")
    video_id = Column(Integer, ForeignKey("video.id"), comment="视频id")
    video = relationship(Video, backref="be_videos")
    user_id = Column(Integer, ForeignKey("user.id"), comment="用户id")
    member_id = Column(Integer, ForeignKey("member.id"), comment="成员id")
    # 行为类型
    behavior_type = Column(SmallInteger, default=0, comment="行为类型：浏览=0，观看=1，收藏=2")
    # 观看时长
    duration = Column(SmallInteger, default=0, comment="时长")

    def __repr__(self):
        # 行为表
        return f"行为表：{self.behavior_type}"


class WorkBenches(BaseTime):
    __tablename__ = 'work_benches'

    id = Column(Integer, primary_key=True, autoincrement=True, comment="主键，自增")
    video_id = Column(Integer, ForeignKey("video.id"), comment="视频id")
    video = relationship(Video, backref="work_benches")
    status_flag = Column(SmallInteger, default=0, comment="状态标记：0-未删除，1-已删除")
    name = Column(String(50), nullable=True, comment="素材名称")
    crop_name = Column(String(50), nullable=True, comment="作品名称")
    status = Column(SmallInteger, nullable=False, default=0,
                    comment="状态：0=上传中；1=上传完成；2=上传失败；3=生成中；4=生成完成；5=生成失败")
    type_flag = Column(SmallInteger, default=0, comment="类型，0-素材，1-作品")


def create_all():
    # 创建表
    Base.metadata.create_all(my_engine)
    print("创建表完成")


def drop_all():
    # 删除表
    Base.metadata.drop_all(my_engine)
    print("删除表完成")


def add_data():
    # 模拟媒资数据
    video_list = []
    for i in range(0, 1000):
        year = random.randint(1990, 2023)
        duration = random.randint(1000, 2000)
        type_int = random.randint(0, 1)
        label_str = "爱情/历史/战争"
        label_list = label_str.split("/")
        # 随机取1-4个组合在一起
        labels = random.sample(label_list, random.randint(1, 2))
        label_str = "/".join(labels)

        video = Video(title=f"战狼:{i}", year=year, label=label_str, type=type_int, duration=duration,
                      cover=f"static/cover/战狼{random.randint(1, 2)}.webp")
        video_list.append(video)
    my_session.add_all(video_list)

    # 模拟用户行为数据
    behavior_list = []
    for i in range(0, 10):
        video_id = random.randint(1, 5)
        behavior_type = random.randint(0, 2)
        duration = random.randint(100, 1000)

        behavior = Behavior(video_id=video_id, user_id=1, member_id=1, behavior_type=behavior_type, duration=duration)
        behavior_list.append(behavior)
    my_session.add_all(behavior_list)

    my_session.commit()
    print("添加数据完成")


if __name__ == '__main__':
    """
    https://blog.csdn.net/Cycloctane/article/details/133795319
    https://www.cnblogs.com/zx0524/p/17304552.html
    https://github.com/sqlalchemy/sqlalchemy
    """
    drop_all()
    create_all()
    add_data()
