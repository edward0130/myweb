# Generated by Django 4.1.4 on 2023-01-07 07:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrettyNum',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=32, verbose_name='电话号码')),
                ('price', models.IntegerField(default=0, verbose_name='价钱')),
                ('level', models.SmallIntegerField(choices=[(1, '一级'), (2, '二级')], default=1, verbose_name='等级')),
                ('status', models.SmallIntegerField(choices=[(1, '未占用'), (2, '已占用')], default=1, verbose_name='状态')),
            ],
        ),
        migrations.AlterField(
            model_name='userinfo',
            name='depart',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.department', verbose_name='部门'),
        ),
    ]