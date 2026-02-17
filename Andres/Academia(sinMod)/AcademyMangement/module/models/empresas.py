# -*- coding: utf-8 -*-

from odoo import models, api, fields

class empresa(models.Model):
    _name = "soulschool.empresas"
    _description = "soulschool.empresas"
    _rec_name = "nombre_referencia"

    _sql_constraints = [
        ('order_id_unique', 'unique(order_id)', 'El valor ya existe.')
    ]

    nombre_empresa = fields.Char(string="Razón Social")
    cif_empresa = fields.Char(string='CIF')
    email_empresa = fields.Char(string="Email contacto")
    calle_empresa = fields.Char(string="Calle")
    country_id = fields.Many2one(
        comodel_name='res.country',
        string='Pais'
        )
    state_id = fields.Many2one(
        'res.country.state',
        string="Provincia",
        domain="[('country_id', '=?', country_id)]"
    )
    codigoPostal_empresa = fields.Char(string="Código Postal")
    localidad_empresa = fields.Char(
        string="Localidad"
    )
    telefono_empresa = fields.Char(
        string="Telefono"
    )
    web_empresa = fields.Char(string="URL Web")

    nombre_referencia = fields.Char(
        string="Referencia Interna",
        compute="_compute_name"
    )
    order_id = fields.Char(
        string="Código",
    )

    @api.depends('order_id','nombre_empresa')
    def _compute_name(self):
        for rec in self:
            rec.nombre_referencia = '[' + str(rec.order_id) + '] ' + str(rec.nombre_empresa)