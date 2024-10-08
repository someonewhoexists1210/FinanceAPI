# Generated by Django 5.1 on 2024-08-16 07:20

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_budgetgoal_date_created_budgetgoal_spent_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='transactions', to='user.budgetgoal'),
        ),
        migrations.AlterField(
            model_name='budgetgoal',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
