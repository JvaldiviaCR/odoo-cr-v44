import os

from lxml import etree

from odoo.tests.common import TransactionCase


class HaciendaV44SchemaTest(TransactionCase):

    def test_official_v44_schemas_load(self):
        data_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            'data',
            'xsd-4.4',
        )
        schema_names = (
            'FacturaElectronica_V4.4.xsd',
            'FacturaElectronicaExportacion_V4.4.xsd',
            'FacturaElectronicaCompra_V4.4.xsd',
            'NotaCreditoElectronica_V4.4.xsd',
            'NotaDebitoElectronica_V4.4.xsd',
            'TiqueteElectronico_V4.4.xsd',
            'ReciboElectronicoPago_V4.4.xsd',
            'MensajeHacienda_V4.4.xsd',
            'MensajeReceptor_V4.4.xsd',
        )

        for schema_name in schema_names:
            schema_path = os.path.join(data_dir, schema_name)
            self.assertTrue(os.path.isfile(schema_path), schema_name)
            etree.XMLSchema(etree.parse(schema_path))
