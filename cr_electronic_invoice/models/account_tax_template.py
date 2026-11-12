from odoo import models

# Odoo 18 removed the legacy account.tax.template model. The custom tax fields are
# defined directly on account.tax in account_tax.py, so this compatibility file is
# intentionally kept as a no-op to avoid loading obsolete template-model data.
class AccountTaxTemplate(models.AbstractModel):
    _description = 'Legacy compatibility stub for removed account.tax.template'
    _inherit = 'account.tax'
