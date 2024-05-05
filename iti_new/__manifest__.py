
{
    'name': 'Hospitals Management System',
    'author': 'Buthina',
    'website': 'https://iti.gov.eg/home',
    'category': 'Healthcare',
    'description': 'This module manages hospitals and patients information.',
    'depends':['base'],
    'data':[
        'security/ir.model.access.csv',
        'security/res_group.xml',
        'views/hms_patient_views.xml',
        'views/hms_department_views.xml',
        'views/hms_doctor_views.xml',
        'views/crm_custmor_views.xml',
        'reports/iti_patient_template.xml',
        'reports/reports.xml'
            ]
}
