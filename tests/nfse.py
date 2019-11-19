from unittest import TestCase
import os
from focusnfe.focusnfe import FocusNFE
from focusnfe.api.nfse import Nfse
import uuid


class NFSeTestCase(TestCase):

    def setUp(self):
        FocusNFE.load_testing_env_variables()
        api_token = os.environ.get('API_TOKEN')
        self.focus = FocusNFE(api_token, FocusNFE.ENV_DEVELOPMENT)

    def test_create_nfse_dentro_municipio(self):
        r = self.focus.nfse.create_nfse(
            reference=uuid.uuid4().hex,
            nfse_natureza=Nfse.NAT_MUNICIPIO,

            prest_razao=os.environ.get('PRESTADOR_RAZAO'),
            prest_cnpj=os.environ.get('PRESTADOR_CNPJ'),
            prest_cultural=False,
            prest_simples=True,
            prest_regime=Nfse.REG_ME_EPP_SIMPLES,
            prest_cod_municipio='5002704',
            prest_inscricao=os.environ.get('PRESTADOR_INSCRICAO'),

            tom_documento=os.environ.get('TOMADOR_DOCUMENTO'),
            tom_razao='Fulaninho da Silva Sauro',
            tom_email='vote@cobra.com',
            tom_telefone='(66)8837-3399',
            tom_end_logradouro='Pedro Pereira',
            tom_end_tipo='Rua',
            tom_end_bairro='Urubu Pelado',
            tom_end_cod_municipio='5002704',
            tom_end_numero='3344',
            tom_end_uf='MS',
            tom_end_cep='79002-010',

            serv_descricao='Desentupimento de Orelha',
            serv_valor_servicos=200.89,
            serv_aliq_iss=3.5,
            serv_valor_iss=7.03,
            serv_item_lista_servico='0104',

        )
        self.assertTrue(r.status_code in [200, 201])
