FROM docker.io/bitnami/spark:2.4.6


USER root
RUN apt-get update && apt-get install -y unzip wget  && rm -rf /var/lib/apt/lists/*
RUN mkdir /opt/gradle && wget -q https://services.gradle.org/distributions/gradle-5.2-bin.zip && unzip -d /opt/gradle gradle-5.2-bin.zip
RUN mkdir /wdir && mkdir /resdir
RUN chown 1001:0 /wdir
RUN chown 1001:0 /resdir
RUN useradd -M -u 1001 -g 0 -d /resdir spark

USER root
COPY collegeregression /wdir/collegeregression/
COPY college_train_headerfix.csv /wdir/
COPY college_test_headerfix.csv /wdir/
COPY training.sh /wdir/
RUN chown -R 1001:0 /wdir
USER 1001
WORKDIR /wdir
RUN cd /wdir/collegeregression && /opt/gradle/gradle-5.2/bin/gradle build
