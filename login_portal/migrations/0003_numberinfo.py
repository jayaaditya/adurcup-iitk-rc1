# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-12 22:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login_portal', '0002_modelinfo_ipaddr'),
    ]

    operations = [
        migrations.CreateModel(
            name='Numberinfo',
            fields=[
                ('modelinfo_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='login_portal.Modelinfo')),
                ('number', models.CharField(max_length=12)),
            ],
            bases=('login_portal.modelinfo',),
        ),
    ]