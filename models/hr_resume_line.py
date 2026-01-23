# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from dateutil.relativedelta import relativedelta
from datetime import date

class ResumeLine(models.Model):
    _inherit = 'hr.resume.line'

    experience_duration = fields.Char(string='Duration (Cal.)', compute='_compute_experience_duration')
    experience_months = fields.Integer(string='Duration Months', compute='_compute_experience_duration', store=True)

    @api.depends('date_start', 'date_end', 'line_type_id')
    def _compute_experience_duration(self):
        experience_type = self.env.ref('hr_skills.resume_type_experience', raise_if_not_found=False)
        
        for line in self:
            start = line.date_start
            end = line.date_end or date.today()
            
            if start and end:
                delta = relativedelta(end, start)
                years = delta.years
                months = delta.months
                

                if experience_type and line.line_type_id == experience_type:
                    line.experience_months = (years * 12) + months
                else:
                    line.experience_months = 0
                
                parts = []
                if years > 0:
                    parts.append(_("%s Years") % years if years > 1 else _("%s Year") % years)
                if months > 0:
                    parts.append(_("%s Months") % months if months > 1 else _("%s Month") % months)
                
                if not parts:
                    line.experience_duration = _("0 Months")
                else:
                    line.experience_duration = " ".join(parts)
            else:
                line.experience_duration = False
                line.experience_months = 0
