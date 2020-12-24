# Generated by Django 3.1.3 on 2020-12-23 06:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('Crm', '0005_auto_20201221_2314'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enquiry',
            name='Enquiry_number',
            field=models.CharField(blank=True, default='ZAPKWFAVSN', max_length=100, unique=True),
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enquiry_status_time', models.DateField(auto_now_add=True)),
                ('Visit_status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Crm.client_visit', verbose_name='enquiry status')),
                ('enquiry_number', models.ForeignKey(on_delete=django.db.models.expressions.Case, to='Crm.enquiry', verbose_name='Enquiry Number ')),
                ('update_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Update By')),
            ],
        ),
    ]
