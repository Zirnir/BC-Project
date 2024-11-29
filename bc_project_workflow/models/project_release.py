from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import datetime

class ProjectRelaese(models.Model):
    _name="project.release"
    _description="Release of project"
    _inherit='mail.thread' 

    name = fields.Char(required=True)
    release_date = fields.Datetime(store=True)
    state = fields.Selection(
        default='draft',
        selection=[('draft', 'Draft'), ('in_progress', 'In Progress'), ('released', 'Released'), ('cancel', 'Cancel')])
    project_id = fields.Many2one('project.project')
    task_ids = fields.One2many( 'project.task', 'release_id', tracking=True)
    task_count = fields.Integer(string='Task', compute='_compute_task_count', default=0)
    is_ready_to_release = fields.Boolean(compute="_compute_is_ready_to_release")
    update_instruction = fields.Html(compute="_compute_update_instruction")


    @api.depends('task_ids', 'task_ids.update_instruction', 'task_ids.stage_id', 'state')
    def _compute_update_instruction(self):
        if self.task_ids:
            for record in self:
                for task in record.task_ids:
                    instruction = f"<p><h4><strong>{task.name}:</strong></h4>{task.update_instruction}</p>"
                    record.update_instruction = str(record.update_instruction or '<h2><strong>Release instruction:</strong></h2>')+ instruction
        else:
            if self.state == 'in_progress':
                self.update_instruction = '<strong>No tasks assigned to this release</strong>'
            else:
                self.update_instruction = None

    @api.depends('task_ids', 'task_ids.test_ids', 'task_ids.test_ids.validated')
    def _compute_is_ready_to_release(self):
        if self.task_ids:
            for record in self:
                for task in record.task_ids:
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
        else:
            self.is_ready_to_release = False
    
    def _compute_task_count(self):
        for record in self:
           record.task_count = len(record.task_ids)


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
    
    def released_button(self):

        self.state = 'released'
        self.release_date = datetime.now()

        return True
    
    def cancel_button(self):

        self.state = 'cancel'
        self.task_ids = [(5, 0, 0)]

        return True

    def draft_button(self):

        self.state = 'draft'
        self.task_ids = [(5, 0, 0)]

        return True

    def in_progress_button(self):
        self.state = 'in_progress'
        return True
    
    def action_get_task_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Task',
            'view_mode': 'tree',
            'res_model': 'project.task',
            'domain': [('release_id', '=', self.id)]
        }