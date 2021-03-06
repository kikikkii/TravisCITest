# Generated by Django 3.1.1 on 2020-11-26 09:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ticketModel', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Wxuser',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('openid', models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='concernFlight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('openid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='userInfo.wxuser', to_field='openid')),
                ('ticketId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ticketModel.tickets')),
            ],
        ),
    ]
