from odoo.http import request, Controller, route

class TagController(Controller):

    @route(['/my/tasks/<int:task_id>'], auth="public", website=True)
    def task_detail(self, **kwargs):

        all_tag_ids = request.env['bc_project_workflow.test.tag'].sudo().search([])
        import pdb;pdb.set_trace()
        return request.render('bc_project_workflow.portal_testing_table', {
            'all_tag_ids': all_tag_ids,
        })
