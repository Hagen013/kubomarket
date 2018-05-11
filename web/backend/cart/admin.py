from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import Order, OrderItem, Order2
from django.db import models
from django.forms import TextInput, Textarea


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ('name', 'vendor_code', 'full_url', 'quantity', 'price', 'total_price')


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'customer_name', 'email',
                    'phone_number', 'created_at', 'modified_at', 'state')

    fieldsets = (
        ('Личные данные', {'fields': (("customer_name", "email", "phone_number"),
                                      ("client_notes", "address")),
                           }
         ),
        ('Доставка', {'fields': (("delivery_mode_selected", "delivery_mode", "delivery_code"),)
                      }
         ),
        # ('Даты', {'fields': ("created_at", "modified_at")}),
        ('Служебная информация', {'fields': (("managet_notes", "state"),
                                             ),
                                  }
         ),

    )
    inlines = [OrderItemInline]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'size': '20'})},
        models.TextField: {'widget': Textarea(attrs={'rows': 4, 'cols': 40})},
    }


from django.contrib.postgres.fields import JSONField
from jsoneditor.forms import JSONEditor


class Order2Admin(admin.ModelAdmin):
    model = Order2

    list_display = ('__str__', 'created_at', 'modified_at', 'source', 'state')
    formfield_overrides = {
        JSONField: {'widget': JSONEditor},
    }
    readonly_fields = ('created_at', 'modified_at')

admin.site.register(Order, OrderAdmin)
admin.site.register(Order2, Order2Admin)
