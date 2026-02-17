# -*- coding: utf-8 -*-

from odoo import models, fields, api

class cursos(models.Model):
    _name = 'soulschool.cursos'
    _description = 'soulschool.cursos'
    _rec_name = 'nombre_referencia'

    _sql_constraints = [
        ('codigo_curso_unique', 'unique(codigo_curso)', 'El valor del campo Codigo Curso ya existe.')
    ]

    nombre_curso = fields.Char(required=True)
    codigo_curso = fields.Char(required=True)
    descripcion = fields.Text()
    coste_mes = fields.Float()
    coste_total = fields.Float(
        string="Coste Total"
    )
    duracion = fields.Integer(
        string="Duración",
    )
    duracion_um = fields.Selection([
        ('horas','Horas'),
        ('semanas','Semanas'),
        ('meses','Meses'),
        ],
        default='meses'
    )
    nombre_modulo = fields.Many2many('soulschool.modulos')

    nombre_referencia = fields.Char(  
        string="Referencia Interna",
        compute="_compute_name"
    )
    @api.depends('nombre_curso','codigo_curso')
    def _compute_name(self):
        for rec in self:
            rec.nombre_referencia = '[' + rec.codigo_curso + '] ' + rec.nombre_curso