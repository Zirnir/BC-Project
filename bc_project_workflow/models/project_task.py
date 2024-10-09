from odoo import models, api
from odoo.exceptions import UserError

class Task(models.Model):
    _inherit = "project.task"

    def write(self, values):
        if 'stage_id' in values:
            stage = self.env['project.task.type'].browse(values['stage_id'])

            if stage.name == "En cours":
                for user in self.user_ids:
                    tasks_in_progress = self.env['project.task'].search([
                        ('user_ids', 'in', [user.id]),
                        ('stage_id.name', '=', 'En cours'),
                        ('id', '!=', self.id)
                    ])
                    if tasks_in_progress:
                        raise UserError(f"L'utilisateur {user.name} a déjà une tâche en cours.") 
        
        if self.stage_id.name == "En cours" or ('stage_id' in values and stage.name == "En cours"):
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
                            ('stage_id.name', '=', 'En cours'),
                            ('id', '!=', self.id)
                        ])
                        if tasks_in_progress:
                            raise UserError(f"L'utilisateur {user.name} a déjà une tâche en cours.")

        return super(Task, self).write(values)
