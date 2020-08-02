import time
import atexit
from datetime import datetime, timedelta
from .models import Order
from apscheduler.schedulers.background import BackgroundScheduler


def manage_reserved_orders():
    print('\nmanage reserved orders')
    print(time.strftime("%A, %d. %B %Y %I:%M:%S %p"))

    today_reserved_orders = Order.objects.filter(is_reserved=True).filter(date_start__lte=datetime.today())
    for order in today_reserved_orders:
        processing_reserved_order(order)


def check_unrelated_clients():
    # ищет и удаляет клиентов с неполными данными, и у которых нет связанных заказов
    print('search unrelated clients...')
    return


scheduler = BackgroundScheduler()
scheduler.add_job(func=manage_reserved_orders, trigger="interval", seconds=1800)
scheduler.add_job(func=check_unrelated_clients, trigger='interval', seconds=1800)
scheduler.start()

# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())


def processing_reserved_order(order):
    print('processing reserved order N {} - {}'.format(order.id, order))
    print('duration: {}'.format((order.date_stop - order.date_start + timedelta(1)).days))
    if order.date_stop < datetime.today().date():
        print('order {} deleted'.format(order.id))
        # order.delete()
    if order.date_start < datetime.today().date():
        print('order {} was deleted'.format(order.id))
        order.delete()
