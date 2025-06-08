from odoo import models, fields, api
import base64
import random
from datetime import date


# Modelo principal para generar la declaración Modelo 200 y almacenar sus datos contables y fiscales
class Modelo200Declaration(models.Model):
    
    xml_file = fields.Binary("Archivo XML", readonly=True)
    xml_filename = fields.Char("Nombre del archivo XML")

    def action_generate_xml(self):
        self.ensure_one()
        root = ET.Element("Modelo200")

        # Añadir datos de la empresa antes del resto del XML
        info_empresa = ET.SubElement(root, "InformacionEmpresa")
        ET.SubElement(info_empresa, "NombreEmpresa").text = self.t00011 or ''
        ET.SubElement(info_empresa, "CIFEmpresa").text = self.t00006 or ''

        # Continuar con la estructura estándar
        for tipo_pagina, campos in estructura_xml_fija.items():
            nodo_pagina = ET.SubElement(root, tipo_pagina)
            for etiqueta in campos:
                campo_odoo = "t" + etiqueta[1:]
                valor = getattr(self, campo_odoo, '')
                if valor in [False, None]:
                    valor = ''
                nodo = ET.SubElement(nodo_pagina, etiqueta)
                nodo.text = str(valor)
                _logger.info(f"Campo {campo_odoo}: {valor}")

        xml_bytes = ET.tostring(root, encoding="utf-8", method="xml")
        self.xml_file = base64.b64encode(xml_bytes)
        self.xml_filename = "modelo200.xml"

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content?model={self._name}&id={self.id}&field=xml_file&download=true&filename={self.xml_filename}",
            "target": "self",
        }

        
    cnae = fields.Char(string="CNAE")
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # Campos faltantes detectados por comparación con XML
    t00001 = fields.Char(
    string="Inicio del identificador de modelo. Constante",
    default='T200'
    
    )
    
   

#------------ moneda
    
    currency_id = fields.Many2one(
    'res.currency',
    string='Moneda',
    default=lambda self: self.env.company.currency_id.id,
    readonly=True
)
#----------------

#t00180

#-----Importar datos Administrador desde res.company---------
    company_id = fields.Many2one('res.company', string='Compañía', required=True, default=lambda self: self.env.company)
    
    nombre_administrador = fields.Char(related='company_id.nombre_administrador', string='Nombre del administrador', store=False)
    telefono_administrador = fields.Char(related='company_id.telefono_administrador', string='Teléfono del administrador', store=False)
    email_administrador = fields.Char(related='company_id.email_administrador', string='Email del administrador', store=False)

