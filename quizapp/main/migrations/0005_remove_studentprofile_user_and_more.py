# Generated by Django 4.1.7 on 2023-03-06 04:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_user_teacherprofile_studentprofile_student_teacher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='teacherprofile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='user',
            name='groups',
        ),
        migrations.RemoveField(
            model_name='user',
            name='user_permissions',
        ),
        migrations.DeleteModel(
            name='Student',
        ),
        migrations.DeleteModel(
            name='Teacher',
        ),
        migrations.DeleteModel(
            name='StudentProfile',
        ),
        migrations.DeleteModel(
            name='TeacherProfile',
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]