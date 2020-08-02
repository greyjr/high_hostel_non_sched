from .models import Consumables, BarItem
from django.forms.models import model_to_dict
from .forms import ItemEdit


def get_consumables_table():
    all_consumables = Consumables.objects.values_list(flat=True)
    consumables1 = []
    consumables2 = []
    counter = 1
    for i in range(0, len(all_consumables), 10):
        odd_record = all_consumables[i:i + 5]
        odd_record.insert(1, counter)
        consumables1.append(odd_record)
        counter += 1
        even_record = (all_consumables[i + 5:i + 10] if i + 5 < len(all_consumables) else [''] * 5)
        even_record.insert(1, counter)
        consumables2.append(even_record)
        counter += 1
    return {'table1': consumables1, 'table2': consumables2}


def prepare_item_form(id_item):
    consumable_dict_from_model = model_to_dict(Consumables.objects.get(id=id_item))
    model_fields = ['name', 'unit', 'id']
    consumable_dict_from_model.update({(i + '_item'): consumable_dict_from_model.pop(i) for i in model_fields})
    return ItemEdit(consumable_dict_from_model)


def get_bar_table():
    all_bar_items = BarItem.objects.values_list(flat=True)
    bar_items1 = []
    bar_items2 = []
    counter = 1
    for i in range(0, len(all_bar_items), 10):
        odd_record = all_bar_items[i:i + 5]
        odd_record.insert(1, counter)
        bar_items1.append(odd_record)
        counter += 1
        even_record = (all_bar_items[i + 5:i + 10] if i + 5 < len(all_bar_items) else [''] * 5)
        even_record.insert(1, counter)
        bar_items2.append(even_record)
        counter += 1
    return {'table1': bar_items1, 'table2': bar_items2}


def prepare_baritem_form(id_item):
    bar_dict_from_model = model_to_dict(BarItem.objects.get(id=id_item))
    model_fields = ['name', 'unit', 'id']
    bar_dict_from_model.update({(i + '_item'): bar_dict_from_model.pop(i) for i in model_fields})
    return ItemEdit(bar_dict_from_model)
