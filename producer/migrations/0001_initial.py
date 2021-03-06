# Generated by Django 3.1.2 on 2020-12-19 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('image', models.ImageField(upload_to='product_images')),
                ('ptype', models.CharField(choices=[('Pulses', 'Pulses'), ('Grains', 'Grains'), ('Vegetables', 'Vegetables')], max_length=20)),
                ('quantity', models.IntegerField()),
                ('ready_to_dispatch', models.BooleanField()),
                ('added_on', models.DateTimeField(auto_now_add=True)),
                ('added_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
