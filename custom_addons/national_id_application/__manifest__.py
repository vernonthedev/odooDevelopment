{
    'name': 'National ID Application',
    'version': '1.0',
    'category': 'Custom',
    'author': 'Masamba Vernon',
    'summary': 'A module to handle national ID applications',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/national_id_form.xml',
        'views/menu.xml',

    ],
    'installable': True,
    'application': True,
}
