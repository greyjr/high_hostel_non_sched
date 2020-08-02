from .models import *
from datetime import date, timedelta, datetime
from .timer import timer
from datetime import time as d_time

time_checkout = 12
time_checkin = 14
repair_id = 9999


def is_bed_free_at_day(bed_id, day_start=date.today()):
    required_moment = day_start
    orders = Order.objects.filter(order_bed_id=bed_id)
    wanted = orders.filter(date_start__lte=required_moment) & orders.filter(date_stop__gte=required_moment)
    return bool(len(wanted))


@timer
def current_bed_map():
    all_rooms = Room.objects.all()
    map_of_hostel = []
    for room in all_rooms:
        beds_in_room = []
        for bed in range(1, room.capacity + 1):
            bed_in_room = Bed.objects.filter(bed_room__id=room.id).get(number=bed).id
            beds_in_room.append(is_bed_free_at_day(bed_in_room))
        map_of_hostel.append(beds_in_room)
    return map_of_hostel


@timer
def take_month_matrix(start_date):
    interval = 28
    start_date -= timedelta(int(interval / 2) - 1)
    # на входе дата в формате date (не в datetime!)

    date_days = [(start_date + timedelta(i)).day for i in range(interval)]
    #
    week = ['пн', 'вт', 'ср', 'чт', 'пт', 'сб', 'вс']
    week_days = (week[start_date.weekday():] + week * 5)[:interval]
    line_blank = []
    for i in range(interval):
        if week_days[i] in ['сб', 'вс']:
            line_blank.append(['free_w', 'none'])
        else:
            line_blank.append(['free__', 'none'])

    matrix = []
    beds = list(Bed.objects.all().values_list())
    for bed in beds:
        get_bed_orders = Order.objects.filter(order_bed_id=bed[0],
                                              date_start__lte=start_date + timedelta(interval - 1),
                                              date_stop__gte=start_date)
        if bed[2] == 1:
            matrix.append(['комната ' + str(bed[1]) + '.  стоимость в сутки {} грн.'.format(
                Room.objects.get(number=bed[1]).price)])

        line = line_blank[:]

        for order in get_bed_orders:
            left = (order.date_start - start_date).days if (order.date_start - start_date).days > -1 else 0
            right = \
                (order.date_stop - start_date).days if (order.date_stop - start_date).days < interval else interval - 1

            if datetime.now() > datetime.combine(order.date_stop + timedelta(1), d_time(time_checkout)):
                color = 'past__'
            elif datetime.now() < datetime.combine(order.date_start, d_time(time_checkin)) and order.is_reserved:
                color = 'pre_or'
            elif datetime.now() < datetime.combine(order.date_start, d_time(time_checkin)) and not order.is_reserved:
                color = 'paid__'
            else:
                color = 'actual'

            if order.order_client_id == 9999:
                color = 'repair'

            for i in range(right - left + 1):
                line[left + i] = [color, order.id]

        matrix.append([bed[2], line])

    # строка названия месяца/месяцев. если для названия мало места (1-2 дня попадает) то пустая строка
    month_line = []
    colspan = 1
    month_names = ['', 'январь', 'февраль', 'март', 'апрель', 'май', 'июнь',
                   'июль', 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    for i in range(interval):
        if (start_date + timedelta(i + 1)).day == 1 or i == interval - 1:
            month = month_names[(start_date + timedelta(i)).month] if colspan > 1 else ''
            month_line.append([month, colspan])
            colspan = 1
        else:
            colspan += 1

    return {'matrix': matrix,
            'date_days': date_days,
            'week_days': week_days,
            'month_line': month_line,
            'half_interval': int(interval / 2),
            'start_date': start_date}
