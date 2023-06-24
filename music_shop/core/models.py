from django.db import models

class InstrumentCategory(models.Model):
    name = models.CharField('Название', max_length=100)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

class Instrument(models.Model):
    name = models.CharField('Название', max_length=100)
    category = models.ForeignKey(InstrumentCategory, on_delete=models.CASCADE, verbose_name='Категория')
    price = models.DecimalField('Цена', max_digits=8, decimal_places=2)
    description = models.TextField('Описание')
    is_available = models.BooleanField('В наличии', default=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Инструмент'
        verbose_name_plural = 'Инструменты'
        #ordering = ('name',)