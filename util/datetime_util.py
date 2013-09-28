# coding: utf-8
import datetime

def timediffer(dt1, dt2):

    """
    计算两个时间点之间的时间差：
    当时间差大于1秒，切小于一分钟时，返回dt1和dt2之间相差的秒数
    当时间差大于一分钟，且小宇一小时时，返回dt1和dt2之间相差的分钟数
    当时间差大于一小时并且小于一天时，返回dt1和dt2之间相差的小时数
    当时间差大于1天，且小于一个月时，dt1和dt2之间相差的天数
    当时间差大于一个月，且小于一年时，返回dt1和dt2之间相差的月数
    @param dt1: datetime
    @param dt2: datetime
    """
    dt = dt2 - dt1
    print type(dt)
    microsecond = dt.microseconds #(>= 0 and less than 1 second)
    second = dt.seconds #>= 0 and less than 1 day

    if second is not 0:
        if second <60:
            print "大约在{0}秒前".format((second))
        elif second >= 60 and second < 3600:
            print "大约在{0}分钟前".format(second/60)
        elif second>=3600:
            print "大约在{0}小时前".format(second/3600)

    day = dt.days
    print "{0}  {1}  {2}  ".format(microsecond, second, day)
    return

if __name__ == '__main__':
    dt1 = datetime.datetime.now()
    dt2 = dt1 + datetime.timedelta(hours=26)
    timediffer(dt1, dt2)