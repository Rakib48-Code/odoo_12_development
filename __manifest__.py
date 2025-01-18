{
    'name':'Hospital Management',
    'version':'12.0.0.1.2',
    'category':'Hospital',
    'sequence':1,
    'summary': 'Odoo 12 development tutorials',
    'author':'Rakib Hasan',
    'depends':['mail'],
    'data':[
        # security file
        'security/ir.model.access.csv',

        # data files
        'data/patient_sequence.xml',
        'data/patient_ref.xml',

        # views file
        'views/menu.xml',
        'views/patient_view.xml',
        'views/appointment_view.xml',
    ],
    'installable':True,
    'application': True,
}