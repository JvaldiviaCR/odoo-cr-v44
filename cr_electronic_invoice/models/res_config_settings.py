
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    expense_product_id = fields.Many2one(
        comodel_name='product.product',
        company_dependent=True,
        string="Default product for expenses when loading data from XML",
        help="The default product used when loading Costa Rican digital invoice"
    )

    expense_account_id = fields.Many2one(
        comodel_name='account.account',
        company_dependent=True,
        string="Default Expense Account when loading data from XML",
        help="The expense account used when loading Costa Rican digital invoice"
    )

    expense_analytic_account_id = fields.Many2one(
        comodel_name='account.analytic.account',
        company_dependent=True,
        string="Default Analytic Account for expenses when loading data from XML",
        help="The analytic account used when loading Costa Rican digital invoice"
    )

    load_lines = fields.Boolean(
        string='Indicates if invoice lines should be load when loading a Costa Rican Digital Invoice',
        default=True
    )

    def get_values(self):
        res = super().get_values()
        get_param = self.env['ir.config_parameter'].sudo().get_param
        expense_account_id = get_param('expense_account_id')
        expense_product_id = get_param('expense_product_id')
        expense_analytic_account_id = get_param('expense_analytic_account_id')
        res.update(
            expense_account_id=int(expense_account_id) if expense_account_id and str(expense_account_id).isdigit() and int(expense_account_id) > 0 else False,
            load_lines=bool(get_param('load_lines', True)),
            expense_product_id=int(expense_product_id) if expense_product_id and str(expense_product_id).isdigit() and int(expense_product_id) > 0 else False,
            expense_analytic_account_id=int(expense_analytic_account_id) if expense_analytic_account_id and str(expense_analytic_account_id).isdigit() and int(expense_analytic_account_id) > 0 else False,
        )
        return res

    def set_values(self):
        super().set_values()
        set_param = self.env['ir.config_parameter'].sudo().set_param
        set_param('expense_account_id', self.expense_account_id.id)
        set_param('load_lines', self.load_lines)
        set_param('expense_product_id', self.expense_product_id.id)
        set_param('expense_analytic_account_id', self.expense_analytic_account_id.id)
