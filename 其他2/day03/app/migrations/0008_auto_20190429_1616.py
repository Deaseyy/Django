# Generated by Django 2.0.7 on 2019-04-29 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_auto_20190429_1516'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='g',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='stu', to='app.Grade'),
        ),
    ]
