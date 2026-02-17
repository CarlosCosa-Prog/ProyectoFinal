# -*- coding: utf-8 -*-
{
    'name': "AcademyManagement",
    'summary': """
        Modulo para la gestión administrativa de academia
	""",
	'author': "xxx",
	'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],
	'images': ['static/description/logo.png'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',

        'views/alumnos.xml',
        'views/alumnos_order.xml',
        'views/pagos.xml',
        'views/empresas.xml',
        'views/cursos.xml',

        'reports/soulschool_pagos_facturas.xml'
    ],
}
