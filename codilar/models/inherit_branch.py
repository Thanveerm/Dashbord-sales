from odoo import api, models, fields


class InheritCustomBranch(models.Model):
    _inherit = 'res.branch'

    gst_num = fields.Char(string='GSTIN')
    pan_num = fields.Char(string='PAN NO')
    cin_num = fields.Char(string='CIN NO')
