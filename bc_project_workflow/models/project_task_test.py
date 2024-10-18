from odoo import fields, models, api
from datetime import date

class TaskTest (models.Model):
    _name = "project.task.test"
    _description = "Test of task"

    name = fields.Char()
    description = fields.Html(sanitize_attributes=False)
    summary = fields.Html(compute = "_compute_summary" ,sanitize_attributes=False)

    create_date = fields.Date(default=lambda self: date.today())

    valideted = fields.Selection(
        default = 'intest',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused'),('intest', 'In Test')],
        help = ""
    )

    refused_justify = fields.Text()

    task_id = fields.Many2one("project.task")

    @api.depends('description')
    def _compute_summary(self):
        for record in self:
            if record.description:
                record.summary = record.description[:40]
            else:
                record.summary = str(record.name) + " de la tâche " + str(record.task_id.name) + " est en cours d'écriture."


    def accepted(self):
        for record in self:
            record.valideted = 'accepted'
    
    def refused(self, justify):
        for record in self:
            record.valideted = 'refused'
            record.refused_justify = justify

            