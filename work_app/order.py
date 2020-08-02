from .models import *
from .forms import *
from django.forms.models import model_to_dict
from datetime import date, timedelta, datetime
from datetime import time as d_time

time_checkout = 12
time_checkin = 14
repair_id = 9999


def max_duration(bed, date_start):
    """ return int: days - from self.start to next start OR 365-max order duration.
    """
    next_orders = Order.objects.filter(order_bed=bed).filter(date_start__gt=date_start)
    return (next_orders.earliest('date_start').date_start - date_start).days if next_orders else 365


def min_duration(date_start):
    """
    Возвращает минимальную продолжительность заказа - количество дней - разницу между Сегодня и date_start.
    """
    return (date.today() - date_start).days


def calculate_bed_from_html_table_row(row):
    """
    принимает номер строчки ячейки, по которой кликнули в html-таблице сетки
    и вычисляет по этому номеру, какой кровати он соответствует
    возвращает объект искомой кровати (или аварийно первую кровать)
    """
    order_bed = None  # вычисляем объект Кровати по его ряду в табличке HTML с учетом строк шапки и комнат
    row_counter = 3  # пропускаем три строки шапки таблицы
    for bed in Bed.objects.all():
        if bed.number == 1:  # если кровать с номером 1
            row_counter += 1  # то пропускаем ряд
        if row == row_counter:
            order_bed = bed
            break
        row_counter += 1
    return order_bed or Bed.objects.get(id=1)


def prepare_new_order_for_view(bed, cell_date_iso):
    context = {
        'daily_price': bed.bed_room.price,
        'order_form': OrderCreateForm(
            data={'date_start': cell_date_iso,
                  'is_reserved': True,
                  'order_bed': bed.id,
                  'order_bed_str': str(bed),
                  },
            max_duration=max_duration(bed.id, cell_date_iso)
        )}

    return context


def prepare_existing_order_for_view(order_number):
    """
    анализирует по номеру заказа его вид: активный/старый/бронь/ремонт/предоплаченный
    и возвращает ...
    """
    order = Order.objects.get(id=order_number)
    order_from_base_dict = model_to_dict(order)

    order_from_base_dict['id_order'] = order_from_base_dict.pop('id')
    order_from_base_dict['duration'] = (order_from_base_dict['date_stop'] - order_from_base_dict[
        'date_start']).days + 1
    order_from_base_dict['order_bed_str'] = str(Bed.objects.get(id=order_from_base_dict['order_bed']))
    order_from_base_dict.update(model_to_dict(Client.objects.get(id=order_from_base_dict['order_client'])))
    order_from_base_dict['id_client'] = order_from_base_dict.pop('id')
    min_dur = min_duration(order_from_base_dict['date_start'])
    max_dur = max_duration(order_from_base_dict['order_bed'],
                           order_from_base_dict['date_start'])

    context = {'daily_price': order.daily_price()}
    # readonly mode = [DURATION, CLIENT]
    readonly_mode = [True, True]

    if order_from_base_dict['is_reserved']:
        readonly_mode = [False, False]
        context['status'] = 'бронь'
    if datetime.combine(order_from_base_dict['date_stop'] + timedelta(1), d_time(time_checkout)) < datetime.now() and \
            order_from_base_dict['order_client'] != repair_id:
        context['status'] = 'закрыто'
    if order_from_base_dict['order_client'] == repair_id:
        context['status'] = 'ремонт'
        readonly_mode = [False, True]
    if order_from_base_dict['date_start'] > date.today() and not order_from_base_dict['is_reserved']:
        context['status'] = 'оплачено'
    if (order_from_base_dict['date_start'] <= date.today() <= order_from_base_dict['date_stop']) and not \
            order_from_base_dict['is_reserved'] and order_from_base_dict['order_client'] != repair_id:
        context['status'] = 'активно'
        readonly_mode = [False, True]
        max_dur = order_from_base_dict['duration']

    context['order_form'] = OrderEditForm(data=order_from_base_dict,
                                          initial=order_from_base_dict,
                                          min_duration=min_dur,
                                          max_duration=max_dur,
                                          readonly_mode=readonly_mode)
    return context


def found_client_in_base(text_for_search, mode):
    client = {'message': 'no'}

    if mode in ['phone', 'passport'] and len(text_for_search) < 16:
        clients = Client.objects.filter(**{mode: text_for_search})
        if len(clients):
            client = model_to_dict(clients.last())
            client['id_client'] = client.pop('id')
            client['message'] = 'ok'
    return client


def post_order(form, is_reserved):

    del form['csrfmiddlewaretoken']

    form = {key: value[0] for key, value in form.items()}

    if 'toggle_reserved' in form:
        del form['toggle_reserved']

    client_fields = ['id_client', 'surname', 'name', 'patronymic', 'passport', 'another_document', 'phone', 'email',
                     'comment']

    data_for_client_model = {field if field != 'id_client' else 'id': form[field] if field in form else '' for field in
                             client_fields}

    date_start = datetime.strptime(form['date_start'], '%Y-%m-%d').date()

    data_for_order_model = {
        'order_bed_id': int(form['order_bed']),
        'date_start': date_start,
        'date_stop': date_start + timedelta(int(form['duration']) - 1),
        'is_reserved': is_reserved.lower() == 'true',
        'order_client_id': calculate_id_client_from_form(data_for_client_model)
    }

    if 'id_order' in form:
        order_update(data_for_order_model, int(form['id_order']))
    else:
        order_create(data_for_order_model)
    return True


def order_update(data, id_order):
    old_order = Order.objects.get(id=id_order)
    Order.objects.get(id=id_order).delete()
    data['id'] = id_order
    new_order = Order(**data)
    new_order.save()
    return new_order


def order_create(data):
    new_order = Order(**data)
    new_order.save()
    return new_order


def client_create(data):
    new_client = Client.objects.create(**data)
    print('NEW CLIENT CREATED. ', new_client)
    return new_client.id


def client_update(data, id_client):
    old_client = Client.objects.get(id=id_client)
    Client.objects.get(id=id_client).delete()
    data['id'] = id_client
    new_client = Client(**data)
    new_client.save()
    return new_client.id  # нет необходмости. можно пустой return


def get_client_data_for_model_from_form(form):
    client_fields = ['surname', 'name', 'patronymic', 'passport', 'another_document', 'phone', 'email', 'comment']
    return {field: form[field] if field in form else '' for field in client_fields}


def calculate_id_client_from_form(data):
    if not data['id']:
        del data['id']
        may_be_the_same_client = Client.objects.filter(**data)
        if bool(may_be_the_same_client):
            id_client = Client.objects.filter(**data).first().id
        else:
            id_client = client_create(data)
    else:
        id_client = data['id']
        client_from_db = Client.objects.get(id=id_client)
        if client_from_db.__dict__ != Client(**data).__dict__:
            client_update(data, id_client)

    return id_client
