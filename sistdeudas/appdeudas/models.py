from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext as _
import uuid
import datetime

class EstadoModelo:
    ACTIVO = 'A'
    INACTIVO = 'I'
    ELIMINADO = '*'
    ESTADOS = (
        (ACTIVO, 'Activo'),
        (INACTIVO, 'Inactivo'),
        (ELIMINADO, 'Eliminado'),
    )

class TipoPedido:
    CONTADO = 'C'
    CREDITO = 'D'
    TIPOS = (
        (CONTADO, 'Contado'),
        (CREDITO, 'A crédito'),
    )

class MetodoPago:
    EFECTIVO = 'E'
    TARJETA = 'T'
    BILLETERA = 'B'
    METODOS = (
        (EFECTIVO, 'Efectivo'),
        (TARJETA, 'Tarjeta'),
        (BILLETERA, 'Billetera Virtual'),
    )

class TipoTrabajador:
    COBRADOR = 'C'
    VENDEDOR = 'V'
    ADMINISTRADOR = 'A'
    TIPOS = (
        (COBRADOR, 'Cobrador'),
        (VENDEDOR, 'Vendedor'),
        (ADMINISTRADOR, 'Administrador')
    )

class Proveedor(models.Model):
    nombre = models.CharField(max_length=40)
    estado = models.CharField(max_length=1, choices=EstadoModelo.ESTADOS, default=EstadoModelo.ACTIVO)

class Producto(models.Model):
    def generate_codigo():
        return uuid.uuid4().hex[:8].upper()

    codigo = models.CharField(max_length=8, primary_key=True, unique=True, default=generate_codigo, editable=False)
    nombre = models.CharField(max_length=40)
    descripcion = models.TextField()
    proveedor = models.ForeignKey(Proveedor, on_delete=models.PROTECT)
    precio = models.DecimalField(max_digits=7, decimal_places=2, default=0.00)
    estado = models.CharField(max_length=1, choices=EstadoModelo.ESTADOS, default=EstadoModelo.ACTIVO)

class UsuarioPersonalizado(AbstractUser):
    dni = models.CharField(max_length=20, blank=True)
    direccion = models.CharField(max_length=100, blank=True)

    groups = models.ManyToManyField(Group, verbose_name=_('groups'), blank=True, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, verbose_name=_('user permissions'), blank=True, related_name='custom_user_set')

class Trabajador(models.Model):
    usuario = models.OneToOneField(UsuarioPersonalizado, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    tipo = models.CharField(max_length=1, choices=TipoTrabajador.TIPOS)
    estado = models.CharField(max_length=1, choices=EstadoModelo.ESTADOS, default=EstadoModelo.ACTIVO)

    def asignar_grupo_y_permisos(self):
        grupo, creado = Group.objects.get_or_create(name=f'{self.get_tipo_display()}s')
        self.usuario.groups.add(grupo)

class Cliente(models.Model):
    usuario = models.OneToOneField(UsuarioPersonalizado, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10)
    nombre = models.CharField(max_length=100)
    correo = models.EmailField()
    habilitado_para_credito = models.BooleanField(default=False)
    limite_credito = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    archivo = models.FileField(upload_to='archivos/clientes/', null=True, blank=True)  # Campo para guardar la ubicación del archivo
    estado = models.CharField(max_length=1, choices=EstadoModelo.ESTADOS, default=EstadoModelo.ACTIVO)

    def asignar_grupo(self):
        grupo, creado = Group.objects.get_or_create(name='Clientes')
        self.usuario.groups.add(grupo)

class Pedido(models.Model):
    def generate_pedido_number():
        year = datetime.datetime.now().strftime("%y")
        last_pedido = Pedido.objects.filter(numero_pedido__startswith=year).order_by('-numero_pedido').first()
        if last_pedido:
            last_number = int(last_pedido.numero_pedido[2:])
            new_number = last_number + 1
        else:
            new_number = 1
        return f"{year}{new_number:04d}"

    numero_pedido = models.CharField(max_length=8, primary_key=True, default=generate_pedido_number, editable=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    tipo_pedido = models.CharField(max_length=1, choices=TipoPedido.TIPOS)
    metodo_pago = models.CharField(max_length=1, choices=MetodoPago.METODOS)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    productos = models.ManyToManyField(Producto)
    estado = models.CharField(max_length=1, choices=EstadoModelo.ESTADOS, default=EstadoModelo.ACTIVO)

class Cronograma(models.Model):
    pedido = models.OneToOneField(Pedido, on_delete=models.CASCADE, related_name='cronograma')
    plazos = models.IntegerField()
    importe_cuota = models.DecimalField(max_digits=10, decimal_places=2)
    importe_saldo_pendiente = models.DecimalField(max_digits=10, decimal_places=2)
    importe_saldado = models.DecimalField(max_digits=10, decimal_places=2)