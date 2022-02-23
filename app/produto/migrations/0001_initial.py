# Generated by Django 4.0.1 on 2022-02-23 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Produto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=255, verbose_name='Nome')),
                ('descricao_curta', models.TextField(max_length=255, verbose_name='Descrição Curta')),
                ('descricao_longa', models.TextField(verbose_name='Descrição Longa')),
                ('imagem', models.ImageField(blank=True, null=True, upload_to='pictures/%Y/%m/', verbose_name='Imagem')),
                ('slug', models.SlugField(unique=True, verbose_name='Apelido')),
                ('preco_marketing', models.FloatField(verbose_name='Preço')),
                ('preco_marketing_promocional', models.FloatField(blank=True, null=True, verbose_name='Preço Promocional')),
                ('tipo', models.CharField(choices=[('V', 'Variação'), ('S', 'Simples')], default='V', max_length=1)),
            ],
        ),
    ]
