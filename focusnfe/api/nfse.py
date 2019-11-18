from focusnfe.api.base import BaseFocusNFEBase


class Nfse(BaseFocusNFEBase):

    NAT_MUNICIPIO = 1
    NAT_FORA_MUNICIPIO = 2
    NAT_ISENCAO = 3
    NAT_IMUNE = 4
    NAT_EXIG_SUSP_JUDICIAL = 5
    NAT_EXIG_SUSP_ADMIN = 6

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

    def create_nfse(
            self, razao_social, natureza, optante_simples, incentivador_cultural=False, data_emissao=None
    ):
        pass

    def get_nfse(self):
        pass

    def cancel_nfse(self):
        pass

    def resent_email(self):
        pass
