from odoo import fields, api, models
from datetime import datetime, date

class pagos(models.Model):
    _name = "soulschool.pagos"
    _description = "soulschool.pagos"
    _rec_name = "nombre_referencia"

    nombre_cliente = fields.Many2one(
        comodel_name="soulschool.alumnos_order",
        string="Línea curso"
    )
    alumno = fields.Char(
        string="Alumno",
        related='nombre_cliente.alumnos_id.nombre'
    )
    edad = fields.Boolean(
        related='nombre_cliente.alumnos_id.edad'
    )
    dni_tutor = fields.Char(
        string="DNI padre o madre",
        related='nombre_cliente.alumnos_id.dni_tutor'
    )
    nombre_tutor = fields.Char(
        string="Nombre padre o madre",
        related='nombre_cliente.alumnos_id.nombre_tutor'
    )
    viene_empresa = fields.Boolean(
        related="nombre_cliente.alumnos_id.empresa_"
    )
    empresa_alumno = fields.Char(
        string="Empresa",
        related="nombre_cliente.alumnos_id.empresa_id.nombre_empresa"
    )
    cif_empresa_alumno = fields.Char(
        string="CIF",
        related="nombre_cliente.alumnos_id.empresa_id.cif_empresa"
    )
    dni_alumno = fields.Char(
        string="Dni",
        related='nombre_cliente.alumnos_id.dni'
    )
    curso = fields.Char(
        string="Curso",
        related='nombre_cliente.curso_id.nombre_curso'
    )
    cantidad = fields.Float(
        string="Cuantía",
        default=25
    )
    es_matricula = fields.Boolean(
        default=False,
        string="Es matrícula"
    )
    tipo_pago = fields.Selection([
        ('mensual', 'Mensual'),
        ('total', 'Total'),
        ],
        string="Tipo de Pago",
        related='nombre_cliente.tipo_pago'
    )
    fecha_pago = fields.Date(
        string="Fecha"
    )
    mes_fecha_pago = fields.Integer(
        string="Mes de pago",
        compute="_get_mes_pago"
    )
    metodo_pago = fields.Selection([
        ('tarjeta','TPV'),
        ('efectivo','Efectivo'),
        ('transfer','Transferencia'),
        ],
        string="Método de pago",
        default="tarjeta"
    )
    factura = fields.Boolean(
        string="Contiene Factura",
        default=False
    )
    num_factura = fields.Char(
        string="Número de Factura",
    )
    fecha_factura = fields.Date(
        string="Fecha Factura"
    )
    descuento_factura = fields.Integer(
        string="Descuento",
    )
    iva_factura = fields.Integer(
        string="IVA",
    )
    nota_factura = fields.Text(
        string="Notas de la factura",
    )
    baseImponible_factura = fields.Integer(
        string="Base imponible",
        compute="_get_baseImponible"
    )
    total_factura = fields.Float(
        string="Total",
        compute="_get_total"
    )

    nombre_referencia = fields.Char(
        string="Referencia Interna",
        compute="_compute_name"
    )
    @api.depends('fecha_pago')
    def _get_mes_pago(self):
        for rec in self:
            rec.mes_fecha_pago = int((rec.fecha_pago).month)

    @api.depends('fecha_pago')
    def _compute_name(self):
        for rec in self:
            rec.nombre_referencia = str(rec.nombre_cliente.alumnos_id.nombre) + " " + str(rec.nombre_cliente.alumnos_id.apellidos) + " " + str(rec.nombre_cliente.alumnos_id.dni) + " [" + str(rec.nombre_cliente.curso_id.nombre_curso) + " - " + str(rec.fecha_pago.strftime("%d/%m/%y")) + "]"

    @api.depends('cantidad','descuento_factura')
    def _get_baseImponible(self):
        for rec in self:
            descuento = (rec.cantidad * rec.descuento_factura) / 100
            rec.baseImponible_factura = rec.cantidad - descuento
    
    @api.depends('iva_factura','cantidad','baseImponible_factura')
    def _get_total(self):
        for rec in self:
            iva = (rec.baseImponible_factura * rec.iva_factura) / 100
            rec.total_factura = rec.baseImponible_factura + iva