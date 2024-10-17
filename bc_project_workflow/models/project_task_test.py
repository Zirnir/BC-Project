from odoo import fields, models
from datetime import date

class TaskTest (models.Model):
    _name = "project.task.test"
    _description = "Test of task"

    name = fields.Char()
    description = fields.Text()

    create_date = fields.Date(default=lambda self: date.today())

    valideted = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help = ""
    )

    refused_justify = fields.Text()

    task_id = fields.Many2one("project.task")

    def accepted(self):
        for record in self:
            record.valideted = 'accepted'
    
    def refused(self, justify):
        for record in self:
            record.valideted = 'refused'
            record.refused_justify = justify

            