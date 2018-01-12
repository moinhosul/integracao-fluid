## Exemplos em Java

### Instalação

1. Install [Docker](https://www.docker.com/).

### Uso

    docker run -it --rm java java -version

#### Rodar `java`

    docker run -it --rm java java

#### Rodar `javac`

    docker run -it --rm java javac

#### Compilar um código

    docker run --rm -v $PWD/src:/src -w /src java javac TestSOAPClient.java

#### Executar um código compilado

    docker run --rm -v $PWD/src:/src -w /src java java TestSOAPClient $PROCESSO $CHAVE
