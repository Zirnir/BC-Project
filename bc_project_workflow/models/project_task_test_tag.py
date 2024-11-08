from odoo import fields, models

class TestTag(models.Model):
    _name = "test.tag"
    _description = "Tag of test"

    name = fields.Char(required=True)