from odoo import models, fields

class Project(models.Model):
    _inherit = "project.project"

    release_ids = fields.One2many('project.release', 'project_id')