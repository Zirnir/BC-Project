from odoo import models, fields
from odoo.exceptions import UserError

class Task(models.Model):
    _inherit = "project.task.type"

    in_progress_stage = fields.Boolean()
    testing_stage = fields.Boolean()
    blocked_stage = fields.Boolean()