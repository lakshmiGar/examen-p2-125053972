FROM debian:bookworm-slim

ENV DEBIAN_FRONTEND=noninteractive \
    HADOOP_VERSION=3.3.6 \
    HADOOP_HOME=/opt/hadoop \
    JAVA_HOME=/usr/lib/jvm/default-java
ENV PATH=$PATH:$HADOOP_HOME/bin:$HADOOP_HOME/sbin

RUN apt-get update && apt-get install -y --no-install-recommends \
      default-jre-headless python3 openssh-server openssh-client \
      curl ca-certificates procps \
    && rm -rf /var/lib/apt/lists/*

# Hadoop en modo standalone (solo descomprimir, sin configurar HDFS)
RUN curl -fsSL https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz \
    | tar -xz -C /opt \
    && mv /opt/hadoop-${HADOOP_VERSION} ${HADOOP_HOME} \
    && echo "export JAVA_HOME=${JAVA_HOME}" >> ${HADOOP_HOME}/etc/hadoop/hadoop-env.sh

# Usuario sin contraseña + SSH solo por llaves
RUN useradd -m -s /bin/bash hadoop && usermod -p '*' hadoop \
    && mkdir -p /run/sshd /shared-ssh /data/input /data/output /home/hadoop/.ssh \
    && printf 'Host *\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n' > /home/hadoop/.ssh/config \
    && chmod 700 /home/hadoop/.ssh && chmod 600 /home/hadoop/.ssh/config \
    && chown -R hadoop:hadoop /home/hadoop/.ssh /data/output \
    && sed -i 's/^#\?PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config \
    && printf 'export JAVA_HOME=%s\nexport HADOOP_HOME=%s\nexport PATH=$PATH:%s/bin\n' \
       "$JAVA_HOME" "$HADOOP_HOME" "$HADOOP_HOME" > /etc/profile.d/hadoop.sh

# Verificación en build (A1: hadoop version)
RUN hadoop version

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 22
ENTRYPOINT ["/entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]