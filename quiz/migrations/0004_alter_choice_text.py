# Generated by Django 5.2.1 on 2025-06-05 20:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_question_quiz_result_userresponse'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='text',
            field=models.CharField(max_length=255),
        ),
    ]
