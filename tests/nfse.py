from unittest import TestCase
import os
from focusnfe.api.nfse import Nfse
from focusnfe.focusnfe import FocusNFE
import uuid


class NFSeTestCase(TestCase):

    def setUp(self):
        FocusNFE.load_testing_env_variables()
        api_token = os.environ.get('API_TOKEN')
        self.focus = FocusNFE(api_token, os.environ.get('ENVIRONMENT'))

    def test_create_nfse_invalid_nature(self):
        from focusnfe.exceptions.nfse import NFSeException
        try:
            self.focus.nfse.create_nfse(
                reference=uuid.uuid4().hex,
                nfse_natureza='Votem',
            )
        except NFSeException as e:
            self.assertTrue(e.code == NFSeException.EC_INVALID_NATURE)

    def test_create_nfse_without_razao(self):
        from focusnfe.exceptions.nfse import NFSeException
        try:
            self.focus.nfse.create_nfse(
                reference=uuid.uuid4().hex,
                nfse_natureza=Nfse.NAT_MUNICIPIO,
                prest_razao='',
            )
        except NFSeException as e:
            self.assertTrue(e.code == NFSeException.EC_INVALID_RAZAO)

    def test_create_nfse_with_invalid_regime(self):
        from focusnfe.exceptions.nfse import NFSeException
        try:
            self.focus.nfse.create_nfse(
                reference=uuid.uuid4().hex,
                nfse_natureza=Nfse.NAT_MUNICIPIO,
                prest_razao=os.environ.get('PRESTADOR_RAZAO'),
                prest_cnpj=os.environ.get('PRESTADOR_CNPJ'),
                prest_cultural=False,
                prest_simples=True,
                prest_regime='Antigo Regime',
            )
        except NFSeException as e:
            self.assertTrue(e.code == NFSeException.EC_INVALID_REGIME)

    def test_create_nfse_with_prestador_invalid(self):
        from focusnfe.exceptions.nfse import NFSeException
        try:
            self.focus.nfse.create_nfse(
                reference=uuid.uuid4().hex,
                nfse_natureza=Nfse.NAT_MUNICIPIO,
                prest_razao=os.environ.get('PRESTADOR_RAZAO'),
                prest_regime=Nfse.REG_ME_EPP_SIMPLES,
                prest_cnpj='',
            )
        except NFSeException as e:
            self.assertTrue(e.code == NFSeException.EC_INVALID_PRESTADOR)

    def test_create_nfse_with_tomador_invalid(self):
        from focusnfe.exceptions.nfse import NFSeException
        try:
            self.focus.nfse.create_nfse(
                reference=uuid.uuid4().hex,
                nfse_natureza=Nfse.NAT_MUNICIPIO,
                prest_razao=os.environ.get('PRESTADOR_RAZAO'),
                prest_cnpj=os.environ.get('PRESTADOR_CNPJ'),
                prest_cultural=bool(os.environ.get('PRESTADOR_CULTURAL')),
                prest_simples=bool(os.environ.get('PRESTADOR_SIMPLES')),
                prest_regime=Nfse.REG_ME_EPP_SIMPLES,
                prest_cod_municipio=os.environ.get('PRESTADOR_COD_IBGE'),
                prest_inscricao=os.environ.get('PRESTADOR_INSCRICAO'),
            )
        except NFSeException as e:
            self.assertTrue(e.code == NFSeException.EC_INVALID_TOMADOR)

    def test_create_nfse_with_service_invalid(self):
        from focusnfe.exceptions.nfse import NFSeException
        try:
            self.focus.nfse.create_nfse(
                reference=uuid.uuid4().hex,
                nfse_natureza=Nfse.NAT_MUNICIPIO,

                prest_razao=os.environ.get('PRESTADOR_RAZAO'),
                prest_cnpj=os.environ.get('PRESTADOR_CNPJ'),
                prest_cultural=bool(os.environ.get('PRESTADOR_CULTURAL')),
                prest_simples=bool(os.environ.get('PRESTADOR_SIMPLES')),
                prest_regime=Nfse.REG_ME_EPP_SIMPLES,
                prest_cod_municipio=os.environ.get('PRESTADOR_COD_IBGE'),
                prest_inscricao=os.environ.get('PRESTADOR_INSCRICAO'),

                tom_documento=os.environ.get('TOMADOR_DOCUMENTO'),
                tom_razao=os.environ.get('TOMADOR_NOME'),
                tom_email=os.environ.get('TOMADOR_EMAIL'),
                tom_telefone=os.environ.get('TOMADOR_TELEFONE'),
                tom_end_logradouro=os.environ.get('TOMADOR_LOGRADOURO'),
                tom_end_tipo='Rua',
                tom_end_bairro=os.environ.get('TOMADOR_BAIRRO'),
                tom_end_cod_municipio=os.environ.get('TOMADOR_COD_IBGE'),
                tom_end_numero=os.environ.get('TOMADOR_NUMBERO'),
                tom_end_uf=os.environ.get('TOMADOR_UF'),
                tom_end_cep=os.environ.get('TOMADOR_CEP'),

            )
        except NFSeException as e:
            self.assertTrue(e.code == NFSeException.EC_INVALID_SERVICE)

    def test_create_nfse_dentro_municipio(self):
        r = self.focus.nfse.create_nfse(
            reference=uuid.uuid4().hex,
            nfse_natureza=Nfse.NAT_FORA_MUNICIPIO,

            prest_razao=os.environ.get('PRESTADOR_RAZAO'),
            prest_cnpj=os.environ.get('PRESTADOR_CNPJ'),
            prest_cultural=bool(os.environ.get('PRESTADOR_CULTURAL')),
            prest_simples=bool(os.environ.get('PRESTADOR_SIMPLES')),
            prest_regime=Nfse.REG_ME_EPP_SIMPLES,
            prest_cod_municipio=os.environ.get('PRESTADOR_COD_IBGE'),
            prest_inscricao=os.environ.get('PRESTADOR_INSCRICAO'),

            tom_documento=os.environ.get('TOMADOR_DOCUMENTO'),
            tom_razao=os.environ.get('TOMADOR_NOME'),
            tom_email=os.environ.get('TOMADOR_EMAIL'),
            tom_telefone=os.environ.get('TOMADOR_TELEFONE'),
            tom_end_logradouro=os.environ.get('TOMADOR_LOGRADOURO'),
            tom_end_tipo='Rua',
            tom_end_bairro=os.environ.get('TOMADOR_BAIRRO'),
            tom_end_cod_municipio=os.environ.get('TOMADOR_COD_IBGE'),
            tom_end_numero=os.environ.get('TOMADOR_NUMERO'),
            tom_end_uf=os.environ.get('TOMADOR_UF'),
            tom_end_cep=os.environ.get('TOMADOR_CEP'),

            serv_descricao='Serviços especiais',
            serv_valor_servicos=10,
            serv_aliq_iss=2,
            serv_valor_iss=0.2,
            serv_item_lista_servico='0107',

        )
        self.assertTrue(r.status_code in [200, 201])

    def test_get_nfse_invalid(self):
        r = self.focus.nfse.get_nfse('3f27a44966f9499f899eaec1577b4d4b')
        self.assertTrue(r.status_code in [200, 201])

    def test_cancel_nfse_valid(self):
        r = self.focus.nfse.cancel_nfse('3f27a44966f9499f899eaec1577b4d4b', 'Era um teste')
        self.assertTrue(r.status_code in [200, 201])
