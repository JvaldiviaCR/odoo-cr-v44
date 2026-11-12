from odoo import models
from odoo.tools.misc import get_lang


class AccountInvoiceSend(models.AbstractModel):
    _inherit = 'account.move.send'

    # -------------------------------------------------------------------------
    # PUBLIC ACTIONS
    # -------------------------------------------------------------------------

    def _get_send_moves(self):
        moves = getattr(self, 'move_ids', False) or getattr(self, 'invoice_ids', False)
        if moves:
            return moves
        active_ids = self.env.context.get('active_ids') or self.env.context.get('active_id')
        if active_ids:
            if isinstance(active_ids, (list, tuple)):
                return self.env['account.move'].browse(active_ids)
            return self.env['account.move'].browse([active_ids])
        return self.env['account.move']

    def _prepare_signed_attachments(self, move):
        attachments = []
        if not hasattr(move, 'xml_comprobante'):
            return attachments
        domain = [
            ('res_model', '=', move._name),
            ('res_id', '=', move.id),
            ('res_field', '=', 'xml_comprobante'),
        ]
        attachment = self.env['ir.attachment'].sudo().search(domain, limit=1)
        if attachment:
            attachments.append(attachment)
            domain_resp = [
                ('res_model', '=', move._name),
                ('res_id', '=', move.id),
                ('res_field', '=', 'xml_respuesta_tributacion'),
            ]
            attachment_resp = self.env['ir.attachment'].sudo().search(domain_resp, limit=1)
            if attachment_resp:
                attachments.append(attachment_resp)
        return attachments

    def send_and_print_action(self):
        self.ensure_one()
        moves = self._get_send_moves()

        if hasattr(self, 'attachment_ids'):
            self.attachment_ids = [(5, 0, 0)]

        for move in moves:
            for attachment in self._prepare_signed_attachments(move):
                if hasattr(self, 'attachment_ids'):
                    self.attachment_ids = [(4, attachment.id, 0)]

        if getattr(self, 'composition_mode', False) == 'mass_mail' and getattr(self, 'template_id', False):
            for move in moves:
                if move.company_id.frm_ws_ambiente == 'disabled':
                    active_records = self.env[self.model].browse(move.ids)
                    langs = active_records.mapped('partner_id.lang')
                    default_lang = get_lang(self.env)
                    for lang in (set(langs) or [default_lang]):
                        active_ids_lang = active_records.filtered(lambda r: r.partner_id.lang == lang).ids
                        self_lang = self.with_context(active_ids=active_ids_lang, lang=lang)
                        self_lang.onchange_template_id()
                        if hasattr(self_lang, '_send_email'):
                            self_lang._send_email()
                else:
                    if hasattr(move, 'state_tributacion') and move.state_tributacion == 'aceptado':
                        if hasattr(move, 'action_invoice_sent_mass'):
                            move.action_invoice_sent_mass()
        elif hasattr(self, '_send_email'):
            self._send_email()

        if getattr(self, 'is_print', False):
            if hasattr(self, '_print_document'):
                return self._print_document()
        return {
            'type': 'ir.actions.act_window_close'
        }
