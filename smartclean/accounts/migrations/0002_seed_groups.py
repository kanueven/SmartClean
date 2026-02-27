# Create a new file: yourapp/migrations/0002_seed_groups.py

from django.db import migrations

def create_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    for name in ['client', 'cleaner', 'admin']:
        Group.objects.get_or_create(name=name)

def remove_groups(apps, schema_editor):
    Group = apps.get_model('auth', 'Group')
    Group.objects.filter(name__in=['client', 'cleaner', 'admin']).delete()

class Migration(migrations.Migration):
    dependencies = [
        
        ('accounts' ,'0003_remove_user_role'),
    ]
    operations = [
        migrations.RunPython(create_groups, remove_groups),
    ]