# Generated by Django 3.2 on 2023-06-11 13:41

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import myauth.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='ChildCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('main_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myauth.category')),
            ],
        ),
        migrations.CreateModel(
            name='Classifieds',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('content', models.TextField()),
                ('phone_number', models.CharField(max_length=30)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('verify', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ClassifiedsTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('bio', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('store_bio', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ClassifiedsUtils',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new', models.BooleanField(blank=True, null=True)),
                ('delivery', models.BooleanField(blank=True, null=True)),
                ('main_classifieds', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myauth.classifieds')),
            ],
        ),
        migrations.AddField(
            model_name='classifieds',
            name='Country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myauth.country'),
        ),
        migrations.AddField(
            model_name='classifieds',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myauth.childcategory'),
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(db_index=True, error_messages={'unique': 'This email has already registered. Choose another one, please'}, max_length=255, unique=True, verbose_name='email address')),
                ('phone_number', models.CharField(error_messages={'unique': 'This phone number has already registered. Choose another one, please'}, max_length=15, null=True, validators=[myauth.models.PhoneNumberValidator()], verbose_name='phone number')),
                ('first_name', models.CharField(max_length=60, verbose_name='first name')),
                ('last_name', models.CharField(max_length=60, verbose_name='last name')),
                ('is_staff', models.BooleanField(blank=True, default=False, help_text='Designates whether the user can log into this admin site.', null=True, verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            managers=[
                ('objects', myauth.models.MyUserManager()),
            ],
        ),
    ]