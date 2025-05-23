from odoo import models, fields, api
import base64
from datetime import date

# Extensión del modelo res.company para incluir datos del administrador de la sociedad
class ResCompany(models.Model):
    _inherit = 'res.company'

    admin_name = fields.Char(string="Administrador - Nombre")
    admin_nif = fields.Char(string="Administrador - NIF")
    admin_position = fields.Char(string="Administrador - Cargo")

# Modelo principal para generar la declaración Modelo 200 y almacenar sus datos contables y fiscales
class Modelo200Declaration(models.Model):
    cnae = fields.Char(string="CNAE")
    _inherit = ['mail.thread', 'mail.activity.mixin']
    # Campos faltantes detectados por comparación con XML
    p20000001 = fields.Float(string="Campo sin descripción")
    p20000003 = fields.Float(string="Campo sin descripción")
    p20000006 = fields.Float(string="Campo sin descripción")
    p20000011 = fields.Float(string="Campo sin descripción")
    p20000012 = fields.Float(string="Campo sin descripción")
    p20000013 = fields.Float(string="Campo sin descripción")
    p20000030 = fields.Float(string="Campo sin descripción")
    p20000047 = fields.Float(string="Campo sin descripción")
    p20000064 = fields.Float(string="Campo sin descripción")
    p20000081 = fields.Float(string="Campo sin descripción")
    p20000098 = fields.Float(string="Campo sin descripción")
    p20000115 = fields.Float(string="Campo sin descripción")
    p20000132 = fields.Float(string="Campo sin descripción")
    p20000149 = fields.Float(string="Campo sin descripción")
    p20000166 = fields.Float(string="Campo sin descripción")
    p20000183 = fields.Float(string="Campo sin descripción")
    p20000200 = fields.Float(string="Campo sin descripción")
    p20000217 = fields.Float(string="Campo sin descripción")
    p20000234 = fields.Float(string="Campo sin descripción")
    p20000251 = fields.Float(string="Campo sin descripción")
    p20000268 = fields.Float(string="Campo sin descripción")
    p20000285 = fields.Float(string="Campo sin descripción")
    p20000302 = fields.Float(string="Campo sin descripción")
    p20000319 = fields.Float(string="Campo sin descripción")
    p20000336 = fields.Float(string="Campo sin descripción")
    p20000353 = fields.Float(string="Campo sin descripción")
    p20000370 = fields.Float(string="Campo sin descripción")
    p20000387 = fields.Float(string="Campo sin descripción")
    p20000404 = fields.Float(string="Campo sin descripción")
    p20000421 = fields.Float(string="Campo sin descripción")
    p20000438 = fields.Float(string="Campo sin descripción")
    p20000455 = fields.Float(string="Campo sin descripción")
    p20000472 = fields.Float(string="Campo sin descripción")
    p20000489 = fields.Float(string="Campo sin descripción")
    p20000506 = fields.Float(string="Campo sin descripción")
    p20000523 = fields.Float(string="Campo sin descripción")
    p20000540 = fields.Float(string="Campo sin descripción")
    p20000557 = fields.Float(string="Campo sin descripción")
    p20000570 = fields.Float(string="Campo sin descripción")
    p20000574 = fields.Float(string="Campo sin descripción")
    p20000591 = fields.Float(string="Campo sin descripción")
    p20000608 = fields.Float(string="Campo sin descripción")
    p20000625 = fields.Float(string="Campo sin descripción")
    p20000642 = fields.Float(string="Campo sin descripción")
    p20000659 = fields.Float(string="Campo sin descripción")
    p20000676 = fields.Float(string="Campo sin descripción")
    p20000693 = fields.Float(string="Campo sin descripción")
    p20000710 = fields.Float(string="Campo sin descripción")
    p20000727 = fields.Float(string="Campo sin descripción")
    p20000744 = fields.Float(string="Campo sin descripción")
    p20000757 = fields.Float(string="Campo sin descripción")
    p20000761 = fields.Float(string="Campo sin descripción")
    p20000778 = fields.Float(string="Campo sin descripción")
    p20000795 = fields.Float(string="Campo sin descripción")
    p20000812 = fields.Float(string="Campo sin descripción")
    p20000829 = fields.Float(string="Campo sin descripción")
    p20000846 = fields.Float(string="Campo sin descripción")
    p20000863 = fields.Float(string="Campo sin descripción")
    p20000876 = fields.Float(string="Campo sin descripción")
    p20000880 = fields.Float(string="Campo sin descripción")
    p20000897 = fields.Float(string="Campo sin descripción")
    p20000914 = fields.Float(string="Campo sin descripción")
    p20000931 = fields.Float(string="Campo sin descripción")
    p20000948 = fields.Float(string="Campo sin descripción")
    p20000965 = fields.Float(string="Campo sin descripción")
    p20000982 = fields.Float(string="Campo sin descripción")
    p20000999 = fields.Float(string="Campo sin descripción")
    p20001016 = fields.Float(string="Campo sin descripción")
    p20001033 = fields.Float(string="Campo sin descripción")
    p20001050 = fields.Float(string="Campo sin descripción")
    p20001063 = fields.Float(string="Campo sin descripción")
    p20001199 = fields.Float(string="Campo sin descripción")
    p20001250 = fields.Float(string="Campo sin descripción")
    _name = 'modelo200.declaration'
    _description = "Declaración IS - Modelo 200"

    company_id = fields.Many2one('res.company', string="Empresa", required=True, default=lambda self: self.env.company)
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

    xml_file = fields.Binary(string="Archivo XML")
    xml_filename = fields.Char(string="Nombre Archivo")

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
    def action_generate_xml(self):
        self.compute_financials()
        for rec in self:
            xml_content = f"""<?xml version='1.0' encoding='UTF-8'?>
<Modelo200 ejercicio='{rec.fiscal_year}'>
    <Identificacion>
        <NIF>{rec.company_id.vat}</NIF>
        <RazonSocial>{rec.company_id.name}</RazonSocial>
    </Identificacion>
    <Balance>
        <Activo>
            <TotalActivo>{int(rec.bs_assets_total)}</TotalActivo>
        </Activo>
        <PasivoPN>
            <TotalPNPasivo>{int(rec.bs_equity_liabs_total)}</TotalPNPasivo>
        </PasivoPN>
    </Balance>
    <CuentaPyG>
        <CifraNegocios>{int(rec.pl_net_turnover)}</CifraNegocios>
        <ResultadoAntesImpuestos>{int(rec.pl_profit_before_tax)}</ResultadoAntesImpuestos>
        <ResultadoEjercicio>{int(rec.pl_profit_after_tax)}</ResultadoEjercicio>
    </CuentaPyG>
    <EstadoCambiosPN>
        <PNInicial>{int(rec.equity_start)}</PNInicial>
        <PNFinal>{int(rec.equity_end)}</PNFinal>
    </EstadoCambiosPN>
</Modelo200>
"""
            rec.xml_file = base64.b64encode(xml_content.encode('utf-8'))
            rec.xml_filename = f"modelo200_{rec.fiscal_year}.xml"
            rec.state = 'generated'


    def generar_xml(self):
        for rec in self:
            contenido = f"""<?xml version="1.0" encoding="UTF-8"?>
<Modelo200 ejercicio="{rec.ejercicio}">
  <Empresa>{rec.company_id.name}</Empresa>
</Modelo200>
"""
            rec.nombre_xml = f"modelo200_{rec.ejercicio}.xml"
            rec.archivo_xml = base64.b64encode(contenido.encode("utf-8"))

    def action_calcular_datos(self):
        for rec in self:
            # Ejemplos de cálculo automático
            # rec.p20000115 = rec.p20000101 + rec.p20000102  # [ejemplo]
            # rec.p20000500 = 0.25 * rec.p20000510  # [ejemplo]
            pass
    