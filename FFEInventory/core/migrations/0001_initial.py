# Generated by Django 5.0.7 on 2024-07-26 04:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Custody',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FFE_number', models.CharField(max_length=255, unique=True)),
                ('old_FFE', models.CharField(blank=True, max_length=255, null=True, unique=True)),
                ('item_type', models.CharField(choices=[('system unit', 'System Unit'), ('monitor', 'Monitor'), ('printer', 'Printer'), ('ups', 'UPS'), ('hub', 'Hub')], max_length=255)),
                ('processor', models.CharField(blank=True, max_length=255, null=True)),
                ('motherboard', models.CharField(blank=True, max_length=255, null=True)),
                ('memory', models.CharField(blank=True, max_length=255, null=True)),
                ('video_card', models.CharField(blank=True, max_length=255, null=True)),
                ('hard_disk', models.CharField(blank=True, max_length=255, null=True)),
                ('others', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('cost', models.CharField(blank=True, max_length=255, null=True)),
                ('date_purchased', models.DateField()),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('current_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='current_branch', to='core.branch')),
                ('custody', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.custody')),
                ('originating_branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='originating_branch', to='core.branch')),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('remark', models.TextField()),
                ('current_branch', models.CharField(blank=True, max_length=255, null=True)),
                ('custody', models.CharField(blank=True, max_length=255, null=True)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.item')),
            ],
        ),
    ]
