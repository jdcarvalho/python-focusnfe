import json
from datetime import datetime
from focusnfe.core import BaseNFSeWrapper
from focusnfe.exceptions.nfse import NFSeException
from focusnfe.exceptions.webhook import WebHookException


class Nfse(BaseNFSeWrapper):

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
    REG_COOPERATIVA = '4'
    REG_MEI = '5'
    REG_ME_EPP_SIMPLES = '6'

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
                raise NFSeException(
                    'Argumento {0} não enviado ao prestador'.format(arg),
                    code=NFSeException.EC_INVALID_PRESTADOR,
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
            'tom_end_bairro',
            'tom_end_numero',
            'tom_end_cod_municipio',
        ]
        for arg in mandatory:
            if arg not in kwargs:
                raise NFSeException(
                    'Argumento {0} não enviado ao tomador'.format(arg),
                    code=NFSeException.EC_INVALID_TOMADOR,
                )
        documento = kwargs.pop('tom_documento')
        documento = self.digits_only(documento)
        if len(documento) == 11:
            document_name = 'cpf'
        elif len(documento) == 14:
            document_name = 'cnpj'
        else:
            raise NFSeException(
                'Documento inválidp. Um documento precisa ter 11 ou 14 dígitos',
                code=NFSeException.EC_BAD_REQUEST,
            )

        razao = kwargs.pop('tom_razao')
        email = kwargs.pop('tom_email')

        payload = {
            document_name: documento,
            'razao_social': razao,
            'email': email,
        }

        inscricao_municipal = kwargs.pop('tom_inscricao', '')
        inscricao_municipal = self.digits_only(inscricao_municipal)
        if inscricao_municipal:
            payload.update({
                'inscricao_municipal': inscricao_municipal,
            })

        telefone = kwargs.pop('tom_telefone', '')
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
            'serv_valor_servicos',
            'serv_aliq_iss',
            'serv_valor_iss',
            'serv_item_lista_servico',
        ]
        for arg in mandatory:
            if arg not in kwargs:
                raise NFSeException(
                    'Argumento {0} não enviado no serviço'.format(arg),
                    code=NFSeException.EC_INVALID_SERVICE,
                )

        total_servicos = kwargs.pop('serv_valor_servicos')

        payload = {
            'discriminacao': kwargs.pop('serv_descricao'),
            'valor_servicos': total_servicos,
            'item_lista_servico': kwargs.pop('serv_item_lista_servico'),
            'base_calculo': total_servicos,
            'aliquota': kwargs.pop('serv_aliq_iss'),
            'valor_iss': kwargs.pop('serv_valor_iss'),
        }

        valor_deducoes = kwargs.pop('serv_valor_deducoes', 0)
        if valor_deducoes:
            payload.update({
                'valor_deducoes': valor_deducoes,
            })
        valor_iss_retido = kwargs.pop('serv_iss_retido', 0)
        if valor_iss_retido:
            payload.update({
                'valor_iss_retido': valor_iss_retido,
                'iss_retido': 'true',
            })
        else:
            payload.update({
                'iss_retido': 'false',
            })
        valor_pis = kwargs.pop('serv_valor_pis', 0)
        if valor_pis:
            payload.update({
                'valor_pis': valor_pis,
            })
        valor_cofins = kwargs.pop('serv_valor_cofins', 0)
        if valor_cofins:
            payload.update({
                'valor_cofins': valor_cofins,
            })
        valor_ir = kwargs.pop('serv_valor_ir', 0)
        if valor_ir:
            payload.update({
                'valor_ir': valor_ir,
            })
        valor_csll = kwargs.pop('serv_valor_cssl', 0)
        if valor_csll:
            payload.update({
                'valor_cssl': valor_csll,
            })
        outras_retencoes = kwargs.pop('serv_outras_retencoes', 0)
        if outras_retencoes:
            payload.update({
                'outras_retencoes': outras_retencoes,
            })
        desconto_incondicionado = kwargs.pop('serv_desconto_incondicionado', '')
        if desconto_incondicionado:
            payload.update({
                'desconto_incondicionado': desconto_incondicionado,
            })
        desconto_condicionado = kwargs.pop('serv_desconto_condicionado', '')
        if desconto_condicionado:
            payload.update({
                'desconto_condicionado': desconto_condicionado,
            })
        codigo_cnae = kwargs.pop('serv_codigo_cnae', '')
        if codigo_cnae:
            payload.update({
                'codigo_cnae': codigo_cnae,
            })
        percentual_total_tributos = kwargs.pop(
            'serv_percentual_total_tributos', '')
        if percentual_total_tributos:
            payload.update({
                'percentual_total_tributos': percentual_total_tributos,
            })
        fonte_total_tributos = kwargs.pop('serv_fonte_total_tributos', '')
        if fonte_total_tributos:
            payload.update({
                'fonte_total_tributos': fonte_total_tributos,
            })
        return payload

    def __prepare(self, **kwargs):

        natureza = kwargs.pop('nfse_natureza', '')

        if natureza not in Nfse.ALL_NATURES:
            raise NFSeException(
                'Natureza inválida. Valores aceitáveis são [{0}]'.format(
                    ','.join(Nfse.ALL_NATURES)
                ),
                code=NFSeException.EC_INVALID_NATURE)

        razao_social = kwargs.pop('prest_razao', '')
        if not razao_social:
            raise NFSeException(
                '[{0}]: Razão Social não informada'.format('prest_razao'),
                code=NFSeException.EC_INVALID_RAZAO,
            )

        incentivador_cultural = json.dumps(
            bool(kwargs.pop('prest_cultural', '')))
        optante_simples = json.dumps(
            bool(kwargs.pop('prest_simples', '')))

        regime = kwargs.pop('prest_regime', '')
        if regime not in Nfse.ALL_REGIMES:
            raise NFSeException(
                '{0}: Regime inválido. Valores aceitáveis são [{1}]'.format(
                    regime, ','.join(Nfse.ALL_REGIMES)
                ),
                code=NFSeException.EC_INVALID_REGIME)

        prestador = self._prepare_prestador(**kwargs)
        tomador = self._prepare_tomador(**kwargs)
        servico = self._prepare_servico(**kwargs)

        data_emissao = kwargs.pop('data_emissao', datetime.now())
        str_emissao = data_emissao.isoformat()

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

        tributacao_rps = kwargs.pop('nfse_prest_rps', '')
        if tributacao_rps:
            if tributacao_rps not in Nfse.ALL_RPS:
                raise NFSeException(
                    '{0} RPS inválido. Valores aceitáveis são: [{1}]'.format(
                        tributacao_rps, ','.join(Nfse.ALL_RPS)
                    ), code=NFSeException.EC_BAD_REQUEST)
            else:
                nfse.update({
                    'tributacao_rps': tributacao_rps,
                })

        codigo_obra = kwargs.pop('serv_cod_obra', '')
        if codigo_obra:
            nfse.update({
                'codigo_obra': codigo_obra,
            })

        art = kwargs.pop('serv_art', '')
        if art:
            nfse.update({
                'art': art
            })

        return nfse

    def create_nfse(self, reference, **kwargs):
        payload_dict = self.__prepare(**kwargs)
        payload = json.dumps(payload_dict)
        response = self.do_post_request(self.url(reference=reference), data=payload)
        return response

    def get_nfse(self, reference):
        if not reference:
            raise NFSeException(
                'Referência não informada',
                code=NFSeException.EC_BAD_REQUEST
            )
        response = self.do_get_request(self.url(reference=reference))
        return response

    def cancel_nfse(self, reference, reason):
        if not reference:
            raise NFSeException(
                'Referência não informada',
                code=NFSeException.EC_BAD_REQUEST
            )
        if not reason:
            raise NFSeException(
                'Justificativa não informada',
                NFSeException.EC_BAD_REQUEST,
            )
        response = self.do_delete_request(
            self.url(reference=reference), data=json.dumps({
                'justificativa': reason,
            }))
        return response

    def resent_email(self, reference):
        if not reference:
            raise NFSeException(
                'Referência não informada',
                code=NFSeException.EC_BAD_REQUEST
            )
        response = self.do_post_request(
            self.url(relative='/{0}/email/'.format(reference))
        )
        return response