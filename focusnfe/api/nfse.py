import json

from focusnfe.api.base import BaseFocusNFEBase


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

    REG_MICROEMPRESA = 1
    REG_ESTIMATIVA = 2
    REG_SOCIEDADE = 3
    REG_COOPERATIVA = 5
    REG_MEI = 6
    REG_ME_EPP_SIMPLES = 7

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

    def __prepare(self, **kwargs):
        """
        prest_razao,
        prest_cpnj,
        pres_i_municipal,
        prest_cod_municipio,
        natureza_operacao,
        prest_optante_simples,
        serv_b_calculo,
        serv_descricao,
        serv_iss_retido,
        serv_item_lista_servico,
        serv_codigo_cnae,
        serv_cod_municipio,
        serv_aliq_iss,
        serv_valor_iss,
        serv_vlr_liquido,
        serv_vlr_bruto,
        tom_documento,
        tom_razao,
        tom_i_municipal,
        tom_telefone,
        tom_email,
        tom_end_logradouro,
        tom_end_tipo,
        tom_end_numero,
        tom_end_complemento,
        tom_end_bairro,
        tom_end_cod_municipio,
        tom_end_uf,
        tom_end_cep,
        prest_incentivador_cultural=False,
        nfse_data_emissao=None,
        """
        payload = dict()
        return payload

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
