from odoo import models, fields

class Modelo200(models.Model):
    _name = 'asesoria.modelo_200'
    _description = 'Modelo 200 - Impuesto sobre Sociedades'

    name = fields.Char(string='Nombre o razón social', required=True)
    nif = fields.Char(string='NIF', required=True)
    ejercicio = fields.Integer(string='Ejercicio', required=True)
    tipo_ejercicio = fields.Selection([
        ('normal', 'Normal'),
        ('corto', 'Ejercicio corto')
    ], string='Tipo de ejercicio')
    periodo = fields.Char(string='Periodo')
    base_imponible = fields.Float(string='Base imponible')
    cuota_integra = fields.Float(string='Cuota íntegra')
    cuota_cero = fields.Boolean(string='Cuota cero')
    ingreso = fields.Float(string='Ingreso')
    devolucion = fields.Float(string='Devolución')
    iban = fields.Char(string='IBAN')
    renuncia_devolucion = fields.Boolean(string='Renuncia a la devolución')
    fraccionamiento = fields.Boolean(string='Fraccionamiento art. 19.1 LIS')
    resultado_aid_abono = fields.Float(string='Abono AID tras regularización')
    resultado_aid_compensacion = fields.Float(string='Compensación AID tras regularización')
    resultado_aid_ingreso = fields.Float(string='Ingreso AID tras regularización')
