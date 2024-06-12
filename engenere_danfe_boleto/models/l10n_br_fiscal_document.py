# Copyright 2024 Engenere.one
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import base64

from odoo import _, models
from odoo.exceptions import UserError


class L10nBrFiscalDocument(models.Model):
    _inherit = "l10n_br_fiscal.document"

    def generate_boleto_pdf(self):
        if self.move_ids.payment_mode_id.cnab_processor != "brcobranca":
            return super().generate_boleto_pdf()

        file_pdf = self.move_ids.file_boleto_pdf_id
        self.file_boleto_pdf_id = False
        file_pdf.unlink()

        receivable_ids = self.mapped("financial_move_line_ids")

        boletos = receivable_ids.send_payment()
        if not boletos:
            raise UserError(
                _(
                    "It is not possible generated boletos\n"
                    "Make sure the Invoice are in Confirm state and "
                    "Payment Mode method are CNAB."
                )
            )

        pdf_string = self._get_brcobranca_boleto(boletos)

        inv_number = self.get_invoice_fiscal_number().split("/")[-1].zfill(8)
        file_name = "boleto_nf-" + inv_number + ".pdf"

        self.move_ids.file_boleto_pdf_id = self.env["ir.attachment"].create(
            {
                "name": file_name,
                "store_fname": file_name,
                "res_model": self._name,
                "res_id": self.id,
                "datas": base64.b64encode(pdf_string),
                "mimetype": "application/pdf",
                "type": "binary",
            }
        )

    def _target_new_tab(self, attachment_id):
        if attachment_id:
            return {
                "type": "ir.actions.act_url",
                "url": "/web/content/{id}/{nome}".format(
                    id=attachment_id.id, nome=attachment_id.name
                ),
                "target": "new",
            }

    def view_boleto_pdf(self):
        if not self.move_ids.file_boleto_pdf_id:
            self.generate_boleto_pdf()
        return self._target_new_tab(self.move_ids.file_boleto_pdf_id)
