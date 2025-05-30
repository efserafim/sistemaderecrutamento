# Generated by Django 5.2 on 2025-05-01 14:09

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_letter', models.TextField()),
                ('status', models.CharField(choices=[('APPLIED', 'Candidatado'), ('REVIEWING', 'Em análise'), ('SHORTLISTED', 'Pré-selecionado'), ('REJECTED', 'Rejeitado'), ('HIRED', 'Contratado')], default='APPLIED', max_length=20)),
                ('applied_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('recruiter_notes', models.TextField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-applied_at'],
            },
        ),
        migrations.CreateModel(
            name='Job',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('company', models.CharField(max_length=100)),
                ('location', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('requirements', models.TextField()),
                ('salary_range', models.CharField(blank=True, max_length=100, null=True)),
                ('job_type', models.CharField(choices=[('FULL_TIME', 'Integral'), ('PART_TIME', 'Parcial'), ('CONTRACT', 'Contrato'), ('INTERNSHIP', 'Estágio')], max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('deadline', models.DateTimeField(default=django.utils.timezone.now)),
                ('is_active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
    ]
