from django.shortcuts import render, HttpResponse, redirect
from django.http.response import json
from .models import *
from datetime import date, datetime, timedelta
from django.forms.models import model_to_dict
# from .cron import *
from .items import *
from .order import *
from .chess_service import *
from urllib.parse import parse_qs

time_checkout = 12
time_checkin = 14
repair_id = 9999

# FCK DRY


def home(request):
    return render(request, 'work_app/home.html')


def get_manage_page(request):
    if request.method == 'GET' and request.is_ajax():
        return render(request, 'work_app/_manage_plan.html')


def get_state_page(request):
    if request.method == 'GET' and request.is_ajax():
        return render(request, 'work_app/_state.html')


def delete_order(request):
    if request.method == 'POST' and request.is_ajax():
        Order.objects.get(id=int(request.POST['id_order'])).delete()
    return show_front_desk_table(request, request.POST.get('cell_date_string'))


@timer
def get_front_desk(request):
    return show_front_desk_table(request, request.GET.get('dateText'))


def show_front_desk_table(request, start_date):
    return render(request, 'work_app/_table_front_desk.html', context=take_month_matrix(
        datetime.strptime(start_date, '%d.%m.%Y').date()))


@timer
def post_order_form(request):
    if request.method == 'POST' and request.is_ajax():
        post_order(parse_qs(request.POST['order_form']), request.POST['is_reserved'])
        return show_front_desk_table(request, request.POST.get('cell_date_string'))


@timer
def get_order_form(request):
    if request.method == 'GET' and request.is_ajax():
        cell_date_string = request.GET.get('cell_date_string')
        cell_date_iso = datetime.strptime(cell_date_string, '%d.%m.%Y').date()
        order_number_str = request.GET.get('order_number_class').split('_')[1]

        if order_number_str == 'none':  # CREATE NEW ORDER_FORM
            context = prepare_new_order_for_view(calculate_bed_from_html_table_row(int(request.GET.get('row'))),
                                                 cell_date_iso)
        else:
            context = prepare_existing_order_for_view(order_number_str)

        context['cell_date_string'] = cell_date_string
        return render(request, 'work_app/_order_form.html', context=context)

    print("шо-то глобально пошло не так!")
    return


@timer
def get_client_from_base(request):
    if request.method == 'GET' and request.is_ajax():
        return HttpResponse(
            json.dumps(found_client_in_base(request.GET.get('text_for_search'), request.GET.get('mode'))),
            content_type='application/json')
    return None


@timer
def get_consumables_page(request):
    if request.method == 'GET' and request.is_ajax():
        return render(request, 'work_app/_consumables.html', context=get_consumables_table())


@timer
def get_consumable_panel(request):
    print('enter subroutine get_consum panel')
    if request.method == 'GET' and request.is_ajax():
        return render(request, 'work_app/_item_form.html',
                      context={'form': prepare_item_form(int(request.GET.get('consumable_id_item').split('_')[2]))})


@timer
def delete_consumable_record(request):
    if request.method == 'POST' and request.is_ajax():
        Consumables.objects.get(id=int(request.POST['id_item'])).delete()
    return redirect(get_consumables_page)


@timer
def save_consumable_record(request):
    if request.method == 'POST' and request.is_ajax():
        consumable_for_update = Consumables.objects.get(id=request.POST['id_item'])
        consumable_for_update.recommended_minimum = request.POST['recommended_minimum']
        consumable_for_update.current_amount = request.POST['current_amount']
        consumable_for_update.save()
    return render(request, 'work_app/_consumables.html', context=get_consumables_table())


@timer
def create_consumable_form(request):
    if request.method == 'GET' and request.is_ajax():
        return render(request, 'work_app/_item_create_form.html', context={'form': ItemCreate()})


@timer
def create_consumable_record(request):
    if request.method == 'POST' and request.is_ajax():
        new_consumable = Consumables.objects.create(name=request.POST['name_item'],
                                                    unit=request.POST['unit_item'],
                                                    recommended_minimum=request.POST['recommended_minimum'],
                                                    current_amount=request.POST['current_amount'])
        new_consumable.save()
    return render(request, 'work_app/_consumables.html', context=get_consumables_table())


@timer
def get_bar_page(request):
    if request.method == 'GET' and request.is_ajax():
        return render(request, 'work_app/_bar.html', context=get_bar_table())


@timer
def get_bar_panel(request):
    if request.method == 'GET' and request.is_ajax():
        return render(request, 'work_app/_bar_item_form.html',
                      context={'form': prepare_baritem_form(int(request.GET.get('bar_id_item').split('_')[2]))})


@timer
def delete_bar_record(request):
    if request.method == 'POST' and request.is_ajax():
        BarItem.objects.get(id=int(request.POST['id_item'])).delete()
    return redirect(get_bar_page)


# @timer
# def delete_item_record(request):
#     if request.method == 'POST' and request.is_ajax():
#         id_item = int(request.POST['id_item'])
#         if request.POST['mode'] == 'bar':
#             BarItem.objects.get(id=id_item).delete()
#             return redirect(get_bar_page)
#         else:
#             Consumables.objects.get(id=id_item).delete()
#             return redirect(get_consumables_page)


@timer
def save_bar_record(request):
    if request.method == 'POST' and request.is_ajax():
        bar_item_for_update = BarItem.objects.get(id=request.POST['id_item'])
        bar_item_for_update.recommended_minimum = request.POST['recommended_minimum']
        bar_item_for_update.current_amount = request.POST['current_amount']
        bar_item_for_update.save()
    return render(request, 'work_app/_bar.html', context=get_bar_table())


@timer
def create_bar_form(request):
    if request.method == 'GET' and request.is_ajax():
        return render(request, 'work_app/_bar_item_create_form.html', context={'form': ItemCreate()})


@timer
def create_bar_record(request):
    if request.method == 'POST' and request.is_ajax():
        new_bar_item = BarItem.objects.create(name=request.POST['name_item'],
                                              unit=request.POST['unit_item'],
                                              recommended_minimum=request.POST['recommended_minimum'],
                                              current_amount=request.POST['current_amount'])
        new_bar_item.save()
    return render(request, 'work_app/_bar.html', context=get_bar_table())
