# Generated by Django 5.1.7 on 2025-03-23 19:44

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
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Enwords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Ratings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('criteria', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Ruwords',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count_words', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dictionary.ratings')),
            ],
        ),
        migrations.CreateModel(
            name='Dictionary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dictionary.categories')),
                ('en_word', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dictionary.enwords')),
                ('ru_word', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dictionary.ruwords')),
            ],
        ),
        migrations.CreateModel(
            name='Userdictionaries',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('translate_choose_ru', models.BooleanField(default=False)),
                ('translate_choose_en', models.BooleanField(default=False)),
                ('translate_write_ru', models.BooleanField(default=False)),
                ('translate_write_en', models.BooleanField(default=False)),
                ('write_word_using_audio', models.BooleanField(default=False)),
                ('is_learn', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
                ('word', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='dictionary.dictionary')),
            ],
        ),
    ]
