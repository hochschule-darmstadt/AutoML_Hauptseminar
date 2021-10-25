FROM docker.io/bitnami/spark:2.4.6


USER root
RUN apt-get update && apt-get install -y unzip wget  && rm -rf /var/lib/apt/lists/*
RUN mkdir /opt/gradle && wget -q https://services.gradle.org/distributions/gradle-7.2-bin.zip && unzip -d /opt/gradle gradle-7.2-bin.zip
RUN mkdir /wdir && mkdir /resdir
RUN chown 1001:0 /wdir
RUN chown 1001:0 /resdir
RUN useradd -M -u 1001 -g 0 -d /resdir spark

USER root
COPY . /wdir/App
RUN chown -R 1001:0 /wdir
USER 1001
RUN cd /wdir/App && /opt/gradle/gradle-7.2/bin/gradle build && cp app/build/libs/*.jar $SPARK_HOME/jars
