# Python FocusNFE Binding

Este projeto tem como objetivo fazer a ligação entre o sistema de emissão de notas fiscais da [FocusNFE](https://focusnfe.com.br/) para a 
linguagem python. Inicialmente irá compor somente os métodos de trabalho para notas fiscais de serviço, posteriormente 
poderá englobar as demais funcionalidades. (Com ajuda dos interessados)

Para instalar a versão atual do Pypy utilize:

~~pip install python-focusnfe~~

*Ainda em desenvolvimento. Não liberado no Pypy*

# Dependências

* [python-requests](https://requests.readthedocs.io/pt_BR/latest/user/quickstart.html)

# Como contribuir?

Para contribuir com o código é bem simples, basta montar o ambiente, aplicar a sua feature ou bugfix e mandar _pull request_

É necessário ter uma estrutura como esta:

    |Raiz
    |_ _ env.focus
    |_ _ src

Para criá-la você deve seguir os passos abaixo:

1) Criar um ambiente virtual com python-virtualenv fora do diretório de código
    
        virtualenv -p python3 env.focus

2) Ativar o ambiente 
        
        source ./env.focus/bin/activate
    
3) Clonar o repositório no subdiretório src dentro da raiz.

        mkdir src
        cd src
        git clone https://github.com/jdcarvalho/python-focusnfe.git
        
4) Instalar as dependências de software:

        cd python-focusnfe
        pip install -r requirements.txt
        
5) Criar o arquivo de variáveis de ambiente conforme o modelo

        cd foccusnfe/api/
        cp environment.sample.py environment.py
        
6) Preencha as variáveis a fim de validar os testes unitários, sendo a principal delas o **API_TOKEN** do ambiente FocusNFe

        
        environment = (
            ('API_TOKEN', 'MEU TOKEN DE HOMOLOGACAO'),
        )





