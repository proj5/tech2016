# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-05 14:27
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('a2ausers', '0001_initial'),
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(max_length=400)),
                ('detail', models.TextField(blank=True, null=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('last_updated', models.DateTimeField(auto_now=True)),
                ('num_answers', models.IntegerField(default=0)),
                ('num_comments', models.IntegerField(default=0)),
                ('followed_by', models.ManyToManyField(blank=True, related_name='followed_questions', to='a2ausers.A2AUser')),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recent_questions', to='a2ausers.A2AUser')),
                ('topics', models.ManyToManyField(blank=True, related_name='questions', to='topics.Topic')),
            ],
        ),
    ]