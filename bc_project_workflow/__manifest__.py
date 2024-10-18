# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'BC_Project_Workflow',
    'depends': ['project'],
    'data': [
        'security/ir.model.access.csv',

        'views/project_task_test_views.xml',
        'views/project_task_type_views.xml',
        'views/project_task_portal_templates.xml',
        'views/project_task_views.xml',
        'views/project_task_test_portal_template.xml',
        'views/project_task_test_list_views.xml',
        'views/project_menu.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'bc_project_workflow/static/src/**/*',
        ],
    },
    'application': True,
}