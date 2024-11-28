from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime

class ProjectRelaese(models.Model):
    _name="project.release"
    _description="Release of project"

    name = fields.Char(required=True)
    release_date = fields.Datetime(store=True)
    state = fields.Selection(
        default=None,
        selection=[('draft', 'Draft'), ('in_progress', 'In Progress'), ('released', 'Released'), ('cancel', 'Cancel')])
    project_id = fields.Many2one('project.project')
    task_ids = fields.One2many( 'project.task', 'release_id')
    is_ready_to_release = fields.Boolean()
    update_instruction = fields.Html()

    @api.onchange('state')
    def _onchange_state(self):
        if self.state == 'in_progress':
            in_progress_release = self.env['project.release'].search([
                ('project_id', '=', self.project_id.id),
                ('state', '=', 'in_progress'),
                ('id', '!=', self._origin.id),
            ])
            if in_progress_release:
                raise UserError(f"The project {self.project_id.name} have already a release in progress")
            
            else:
                print("OK")

    @api.onchange('task_ids')
    def _onchange_state(self):
        for task in self.project_id.task_ids:
            if task.release_id == self.id:
                self.task_ids = [(4, task.id)]

    def all_test_validated (self):
        for task in self.task_ids:
            parent_test = self.env['project.task.test'].search([
                ('parent_id', '=', None),
                ('task_id', '=', task.id),
            ])
            parent_count = 0
            for test in parent_test:
                if test.validated == 'accepted':
                    parent_count +=1

            if parent_count == len(parent_test):
                self.is_ready_to_release = True
                parent_count = 0
            else:
                self.is_ready_to_release = False
                parent_count = 0
    
    def released_button(self):

        self.state = 'released'
        self.release_date = datetime.now()

        return True
    
    def cancel_button(self):

        self.state = 'cancel'
        self.is_ready_to_release = False
        self.task_ids = [(5, 0, 0)]

        return True



