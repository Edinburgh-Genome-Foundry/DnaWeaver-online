FROM python:3.6
ENV PYTHONUNBUFFERED 1
ENV USING_DOCKER 1


RUN apt-get update
RUN apt-get install -y libgraphviz-dev graphviz

# The next line enables to build NumberJack (used by GoldenHinges)
RUN apt-get install -y python-dev swig libxml2-dev zlib1g-dev libgmp-dev

# The next line installs NCBI BLAST (for GeneBlocks, DNAWeaver, etc.)
RUN apt-get install -y ncbi-blast+

RUN mkdir /code

# The next lines install wkhtmltopdf (for Caravagene)
ENV QT_QPA_PLATFORM offscreen
# ENV QT_QPA_FONTDIR=/usr/share/fonts
RUN apt-get install -y fontconfig libfontconfig1 libfreetype6 libx11-6 libxext6 libxrender1
RUN apt-get install -y xfonts-base xfonts-75dpi fonts-font-awesome fonts-lato
RUN apt-get install -y xvfb wkhtmltopdf
RUN apt-get install -y unzip
ENV QT_QPA_FONTDIR=/root/.fonts/
# RUN wget -O "Lato.zip" "https://fonts.google.com/download?family=Lato" \
#     && unzip -u "Lato.zip" -d /root/.fonts \
#     && rm -f "Lato.zip"
RUN wget -O "Raleway.zip" "https://fonts.google.com/download?family=Raleway" \
    && unzip -u "Raleway.zip" -d /root/.fonts \
    && rm -f "Raleway.zip"
RUN wget -O "Inconsolata.zip" "https://fonts.google.com/download?family=Inconsolata" \
    && unzip -u "Inconsolata.zip" -d /root/.fonts \
    && rm -f "Inconsolata.zip"
RUN wget -O "OpenSans.zip" "https://fonts.google.com/download?family=Open+Sans" \
    && unzip -u "OpenSans.zip" -d /root/.fonts \
    && rm -f "OpenSans.zip"

ADD requirements.txt /code/
WORKDIR /code
RUN pip install -r requirements.txt

ADD . /code/

ARG CACHEBUST=8
RUN pip install --upgrade git+git://github.com/Edinburgh-Genome-Foundry/DnaWeaver
# RUN pip install biopython==1.70
