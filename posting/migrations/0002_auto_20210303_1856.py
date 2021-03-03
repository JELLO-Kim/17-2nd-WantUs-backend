# Generated by Django 3.1.7 on 2021-03-03 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('posting', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='like',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
        migrations.AddField(
            model_name='jobcategory',
            name='occupation',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.occupation'),
        ),
        migrations.AddField(
            model_name='companytag',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.company'),
        ),
        migrations.AddField(
            model_name='companytag',
            name='tag_detail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.tagdetail'),
        ),
        migrations.AddField(
            model_name='companyimage',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.company'),
        ),
        migrations.AddField(
            model_name='company',
            name='tag',
            field=models.ManyToManyField(through='posting.CompanyTag', to='posting.TagDetail'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='posting',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posting.posting'),
        ),
        migrations.AddField(
            model_name='bookmark',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.user'),
        ),
    ]
