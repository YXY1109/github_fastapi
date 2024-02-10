import subprocess
from datetime import datetime, timedelta

from moviepy.video.io.VideoFileClip import VideoFileClip


def str_to_second(second_st):
    """
    时间字符串转为秒数据
    :param second_st: 00:00:43
    :return: 43
    """
    time_list = second_st.split(":")

    # 转为多少秒
    second = int(time_list[0]) * 3600 + int(time_list[1]) * 60 + int(time_list[2])
    return second


def time_to_second(second_st):
    """
    时间字符串转为秒数据
    :param second_st: 00:00:43
    :return: 43
    """
    # 转为多少秒
    second = int(second_st.hour) * 3600 + int(second_st.minute) * 60 + int(second_st.second)
    return second


def second_to_str(second):
    """
    将秒数转为时分秒格式
    :param second:
    :return:
    """
    # 将秒数转为时分秒格式：00:00:00
    m, s = divmod(second, 60)
    h, m = divmod(m, 60)
    return "%02d:%02d:%02d" % (h, m, s)


def get_video_duration(file_name: str) -> float:
    """
    获取音视频的时长
    :param file_name: 文件路径
    :return:
    """
    try:
        result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                                 "format=duration", "-of",
                                 "default=noprint_wrappers=1:nokey=1", file_name],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.STDOUT)
        duration = float(result.stdout)
        # 保留两位小数
        duration = round(duration, 2)
        return duration
    except Exception as e:
        print(f"使用moviepy获取时长，ffprobe异常：{e}")
        return get_video_duration_from_url(file_name)


def get_video_duration_from_url(video_url):
    """
    直播流时长
    :param video_url:
    :return:
    """
    try:
        video = VideoFileClip(video_url)
        duration = video.duration
        video.close()  # 关闭视频文件以释放资源
        return duration
    except Exception as e:
        print(f"无法获取视频时长: {e}")
        return 0


def get_today_time(day=0, is_zero=False):
    """
    获取今天的时间
    """
    today = datetime.today() - timedelta(days=day)
    if is_zero:
        time_format = '%Y-%m-%d 00:00:00'
    else:
        time_format = '%Y-%m-%d %H:%M:%S'
    today_time = today.strftime(time_format)
    return today_time


def seconds_to_hms(seconds_num):
    # 利用divmod函数分别计算小时、分钟和秒
    hours, remainder = divmod(seconds_num, 3600)
    minutes, seconds = divmod(remainder, 60)

    # 格式化输出结果为00:00:00的格式
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


if __name__ == '__main__':
    # url = "http://vjs.zencdn.net/v/oceans.mp4"
    # print(get_video_duration(url))
    # print(get_video_duration_from_url(url))

    print(second_to_str(3600))
