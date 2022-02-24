# ================================== BUILDER ===================================
ARG INSTALL_PYTHON_VERSION=${INSTALL_PYTHON_VERSION:-3.7}

FROM condaforge/mambaforge AS base

RUN apt-get update
RUN apt-get install -y \
    gcc \
    wget


RUN mamba install -c ome omero-py
ARG INSTALL_NODE_VERSION=${INSTALL_NODE_VERSION:-12}
RUN mamba install nodejs=${INSTALL_NODE_VERSION}

WORKDIR /app
COPY requirements requirements
RUN pip install --no-cache -r requirements/prod.txt

COPY package.json ./
RUN npm install

COPY webpack.config.js autoapp.py ./
COPY metrologist metrologist
COPY assets assets
COPY .env .env
RUN npm run-script build

# ================================= PRODUCTION =================================
FROM base as production

WORKDIR /app

RUN useradd -m sid
RUN chown -R sid:sid /app
USER sid
ENV PATH="/home/sid/.local/bin:${PATH}"

COPY requirements requirements
RUN pip install --no-cache --user -r requirements/prod.txt

COPY supervisord.conf /etc/supervisor/supervisord.conf
COPY supervisord_programs /etc/supervisor/conf.d

COPY . .

EXPOSE 5000
ENTRYPOINT ["/bin/bash", "shell_scripts/supervisord_entrypoint.sh"]
CMD ["-c", "/etc/supervisor/supervisord.conf"]


# ================================= DEVELOPMENT ================================
FROM base AS development
RUN pip install --no-cache -r requirements/dev.txt
EXPOSE 2992
EXPOSE 5000
CMD [ "npm", "start" ]

# =================================== MANAGE ===================================
FROM base AS manage
RUN pip install --user -r requirements/dev.txt
ENTRYPOINT [ "flask" ]
