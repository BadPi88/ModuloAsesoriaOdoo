{
    'name': "Modelo 200 - Impuesto sobre Sociedades",
    'summary': "Generación del Modelo 200 (IS) en XML para AEAT",
    'version': '16.0.1.0.0',
    'category': 'Accounting/Localization',
    'author': "Tu Empresa",
    'website': "http://www.tu-empresa.com",
    'license': "AGPL-3",
    'depends': ['account', 'l10n_es'],
    'data': [
        'models/modelo200_declaration.xml',
        'security/ir.model.access.csv',
        'views/res_company_view.xml',
        'views/modelo200_views.xml',
    ],
    'installable': True,
    'application': False,
}
