# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
import csv

class alumnos(models.Model):
    _name = 'soulschool.alumnos'
    _description = 'soulschool.alumnos'
    _rec_name = 'nombre_referencia'

    _sql_constraints = [
        ('dni_unique', 'unique(dni)', 'El valor del campo DNI ya existe.')
    ]

    nombre = fields.Char(
        string="Nombre"
    )
    apellidos = fields.Char(
        string="Apellidos"
    )
    direccion = fields.Char(
        string="Calle"
    )
    state_id = fields.Many2one(
        'res.country.state',
        string="Provincia",
        domain="[('country_id', '=?', country_id)]"
    )
    codigo_postal = fields.Char(
        string="Codigo Postal"
    )
    localidad = fields.Char(
        string="Localidad"
    )
    telefono = fields.Char(
        string="Telefono"
    )
    telefono_tutor = fields.Char(
        string="Telefono padre o madre"
    )
    email_tutor = fields.Char(
        string="Email padre o madre"
    )
    email = fields.Char(
        string="Email"
    )
    dni = fields.Char(
        "DNI",
        )
    edad = fields.Boolean(
        "Es mayor de edad", 
        default=False
        )
    edad_ = fields.Boolean(
        "Es mayor de edad pero se lo paga un padre/madre", 
        default=False
        )
    empresa_ = fields.Boolean(
        "Viene de Empresa",
        default=False
        )
    dni_tutor = fields.Char(
        string="Dni padre o madre"
    )
    nombre_tutor = fields.Char(
        string="Nombre padre o madre"
    )
    order_line = fields.One2many(
        "soulschool.alumnos_order",
        "alumnos_id",
        string="Cursos"
    )
    empresa_id = fields.Many2one(
        comodel_name='soulschool.empresas',
        string="Empresa"
        )
    nombre_empresa = fields.Char(
        related="empresa_id.nombre_empresa",
        string='Nombre Empresa'
    )
    cif_empresa = fields.Char(
        related="empresa_id.cif_empresa",
        string='CIF'
    )
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Pais'
        )
    fecha_pago = fields.Date(
        string="Fecha de pago",
        related='order_line.fecha_pago'
    )
    fecha_actual = fields.Datetime(
        string="Fecha actual",
        compute="_get_fecha_actual"
    )
    metodo_pago = fields.Selection([
        ('tarjeta','TPV'),
        ('efectivo','Efectivo'),
        ('transfer','Transferencia'),
        ],
        related="order_line.metodo_pago",
        string="Metodo de Pago"

    )
    horario_dias = fields.Selection([
        ('uno','Lunes - Miércoles'),
        ('dos','Martes - Jueves'),
        ('tres','Lunes - Jueves'),
        ('cuatro','Miércoles - Jueves'),
        ('cinco','Lunes - Viernes'),
        ('siete', 'Lunes'),
        ('ocho', 'Martes'),
        ('nueve', 'Miércoles'),
        ('diez', 'Jueves'),
        ('seis', 'Viernes'),
        ],
        string="Días"
    )
    horario_horas = fields.Selection([
        ('primera','12:00 - 13:30'),
        ('segunda','16:00 - 17:30'),
        ('tercera','17:30 - 19:00'),
        ('cuarta','19:00 - 20:30'),
        ('quinta', '16:00 - 19:00'),
        ('sexta', '17:30 - 20:30')
        ],
        string="Horas"
    )
    foto = fields.Binary(string="Imagen")

    nombre_referencia = fields.Char(
        string="Referencia Interna",
        compute="_compute_name"
    )
    @api.depends('nombre','dni')
    def _compute_name(self):
        for rec in self:
            rec.nombre_referencia = str(rec.nombre) + " " + str(rec.apellidos) + '  [' + str(rec.dni) + '] '

    def _get_fecha_actual(self):
        for rec in self:
            rec.fecha_actual = datetime.today()

    def _get_backup_csv(self):
        registros = self.search([])
        with open('/home/administrador/Escritorio/Backups_odoo/backup_alumnos.csv', 'w', newline='') as csvfile:
            campo_nombres = ['Nombre', 'Apellidos', 'Calle', 'Provincia', 'Codigo postal',
                              'Localidad', 'Telefono', 'Telefono padre o madre',
                              'Email padre o madre', 'Email', 'DNI', 'Es mayor de edad',
                              'Es mayor de edad pero se lo paga un padre/madre',
                              'Viene de Empresa', 'Dni padre o madre', 'Nombre padre o madre',
                              'Cursos', 'Empresa', 'Pais', 'Dias', 'Horas']
            # campo_nombres = ['Nombre', 'Apellidos']

            writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)

            # Escribir encabezados al archivo CSV
            writer.writeheader()

            # Escribir datos al archivo CSV
            for registro in registros:
                writer.writerow({
                    'Nombre': registro.nombre, 'Apellidos': registro.apellidos,
                    'Calle': registro.direccion, 'Provincia': registro.state_id.name,
                    'Codigo postal': registro.codigo_postal, 'Localidad': registro.localidad,
                    'Telefono': registro.telefono, 'Telefono padre o madre': registro.telefono_tutor,
                    'Email padre o madre': registro.email_tutor, 'Email': registro.email,
                    'DNI': registro.dni, 'Es mayor de edad': registro.edad,
                    'Es mayor de edad pero se lo paga un padre/madre': registro.edad_,
                    'Viene de Empresa': registro.empresa_, 'Dni padre o madre': registro.dni_tutor,
                    'Nombre padre o madre': registro.nombre_tutor, 'Cursos': registro.order_line,
                    'Empresa': registro.empresa_id, 'Pais': registro.country_id.name,
                    'Dias': registro.horario_dias, 'Horas': registro.horario_horas,
                })
