from odoo import fields, models, api, _
from datetime import datetime

class TaskTest (models.Model):
    _name = "project.task.test"
    _description = "Test of task"
    _inherit = ['mail.thread']

    name = fields.Char()

    description = fields.Html(sanitize_attributes=False)
    summary = fields.Html(compute = "_compute_summary" ,sanitize_attributes=False)

    validated_date = fields.Datetime(store=True)

    validated = fields.Selection(
        default= None,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused'),('intest', 'In Test')],
        help = ""
    )

    refused_justify = fields.Html()
    customer = fields.Char()

    task_id = fields.Many2one("project.task")

    parent_id = fields.Many2one('project.task.test', string='Parent Test')
    child_ids = fields.One2many('project.task.test', 'parent_id', string="Child-Test")
    childtest_count = fields.Integer("Child Test", default=0)

    tags = fields.Many2many("test.tag", string="Justify Tag")

    files = fields.Binary(string="Upload File", attachment=True)

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

    def child_test_created(self):
        if self.parent_id : 
            parent_test = self.parent_id
            parent_test.childtest_count +=1
            child_test_vals = {
                'name' : parent_test.name + ".Version " + str(parent_test.childtest_count),
                'parent_id' : parent_test.id,
                'task_id' : parent_test.task_id.id,
            }
            self.env['project.task.test'].create(child_test_vals) 
            
        else:
            self.childtest_count +=1
            child_test_vals = {
                'name' : self.name + ".Version " + str(self.childtest_count),
                'parent_id' : self.id,
                'task_id' : self.task_id.id,
            }
            self.env['project.task.test'].create(child_test_vals) 

    def accepted(self):
        for record in self.sudo():
            record.validated = 'accepted'
            record.validated_date = datetime.now()
            record.customer = self.env.user.name
    
    def refused(self, justify, tag_id, file):
        for record in self.sudo():
            record.validated = 'refused'
            record.refused_justify = justify
            record.files = file
            record.validated_date = datetime.now()

            record.tags = [(6, 0, [tag_id])]

            record.customer = self.env.user.name

            blocked_stage = self.env['project.task.type'].search([('blocked_stage', '=', True)])
            record.task_id.stage_id = blocked_stage.id

            record.child_test_created()

            
            record.task_id.message_post(
                body="The test : " + str(record.name) + ", are refused.",
                message_type='notification',
                partner_ids=self.task_id.user_ids.ids,
            )

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

            