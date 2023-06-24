from django.contrib import admin
from django.shortcuts import redirect
from core.models import Instrument, InstrumentCategory
from django.urls import reverse
from django.utils.http import urlencode
from django.utils.html import format_html
from django import forms
from django.db.models import QuerySet

import pandas as pd


admin.site.site_title = "Админ-панель магазина музыкальных инструментов 🎸"
admin.site.site_header = "Админ-панель магазина музыкальных инструментов 🎸"


class InstrumentInline(admin.TabularInline): #TabularInline
    model = Instrument


class InstrumentAdminForm(forms.ModelForm):
    class Meta:
        model = Instrument
        fields = "__all__"
        
    def clean_price(self):
        if self.cleaned_data["price"] < 100:
            raise forms.ValidationError("Цена маловата...")
        return self.cleaned_data["price"]
# ...


@admin.register(Instrument)
class InstrumentAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'category', 'price', 'description', 'is_available', ) #'show_discount'
    list_filter = ('category', )
    search_fields = ('name__startswith',)
    fields = ('name', 'description', 'category', 'price', )
    ordering = ('-price', )
    list_editable = ('is_available', 'price', )
    
    actions = ('export_data_to_excel', )
    
    form = InstrumentAdminForm
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["price"].label = "Цена (не меньше 100р.):"
        return form
    
    @admin.action(description='Экспортировать в Excel')
    def export_data_to_excel(self, request, qs: QuerySet):
        data = []
        
        for obj in qs:
            data.append({
                "ID": obj.id,
                "Название": obj.name,
                "Описание": obj.description,
                "Категория": obj.category,
                "Цена": obj.price,
                "В наличии": obj.is_available,
            })
        sorted_data = sorted(data, key=lambda x: x["ID"])  # Сортировка по полю "ID"
        pd.DataFrame(sorted_data).to_excel('instruments.xlsx', index=False)
        
        

    #def show_discount(self, obj):
    #    from django.utils.html import format_html
    #    instrument = obj
    #    discount = 0.5
    #    result = int(instrument.price) - int(instrument.price) * discount
    #    return format_html("<b><i>{}</i></b>",f'{result:10.2f}')

    #show_discount.short_description = 'Цена со скидкой'


@admin.register(InstrumentCategory)
class InstrumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'view_instruments_link')
    
    inlines = [
        InstrumentInline,
    ]
    
    def view_instruments_link(self, obj):
        count = obj.instrument_set.count()
        url = (
            reverse("admin:core_instrument_changelist")
            + "?"
            + urlencode({"category__id": f"{obj.id}"})
        )
        return format_html('<a href="{}">{} Инструмента</a>', url, count)
    
    view_instruments_link.short_description = "Инструменты"