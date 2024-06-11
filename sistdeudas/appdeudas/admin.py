from django.contrib import admin
from .models import Producto, Pedido, Proveedor, Cronograma, Trabajador, Cliente

class ProductoAdmin(admin.ModelAdmin):
    readonly_fields = ('codigo',)

    fieldsets = (
        ('Detalles del Producto', {
            'fields': ('codigo', 'nombre', 'descripcion', 'proveedor', 'precio', 'estado')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Asegura que el campo codigo permanezca sin cambios
        if change:
            obj.codigo = Producto.objects.get(pk=obj.pk).codigo
        super().save_model(request, obj, form, change)

class PedidoAdmin(admin.ModelAdmin):
    readonly_fields = ('numero_pedido',)

    fieldsets = (
        ('Detalles del Pedido', {
            'fields': ('numero_pedido', 'cliente', 'fecha', 'tipo_pedido', 'metodo_pago', 'total', 'productos', 'estado')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Asegura que el campo numero_pedido permanezca sin cambios
        if change:
            obj.numero_pedido = Pedido.objects.get(pk=obj.pk).numero_pedido
        super().save_model(request, obj, form, change)

admin.site.register(Producto, ProductoAdmin)
admin.site.register(Pedido, PedidoAdmin)
admin.site.register(Proveedor)
admin.site.register(Cronograma)
admin.site.register(Trabajador)
admin.site.register(Cliente)
