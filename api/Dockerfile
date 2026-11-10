FROM python:3.12-slim
RUN apt-get update && apt-get install -y --no-install-recommends openssh-client \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
# Permite "ssh hadoop@hadoop" sin contraseña ni -i
RUN mkdir -p /root/.ssh && printf 'Host hadoop\n  User hadoop\n  IdentityFile /shared-ssh/id_ed25519\n  StrictHostKeyChecking no\n  UserKnownHostsFile /dev/null\n' > /root/.ssh/config \
    && chmod 600 /root/.ssh/config
EXPOSE 8000
CMD ["python", "app.py"]
