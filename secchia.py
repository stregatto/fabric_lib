import datetime


def separated_string_to_list(my_string, s=','):
    '''
    This function accept a "s" separated string and transform it in a list
    remove also all spaces.
    s is by default a comma
    '''
    my_list = my_string.split(s)
    _list = [x.strip(' ') for x in my_list]
    return _list


def chop_seconds_microseconds(dt):
    '''
    Remove seconds and microseconds form a datetime object
    '''
    return dt - datetime.timedelta(seconds=dt.second, microseconds=dt.microsecond)


def add_minutes(dt, minutes):
    '''
    Add minutes to a datetime object
    '''
    return dt + datetime.timedelta(minutes=minutes)


def add_minute_from_now(minutes):
    '''
    Add minutes from now
    '''
    return add_minutes(datetime.datetime.now(), minutes)


# downtime = 10
# now = datetime.datetime.now()
# end_time = chop_seconds_microseconds(add_minutes(now,
#                                                  downtime))
# end_time = str(end_time)
# start_time = str(chop_seconds_microseconds(now))

# print("%s - %s" % (end_time, start_time))
