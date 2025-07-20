# Use uma imagem base oficial do Python
FROM python:3.9-slim-buster

# Defina variáveis de ambiente para a sua aplicação Django
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Crie e defina o diretório de trabalho dentro do container
WORKDIR /app

# Copie o arquivo requirements.txt para o diretório de trabalho
# e instale as dependências. Fazer isso em uma etapa separada
# aproveita o cache do Docker, acelerando builds futuros se as dependências não mudarem.
COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

# Copie o restante do código da sua aplicação para o diretório de trabalho
# Lembre-se que a sua pasta raiz do projeto (onde está o manage.py)
# deve ser copiada para /app.
# Pela sua imagem anterior, a pasta raiz é SIPED.
# Então, assumindo que este Dockerfile esteja dentro da pasta SIPED
# ou que o contexto do build seja a pasta SIPED, o COPY . . funcionará.
COPY . /app/

# Opcional: Coletar arquivos estáticos
# (Isso é crucial para deploy em produção, mas pode ser pulado para testes locais iniciais)
# RUN python manage.py collectstatic --noinput

# Exponha a porta em que a aplicação Django será executada
# A porta padrão para o Gunicorn (servidor de produção comum) é 8000
EXPOSE 8000

# Comando para iniciar a aplicação Django usando Gunicorn (recomendado para produção)
# Substitua 'seu_projeto.wsgi:application' pelo caminho real para o seu arquivo wsgi.py.
# Exemplo: se seu manage.py e o diretório da aplicação principal (com settings.py e wsgi.py)
# estão dentro de SIPED, e o wsgi.py está em 'SIPED/SIPED/wsgi.py',
# então o caminho pode ser 'SIPED.wsgi:application'.
# Se o seu diretório da aplicação principal é 'core', e o wsgi.py está em 'SIPED/core/wsgi.py',
# então o caminho pode ser 'core.wsgi:application'.
# Consulte a documentação do Django para o nome correto do módulo WSGI.

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "SIPED.wsgi:application"]

# Se você preferir usar o servidor de desenvolvimento do Django (apenas para DEV/testes, não produção):
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]