# Generated by Django 4.0 on 2021-12-23 09:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_comment_post_alter_comment_reply_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created',)},
        ),
    ]
