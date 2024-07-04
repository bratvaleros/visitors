from django.db import migrations, models
import django.db.models.deletion as deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Наименование подразделения')),
                ('parent', models.ForeignKey(on_delete=deletion.CASCADE, blank=True, null=True,
                                             verbose_name='Входит в состав',  related_name='departments',
                                             to='departments.department')),
            ],
            options={
                'verbose_name': 'Подразделение',
                'verbose_name_plural': 'Подразделения',
            },
        ),
    ]
