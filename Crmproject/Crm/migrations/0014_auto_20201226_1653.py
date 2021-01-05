# Generated by Django 3.1.3 on 2020-12-26 11:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Crm', '0013_auto_20201225_1229'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='history',
            name='enquiry_number',
        ),
        migrations.AddField(
            model_name='history',
            name='Contact_number',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Crm.enquiry', verbose_name='Contact Number '),
        ),
        migrations.AlterField(
            model_name='enquiry',
            name='Enquiry_number',
            field=models.CharField(blank=True, default='QFKWMILGVG', max_length=100, unique=True),
        ),
    ]