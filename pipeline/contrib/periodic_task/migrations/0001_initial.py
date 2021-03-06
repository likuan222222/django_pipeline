# Generated by Django 2.2.4 on 2019-08-23 06:56

from django.db import migrations, models
import django.db.models.deletion
import pipeline.models
import timezone_field.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pipeline', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CrontabSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('minute', models.CharField(default='*', max_length=64, verbose_name='minute')),
                ('hour', models.CharField(default='*', max_length=64, verbose_name='hour')),
                ('day_of_week', models.CharField(default='*', max_length=64, verbose_name='day of week')),
                ('day_of_month', models.CharField(default='*', max_length=64, verbose_name='day of month')),
                ('month_of_year', models.CharField(default='*', max_length=64, verbose_name='month of year')),
                ('timezone', timezone_field.fields.TimeZoneField(default='UTC')),
            ],
            options={
                'verbose_name': 'crontab',
                'verbose_name_plural': 'crontabs',
                'ordering': ['month_of_year', 'day_of_month', 'day_of_week', 'hour', 'minute'],
            },
        ),
        migrations.CreateModel(
            name='DjCeleryPeriodicTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Useful description', max_length=200, unique=True, verbose_name='name')),
                ('task', models.CharField(max_length=200, verbose_name='task name')),
                ('args', models.TextField(blank=True, default='[]', help_text='JSON encoded positional arguments', verbose_name='Arguments')),
                ('kwargs', models.TextField(blank=True, default='{}', help_text='JSON encoded keyword arguments', verbose_name='Keyword arguments')),
                ('queue', models.CharField(blank=True, default=None, help_text='Queue defined in CELERY_QUEUES', max_length=200, null=True, verbose_name='queue')),
                ('exchange', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='exchange')),
                ('routing_key', models.CharField(blank=True, default=None, max_length=200, null=True, verbose_name='routing key')),
                ('expires', models.DateTimeField(blank=True, null=True, verbose_name='expires')),
                ('enabled', models.BooleanField(default=True, verbose_name='enabled')),
                ('last_run_at', models.DateTimeField(blank=True, editable=False, null=True)),
                ('total_run_count', models.PositiveIntegerField(default=0, editable=False)),
                ('date_changed', models.DateTimeField(auto_now=True)),
                ('description', models.TextField(blank=True, verbose_name='description')),
                ('crontab', models.ForeignKey(blank=True, help_text='Use one of interval/crontab', null=True, on_delete=django.db.models.deletion.CASCADE, to='periodic_task.CrontabSchedule', verbose_name='crontab')),
            ],
            options={
                'verbose_name': 'djcelery periodic task',
                'verbose_name_plural': 'djcelery periodic tasks',
            },
        ),
        migrations.CreateModel(
            name='DjCeleryPeriodicTasks',
            fields=[
                ('ident', models.SmallIntegerField(default=1, primary_key=True, serialize=False, unique=True)),
                ('last_update', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='IntervalSchedule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('every', models.IntegerField(verbose_name='every')),
                ('period', models.CharField(choices=[('days', 'Days'), ('hours', 'Hours'), ('minutes', 'Minutes'), ('seconds', 'Seconds'), ('microseconds', 'Microseconds')], max_length=24, verbose_name='period')),
            ],
            options={
                'verbose_name': 'interval',
                'verbose_name_plural': 'intervals',
                'ordering': ['period', 'every'],
            },
        ),
        migrations.CreateModel(
            name='PeriodicTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='周期任务名称')),
                ('cron', models.CharField(max_length=128, verbose_name='调度策略')),
                ('total_run_count', models.PositiveIntegerField(default=0, verbose_name='执行次数')),
                ('last_run_at', models.DateTimeField(null=True, verbose_name='上次运行时间')),
                ('creator', models.CharField(default='', max_length=32, verbose_name='创建者')),
                ('extra_info', pipeline.models.CompressJSONField(null=True, verbose_name='额外信息')),
                ('celery_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='periodic_task.DjCeleryPeriodicTask', verbose_name='celery 周期任务实例')),
                ('snapshot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='periodic_tasks', to='pipeline.Snapshot', verbose_name='用于创建流程实例的结构数据')),
                ('template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='periodic_tasks', to='pipeline.PipelineTemplate', to_field='template_id', verbose_name='周期任务对应的模板')),
            ],
        ),
        migrations.CreateModel(
            name='PeriodicTaskHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ex_data', models.TextField(verbose_name='异常信息')),
                ('start_at', models.DateTimeField(auto_now_add=True, verbose_name='开始时间')),
                ('start_success', models.BooleanField(default=True, verbose_name='是否启动成功')),
                ('periodic_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='instance_rel', to='periodic_task.PeriodicTask', verbose_name='周期任务')),
                ('pipeline_instance', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='periodic_task_rel', to='pipeline.PipelineInstance', to_field='instance_id', verbose_name='Pipeline 实例')),
            ],
        ),
        migrations.AddField(
            model_name='djceleryperiodictask',
            name='interval',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='periodic_task.IntervalSchedule', verbose_name='interval'),
        ),
    ]
