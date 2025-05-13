from odoo import models, fields, api  # Importación de módulos de Odoo necesarios para definir modelos, campos y lógica
from lxml import etree  # Para generar el archivo XML
import base64  # Para codificar el archivo XML en base64

class Modelo303(models.Model):
    # Definición del modelo en Odoo: 'asesoria.modelo_303' será la tabla en la base de datos
    _name = 'asesoria.modelo_303'
    _description = 'Modelo 303 AEAT'

    # Campos del modelo
    name = fields.Char(string='Nombre del Modelo', required=True)  # Nombre identificativo del registro
    cliente_id = fields.Many2one('res.partner', string='Cliente')  # Relación con un cliente de Odoo
    base_general = fields.Float(string='Base General')  # Base imponible sujeta a IVA general
    cuota_general = fields.Float(string='Cuota General')  # IVA repercutido al tipo general
    iva_soportado = fields.Float(string='IVA Soportado')  # IVA soportado deducible
    total_a_ingresar = fields.Float(string='Total a Ingresar', compute='_compute_total', store=True)  # Resultado final

    # Cálculo automático del total a ingresar: cuota - iva soportado
    @api.depends('cuota_general', 'iva_soportado')
    def _compute_total(self):
        for record in self:
            record.total_a_ingresar = (record.cuota_general or 0) - (record.iva_soportado or 0)

    # Campos para almacenar el archivo XML generado
    xml_file = fields.Binary(string='Archivo XML')  # Binario que contiene el XML codificado
    xml_filename = fields.Char(string='Nombre del archivo XML')  # Nombre del archivo para descarga

    # Método que genera un archivo XML con los datos del modelo
    def generar_xml_303(self):
        for rec in self:
            root = etree.Element('modelo_303')  # Elemento raíz del XML
            # Lista de campos a incluir en el XML
            for field in ['name', 'cliente_id', 'base_general', 'cuota_general', 'iva_soportado', 'total_a_ingresar']:
                value = getattr(rec, field)
                if hasattr(value, 'id'):  # Si es un Many2one, usamos su nombre en vez del objeto
                    value = value.name
                sub = etree.SubElement(root, field)
                sub.text = str(value or '')
                
            # Convertimos el XML a texto y lo codificamos en base64
            archivo = etree.tostring(root, pretty_print=True, encoding='utf-8', xml_declaration=True)
            rec.xml_file = base64.b64encode(archivo)
            rec.xml_filename = f'Modelo303_{rec.id}.xml'