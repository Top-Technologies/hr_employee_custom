# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
from datetime import date

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    age = fields.Integer(string='Age', compute='_compute_age', store=True, groups="hr.group_hr_user")
        joining_date = fields.Date(
        string='Joining Date',
        compute='_compute_joining_date',
        store=True,
        readonly=True,
        groups="hr.group_hr_user",
        tracking=True,
        help="Date the employee joined the company. Defaults to the first contract date.")
    experience_summary = fields.Char(string='Total Experience', compute='_compute_experience_summary', store=True, groups="hr.group_hr_user")

   @api.depends('contract_ids.date_start')
    def _compute_joining_date(self):
        for employee in self:
            contracts = employee.contract_ids.filtered(lambda c: c.date_start)
            employee.joining_date = (
                min(contracts.mapped('date_start')) if contracts else False
            )

    @api.depends('birthday')
    def _compute_age(self):
        today = date.today()
        for employee in self:
            if employee.birthday:
                delta = relativedelta(today, employee.birthday)
                employee.age = delta.years
            else:
                employee.age = 0

    @api.depends('joining_date', 'resume_line_ids.experience_months')
    def _compute_experience_summary(self):
        today = date.today()
        for employee in self:
            total_months = 0


            if employee.joining_date:
                delta = relativedelta(today, employee.joining_date)
                total_months += (delta.years * 12) + delta.months
                

            total_months += sum(employee.resume_line_ids.mapped('experience_months'))
            
            if total_months > 0:
                years = total_months // 12
                months = total_months % 12
                
                parts = []
                if years > 0:
                    parts.append(_("%s Years") % years if years > 1 else _("%s Year") % years)
                if months > 0:
                    parts.append(_("%s Months") % months if months > 1 else _("%s Month") % months)
                
                if not parts:
                    employee.experience_summary = _("0 Months")
                else:
                    employee.experience_summary = " ".join(parts)
            else:
                employee.experience_summary = False

    @api.constrains('birthday')
    def _check_age(self):
        for employee in self:
            if employee.birthday and employee.age < 18:
                raise ValidationError(_("Hey, you cannot enter an age less than 18! An employee must be at least 18 years old."))

