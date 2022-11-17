# Generated by Django 3.2.13 on 2022-11-16 14:46

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import imagekit.models.fields
import multiselectfield.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('naver_id', models.CharField(max_length=100, null=True, unique=True)),
                ('goo_id', models.CharField(max_length=50, null=True, unique=True)),
                ('press', multiselectfield.db.fields.MultiSelectField(choices=[(1, '가벼움'), (2, '무거움'), (3, '상관없음')], max_length=5, null=True)),
                ('weight', multiselectfield.db.fields.MultiSelectField(choices=[(1, '가벼움'), (2, '상관없음')], max_length=3, null=True)),
                ('array', multiselectfield.db.fields.MultiSelectField(choices=[(1, 'ten'), (2, 'tenkeyless'), (3, '상관없음')], max_length=5, null=True)),
                ('sound', multiselectfield.db.fields.MultiSelectField(choices=[(1, '소음'), (2, '저소음'), (3, '상관없음')], max_length=5, null=True)),
                ('rank', models.IntegerField(default=0)),
                ('connect', multiselectfield.db.fields.MultiSelectField(choices=[(1, '유'), (2, '무'), (3, '상관없음')], max_length=5, null=True)),
                ('image', imagekit.models.fields.ProcessedImageField(blank=True, upload_to='')),
                ('is_social', models.IntegerField(default=0)),
                ('notice', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('content', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('reception_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reception', to=settings.AUTH_USER_MODEL)),
                ('send_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='send', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
