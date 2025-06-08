from odoo import models, fields

class ResCompany(models.Model):
    _inherit = 'res.company'

    nombre_administrador = fields.Char(string="Nombre del administrador")
    telefono_administrador = fields.Char(string="Teléfono del administrador")
    email_administrador = fields.Char(string="Email del administrador")
