from django.urls import path
from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('get_front_desk', get_front_desk, name='get_front_desk'),
    path('get_order_form', get_order_form, name='get_order_form'),
    path('post_order_form', post_order_form, name='post_order_form'),
    path('get_client_from_base', get_client_from_base, name='get_client_from_base'),
    path('delete_order', delete_order, name='delete_order'),
    path('get_consumables_page', get_consumables_page, name='get_consumables_page'),
    path('get_consumable_panel', get_consumable_panel, name='get_consumable_panel'),
    path('delete_consumable_record', delete_consumable_record, name='delete_consumable_record'),
    path('create_consumable_form', create_consumable_form, name='create_consumable_form'),
    path('create_consumable_record', create_consumable_record, name='create_consumable_record'),
    path('save_consumable_record', save_consumable_record, name='save_consumable_record'),
    path('get_bar_page', get_bar_page, name='get_bar_page'),
    path('get_bar_panel', get_bar_panel, name='get_bar_panel'),
    path('delete_bar_record', delete_bar_record, name='delete_bar_record'),
    path('create_bar_form', create_bar_form, name='create_bar_form'),
    path('create_bar_record', create_bar_record, name='create_bar_record'),
    path('save_bar_record', save_bar_record, name='save_bar_record'),
    path('get_manage_page', get_manage_page, name='get_manage_page'),
    path('get_state_page', get_state_page, name='get_state_page'),

]
