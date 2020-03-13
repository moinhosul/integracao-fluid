Instale um ambiente virutal Python com o comando:
> virtualenv venv

Inicie o ambiente virutal com:
> source venv/bin/activate

Rode as dependências com:
> pip install -r requirements.txt

Exporte as variáveis de ambiente para o Flask com:
> export FLASK_APP=client.py
> export FLASK_ENV=development

Para gerar a base de dados entre com os comandos:

> flask db init
> flask db migrate -m "Migration"
> flask db upgrade

Modifique no arquivo client.py a variável BASE_URL para a url da sua Cooperativa.
Por exemplo, se você acessa o Fluid pelo link https://suacooperativa.websicredi.com.br modifique dessa forma:

BASE_URL = 'https://suacooperativa.websicredi.com.br'

Por fim, rode a aplicação Flask com:
> flask run --cert=adhoc

No seu navegador acesse:

https://localhost:5000
Nessa tela é possível inserir o client id e solicitar os escopos para esse cliente.
Ao clicar em autenticar você será direcionado para o seu ambiente de produção (você já deve estar logado) para autorizar os escopos solicitados.

https://localhost:5000/procurar
Você pode buscar através dos identificadores dos clientes suas informações.

Esse código é só um exemplo de como funciona um Client Provider para o Oauth2.0
Você pode implementar em qualquer linguagem e de qualquer maneira desde que cada rota tenha suas necessidades atendidas.

Você pode ver mais sobre o Oauth2.0 nos links:


