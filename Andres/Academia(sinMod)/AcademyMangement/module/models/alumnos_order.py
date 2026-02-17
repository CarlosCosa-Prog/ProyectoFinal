# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime, date
import csv
class AlumnosOrder(models.Model):
    _name="soulschool.alumnos_order"
    _description="soulschool.alumnos_order"
    _rec_name="nombre_referencia"

    alumnos_id = fields.Many2one(
        comodel_name="soulschool.alumnos",
        string="Alumnos Reference"
    )
    curso_id = fields.Many2one(
        comodel_name="soulschool.cursos",
        string="Curso",
    )
    duracion_curso = fields.Integer(
        string="Duracion Curso",
        related="curso_id.duracion"
    )
    fecha_inicio = fields.Date(
        string="Fecha Inicio",
    )
    fecha_fin = fields.Date(
        string="Fecha Fin",
    )
    pagado = fields.Boolean(
        string="Pagado",
        default=False,
        compute="_es_pagado"
    )
    pago = fields.One2many(
        comodel_name="soulschool.pagos",
        inverse_name='nombre_cliente',
        string="Pagar"
    )
    pagos_totales = fields.Float(
        string="Total",
        compute="_get_pagos"
    )
    meses_pagados = fields.Integer(
        string="Meses pagados",
        compute="_get_mes"
    )
    fecha_pago = fields.Date(
        string="Fecha de pago",
        related='pago.fecha_pago'
    )
    mes_fecha_inicio = fields.Integer(
        string="Mes fecha inicio",
        compute='_get_mes'
    )
    en_curso = fields.Boolean(
        "En curso",
        default=True,
        compute='_curso_transcurso'
        )
    coste_mes = fields.Float(
        string="Coste mes",
        related='curso_id.coste_mes'
    )
    coste_total = fields.Float(
        string="Coste total",
        related='curso_id.coste_total'
    )
    tipo_pago = fields.Selection([
        ('mensual', 'Mensual'),
        ('total', 'Total'),
        ],
        string="Tipo de Pago",
        default="mensual"
    )
    tipo_curso = fields.Selection([
        ('presencial', 'Presencial'),
        ('online', 'Online'),
        ],
        string="Tipo de Curso",
        default="presencial"
    )
    metodo_pago = fields.Selection([
        ('tarjeta','TPV'),
        ('efectivo','Efectivo'),
        ('transfer','Transferencia'),
        ],
        related="pago.metodo_pago"
    )

    nombre_referencia = fields.Char(
        string="Referencia Interna",
        compute="_compute_name"
    )

    @api.depends('curso_id.nombre_curso','fecha_inicio', "alumnos_id")
    def _compute_name(self):
        for rec in self:
            rec.nombre_referencia =  str(rec.alumnos_id.nombre) + " " + str(rec.alumnos_id.apellidos) + " " + str(rec.alumnos_id.dni) +" [" + str(rec.curso_id.nombre_curso) + "] "

    @api.depends('fecha_fin')
    def _curso_transcurso(self):
        for rec in self:    
            if rec.fecha_fin:
                actual_date = date.today()
                end_date = rec.fecha_fin
                resta = (end_date - actual_date).days

                if resta <= 0:
                    rec.en_curso = False
                else:
                    rec.en_curso = True
            else:
                rec.en_curso = True
    
    @api.depends('fecha_inicio')
    def _get_mes(self):
        for rec in self:
            rec.mes_fecha_inicio = int((rec.fecha_inicio).month)

    @api.depends('pago.es_matricula', 'pago.cantidad')
    def _get_pagos(self):
        for rec in self:
            rec.pagos_totales = sum(
                registro.cantidad for registro in rec.pago if not registro.es_matricula
            )

    @api.depends('pago.es_matricula')
    def _get_mes(self):
        for rec in self:
            rec.meses_pagados = len(rec.pago.filtered(lambda x: not x.es_matricula))

    @api.depends('en_curso','tipo_pago','coste_total','pagos_totales','duracion_curso')
    def _es_pagado(self):
        for rec in self:
            if rec.en_curso == False:
                rec.pagado = True
            elif rec.en_curso == True and (rec.tipo_pago == 'total' or rec.tipo_pago == 'mensual'):
                rec.pagado = rec.pagos_totales == rec.coste_total
            elif rec.en_curso == True and rec.tipo_pago == 'mensual':
                rec.pagado = rec.meses_pagados == rec.duracion_curso

            else:
                rec.pagado = False

    def _get_backup_csv(self):
        registros = self.search([])
        with open('/home/administrador/Escritorio/Backups_odoo/backup_alumnos_order.csv', 'w', newline='') as csvfile:
            # campo_nombres = ['Nombre', 'Apellidos']
            campo_nombres = ['Alumnos Reference', 'Curso', 'Fecha Fin', 'Fecha Inicio',
                              'Pagar', 'Tipo de Curso', 'Tipo de Pago']

            writer = csv.DictWriter(csvfile, fieldnames=campo_nombres)

            # Escribir encabezados al archivo CSV
            writer.writeheader()

            # Escribir datos al archivo CSV
            for registro in registros:
                writer.writerow({
                    'Alumnos Reference': registro.alumnos_id, 'Curso': registro.curso_id,
                    'Fecha Fin': registro.fecha_fin, 'Fecha Inicio': registro.fecha_inicio,
                    'Pagar': registro.pago, 'Tipo de Curso': registro.tipo_curso,
                    'Tipo de Pago': registro.tipo_pago
                })