from odoo import models

# Odoo 18 removed the legacy template-tax model. The custom tax fields are defined
# directly on account.tax in account_tax.py, so this compatibility file is kept as a
# no-op to avoid loading obsolete template-model data.
class AccountTaxTemplate(models.AbstractModel):
    _description = 'Legacy compatibility stub for removed template tax model'
    _inherit = 'account.tax'
