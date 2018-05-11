from .models import CubesProductCard, CubesCategoryNodeGroup


from django.contrib import admin


@admin.register(CubesCategoryNodeGroup)
class CubesCategoryNodeGroupAdmin(admin.ModelAdmin):
    model = CubesCategoryNodeGroup
    list_display = ('name', 'order',)


@admin.register(CubesProductCard)
class CubesProductPageAdmin(admin.ModelAdmin):
    model = CubesProductCard
    list_per_page = 48
    search_fields = ('id', 'vendor_code', 'slug', 'model', 'name')
    list_display = ('public_id', 'vendor_code', 'name', 'is_published', 'is_in_stock', 'price')
    readonly_fields = ('url', 'id', 'public_id', 'vendor_code')
    fieldsets = (
        ('Основное', {'fields': (("name", "scoring"),
                                 ("public_id", "vendor_code"),
                                 ("slug", "url"),
                                 ('is_published', 'is_in_stock'),
                                 ('price', 'purchase_price')
                                 )
                      }
         ),
        ('Габариты', {'fields': (("height", "width", "length"), ('weigh')
                                 )
                      }
         )
    )
