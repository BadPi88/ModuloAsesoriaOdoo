{
    'name': "Modelo 200 - Impuesto sobre Sociedades",
    'summary': "Generación del Modelo 200 (IS) en XML para AEAT",
    'version': '16.0.1.0.0',
    'category': 'Accounting/Localization',
    'author': "Miguel Martin Gil",
    'website': "http://www.mmg.com",
    'license': "AGPL-3",
    'depends': ['account', 'l10n_es'],
    'data': [
        'security/ir.model.access.csv',
        'views/modelo200_views.xml',
        'views/res_company_views.xml',
    ],
    'installable': True,
    'application': False,
}
