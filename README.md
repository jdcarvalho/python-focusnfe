# Python FocusNFE Binding

Este projeto tem como objetivo fazer a ligação entre o sistema de emissão de notas fiscais da FocusNFE para a 
linguagem python. Inicialmente irá compor somente os métodos de trabalho para notas fiscais de serviço, posteriormente 
poderá englobar as demais funcionalidades.

Para instalar a versão atual do Pypi utilize:

`pip install python-focusnfe`

# Dependências

Python Requests
URL Lib

# Ambiente de Desenvolvimento

Para contribuir com o código é bem simples, basta montar o ambiente, aplicar a feature ou bugfix e mandar _pull request_


1) Criar um ambiente virtual com python-virtualenv fora do diretório de código
    
        virtualenv -p python3 env.focus
2) Ativar o ambiente 
        
        source ./env.focus/bin/activate
    
3) Clonar o repositório no subdiretório src dentro da raiz.

        git clone https://github.com/jdcarvalho/python-focusnfe.git
        
4) Instalar as dependências de software:

        pip install -r src/python-focus-nfe/requirements.txt


No final você deve ter uma estrutura parecida com esta:

    |Raiz
    |_ _ env.focus
    |_ _ src


