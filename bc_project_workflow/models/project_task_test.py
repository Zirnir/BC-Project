from odoo import fields, models, api, _
from datetime import datetime

class TaskTest (models.Model):
    _name = "project.task.test"
    _description = "Test of task"

    name = fields.Char()

    description = fields.Html(sanitize_attributes=False)
    summary = fields.Html(compute = "_compute_summary" ,sanitize_attributes=False)

    validated_date = fields.Datetime(store=True)

    validated = fields.Selection(
        
        selection=[('accepted', 'Accepted'), ('refused', 'Refused'),('intest', 'In Test')],
        help = ""
    )

    refused_justify = fields.Text()
    customer = fields.Char()

    task_id = fields.Many2one("project.task")

    @api.depends('description')
    def _compute_summary(self):
        for record in self:
            if record.description:
                record.summary = record.description[:40]
            else:
                record.summary = ""
    
    @api.model
    def create(self, values):
        task = self.env['project.task'].browse(values['task_id'])
        if task.stage_id.testing_stage:
            values['validated'] = 'intest'

        return super(TaskTest, self).create(values)

    def accepted(self):
        for record in self.sudo():
            record.validated = 'accepted'
            record.validated_date = datetime.now()
            record.customer = self.env.user.name
    
    def refused(self, justify):
        for record in self.sudo():
            record.validated = 'refused'
            record.refused_justify = justify

            record.customer = self.env.user.name

            blocked_stage = self.env['project.task.type'].search([('blocked_stage', '=', True)])
            record.task_id.stage_id = blocked_stage.id

    def button_test_modal(self):
        return {
            "name": _("Test modal"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "project.task.test",
            "res_id": self.id,
            "target": "new",
            "context": {
                "default_test_id": self.id,
            },
        }

            