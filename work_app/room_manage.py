from .models import *


# Визначення, чи є вільна кровать у заданій кімнаті в заданому відрізку часу
def is_free_place(room, date_start, date_stop):
    capacity = Room.objects.get(room=room).capacity
    found_orders = 0
    select_orders_by_room = Order.objects.get(order_room=room)
    for order in select_orders_by_room:
        if order.date_start <= date_start and order.date_stop >= date_stop:
            found_orders += 1
    return found_orders < capacity

