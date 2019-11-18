import json
from datetime import datetime
from focusnfe.api.base import BaseFocusNFEBase, FocusNFEException


class Nfse(BaseFocusNFEBase):

    NAT_MUNICIPIO = '1'
    NAT_FORA_MUNICIPIO = '2'
    NAT_ISENCAO = '3'
    NAT_IMUNE = '4'
    NAT_EXIG_SUSP_JUDICIAL = '5'
    NAT_EXIG_SUSP_ADMIN = '6'

    ALL_NATURES = [
        NAT_MUNICIPIO, NAT_FORA_MUNICIPIO,
        NAT_ISENCAO, NAT_IMUNE, NAT_EXIG_SUSP_JUDICIAL,
        NAT_EXIG_SUSP_ADMIN,
    ]

    REG_MICROEMPRESA = '1'
    REG_ESTIMATIVA = '2'
    REG_SOCIEDADE = '3'
    REG_COOPERATIVA = '5'
    REG_MEI = '6'
    REG_ME_EPP_SIMPLES = '7'

    ALL_REGIMES = [
        REG_MICROEMPRESA,
        REG_ESTIMATIVA,
        REG_SOCIEDADE,
        REG_COOPERATIVA,
        REG_MEI,
        REG_ME_EPP_SIMPLES,
    ]

    RPS_DENTRO_SP = 'T'
    RPS_FORA_SP = 'F'
    RPS_DENTRO_SP_ISENTO = 'A'
    RPS_FORA_SP_ISENTO = 'B'
    RPS_DENTRO_SP_IMUNE = 'M'
    RPS_FORA_SP_IMUNE = 'N'
    RPS_DENTRO_SP_SUSPENSO = 'X'
    RPS_FORA_SP_SUSPENSO = 'V'
    RPS_EXPORTACAO = 'P'

    ALL_RPS = [
        RPS_DENTRO_SP,
        RPS_FORA_SP,
        RPS_DENTRO_SP_ISENTO,
        RPS_FORA_SP_ISENTO,
        RPS_DENTRO_SP_IMUNE,
        RPS_FORA_SP_IMUNE,
        RPS_DENTRO_SP_SUSPENSO,
        RPS_FORA_SP_SUSPENSO,
        RPS_EXPORTACAO,
    ]

    def _prepare_prestador(self, **kwargs):
        mandatory = [
            'prest_cnpj',
            'prest_inscricao',
            'prest_cod_municipio',
        ]
        for arg in mandatory:
            if arg not in kwargs:
                raise FocusNFEException(
                    'Argumento {0} não enviado aos dados do prestador'.format(arg)
                )

        cnpj = kwargs.pop('prest_cnpj')
        cnpj = self.digits_only(cnpj)

        codigo_municipio = kwargs.pop('prest_cod_municipio')
        codigo_municipio = self.digits_only(codigo_municipio)

        inscricao_municipal = kwargs.pop('prest_inscricao')
        inscricao_municipal = self.digits_only(inscricao_municipal)

        payload = {
            'cnpj': cnpj,
            'codigo_municipio': codigo_municipio,
            'inscricao_municipal': inscricao_municipal,
        }

        return payload

    def _prepare_tomador(self, **kwargs):
        mandatory = [
            'tom_documento',
            'tom_razao',
            'tom_email',

            'tom_end_uf',
            'tom_end_cep',
            'tom_end_logradouro',
            'tom_end_tipo',
            'tom_end_numero',
            'tom_end_complemento',
            'tom_end_cod_municipio',
        ]
        for arg in mandatory:
            if arg not in kwargs:
                raise FocusNFEException(
                    'Argumento {0} não enviado aos dados do tomador'.format(arg)
                )
        documento = kwargs.pop('tom_documento')
        documento = self.digits_only(documento)
        if len(documento) == 11:
            document_name = 'cpf'
        elif len(documento) == 14:
            document_name = 'cnpj'
        else:
            raise FocusNFEException('Documento inválidp. Um documento precisa ter 11 ou 14 dígitos')

        razao = kwargs.pop('tom_razao')
        email = kwargs.pop('tom_email')

        payload = {
            document_name: documento,
            'razao_social': razao,
            'email': email,
        }

        inscricao_municipal = kwargs.pop('tom_inscricao')
        inscricao_municipal = self.digits_only(inscricao_municipal)
        if inscricao_municipal:
            payload.update({
                'inscricao_municipal': inscricao_municipal,
            })

        telefone = kwargs.pop('tom_teleone')
        telefone = self.digits_only(telefone)
        if telefone:
            payload.update({
                'telefone': telefone,
            })

        payload.update({
            'endereco': {
                'logradouro': kwargs.pop('tom_end_logradouro'),
                'tipo_logradouro': kwargs.pop('tom_end_tipo'),
                'numero': kwargs.pop('tom_end_numero'),
                'bairro': kwargs.pop('tom_end_bairro'),
                'codigo_municipio': kwargs.pop('tom_end_cod_municipio'),
                'uf': kwargs.pop('tom_end_uf'),
                'cep': self.digits_only(kwargs.pop('tom_end_cep', '')),
            }
        })

        return payload

    def _prepare_servico(self, **kwargs):
        mandatory = [
            'serv_descricao',
            'serv_base_calculo',
            'serv_aliq_iss',
            'serv_valor_iss',
            'serv_iss_retido',
            'serv_item_lista_servico',
            'serv_cnae',
            'serv_vlr_liquido',
            'serv_vlr_bruto',
        ]
        for arg in mandatory:
            if arg not in kwargs:
                raise FocusNFEException(
                    'Argumento {0} não enviado aos dados do serviço'.format(arg)
                )
        return dict()

    def __prepare(self, **kwargs):

        natureza = kwargs.pop('nfse_natureza', '')

        if natureza not in Nfse.ALL_NATURES:
            raise FocusNFEException(
                'Natureza da Operação {0} inválida. Valores aceitáveis são [{1}]'.format(
                    natureza, ','.join(Nfse.ALL_NATURES)
                ))

        razao_social = kwargs.pop('prest_razao', '')
        if not razao_social:
            raise FocusNFEException('[{0}]: Razão Social não informada'.format('prest_razao'))

        incentivador_cultural = json.dumps(bool(kwargs.pop('prest_cultural', '')))
        optante_simples = json.dumps(bool(kwargs.pop('prest_simples', '')))

        regime = kwargs.pop('prest_regime', '')
        if regime not in Nfse.ALL_REGIMES:
            raise FocusNFEException(
                '{0}: Não é um regime de tributação válido. Valores aceitáveis são [{1}]'.format(
                    regime, ','.join(Nfse.ALL_REGIMES)
                ))

        prestador = self._prepare_prestador(**kwargs)
        servico = self._prepare_servico(**kwargs)
        tomador = self._prepare_tomador(**kwargs)

        str_emissao = datetime.now().isoformat()

        nfse = {
            'data_emissao': str_emissao,
            'natureza_operacao': natureza,
            'razao_social': razao_social,
            'regime_especial_tributacao': regime,
            'incentivador_cultural': incentivador_cultural,
            'optante_simples_nacional': optante_simples,

            'prestador': prestador,
            'tomador': tomador,
            'servico': servico,
        }

        tributacao_rps = kwargs.pop('prest_rps')
        if tributacao_rps:
            if tributacao_rps not in Nfse.ALL_RPS:
                raise FocusNFEException(
                    '{0} não é um código RPS válido. Valores aceitáveis são: [{1}]'.format(
                        tributacao_rps, ','.join(Nfse.ALL_RPS)
                    ))
            else:
                nfse.update({
                    'tributacao_rps': tributacao_rps,
                })

        codigo_obra = kwargs.pop('serv_cod_obra')
        if codigo_obra:
            nfse.update({
                'codigo_obra': codigo_obra,
            })

        art = kwargs.pop('serv_art')
        if art:
            nfse.update({
                'art': art
            })

        return nfse

    def create_nfse(self, **kwargs):
        payload_dict = self.__prepare(**kwargs)
        payload = json.dumps(payload_dict)
        response = self.do_post_request(self.url(), data=payload)
        return response

    def get_nfse(self, reference):
        response = self.do_get_request(self.url(reference=reference))
        return response

    def cancel_nfse(self):
        pass

    def resent_email(self):
        pass