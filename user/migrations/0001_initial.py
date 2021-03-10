# Generated by Django 3.1.7 on 2021-03-10 16:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posting', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'skills',
            },
        ),
        migrations.CreateModel(
            name='SocialStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'social_statuses',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50, unique=True)),
                ('phone_number', models.CharField(max_length=50, null=True, unique=True)),
                ('is_spam', models.BooleanField(default=True)),
                ('image_url', models.URLField(max_length=2000, null=True)),
                ('salary', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'db_table': 'users',
            },
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'db_table': 'work_experiences',
            },
        ),
        migrations.CreateModel(
            name='UserSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.skill')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'user_skills',
            },
        ),
        migrations.CreateModel(
            name='UserJobCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('job_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.jobcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user')),
            ],
            options={
                'db_table': 'user_job_categories',
            },
        ),
        migrations.AddField(
            model_name='user',
            name='job_category',
            field=models.ManyToManyField(through='user.UserJobCategory', to='posting.JobCategory'),
        ),
        migrations.AddField(
            model_name='user',
            name='skill',
            field=models.ManyToManyField(through='user.UserSkill', to='user.Skill'),
        ),
        migrations.AddField(
            model_name='user',
            name='social_status',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.socialstatus'),
        ),
        migrations.AddField(
            model_name='user',
            name='work_experience',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user.workexperience'),
        ),
        migrations.CreateModel(
            name='Recommand',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommander', to='user.user')),
                ('to_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommanded_person', to='user.user')),
            ],
            options={
                'db_table': 'recommands',
            },
        ),
    ]
