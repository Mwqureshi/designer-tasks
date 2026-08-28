import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=500)),
                ('is_urgent', models.BooleanField(default=False)),
                ('deadline', models.DateField(blank=True, null=True)),
                ('added_by', models.CharField(choices=[('waleed', 'Waleed'), ('adnan', 'Adnan'), ('hamid', 'Hamid'), ('zain', 'Zain')], max_length=20)),
                ('status', models.CharField(choices=[('available', 'Available'), ('active', 'Active'), ('paused', 'Paused'), ('done', 'Done')], default='available', max_length=20)),
                ('assigned_to', models.CharField(blank=True, choices=[('adnan', 'Adnan'), ('hamid', 'Hamid'), ('zain', 'Zain')], max_length=20, null=True)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('started_at', models.DateTimeField(blank=True, null=True)),
                ('completed_at', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'ordering': ['-is_urgent', 'deadline', 'created_at'],
            },
        ),
    ]
