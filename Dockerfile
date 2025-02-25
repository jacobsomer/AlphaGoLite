# The build-stage image, utilizing miniconda to set up 
# the virtual environment. 
FROM continuumio/miniconda3 AS build
# WORKDIR /app


# create conda env & install dependencies
# bring in the needed dependency files
COPY env_setup/environment.yml .

RUN conda env create -f environment.yml

SHELL ["/bin/bash", "-c" ]

RUN conda install -c conda-forge conda-pack
# standalone env in /venv (aranlp-env)
RUN conda-pack -n  alphagolite -o /tmp/env.tar && \
    mkdir /venv && \
    cd /venv && tar xf /tmp/env.tar && \
    rm /tmp/env.tar \
    /venv/bin/conda-unpack


FROM debian:buster


COPY --from=build /venv /venv 
# copy local main.py (in this directory) and move copy to the container's app folder 
COPY test_tf.py alphagolite/test_tf.py
# needed to pip install additional requirements
# The reason I did not do pip installations inside the conda environment is that there would be versioning 
# incompatabilities. Somehow though, no version incompatibilities occur when I pip install from requirements.txt 
# after conda packing and unpacking. 
COPY env_setup alpahgolite/env_setup
COPY algorithms alphagolite/algorithms
COPY play_go_web_app alphagolite/play_go_web_app

# activates virtual environment 
# https://pythonspeed.com/articles/activate-virtualenv-dockerfile/
ENV VIRTUAL_ENV=/venv
ENV PATH="$PATH:${VIRTUAL_ENV}/bin"


WORKDIR /alphagolite

RUN apt update && apt install nodejs npm
RUN npm --version 

RUN cd /play_go_web_app/frontend 
RUN npm i && npm run dev
RUN cd .. && cd .. 

# An answer to the above comment (It works! Yay!)
RUN echo "source /venv/bin/activate" >> /root/.bashrc


# ensures that the Docker container is kept running 
# to then develop inside the Docker environment (using volumes, specified in docker-compose.yml
#, which you can use the bash terminal or use Visual Studio Code Docker extension
ENTRYPOINT ["python3", "manage.py", "runserver"]
