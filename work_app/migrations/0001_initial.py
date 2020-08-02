# Generated by Django 2.0 on 2020-08-02 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BarItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('unit', models.CharField(blank=True, default='', max_length=16)),
                ('recommended_minimum', models.IntegerField(blank=True, default=0)),
                ('current_amount', models.IntegerField(blank=True, default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Bed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('surname', models.CharField(max_length=64)),
                ('name', models.CharField(blank=True, max_length=64)),
                ('patronymic', models.CharField(blank=True, default='', max_length=64)),
                ('passport', models.CharField(blank=True, default='', max_length=64)),
                ('another_document', models.CharField(blank=True, default='', max_length=128)),
                ('phone', models.CharField(blank=True, max_length=16)),
                ('email', models.EmailField(blank=True, default='', max_length=254)),
                ('comment', models.CharField(blank=True, default='', max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Consumables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=128)),
                ('unit', models.CharField(blank=True, default='', max_length=16)),
                ('recommended_minimum', models.IntegerField(blank=True, default=0)),
                ('current_amount', models.IntegerField(blank=True, default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=128)),
                ('register_date', models.DateTimeField()),
                ('instance', models.CharField(max_length=32)),
                ('action', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField()),
                ('date_stop', models.DateField()),
                ('is_reserved', models.BooleanField(default=False)),
                ('order_bed', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='work_app.Bed')),
                ('order_client', models.ForeignKey(default=42, on_delete=django.db.models.deletion.SET_DEFAULT, to='work_app.Client')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('capacity', models.IntegerField()),
                ('price', models.IntegerField()),
                ('number', models.CharField(max_length=10)),
            ],
        ),
        migrations.AddField(
            model_name='bed',
            name='bed_room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='work_app.Room'),
        ),
    ]