from odoo.tests.common import TransactionCase
import os

class TestPynfedance(TransactionCase):
    def setUp(self):
        super().setUp()
        self.pynfedance = self.env['odoo.addons.engenere_danfe.pynfedanfe.danfe']
        test_data = os.path.join(os.path.dirname(__file__), 'data')
        xml_file_path = os.path.join(test_data, 'NFe_teste_cce.xml')
        with open(xml_file_path, "r") as f:
            self.cce_xml = f.read()

    def test_generate_cce(self):
        self.pynfedanfe._generate_cce(self.cce_xml)
        # Desenvolver o Teste
