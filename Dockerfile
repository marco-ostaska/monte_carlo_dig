# Use a imagem oficial do Python como imagem base
FROM python:latest

# Instale build-essential e atualize o gcc, depois limpe o cache
RUN apt-get update && apt-get install -y build-essential \
    && apt-get upgrade -y gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Atualize o pip
RUN pip install --upgrade pip

RUN mkdir /application && mkdir -p /tmp/mcd

# Copie o arquivo requirements.txt para o contêiner
COPY requirements.txt /requirements.txt
COPY monte_carlo_dig.py /application/monte_carlo_dig.py
COPY bancoCentral.py /application/bancoCentral.py 


# Instale as dependências do Python e limpe o cache do pip
RUN pip install -r /requirements.txt \
    && rm -rf /root/.cache/pip

# Defina o diretório de trabalho
WORKDIR /application


# Montar o volume

# O comando para iniciar a aplicação (ajuste conforme necessário)
CMD ["python", "monte_carlo_dig.py"]
