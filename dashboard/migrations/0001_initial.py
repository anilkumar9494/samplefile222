# Generated by Django 5.0.3 on 2024-03-05 23:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Access_level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Addaccounttype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=400)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Addbrand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Addcurrency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=400)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Adddepartment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Addleadsregions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Addoffice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=200)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Agentusercreate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('firstname', models.CharField(max_length=100)),
                ('lastname', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('department', models.CharField(max_length=100)),
                ('office', models.CharField(max_length=100)),
                ('brandvisibility', models.CharField(max_length=100)),
                ('accesslevel', models.CharField(max_length=100)),
                ('leadsaccesslevel', models.CharField(max_length=100)),
                ('leadsregions', models.CharField(max_length=1000)),
                ('password', models.CharField(max_length=100)),
                ('confirmpassword', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Depositpaymentgetway',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('trans_id', models.CharField(max_length=100)),
                ('payment_status', models.CharField(max_length=100)),
                ('fees', models.FloatField()),
                ('amount', models.FloatField()),
                ('type', models.SmallIntegerField(default=0)),
                ('total_amount', models.FloatField()),
                ('currency', models.CharField(max_length=100)),
                ('additional_message', models.CharField(max_length=200)),
                ('member', models.CharField(max_length=100)),
                ('buyer', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('tawkuuid', models.CharField(max_length=500)),
                ('phpsessid', models.CharField(max_length=500)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Leads_access_level',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalesAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('enabled_state', models.BooleanField(blank=True, null=True)),
                ('default_state', models.BooleanField(blank=True, null=True)),
                ('country_list', models.CharField(blank=True, max_length=255, null=True)),
                ('promo_code', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SalesQueue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Securityque',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('name', models.CharField(max_length=300)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='transaction_ibmethod_mdl',
            fields=[
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('client_id', models.BigIntegerField(blank=True, null=True)),
                ('type', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('batch_number', models.CharField(max_length=100)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction_Method',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('type', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('batch_number', models.CharField(max_length=100)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
        migrations.CreateModel(
            name='Addsalesnotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('object_status', models.SmallIntegerField(choices=[(0, 'Active'), (1, 'Deleted')], default=0)),
                ('note', models.CharField(blank=True, max_length=1000, null=True)),
                ('client_id', models.CharField(blank=True, max_length=10, null=True)),
                ('created_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
