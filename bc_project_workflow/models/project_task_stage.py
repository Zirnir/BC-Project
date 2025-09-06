from odoo import models, fields
from odoo.exceptions import UserError

class TaskStage(models.Model): #Définition du nom du model.
    _inherit = "project.task.type" #Héritage: ici le model Task hérite de caractérique 
                                   #du model project.task pour le modifier.

    in_progress_stage = fields.Boolean() #Ajout de l'attribut in_progress_stage
    testing_stage = fields.Boolean()
    blocked_stage = fields.Boolean()