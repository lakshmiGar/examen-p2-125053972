#!/bin/bash
set -e
KEY=/shared-ssh/id_ed25519

[ -f "$KEY" ] || ssh-keygen -t ed25519 -N "" -f "$KEY" -q
chmod 600 "$KEY"

# authorized_keys para entrar al contenedor hadoop
cp "$KEY.pub" /home/hadoop/.ssh/authorized_keys
# llave privada propia para "ssh localhost"
cp "$KEY" /home/hadoop/.ssh/id_ed25519
chown hadoop:hadoop /home/hadoop/.ssh/authorized_keys /home/hadoop/.ssh/id_ed25519
chmod 600 /home/hadoop/.ssh/authorized_keys /home/hadoop/.ssh/id_ed25519

/usr/sbin/sshd
exec "$@"