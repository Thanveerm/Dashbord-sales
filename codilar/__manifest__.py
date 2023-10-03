{
    'name': 'Codilar Project and Timesheet',
    'version': '15.0.1.1.0',
    'sequence': -100,
    'description': """
        This module is project and timesheet
        """,

    'author': "Thanveer",
    'company': 'Codilar Technology',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.codilar.com",
    'depends': ['project', 'hr_timesheet', 'sale', ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/task_start_date.xml',
        'views/sale_order_sdate_edate.xml',
        'reports/sale_report_inherit.xml',
        'reports/invoice_inherit_report.xml',
        'views/invoice_nofication_template.xml',
        'views/crone.xml',
        # 'views/inherit_branch.xml',
        'views/mail_confirm_template.xml',
        'views/mail_invoice_template.xml',

    ],

    'license': 'AGPL-3',
    'installable': True,
    'auto_install': False,
    'application': True,
}
