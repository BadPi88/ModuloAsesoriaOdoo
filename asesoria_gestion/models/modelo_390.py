
from odoo import models, fields

class Modelo390(models.Model):
    _name = 'asesoria.modelo_390'
    _description = 'Modelo 390 AEAT'

    cliente_id = fields.Many2one('res.partner', string='Cliente', required=True)
    ejercicio = fields.Char(string='Ejercicio', required=True)
    total_operaciones = fields.Float(string='Total Operaciones', required=True)
    iva_total = fields.Float(string='IVA Total', required=True)
