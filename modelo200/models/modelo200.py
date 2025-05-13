from odoo import models, fields, api
import base64
from datetime import date

class ResCompany(models.Model):
    _inherit = 'res.company'

    admin_name = fields.Char(string="Administrador - Nombre")
    admin_nif = fields.Char(string="Administrador - NIF")
    admin_position = fields.Char(string="Administrador - Cargo")

class Modelo200Declaration(models.Model):
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
