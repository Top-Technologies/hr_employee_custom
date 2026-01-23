{
    'name': 'Employee Age & Experience',
    'version': '1.0',
    'category': 'Human Resources/Employees',
    'summary': 'Automatic calculation of age and experience.',

    'author': 'Yohannes Shiwerekey',
    'depends': ['hr', 'hr_skills', 'hr_contract'],
    'data': [
        'views/hr_employee_views.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'hr_employee_custom/static/src/xml/resume_templates.xml',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
