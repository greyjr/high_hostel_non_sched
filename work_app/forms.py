from django import forms
from .models import *
from datetime import datetime


class DateInput(forms.DateInput):
    input_type = 'date'


class OrderCreateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        max_duration = kwargs.pop('max_duration')
        super(OrderCreateForm, self).__init__(*args, **kwargs)

        self.fields['duration'].widget.attrs['max'] = max_duration
        self.fields['order_bed'].widget.attrs['readonly'] = True
        self.fields['order_bed_str'].widget.attrs['readonly'] = True

    id_order = forms.IntegerField(label='номер заказа')
    date_start = forms.DateField(label='дата заселения', widget=DateInput)
    duration = forms.IntegerField(label='продолжительность')
    date_stop = forms.DateField(label='дата выселения')
    # order_client = forms.ModelChoiceField(label='клиент', queryset=Client.objects.all())
    order_bed = forms.IntegerField(label='комната')
    order_bed_str = forms.CharField(label='комната')
    is_reserved = forms.BooleanField(label='бронь')

    id_client = forms.IntegerField(label='номер клиента', initial=0, required=False)
    surname = forms.CharField(label='фамилия', max_length=64)
    name = forms.CharField(label='имя', max_length=64, required=False)
    patronymic = forms.CharField(label='отчество', max_length=64, required=False)
    passport = forms.CharField(label='паспорт', max_length=128, required=False)
    another_document = forms.CharField(label='или другой документ', max_length=128, required=False)
    phone = forms.CharField(label='телефон', max_length=16, required=False)
    email = forms.EmailField(label='email', required=False)
    comment = forms.CharField(label='комментарий', max_length=256, initial=' ', required=False)

    date_start.widget.attrs.update({'onchange': 'refresh_date_stop()', 'min': datetime.now().strftime('%Y-%m-%d')})
    duration.widget.attrs.update({'min': '1', 'value': '1', 'onchange': 'refresh_date_stop()'})


class OrderEditForm(forms.Form):
    def __init__(self, *args, **kwargs):

        readonly_mode = kwargs.pop('readonly_mode') if 'readonly_mode' in kwargs else [True, True]
        max_duration = kwargs.pop('max_duration') if 'max_duration' in kwargs else 365
        min_duration = kwargs.pop('min_duration') if 'min_duration' in kwargs else 1
        if min_duration < 1:
            min_duration = 1
        super(OrderEditForm, self).__init__(*args, **kwargs)

        self.fields['duration'].widget.attrs['min'] = min_duration
        self.fields['duration'].widget.attrs['max'] = max_duration
        self.fields['date_start'].widget.attrs['readonly'] = True
        self.fields['duration'].widget.attrs['readonly'] = readonly_mode[0]
        self.fields['order_bed_str'].widget.attrs['readonly'] = True
        self.fields['date_start'].widget.attrs['onchange'] = 'refresh_date_stop()'
        self.fields['duration'].widget.attrs['onchange'] = 'refresh_date_stop()'

        client_fields = ['id_client', 'surname', 'name', 'patronymic', 'passport', 'another_document', 'phone', 'email']
        for field in client_fields:
            self.fields[field].widget.attrs['readonly'] = readonly_mode[1]

    id_order = forms.IntegerField(label='номер заказа', required=False)
    date_start = forms.DateField(label='дата заселения', widget=DateInput)
    date_stop = forms.DateField(label='дата выселения', required=False)
    duration = forms.IntegerField(label='продолжительность')
    # order_client = forms.ModelChoiceField(label='клиент', queryset=Client.objects.all())
    order_bed = forms.IntegerField(label='комната')
    order_bed_str = forms.CharField(label='комната')
    is_reserved = forms.BooleanField(label='бронь', required=False)

    id_client = forms.IntegerField(label='номер клиента', required=False)
    surname = forms.CharField(label='фамилия', max_length=64)
    name = forms.CharField(label='имя', max_length=64, required=False)
    patronymic = forms.CharField(label='отчество', max_length=64, required=False)
    passport = forms.CharField(label='паспорт', max_length=128, required=False)
    another_document = forms.CharField(label='или другой документ', max_length=128, required=False)
    phone = forms.CharField(label='телефон', max_length=16, required=False)
    email = forms.EmailField(label='email', required=False)
    comment = forms.CharField(label='комментарий', max_length=256, initial='', required=False)


class ItemCreate(forms.Form):
    id_item = forms.IntegerField(label='ID')
    name_item = forms.CharField(label='наименование', max_length=24)
    unit_item = forms.CharField(label='единица измерения', max_length=16, required=False)
    recommended_minimum = forms.IntegerField(label='рекомендуемый минимум', required=False, min_value=0,
                                             max_value=10000)
    current_amount = forms.IntegerField(label='в наличии', min_value=0, max_value=10000)


class ItemEdit(ItemCreate):
    current_amount = forms.IntegerField(label='в наличии', required=False, min_value=0, max_value=10000,
                                        widget=forms.NumberInput(attrs={'autofocus': 'autofocus', }))
