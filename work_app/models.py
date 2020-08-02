from django.db import models
import re


class Log(models.Model):
    author = models.CharField(max_length=128)
    register_date = models.DateTimeField()
    instance = models.CharField(max_length=32)
    action = models.CharField(max_length=255)


class Item(models.Model):
    name = models.CharField(max_length=128, default='')
    unit = models.CharField(max_length=16, default='', blank=True)
    recommended_minimum = models.IntegerField(blank=True, default=0)
    current_amount = models.IntegerField(blank=True, default=0)

    class Meta:
        abstract = True

    def delta(self):
        return (self.current_amount if self.current_amount else 0) - (
            self.recommended_minimum if self.recommended_minimum else 0)


class Consumables(Item):
    pass


class BarItem(Item):
    pass


class Client(models.Model):
    surname = models.CharField(max_length=64)
    name = models.CharField(max_length=64, blank=True)
    patronymic = models.CharField(max_length=64, blank=True, default='')
    passport = models.CharField(max_length=64, blank=True, default='')
    another_document = models.CharField(max_length=128, blank=True, default='')
    phone = models.CharField(max_length=16, blank=True)
    email = models.EmailField(blank=True, default='')
    comment = models.CharField(max_length=256, default='', blank=True)

    def __str__(self):
        return self.surname + ' ' + (self.name[0] + '. ') if self.name else ' ' + (
                self.patronymic[0] + '.') if self.patronymic else ''

    # def all_client(self):
    #     return '{}, {}, {}'.format(self.__str__(), self.passport, self.phone)

    # def passport_slug(self):
    #     return re.compile('[^a-zA-Zа-яёА-ЯЁ0-9їЇіІ]').sub('', self.passport)


class Room(models.Model):
    capacity = models.IntegerField()
    price = models.IntegerField()
    number = models.CharField(max_length=10)

    def __str__(self):
        return 'кімната ' + self.number


class Bed(models.Model):
    bed_room = models.ForeignKey(Room, on_delete=models.CASCADE)
    number = models.IntegerField()

    def full_bed_name(self):
        return '{}.{}'.format(str(self.bed_room), str(self.number))

    def __str__(self):
        return '№ {}; ключ {}'.format(self.bed_room.number, self.number)


class Order(models.Model):
    order_client = models.ForeignKey(Client, on_delete=models.SET_DEFAULT, default=42)
    order_bed = models.ForeignKey(Bed, on_delete=models.CASCADE, default=1)
    date_start = models.DateField()
    date_stop = models.DateField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return '{}, {} {} - {}'.format(str(self.order_bed), str(self.order_client),
                                       str(self.date_start), str(self.date_stop))

    def daily_price(self):
        return self.order_bed.bed_room.price

    def save_order(self):
        self.save()
