# Generated by Django 2.0.2 on 2018-05-01 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0003_attribute_provider'),
    ]

    operations = [
        migrations.AddField(
            model_name='terraformfile',
            name='provider',
            field=models.ForeignKey(default=None, on_delete=False, to='common.Provider'),
        ),
    ]