#--------


    def rellenar_campos_demo(self):
        float_fields = [f.name for f in self._fields.values() if f.name.startswith('t') and isinstance(f, fields.Float)]

        campos_no_random = ['t00101', 't00136', 't00180']
        campos_random = [f for f in float_fields if f not in campos_no_random]

        for rec in self:
            # Paso 1: Rellenar aleatoriamente todos los campos salvo los calculados
            for field in campos_random:
                setattr(rec, field, round(random.uniform(1000, 50000), 2))

            # Paso 2: Calcular ACTIVO NO CORRIENTE [00101]
            campos_anc = [f't00{str(i).zfill(3)}' for i in range(102, 136) if f't00{str(i).zfill(3)}' in float_fields]
            rec.t00101 = sum(getattr(rec, f, 0.0) for f in campos_anc)

            # Paso 3: Calcular ACTIVO CORRIENTE [00136]
            campos_ac = [f't00{str(i).zfill(3)}' for i in range(137, 180) if f't00{str(i).zfill(3)}' in float_fields]
            rec.t00136 = sum(getattr(rec, f, 0.0) for f in campos_ac)

            # Paso 4: Calcular TOTAL ACTIVO [00180]
            rec.t00180 = rec.t00101 + rec.t00136
            # Paso 5: Calcular PASIVO + PN
            total_pasivo_pn = rec.t00180  # Debe cuadrar con el activo total

            # Generar pesos aleatorios para las 3 partes
            pesos_pn = [random.uniform(1, 3) for _ in range(3)]
            peso_total_pn = sum(pesos_pn)

            # Calcular valores proporcionados
            valores_pn = [round(total_pasivo_pn * (p / peso_total_pn), 2) for p in pesos_pn]

            # Asignar
            rec.t00185 = valores_pn[0]  # Patrimonio neto
            rec.t00210 = valores_pn[1]  # Pasivo no corriente
            rec.t00228 = valores_pn[2]  # Pasivo corriente

            # Calcular TOTAL PN Y PASIVO
            rec.t00252 = round(sum(valores_pn), 2)


    

    t00003 = fields.Char(string="Ejercicio económico")
    t00006 =t00006 = fields.Char(
    string='NIF de la empresa [00006]',
    compute='_compute_nif_empresa',
    store=True,
    readonly=True
)

    @api.depends('company_id')
    def _compute_nif_empresa(self):
        for record in self:
            if record.company_id:
                partner = self.env['res.company'].browse(record.company_id.id).partner_id
                record.t00006 = partner.vat or ''
            else:
                record.t00006 = ''


    t00011 = fields.Char(
    string="Nombre o razón social de la entidad",
    compute='_compute_nombre_empresa',
    store=True,
    readonly=True
)
    def recalculate_t00101(self):
        for rec in self:
            rec._compute_t00101()

    @api.depends('company_id')
    def _compute_nombre_empresa(self):
        for record in self:
            if record.company_id:
                record.t00011 = record.company_id.name
            else:
                record.t00011 = ''



    
    def actualizar_datos_facturacion(self):
        for rec in self:
            year = int(rec.fiscal_year)
            start_date = date(year, 1, 1)
            end_date = date(year, 12, 31)

            # Guardar fechas en el modelo
            rec.date_start = start_date
            rec.date_end = end_date

            # 🧾 Facturas emitidas y rectificativas del año pasado
            moves = rec.env['account.move'].search([
                ('company_id', '=', rec.company_id.id),
                ('state', '=', 'posted'),
                ('move_type', 'in', ['out_invoice', 'out_refund']),
                ('invoice_date', '>=', start_date),
                ('invoice_date', '<=', end_date),
            ])
            

            # t00102: Inmovilizado intangible (cuentas 200000–209999)
            lines_20 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '20%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00102 = sum(line.debit - line.credit for line in lines_20)
            
            
            # t00111: Inmovilizado material (cuentas 21XXXX)
            lines_21 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '21%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00111 = sum(line.debit - line.credit for line in lines_21)
            
            # t00115: Inversiones inmobiliarias (cuentas 22XXXX)
            lines_22 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '22%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00115 = sum(line.debit - line.credit for line in lines_22)
            
            # t00118: Inversiones en empresas del grupo y asociadas a largo plazo (cuentas 24XXXX)
            lines_24 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '24%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00118 = sum(line.debit - line.credit for line in lines_24)
            
            # t00126: Inversiones financieras a largo plazo (cuentas 25XXXX)
            lines_25 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '25%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00126 = sum(line.debit - line.credit for line in lines_25)
            
            # t00134: Activos por impuesto diferido (cuentas 474XXX)
            lines_474 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '474%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00134 = sum(line.debit - line.credit for line in lines_474)
            
            
            # t00138: Existencias (cuentas 3XXXX)
            lines_3 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '3%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00138 = sum(line.debit - line.credit for line in lines_3)
            
            # t00149: Deudores comerciales y otras cuentas a cobrar
            lines_t00149 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '43%'),
                ('move_id.state', '=', 'posted'),
            ])

            # Incluimos otras cuentas de deudores: 46, 47, 54
            lines_extra_t00149 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '46%'),
                ('move_id.state', '=', 'posted'),
            ]) + rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '47%'),
                ('move_id.state', '=', 'posted'),
            ]) + rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '54%'),
                ('move_id.state', '=', 'posted'),
            ])

            rec.t00149 = sum(line.debit - line.credit for line in lines_t00149 + lines_extra_t00149)
            
            # t00159: Otros deudores (472000)
            lines_t00159 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', 'in', ['472000']),
                ('move_id.state', '=', 'posted'),
            ])

            rec.t00159 = sum(line.debit - line.credit for line in lines_t00159)
            
            # t00167: Inversiones financieras a corto plazo (cuentas 54XXXX, excluyendo grupo)
            lines_t00167 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '54%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00167 = sum(line.debit - line.credit for line in lines_t00167)
            
            # t00177: Efectivo y otros activos líquidos equivalentes (cuentas 57XXXX)
            lines_t00177 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '57%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00177 = sum(line.debit - line.credit for line in lines_t00177)

            
            # t00188: Capital escriturado cuenta 100000 de Odoo
            domain_capital = [
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=', '100000'),
                ('move_id.state', '=', 'posted'),
            ]
            apuntes_capital = rec.env['account.move.line'].search(domain_capital)
            rec.t00188 = sum(line.debit - line.credit for line in apuntes_capital)


            # t00255: Base imponible (sin IVA)
            rec.t00255 = sum(m.amount_untaxed * (-1 if m.move_type == 'out_refund' else 1) for m in moves)

            # t00256: Total facturado con IVA (ventas brutas)
            rec.t00256 = sum(m.amount_total * (-1 if m.move_type == 'out_refund' else 1) for m in moves)

            # t00150: Clientes a corto plazo (pendientes al 31/12 del año pasado)
            # t00150: Clientes por ventas y prestaciones de servicios a corto plazo (cuenta 430000)
            lines_t00150 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=', '430000'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00150 = sum(line.debit - line.credit for line in lines_t00150)

            # t00151: Clientes a largo plazo (no implementado aún se suman todos en t00150)
            rec.t00151 = 0.0
            
            # t00158: Accionistas (socios) por desembolsos exigidos (cuentas 103XXX y 104XXX)
            lines_t00158 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', 'in', ['103000', '103400', '104000', '104400']),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00158 = sum(line.debit - line.credit for line in lines_t00158)

            # t00160: Inversiones en empresas del grupo y asociadas a corto plazo (cuentas 53XXXX)
            lines_t00160 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '53%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00160 = sum(line.debit - line.credit for line in lines_t00160)
            
            # t00176: Periodificaciones a corto plazo (cuentas 480XXX, 485XXX, 486XXX)
            lines_t00176 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=like', '48%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00176 = sum(line.debit - line.credit for line in lines_t00176)
            
            # t00180: TOTAL ACTIVO = Activo no corriente + Activo corriente + Desembolsos exigidos
            rec.t00180 = rec.t00101 + rec.t00136 + rec.t00158
            
            # t00186: Fondos propios = suma de sus componentes
            rec.t00186 = sum([
                rec.t00188,  # Capital escriturado
                rec.t00191,  # Reservas
                rec.t00195,  # Resultados anteriores
                rec.t00199,  # Resultado del ejercicio
                rec.t00204,  # Otras aportaciones de socios
                rec.t00207,  # Dividendos a cuenta (valor negativo si es pasivo)
            ])
            
            # t00188: Capital escriturado (cuenta 100000)
            lines_t00188 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=', '100000'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00188 = sum(line.credit - line.debit for line in lines_t00188)
            
            # t00199: Resultado del ejercicio (cuenta 129000)
            lines_t00199 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                ('account_id.code', '=', '129000'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00199 = sum(line.credit - line.debit for line in lines_t00199)




            # t00210: PASIVO NO CORRIENTE (cuentas 14XXXX, 15XXXX, 16XXXX, 17XXXX, 18XXXX)
            lines_t00210 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                '|',
                    ('account_id.code', '=like', '14%'),
                    '|',
                        ('account_id.code', '=like', '15%'),
                        '|',
                            ('account_id.code', '=like', '16%'),
                            '|',
                                ('account_id.code', '=like', '17%'),
                                ('account_id.code', '=like', '18%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00210 = sum(line.credit - line.debit for line in lines_t00210)
            
            # t00239: Acreedores comerciales y otras cuentas a pagar
            lines_t00239 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                '|',
                    ('account_id.code', '=like', '41%'),
                    '|',
                        ('account_id.code', 'in', ['410000', '475100', '477000']),
                        ('account_id.code', '=like', '465%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00239 = sum(line.credit - line.debit for line in lines_t00239)
            
            # t00249: Otros acreedores (cuentas varias no comerciales)
            lines_t00249 = rec.env['account.move.line'].search([
                ('company_id', '=', rec.company_id.id),
                ('date', '>=', start_date),
                ('date', '<=', end_date),
                '|',
                    ('account_id.code', '=like', '465%'),
                    '|',
                        ('account_id.code', '=like', '466%'),
                        '|',
                            ('account_id.code', '=like', '476%'),
                            '|',
                                ('account_id.code', '=like', '555%'),
                                '|',
                                    ('account_id.code', '=like', '529%'),
                                    ('account_id.code', '=like', '553%'),
                ('move_id.state', '=', 'posted'),
            ])
            rec.t00249 = sum(line.credit - line.debit for line in lines_t00249)










# t00101: ACTIVO NO CORRIENTE = suma de sus componentes
            rec.t00101 = sum([
                rec.t00102,  # Inmovilizado intangible
                rec.t00111,  # Inmovilizado material
                rec.t00115,  # Inversiones inmobiliarias
                rec.t00118,  # Inversiones en empresas del grupo y asociadas
                rec.t00126,  # Inversiones financieras a largo plazo
                rec.t00134,  # Activos por impuesto diferido
                rec.t00135,  # Deudores comerciales no corrientes (si se implementa)
            ])
            
# t00136: ACTIVO CORRIENTE = suma de sus componentes
            rec.t00136 = sum([
                rec.t00138,  # Existencias
                rec.t00149,  # Deudores comerciales y otras cuentas a cobrar
                rec.t00159,  # Otros deudores
                rec.t00160,  # Inversiones en empresas del grupo a corto plazo
                rec.t00167,  # Inversiones financieras a corto plazo
                rec.t00176,  # Periodificaciones a corto plazo
                rec.t00177,  # Efectivo y otros activos líquidos equivalentes
            ])
            
            # t00252: TOTAL PATRIMONIO NETO Y PASIVO
            rec.t00252 = rec.t00185 + rec.t00210 + rec.t00228


# Declaracion de campos del modelo Modelo200Declaration

    t00012 = fields.Char(string="Indicador de página complementaria. En blanco")

# Página 3: Balance Activo (I)
    t00101 = fields.Monetary(
    string="ACTIVO NO CORRIENTE [00101]",
    compute="_compute_t00101",
    store=True,
    readonly=True
)
    t00102 = fields.Monetary(
    string="Inmovilizado intangible [00102]",
    currency_field='currency_id'
)
    t00103 = fields.Float(string="Desarrollo [00103]")
    t00104 = fields.Float(string="Concesiones [00104]")
    t00105 = fields.Float(string="Patentes, licencias, marcas y similares [00105]")
    t00106 = fields.Float(string="Fondo de comercio [00106]")
    t00107 = fields.Float(string="Aplicaciones informáticas [00107]")
    t00108 = fields.Float(string="Investigación [00108]")
    t00700 = fields.Float(string="Propiedad intelectual [00700]")
    t00109 = fields.Float(string="Otro inmovilizado intangible [00109]")
    t00110 = fields.Float(string="Resto [00110]")
    t00111 = fields.Float(string="Inmovilizado material [00111]")
    t00112 = fields.Float(string="Terrenos y construcciones [00112]")
    t00113 = fields.Float(string="Instalaciones técnicas y otro inmovilizado material [00113]")
    t00114 = fields.Float(string="Inmovilizado en curso y anticipos [00114]")
    
    t00115 = fields.Monetary(
    string="Inversiones inmobiliarias [00115]",
    currency_field='currency_id'
)

    t00116 = fields.Float(string="Terrenos [00116]")
    t00117 = fields.Float(string="Construcciones [00117]")
    
    t00118 = fields.Monetary(
    string="Inversiones en empresas del grupo y asociadas a largo plazo [00118]",
    currency_field='currency_id'
)

    t00119 = fields.Float(string="Instrumentos de patrimonio [00119]")
    t00120 = fields.Float(string="Créditos a empresas [00120]")
    t00121 = fields.Float(string="Valores representativos de deuda [00121]")
    t00122 = fields.Float(string="Derivados [00122]")
    t00123 = fields.Float(string="Otros activos financieros [00123]")
    t00124 = fields.Float(string="Otras inversiones [00124]")
    t00125 = fields.Float(string="Resto [00125]")
    t00126 = fields.Monetary(
    string="Inversiones financieras a largo plazo [00126]",
    currency_field='currency_id'
)

    t00127 = fields.Float(string="Instrumentos de patrimonio [00127]")
    t00128 = fields.Float(string="Créditos a terceros [00128]")
    t00129 = fields.Float(string="Valores representativos de deuda [00129]")
    t00130 = fields.Float(string="Derivados [00130]")
    t00131 = fields.Float(string="Otros activos financieros [00131]")
    t00132 = fields.Float(string="Otras inversiones [00132]")
    t00133 = fields.Float(string="Resto [00133]")
    
    t00134 = fields.Monetary(
    string="Activos por impuesto diferido [00134]",
    currency_field='currency_id'
)

    t00135 = fields.Float(string="Deudores comerciales no corrientes [00135]")
    
    t00136 = fields.Monetary(
    string="ACTIVO CORRIENTE [00136]",
    currency_field='currency_id'
)

    t00137 = fields.Float(string="Activos no corrientes mantenidos para la venta [00137]")
    
    t00138 = fields.Monetary(
    string="Existencias [00138]",
    currency_field='currency_id'
)

    t00139 = fields.Float(string="Comerciales [00139]")
    t00140 = fields.Float(string="Materias primas y otros aprovisionamientos [00140]")
    t00141 = fields.Float(string="Productos en curso [00141]")
    t00142 = fields.Float(string="Productos en curso - De ciclo largo de producción [00142]")
    t00143 = fields.Float(string="Productos en curso - De ciclo corto de producción [00143]")
    t00144 = fields.Float(string="Productos terminados [00144]")
    t00145 = fields.Float(string="Productos terminados - De ciclo largo de producción [00145]")
    t00146 = fields.Float(string="Productos terminados - De ciclo corto de producción [00146]")
    t00147 = fields.Float(string="Subproductos, residuos y materiales recuperados [00147]")
    t00148 = fields.Float(string="Anticipos a proveedores [00148]")
    t00701 = fields.Float(string="Derechos de emisión de gases de efecto invernadero [00701]")
    
    
   # Página 4: Balance Activo (II)
    t00149 = fields.Monetary(
    string="Deudores comerciales y otras cuentas a cobrar [00149]",
    currency_field='currency_id'
)

    t00150 = fields.Monetary(
        string="Clientes por ventas y prestaciones de servicios a corto plazo [00150]",
        currency_field='currency_id'
)

    t00151 = fields.Monetary(
        string="Clientes por ventas y prestaciones de servicios a largo plazo [00151]",
        currency_field='currency_id'
)

    t00152 = fields.Float(string="Clientes por ventas y prestaciones de servicios dudoso cobro [00152]")
    t00153 = fields.Float(string="Clientes empresas del grupo y asociadas [00153]")
    t00154 = fields.Float(string="Deudores varios [00154]")
    t00155 = fields.Float(string="Personal [00155]")
    t00156 = fields.Float(string="Activos por impuesto corriente [00156]")
    t00157 = fields.Float(string="Otros créditos con las Administraciones Públicas [00157]")
    
    t00158 = fields.Monetary(
        string="Accionistas (socios) por desembolsos exigidos [00158]",
        currency_field='currency_id'
)

    t00159 = fields.Monetary(
    string="Otros deudores [00159]",
    currency_field='currency_id'
)

    t00160 = fields.Monetary(
    string="Inversiones en empresas del grupo y asociadas a corto plazo [00160]",
    currency_field='currency_id'
)

    t00161 = fields.Float(string="Instrumentos de patrimonio [00161]")
    t00162 = fields.Float(string="Créditos a empresas [00162]")
    t00163 = fields.Float(string="Valores representativos de deuda [00163]")
    t00164 = fields.Float(string="Derivados [00164]")
    t00165 = fields.Float(string="Otros activos financieros [00165]")
    t00166 = fields.Float(string="Resto [00166]")
    
    t00167 = fields.Monetary(
    string="Inversiones financieras a corto plazo [00167]",
    currency_field='currency_id'
)

    t00168 = fields.Float(string="Instrumentos de patrimonio [00168]")
    t00169 = fields.Float(string="Créditos a terceros [00169]")
    t00170 = fields.Float(string="Valores representativos de deuda [00170]")
    t00171 = fields.Float(string="Derivados [00171]")
    t00172 = fields.Float(string="Otros activos financieros [00172]")
    t00173 = fields.Float(string="Resto [00173]")
    t00174 = fields.Float(string="Otras inversiones [00174]")
    t00175 = fields.Float(string="Resto [00175]")
    
    t00176 = fields.Monetary(
    string="Periodificaciones a corto plazo [00176]",
    currency_field='currency_id'
)

    t00177 = fields.Monetary(
    string="Efectivo y otros activos líquidos equivalentes [00177]",
    currency_field='currency_id'
)

    t00178 = fields.Float(string="Tesorería [00178]")
    t00179 = fields.Float(string="Otros activos líquidos equivalentes [00179]")
    
    t00180 = fields.Monetary(
    string="TOTAL ACTIVO [00180]",
    currency_field='currency_id'
)




    # Página 5: Balance Pasivo (I)
    
    t00185 = fields.Float(string="PATRIMONIO NETO [00185]")
    
    t00186 = fields.Monetary(
    string="Fondos propios [00186]",
    currency_field='currency_id'
)

    t00187 = fields.Float(string="Capital [00187]")
    
    t00188 = fields.Monetary(
    string="Capital escriturado [00188]",
    currency_field='currency_id'
)

    


    
    t00189 = fields.Float(string="Capital no exigido [00189]")
    t00764 = fields.Float(string="Capital cooperativo suscrito (cooperativas) [00764]")
    t00765 = fields.Float(string="Capital cooperativo no exigido (cooperativas) [00765]")
    t00190 = fields.Float(string="Prima de emisión [00190]")
    t00191 = fields.Float(string="Reservas [00191]")
    t00192 = fields.Float(string="Legal y estatutarias [00192]")
    t00193 = fields.Float(string="Otras reservas [00193]")
    t00702 = fields.Float(string="Reserva de revalorización [00702]")
    t01001 = fields.Float(string="Reserva de capitalización [01001]")
    t01002 = fields.Float(string="Reserva de nivelación [01002]")
    t00712 = fields.Float(string="Fondo de reserva obligatorio de cooperativas [00712]")
    t00766 = fields.Float(string="Fondo de reembolso o actualización (cooperativas) [00766]")
    t00767 = fields.Float(string="Fondo de reserva voluntario (cooperativas) [00767]")
    t00194 = fields.Float(string="Acciones y participaciones en patrimonio propias [00194]")
    t00195 = fields.Float(string="Resultados de ejercicios anteriores [00195]")
    t00196 = fields.Float(string="Remanente [00196]")
    t00197 = fields.Float(string="Resultados negativos de ejercicios anteriores [00197]")
    t00198 = fields.Float(string="Otras aportaciones de socios [00198]")
    
    t00199 = fields.Monetary(
    string="Resultado del ejercicio [00199]",
    currency_field='currency_id'
)

    t00200 = fields.Float(string="Dividendo a cuenta [00200]")
    t00768 = fields.Float(string="Retorno cooperativo y remuneración discrecional a cuenta entregado en el ejercicio) (cooperativas) [00768]")
    t00769 = fields.Float(string="Fondos capitalizados (cooperativas) [00769]")
    t00201 = fields.Float(string="Otros instrumentos de patrimonio neto [00201]")
    t00202 = fields.Float(string="Ajustes por cambios de valor [00202]")
    t00203 = fields.Float(string="Activos financieros a valor razonable con cambios en el patrimonio neto [00203]")
    t00204 = fields.Float(string="Operaciones de cobertura [00204]")
    t00205 = fields.Float(string="Activos no corrientes y pasivos vinculados [00205]")
    t00206 = fields.Float(string="Diferencia de conversión [00206]")
    t00207 = fields.Float(string="Otros [00207]")
    t00208 = fields.Float(string="Ajustes en patrimonio neto [00208]")
    t00209 = fields.Float(string="Subvenciones, donaciones y legados recibidos [00209]")
    t00210 = fields.Monetary(
    string="PASIVO NO CORRIENTE [00210]",
    currency_field='currency_id'
)

    t00780 = fields.Float(string="Fondo de Educación, Formación y Promoción a largo plazo (cooperativas) [00780]")
    t00781 = fields.Float(string="Deudas con características especiales a largo plazo (cooperativas) [00781]")
    t00782 = fields.Float(string="Capital reembolsable exigible (cooperativas) [00782]")
    t00783 = fields.Float(string="Fondos especiales calificados como pasivo (cooperativas) [00783]")
    t00784 = fields.Float(string="Acreedores por fondos capitalizados a largo plazo (cooperativas) [00784]")
    t00211 = fields.Float(string="Provisiones a largo plazo [00211]")
    t00212 = fields.Float(string="Obligaciones por prestaciones a largo plazo al personal [00212]")
    t00213 = fields.Float(string="Actuaciones medioambientales [00213]")
    t00214 = fields.Float(string="Provisiones por reestructuración [00214]")
    t00215 = fields.Float(string="Otras provisiones [00215]")
    t00216 = fields.Float(string="Deudas a largo plazo [00216]")
    t00217 = fields.Float(string="Obligaciones y otros valores negociables [00217]")
    t00218 = fields.Float(string="Deudas con entidades de crédito [00218]")
    t00219 = fields.Float(string="Acreedores por arrendamiento financiero [00219]")
    t00220 = fields.Float(string="Derivados [00220]")
    t00221 = fields.Float(string="Otros pasivos financieros [00221]")
    t00222 = fields.Float(string="Otras deudas a largo plazo [00222]")
    t00223 = fields.Float(string="Deudas con empresas del grupo y asociadas a largo plazo [00223]")
    t00224 = fields.Float(string="Pasivos por impuesto diferido [00224]")
    t00225 = fields.Float(string="Periodificaciones a largo plazo [00225]")
    t00226 = fields.Float(string="Acreedores comerciales no corrientes [00226]")
    t00227 = fields.Float(string="Deuda con características especiales a largo plazo [00227]")

  # Página 6: Balance Pasivo (II)
    t00228 = fields.Float(string="PASIVO CORRIENTE [00228]")
    t00785 = fields.Float(string="Fondo de Educación, Formación y Promoción a corto plazo (cooperativas) [00785]")
    t00786 = fields.Float(string="Deudas con características especiales a corto plazo (cooperativas) [00786]")
    t00787 = fields.Float(string="Capital reembolsable exigible (cooperativas) [00787]")
    t00788 = fields.Float(string="Fondos especiales calificados como pasivo (cooperativas) [00788]")
    t00789 = fields.Float(string="Acreedores por fondos capitalizados a corto plazo (cooperativas) [00789]")
    t00229 = fields.Float(string="Pasivos vinculados con activos no corrientes [00229]")
    t00230 = fields.Float(string="Provisiones a corto plazo [00230]")
    t00703 = fields.Float(string="Provisiones por derechos emisión de gases de efecto invernadero [00703]")
    t00704 = fields.Float(string="Otras provisiones [00704]")
    t00231 = fields.Float(string="Deudas a corto plazo [00231]")
    t00232 = fields.Float(string="Obligaciones y otros valores negociables [00232]")
    t00233 = fields.Float(string="Deudas con entidades de crédito [00233]")
    t00234 = fields.Float(string="Acreedores por arrendamiento financiero [00234]")
    t00235 = fields.Float(string="Derivados [00235]")
    t00236 = fields.Float(string="Otros pasivos financieros [00236]")
    t00237 = fields.Float(string="Otras deudas a corto plazo [00237]")
    t00238 = fields.Float(string="Deudas con empresas del grupo y asociadas a corto plazo [00238]")
    
    
    t00249 = fields.Monetary(
        string="Otros acreedores [00249]",
        currency_field='currency_id'
)


    t00240 = fields.Float(string="Proveedores [00240]")
    t00241 = fields.Float(string="Proveedores - Proveedores a largo plazo [00241]")
    t00242 = fields.Float(string="Proveedores - Proveedores a corto plazo [00242]")
    t00243 = fields.Float(string="Proveedores, empresas del grupo y asociadas [00243]")
    t00244 = fields.Float(string="Acreedores varios [00244]")
    t00245 = fields.Float(string="Personal (remuneraciones pendientes de pago) [00245]")
    t00246 = fields.Float(string="Pasivos por impuesto corriente [00246]")
    t00247 = fields.Float(string="Otras deudas con las Administraciones Públicas [00247]")
    t00248 = fields.Float(string="Anticipos de clientes [00248]")
    t00249 = fields.Float(string="Otros acreedores [00249]")
    t00250 = fields.Float(string="Periodificaciones a corto plazo [00250]")
    t00251 = fields.Float(string="Deuda con características especiales a corto plazo [00251]")
    t00252 = fields.Float(string="TOTAL PATRIMONIO NETO Y PASIVO [00252]")

    # Página 7: Cuenta de Pérdidas y Ganancias (I)
    t00255 = fields.Float(string="Importe neto de la cifra de negocios [00255]")
    t00256 = fields.Float(string="Ventas [00256]")
    t00257 = fields.Float(string="Prestaciones de servicios [00257]")
    t00711 = fields.Float(string="Ingresos de carácter financiero de las entidades concesionarias de infraestructuras públicas [00711]")
    t00705 = fields.Float(string="Ingresos carácter financiero sociedades holding [00705]")
    t00706 = fields.Float(string="Ingresos carácter financiero sociedades holding - De participaciones en instrumentos patrimonio [00706]")
    t00707 = fields.Float(string="Ingresos carácter financiero sociedades holding - De valores negociables y otros instrumentos financieros [00707]")
    t00708 = fields.Float(string="Ingresos carácter financiero sociedades holding - Resto [00708]")
    t00258 = fields.Float(string="Variación de existencias de productos terminados y en curso de fabricación [00258]")
    t00259 = fields.Float(string="Trabajos realizados por la empresa para su activo [00259]")
    t00260 = fields.Float(string="Aprovisionamientos [00260]")
    t00261 = fields.Float(string="Consumo de mercaderías [00261]")
    t00760 = fields.Float(string="Compras de mercaderías [00760]")
    t00761 = fields.Float(string="Variación de existencias [00761]")
    t00262 = fields.Float(string="Consumo de materias primas y otras materias consumibles [00262]")
    t00762 = fields.Float(string="Compras de materias primas y otras materias consumibles [00762]")
    t00763 = fields.Float(string="Variación de materias primas y otras materias consumibles [00763]")
    t00770 = fields.Float(string="Consumo de existencias de socios (cooperativas) [00770]")
    t00771 = fields.Float(string="Compras efectuadas a los socios (cooperativas) [00771]")
    t00772 = fields.Float(string="Variación de existencias adquiridas a socios (cooperativas) [00772]")
    t00263 = fields.Float(string="Trabajos realizados por otras empresas [00263]")
    t00264 = fields.Float(string="Deterioro de mercaderías, materias primas [00264]")
    t00265 = fields.Float(string="Otros ingresos de explotación [00265]")
    t00266 = fields.Float(string="Ingresos accesorios y otros de gestión corriente [00266]")
    t00267 = fields.Float(string="Ingresos accesorios y otros de gestión corriente - Ingresos por arrendamientos [00267]")
    t00268 = fields.Float(string="Ingresos accesorios y otros de gestión corriente - Resto [00268]")
    t00269 = fields.Float(string="Subvenciones de explotación incorporadas al resultado del ejercicio [00269]")
    t00270 = fields.Float(string="Gastos de personal [00270]")
    t00271 = fields.Float(string="Sueldos, salarios y asimilados [00271]")
    t00790 = fields.Float(string="Servicios de trabajo de socios (cooperativas) [00790]")
    t00273 = fields.Float(string="Indemnizaciones [00273]")
    t00274 = fields.Float(string="Seguridad Social a cargo de la empresa [00274]")
    t00275 = fields.Float(string="Retribuciones a largo plazo por sistemas de aportación o prestación definitiva [00275]")
    t00276 = fields.Float(string="Retribuciones mediante instrumentos de patrimonio [00276]")
    t00277 = fields.Float(string="Otros gastos sociales [00277]")
    t00278 = fields.Float(string="Provisiones [00278]")
    t00279 = fields.Float(string="Otros gastos de explotación [00279]")
    t00280 = fields.Float(string="Servicios exteriores [00280]")
    t00253 = fields.Float(string="Servicios profesionales independientes [00253]")
    t00254 = fields.Float(string="Resto [00254]")
    t00281 = fields.Float(string="Tributos [00281]")
    t00282 = fields.Float(string="Pérdidas, deterioro y variación de provisiones por operaciones comerciales [00282]")
    t00283 = fields.Float(string="Otros gastos de gestión corriente [00283]")
    t00709 = fields.Float(string="Gastos por emisión de gases de efecto invernadero [00709]")
    t00284 = fields.Float(string="Amortización del inmovilizado [00284]")
    t00285 = fields.Float(string="Imputación de subvenciones de inmovilizado no financiero y otras [00285]")
    t00286 = fields.Float(string="Excesos de provisiones [00286]")
    t00287 = fields.Float(string="Deterioro y resultado por enajenaciones del inmovilizado [00287]")
    t00288 = fields.Float(string="Deterioro y pérdidas [00288]")
    t00289 = fields.Float(string="Deterioro y pérdidas - Deterioros [00289]")
    t00290 = fields.Float(string="Deterioro y pérdidas - Reversión de deterioros [00290]")
    t00291 = fields.Float(string="Resultados por enajenaciones y otras [00291]")
    t00292 = fields.Float(string="Resultados por enajenaciones y otras - Beneficios [00292]")
    t00293 = fields.Float(string="Resultados por enajenaciones y otras - Pérdidas [00293]")
    t00710 = fields.Float(string="Deterioro y resultados por enajenaciones del inmovilizado de las sociedades holding [00710]")
    t00791 = fields.Float(string="Fondo de Educación, Formación y Promoción (cooperativas) [00791]")
    t00792 = fields.Float(string="Dotación (cooperativas) [00792]")
    t00793 = fields.Float(string="Subvenciones, donaciones y ayudas y sanciones (cooperativas) [00793]")
    t00294 = fields.Float(string="Diferencia negativa de combinaciones de negocio [00294]")
    t00295 = fields.Float(string="Otros resultados [00295]")
    t00296 = fields.Float(string="RESULTADO DE EXPLOTACION [00296]")

# Página 8: Cuenta de Pérdidas y Ganancias (II)
    # --- Sección I ---
    t00297 = fields.Float(string="Ingresos financieros [00297]")
    t00298 = fields.Float(string="De participaciones en instrumentos de patrimonio [00298]")
    t00299 = fields.Float(string="De participaciones en instrumentos de patrimonio - En empresas del grupo y asociadas [00299]")
    t00300 = fields.Float(string="De participaciones en instrumentos de patrimonio - En terceros [00300]")
    t00301 = fields.Float(string="De valores negociables y otros instrumentos financieros [00301]")
    t00302 = fields.Float(string="De valores negociables y otros instrumentos financieros - De empresas del grupo y asociadas [00302]")
    t00303 = fields.Float(string="De valores negociables y otros instrumentos financieros - De terceros [00303]")
    t00794 = fields.Float(string="De valores negociables y otros instrumentos financieros - De socios (cooperativas) [00794]")
    t00304 = fields.Float(string="Imputación de subvenciones, donaciones y legados de carácter financiero [00304]")

    # --- Sección II ---
    t00305 = fields.Float(string="Gastos financieros [00305]")
    t00306 = fields.Float(string="Por deudas con empresas del grupo y asociadas [00306]")
    t00307 = fields.Float(string="Por deudas con terceros [00307]")
    t00308 = fields.Float(string="Por actualización de provisiones [00308]")
    t00796 = fields.Float(string="Intereses y retorno obligatorio de las aportaciones al capital social y de otros fondos calificados con características de deuda (cooperativas) [00796]")
    t00309 = fields.Float(string="Variación de valor razonable en instrumentos financieros [00309]")
    t00310 = fields.Float(string="Valor razonable con cambios en pérdidas y ganancias [00310]")
    t00311 = fields.Float(string="Transferencia de ajustes de valor razonable con cambios en el patrimonio neto [00311]")
    t00312 = fields.Float(string="Diferencias de cambio [00312]")
    t00313 = fields.Float(string="Deterioro y resultado por enajenaciones de instrumentos financieros [00313]")
    t00314 = fields.Float(string="Deterioros y pérdidas [00314]")
    t00315 = fields.Float(string="Deterioros y pérdidas - Deterioros, empresas del grupo, asociadas y vinculadas [00315]")
    t00316 = fields.Float(string="Deterioros y pérdidas - Deterioros, otras empresas [00316]")
    t00317 = fields.Float(string="Deterioros y pérdidas - Reversión de deterioros, empresas del grupo, asociadas y vinculadas [00317]")
    t00318 = fields.Float(string="Deterioros y pérdidas - Reversión de deterioros, otras empresas [00318]")
    t00319 = fields.Float(string="Resultados por enajenaciones y otras [00319]")
    t00320 = fields.Float(string="Resultados por enajenaciones y otras - Beneficios, empresas del grupo, asociadas y vinculadas [00320]")
    t00321 = fields.Float(string="Resultados por enajenaciones y otras - Beneficios, otras empresas [00321]")
    t00322 = fields.Float(string="Resultados por enajenaciones y otras - Pérdidas, empresas del grupo, asociadas y vinculadas [00322]")
    t00323 = fields.Float(string="Resultados por enajenaciones y otras - Pérdidas, otras empresas [00323]")
    t00329 = fields.Float(string="Otros ingresos y gastos de carácter financiero [00329]")
    t00330 = fields.Float(string="Incorporación al activo de gastos financieros [00330]")
    t00331 = fields.Float(string="Ingresos financieros derivados de convenios de acreedores [00331]")
    t00332 = fields.Float(string="Resto de ingresos y gastos [00332]")
    t00324 = fields.Float(string="RESULTADO FINANCIERO [00324]")
    t00325 = fields.Float(string="RESULTADO ANTES DE IMPUESTOS [00325]")
    t00326 = fields.Float(string="Impuestos sobre beneficios [00326]")
    t00327 = fields.Float(string="RESULTADO DEL EJERCICIO PROCEDENTE DE OPERACIONES CONTINUADAS [00327]")
    t00328 = fields.Float(string="RESULTADO DEL EJERCICIO PROCEDENTE DE OPERACIONES INTERRUMPIDAS NETO DE IMPUESTOS [00328]")
    t00500 = fields.Float(string="RESULTADO DE LA CUENTA DE PÉRDIDAS Y GANANCIAS [00500]")

    # Página 9: Estado de cambios patrimonio neto (I)
    t00500 = fields.Float(string="Resultado de la cuenta de pérdidas y ganancias [00500]")
    t00336 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Por valoración de instrumentos financieros [00336]")
    t00337 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Activos financieros a valor razonable con cambios en el patrimonio neto [00337]")
    t00338 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Otros ingresos/gastos [00338]")
    t00339 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Por coberturas de flujos de efectivo [00339]")
    t00340 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Subvenciones, donaciones y legados recibidos [00340]")
    t00341 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Por ganancias y pérdidas actuariales y otros ajustes [00341]")
    t00342 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Por activos no corrientes y pasivos vinculados, mantenidos para la venta [00342]")
    t00343 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Diferencias de conversión [00343]")
    t00344 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Efecto impositivo [00344]")
    t00345 = fields.Float(string="Ingresos y gastos imputados al patrimonio neto - Total ingresos y gastos imputados en el patrimonio neto [00345]")
    t00346 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - Por valoración de instrumentos financieros [00346]")
    t00347 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - Activos financieros a valor razonable con cambios en el patrimonio neto [00347]")
    t00348 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - Otros ingresos/gastos [00348]")
    t00349 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - Por coberturas de flujos de efectivo [00349]")
    t00350 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - Subvenciones, donaciones y legados recibidos [00350]")
    t00351 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - Por activos no corrientes y pasivos vinculados , mantenidos para la venta [00351]")
    t00352 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - Diferencias de conversión [00352]")
    t00353 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - Efecto impositivo [00353]")
    t00354 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - Total transferencia a la cuenta de pérdidas y ganancias [00354]")
    t00355 = fields.Float(string="Transferencias a la cta. pérdidas y ganancias - TOTAL DE INGRESOS Y GASTOS RECONOCIDOS [00355]")

# Página 10: Estado de cambios patrimonio neto (II)
    t00380 = fields.Float(string="Saldo,  final del ejercicio anterior - Capital - Escriturado [00380]")
    t00381 = fields.Float(string="Saldo,  final del ejercicio anterior - Capital - No exigido  [00381]")
    t00382 = fields.Float(string="Saldo,  final del ejercicio anterior - Prima de emisión  [00382]")
    t00383 = fields.Float(string="Saldo,  final del ejercicio anterior - Reservas  [00383]")
    t00384 = fields.Float(string="Saldo,  final del ejercicio anterior - Acciones y participaciones en patrimonio propias  [00384]")
    t00385 = fields.Float(string="Saldo,  final del ejercicio anterior - Resultados ejercicios anteriores  [00385]")
    t00386 = fields.Float(string="Saldo,  final del ejercicio anterior - Otras aportaciones de socios  [00386]")
    t00394 = fields.Float(string="Ajustes por cambio de criterio de ejercicios anteriores - Capital - Escriturado  [00394]")
    t00395 = fields.Float(string="Ajustes por cambio de criterio de ejercicios anteriores - Capital - No exigido [00395]")
    t00396 = fields.Float(string="Ajustes por cambio de criterio de ejercicios anteriores - Prima de emisión [00396]")
    t00397 = fields.Float(string="Ajustes por cambio de criterio de ejercicios anteriores - Reservas [00397]")
    t00398 = fields.Float(string="Ajustes por cambio de criterio de ejercicios anteriores - Acciones y participaciones en patrimonio propias [00398]")
    t00399 = fields.Float(string="Ajustes por cambio de criterio de ejercicios anteriores - Resultados ejercicios anteriores [00399]")
    t00400 = fields.Float(string="Ajustes por cambio de criterio de ejercicios anteriores - Otras aportaciones de socios [00400]")
    t00408 = fields.Float(string="Ajustes por errores de ejercicios anteriores - Capital - Escriturado [00408]")
    t00409 = fields.Float(string="Ajustes por errores de ejercicios anteriores - Capital - No exigido [00409]")
    t00410 = fields.Float(string="Ajustes por errores de ejercicios anteriores - Prima de emisión [00410]")
    t00411 = fields.Float(string="Ajustes por errores de ejercicios anteriores - Reservas [00411]")
    t00412 = fields.Float(string="Ajustes por errores de ejercicios anteriores - Acciones y participaciones en patrimonio propias [00412]")
    t00413 = fields.Float(string="Ajustes por errores de ejercicios anteriores - Resultados ejercicios anteriores [00413]")
    t00414 = fields.Float(string="Ajustes por errores de ejercicios anteriores - Otras aportaciones de socios [00414]")
    t00422 = fields.Float(string="Saldo ajustado, inicio del ejercicio - Capital - Escriturado [00422]")
    t00423 = fields.Float(string="Saldo ajustado, inicio del ejercicio - Capital - No exigido [00423]")
    t00424 = fields.Float(string="Saldo ajustado, inicio del ejercicio - Prima de emisión [00424]")
    t00425 = fields.Float(string="Saldo ajustado, inicio del ejercicio - Reservas [00425]")
    t00426 = fields.Float(string="Saldo ajustado, inicio del ejercicio - Acciones y participaciones en patrimonio propias [00426]")
    t00427 = fields.Float(string="Saldo ajustado, inicio del ejercicio - Resultados ejercicios anteriores [00427]")
    t00428 = fields.Float(string="Saldo ajustado, inicio del ejercicio - Otras aportaciones socios [00428]")
    t00436 = fields.Float(string="Total ingresos y gastos reconocidos - Capital - Escriturado [00436]")
    t00437 = fields.Float(string="Total ingresos y gastos reconocidos - Capital - No exigido [00437]")
    t00438 = fields.Float(string="Total ingresos y gastos reconocidos - Prima de emisión [00438]")
    t00439 = fields.Float(string="Total ingresos y gastos reconocidos - Reservas [00439]")
    t00440 = fields.Float(string="Total ingresos y gastos reconocidos - Acciones y participaciones en patrimonio propias [00440]")
    t00441 = fields.Float(string="Total ingresos y gastos reconocidos - Resultados ejercicios anteriores [00441]")
    t00442 = fields.Float(string="Total ingresos y gastos reconocidos - Otras aportaciones de socios [00442]")
    t00450 = fields.Float(string="Resultado cuenta pérdidas y ganancias - Capital - Escriturado [00450]")
    t00451 = fields.Float(string="Resultado cuenta pérdidas y ganancias - Capital - No exigido [00451]")
    t00452 = fields.Float(string="Resultado cuenta pérdidas y ganancias - Prima de emisión [00452]")
    t00453 = fields.Float(string="Resultado cuenta pérdidas y ganancias - Reservas [00453]")
    t00454 = fields.Float(string="Resultado cuenta pérdidas y ganancias - Acciones y participaciones en patrimonio propias [00454]")
    t00455 = fields.Float(string="Resultado cuenta pérdidas y ganancias - Resultados ejercicios anteriores [00455]")
    t00456 = fields.Float(string="Resultado cuenta pérdidas y ganancias - Otras aportaciones de socios [00456]")
    t00464 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Capital - Escriturado [00464]")
    t00465 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Capital - No exigido [00465]")
    t00466 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Prima de emisión [00466]")
    t00467 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Reservas [00467]")
    t00468 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Acciones y participaciones en patrimonio propias [00468]")
    t00469 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Resultados ejercicios anteriores [00469]")
    t00470 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Otras aportaciones de socios [00470]")
    t00478 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Capital - Escriturado [00478]")
    t00479 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Capital - No exigido [00479]")
    t00480 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Prima de emisión [00480]")
    t00481 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Reservas [00481]")
    t00482 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Acciones y participaciones en patrimonio propias  [00482]")
    t00483 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Resultados ejercicios anteriores [00483]")
    t00484 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Ingresos fiscales a distribuir en varios ejercicios - Otras aportaciones de socios [00484]")
    t00492 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Capital - Escriturado [00492]")
    t00493 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Capital - No exigido [00493]")
    t00494 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Prima de emisión [00494]")
    t00495 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Reservas [00495]")
    t00496 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Acciones y participaciones en patrimonio propias  [00496]")
    t00497 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Resultados ejercicios anteriores [00497]")
    t00498 = fields.Float(string="Ingresos y gastos reconocidos en patrimonio neto - Otros ingresos y gastos reconocidos en patrimonio neto - Otras aportaciones de socios [00498]")
    t00506 = fields.Float(string="Operaciones con socios o propietarios - Capital - Escriturado [00506]")
    t00507 = fields.Float(string="Operaciones con socios o propietarios - Capital - No exigido [00507]")
    t00508 = fields.Float(string="Operaciones con socios o propietarios - Prima de emisión [00508]")
    t00509 = fields.Float(string="Operaciones con socios o propietarios - Reservas [00509]")
    t00510 = fields.Float(string="Operaciones con socios o propietarios - Acciones y participaciones en patrimonio propias [00510]")
    t00511 = fields.Float(string="Operaciones con socios o propietarios - Resultados ejercicios anteriores [00511]")
    t00512 = fields.Float(string="Operaciones con socios o propietarios - Otras aportaciones de socios [00512]")
    t00520 = fields.Float(string="Operaciones con socios o propietarios - Aumentos de capital - Capital - Escriturado [00520]")
    t00521 = fields.Float(string="Operaciones con socios o propietarios - Aumentos de capital - Capital - No exigido [00521]")
    t00522 = fields.Float(string="Operaciones con socios o propietarios - Aumentos de capital - Prima de emisión [00522]")
    t00523 = fields.Float(string="Operaciones con socios o propietarios - Aumentos de capital - Reservas [00523]")
    t00524 = fields.Float(string="Operaciones con socios o propietarios - Aumentos de capital - Acciones y participaciones en patrimonio propias  [00524]")
    t00525 = fields.Float(string="Operaciones con socios o propietarios - Aumentos de capital - Resultados ejercicios anteriores [00525]")
    t00526 = fields.Float(string="Operaciones con socios o propietarios - Aumentos de capital - Otras aportaciones de socios [00526]")
    t00534 = fields.Float(string="Operaciones con socios o propietarios - (-) Reducciones de capital - Capital - Escriturado [00534]")
    t00535 = fields.Float(string="Operaciones con socios o propietarios - (-) Reducciones de capital - Capital - No exigido [00535]")
    t00536 = fields.Float(string="Operaciones con socios o propietarios - (-) Reducciones de capital - Prima de emisión [00536]")
    t00537 = fields.Float(string="Operaciones con socios o propietarios - (-) Reducciones de capital - Reservas [00537]")
    t00538 = fields.Float(string="Operaciones con socios o propietarios - (-) Reducciones de capital - Acciones y participaciones en patrimonio propias  [00538]")
    t00539 = fields.Float(string="Operaciones con socios o propietarios - (-) Reducciones de capital - Resultados ejercicios anteriores [00539]")
    t00540 = fields.Float(string="Operaciones con socios o propietarios - (-) Reducciones de capital - Otras aportaciones de socios [00540]")
    t00548 = fields.Float(string="Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Capital - Escriturado [00548]")
    t00549 = fields.Float(string="Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Capital - No exigido [00549]")
    t00550 = fields.Float(string="Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Prima de emisión [00550]")
    t00551 = fields.Float(string="Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Reservas [00551]")
    t00552 = fields.Float(string="Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Acciones y participaciones en patrimonio propias [00552]")
    t00553 = fields.Float(string="Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Resultados ejercicios anteriores [00553]")
    t00554 = fields.Float(string="Operaciones con socios o propietarios - Conversión de pasivos en patrim. neto - Otras aportaciones de socios [00554]")
    t00562 = fields.Float(string="Operaciones con socios o propietarios - (-) Distribución de dividendos - Capital - Escriturado [00562]")
    t00563 = fields.Float(string="Operaciones con socios o propietarios - (-) Distribución de dividendos - Capital - No exigido [00563]")
    t00564 = fields.Float(string="Operaciones con socios o propietarios - (-) Distribución de dividendos - Prima de emisión [00564]")
    t00565 = fields.Float(string="Operaciones con socios o propietarios - (-) Distribución de dividendos - Reservas [00565]")
    t00566 = fields.Float(string="Operaciones con socios o propietarios - (-) Distribución de dividendos - Acciones y participaciones en patrimonio propias  [00566]")
    t00567 = fields.Float(string="Operaciones con socios o propietarios - (-) Distribución de dividendos - Resultados ejercicios anteriores [00567]")
    t00568 = fields.Float(string="Operaciones con socios o propietarios - (-) Distribución de dividendos - Otras aportaciones de socios [00568]")
    t00576 = fields.Float(string="Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Capital - Escriturado [00576]")
    t00577 = fields.Float(string="Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Capital - No exigido [00577]")
    t00578 = fields.Float(string="Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Prima de emisión [00578]")
    t00579 = fields.Float(string="Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Reservas [00579]")
    t00580 = fields.Float(string="Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Acciones y participaciones en patrimonio propias [00580]")
    t00581 = fields.Float(string="Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Resultados ejercicios anteriores [00581]")
    t00582 = fields.Float(string="Operaciones con socios o propietarios - Operaciones con acciones o participaciones propias - Otras aportaciones de socios [00582]")
    t00590 = fields.Float(string="Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Capital  - Escriturado [00590]")
    t00591 = fields.Float(string="Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Capital  - No exigido [00591]")
    t00592 = fields.Float(string="Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Prima de emisión [00592]")
    t00593 = fields.Float(string="Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Reservas [00593]")
    t00594 = fields.Float(string="Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Acciones y participaciones en patrimonio propias [00594]")
    t00595 = fields.Float(string="Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Resultados ejercicios anteriores [00595]")
    t00596 = fields.Float(string="Operaciones con socios o propietarios - Incremento (reducción) de patr. neto de combinación de negocios - Otras aportaciones de socios [00596]")
    t00604 = fields.Float(string="Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Capital -  Escriturado [00604]")
    t00605 = fields.Float(string="Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Capital - No exigido [00605]")
    t00606 = fields.Float(string="Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Prima de emisión [00606]")
    t00607 = fields.Float(string="Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Reservas [00607]")
    t00608 = fields.Float(string="Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Acciones y participaciones en patrimonio propias [00608]")
    t00609 = fields.Float(string="Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Resultados ejercicios anteriores [00609]")
    t00610 = fields.Float(string="Operaciones con socios o propietarios - Otras operaciones con socios o propietarios - Otras aportaciones de socios [00610]")
    t00618 = fields.Float(string="Otras variaciones del patrimonio neto - Capital - Escriturado [00618]")
    t00619 = fields.Float(string="Otras variaciones del patrimonio neto - Capital - No exigido [00619]")
    t00620 = fields.Float(string="Otras variaciones del patrimonio neto - Prima de emisión [00620]")
    t00621 = fields.Float(string="Otras variaciones del patrimonio neto - Reservas [00621]")
    t00622 = fields.Float(string="Otras variaciones del patrimonio neto - Acciones y participaciones en patrimonio propias [00622]")
    t00623 = fields.Float(string="Otras variaciones del patrimonio neto - Resultados ejercicios anteriores [00623]")
    t00624 = fields.Float(string="Otras variaciones del patrimonio neto - Otras aportaciones de socios [00624]")
    t00715 = fields.Float(string="Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Capital - Escriturado [00715]")
    t00716 = fields.Float(string="Otras variaciones del patrimonio neto - Movimiento reserva revalorización -  Capital - No exigido [00716]")
    t00717 = fields.Float(string="Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Prima de emisión [00717]")
    t00718 = fields.Float(string="Otras variaciones del patrimonio neto - Movimiento reserva revalorización -  Reservas [00718]")
    t00719 = fields.Float(string="Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Acciones y participaciones en patrimonio propias [00719]")
    t00720 = fields.Float(string="Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Resultados ejercicios anteriores [00720]")
    t00721 = fields.Float(string="Otras variaciones del patrimonio neto - Movimiento reserva revalorización - Otras aportaciones de socios [00721]")
    t00729 = fields.Float(string="Otras variaciones del patrimonio neto - Otras variaciones - Capital - Escriturado [00729]")
    t00730 = fields.Float(string="Otras variaciones del patrimonio neto - Otras variaciones -  Capital - No exigido [00730]")
    t00731 = fields.Float(string="Otras variaciones del patrimonio neto - Otras variaciones - Prima de emisión [00731]")
    t00732 = fields.Float(string="Otras variaciones del patrimonio neto - Otras variaciones -  Reservas [00732]")
    t00733 = fields.Float(string="Otras variaciones del patrimonio neto - Otras variaciones - Acciones y participaciones en patrimonio propias  [00733]")
    t00734 = fields.Float(string="Otras variaciones del patrimonio neto - Otras variaciones - Resultados ejercicios anteriores [00734]")
    t00735 = fields.Float(string="Otras variaciones del patrimonio neto - Otras variaciones - Otras aportaciones de socios [00735]")
    t00632 = fields.Float(string="SALDO, FINAL DEL EJERCICIO - Capital - Escriturado [00632]")
    t00633 = fields.Float(string="SALDO, FINAL DEL EJERCICIO - Capital - No exigido [00633]")
    t00634 = fields.Float(string="SALDO, FINAL DEL EJERCICIO - Prima de emisión [00634]")
    t00635 = fields.Float(string="SALDO, FINAL DEL EJERCICIO - Reservas [00635]")
    t00636 = fields.Float(string="SALDO, FINAL DEL EJERCICIO - Acciones y participaciones en patrimonio propias [00636]")
    t00637 = fields.Float(string="SALDO, FINAL DEL EJERCICIO - Resultados ejercicios anteriores [00637]")
    t00638 = fields.Float(string="SALDO, FINAL DEL EJERCICIO - Otras aportaciones de socios [00638]")
    
  #Acontinuación se define el modelo para la declaración del Modelo 200

    _name = 'modelo200.declaration'
    _description = "Declaración IS - Modelo 200"

    company_id = fields.Many2one('res.company', string="Empresa", required=True, default=lambda self: self.env.company.id)
    fiscal_year = fields.Char(string="Ejercicio", required=True, default=lambda self: str(fields.Date.today().year - 1))
    date_start = fields.Date(string="Inicio Ejercicio")
    date_end = fields.Date(string="Fin Ejercicio")
    state = fields.Selection([('draft', 'Borrador'), ('generated', 'Generado')], default='draft')

    bs_assets_total = fields.Float(string="Total Activo")
    bs_equity_liabs_total = fields.Float(string="Total PN y Pasivo")
    pl_net_turnover = fields.Float(string="Importe Neto Cifra Negocios")
    pl_profit_before_tax = fields.Float(string="Resultado Antes Impuestos")
    pl_profit_after_tax = fields.Float(string="Resultado del Ejercicio")
    equity_start = fields.Float(string="PN Inicial")
    equity_end = fields.Float(string="PN Final")
# Suma los movimientos contables de las cuentas cuyo código comience con los prefijos indicados
# Esta función filtra las líneas del diario dentro del ejercicio fiscal y compañía actual

    # Función interna para obtener el saldo de todas las cuentas contables cuyo código empieza por determinados prefijos
    # Usa dominios de búsqueda de Odoo sobre 'account.move.line' para filtrar los apuntes contables
    def _sum_accounts(self, account_prefixes):
        domain = [
            ('date', '>=', self.date_start),
            ('date', '<=', self.date_end),
            ('company_id', '=', self.company_id.id),
            ('move_id.state', '=', 'posted')
        ]
        prefix_domain = [('account_id.code', '=like', f'{p}%') for p in account_prefixes]
        lines = self.env['account.move.line'].search(domain + ['|'] * (len(prefix_domain) - 1) + prefix_domain)
        return sum(line.debit - line.credit for line in lines)

# Calcula automáticamente los valores contables clave para el Modelo 200 a partir de los apuntes contables

        # Calcula automáticamente los datos contables relevantes para el Modelo 200
        # Esta función se ejecuta antes de generar el XML para asegurar que los valores estén actualizados
    def compute_financials(self):
        for rec in self:
            year = int(rec.fiscal_year)
            rec.date_start = date(year, 1, 1)
            rec.date_end = date(year, 12, 31)
            rec.bs_assets_total = rec._sum_accounts(['2', '3', '4', '5'])
            rec.bs_equity_liabs_total = rec._sum_accounts(['1', '5'])
            rec.pl_net_turnover = rec._sum_accounts(['70']) - rec._sum_accounts(['706']) + rec._sum_accounts(['705'])
            ingresos = rec._sum_accounts(['7'])
            gastos = rec._sum_accounts(['6'])
            rec.pl_profit_before_tax = ingresos - gastos
            resultado = rec._sum_accounts(['129'])
            impuesto = rec._sum_accounts(['630'])
            rec.pl_profit_after_tax = resultado if resultado else rec.pl_profit_before_tax - impuesto
            rec.equity_end = rec._sum_accounts(['1'])
            opening_lines = self.env['account.move.line'].search([
                ('date', '<', rec.date_start),
                ('account_id.code', '=like', '1%'),
                ('company_id', '=', rec.company_id.id),
                ('move_id.state', '=', 'posted')
            ])
            rec.equity_start = sum(line.debit - line.credit for line in opening_lines)

# Genera el archivo XML de la declaración con los datos calculados
# Este archivo puede ser importado en la sede electrónica de la AEAT

    # Función principal para generar el archivo XML del Modelo 200
    # Llama a compute_financials(), genera una cadena XML y la guarda como archivo adjunto binario

from ..utils.estructura_xml_fija import estructura_xml_fija
import xml.etree.ElementTree as ET
import base64
import logging
_logger = logging.getLogger(__name__)

