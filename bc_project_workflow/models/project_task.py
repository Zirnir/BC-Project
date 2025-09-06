from odoo import models, api, fields #Importantion des packets Odoo.
from odoo.exceptions import UserError

class Task(models.Model): 
    _inherit = "project.task" 
                              
    test_ids = fields.One2many("project.task.test", "task_id") 
    

    release_id = fields.Many2one('project.release')
    update_instruction = fields.Html()

    @api.model
    def create(self, values):
        task = super(Task, self).create(values)
        return task

    def write(self, values):
        if 'stage_id' in values: 
            stage = self.env['project.task.type'].browse(values['stage_id'])

            if stage.in_progress_stage: 
                for user in self.user_ids: 
                    tasks_in_progress = self.env['project.task'].search([
                        ('user_ids', 'in', [user.id]),
                        ('stage_id.in_progress_stage', '=', True),
                        ('id', '!=', self.id)
                    ])
                    if tasks_in_progress: 
                        raise UserError(f"L'utilisateur {user.name} a déjà une tâche en cours.")

            if stage.testing_stage:
                for test in self.test_ids:
                    if test.validated == False :
                        test.validated = 'intest'
                in_progress_releases = self.project_id.release_ids.filtered(lambda r: r.state == 'in_progress')
                if in_progress_releases:
                    release = in_progress_releases[0]
                    self.release_id = release.id
                else: 
                    draft_releases = self.project_id.release_ids.filtered(lambda r: r.state == 'draft')
                    if draft_releases:
                        release = draft_releases[0]
                        self.release_id = release.id 
                        release.state = 'in_progress'
                    else:
                        release_data = {
                            'name': f"Release {len(self.project_id.release_ids) + 1}",
                            'project_id': self.project_id.id,
                            'state': 'in_progress',
                        }
                        new_release = self.env['project.release'].create(release_data)
                        self.release_id = new_release.id 
                
        if self.stage_id.in_progress_stage:
            if 'user_ids' in values:
                user_ids_operations = values.get('user_ids', [])
                new_user_ids = []
                
                for operation in user_ids_operations:
                    if operation[0] == 6:
                        new_user_ids = operation[2]
                    elif operation[0] == 4:
                        new_user_ids.append(operation[1])

                if new_user_ids:
                    users = self.env['res.users'].browse(new_user_ids)
                    for user in users:
                        tasks_in_progress = self.env['project.task'].search([
                            ('user_ids', 'in', [user.id]),
                            ('stage_id.in_progress_stage', '=', True),
                            ('id', '!=', self.id)
                        ])
                        if tasks_in_progress:
                            raise UserError(f"L'utilisateur {user.name} a déjà une tâche en cours.")

        return super(Task, self).write(values)
    
    def action_get_test_record(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Task',
            'view_mode': 'tree',
            'res_model': 'project.task.test',
            'domain': [('task_id', '=', self.id)]
        }