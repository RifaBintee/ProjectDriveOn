# Generated by Django 4.2.4 on 2023-10-07 19:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carInfo', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Rent_Car_Record',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rent_time', models.DateTimeField()),
                ('return_time', models.DateTimeField()),
                ('pickup_loc', models.CharField(max_length=100)),
                ('rent_car_id', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='carInfo.rental_car')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
