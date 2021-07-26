certbot-dns-websupportsk
======================

Websupport DNS Authenticator plugin for Certbot

This plugin automates the process of completing a ``dns-01`` challenge by
creating, and subsequently removing, TXT records using the Websupport Remote API.

---

Installation
------------

    pip install certbot-dns-websupportsk

---   
 
Named Arguments
---------------

To start using DNS authentication for [Websupport.sk](https://www.websupport.sk), pass the following arguments on
certbot's command line:

|   Command                                                                              | Description                                 |
| -------------------------------------------------------------------------------------- | ------------------------------------------- |
| ``--authenticator certbot-dns-websupportsk:dns-websupportsk``                          | select the authenticator plugin (Required)  |
| ``--certbot-dns-websupportsk:dns-websupportsk-credentials "/path/to/credentials.ini"`` | websupport Remote User INI file. (Required) |
| ``--certbot-dns-websupportsk:dns-websupportsk-propagation-seconds "600"``               | waiting time  for DNS to propagate before the ACMEserver to verify the DNS (Default: 120, Recommended: >= 600) |

(Note that the verbose and seemingly redundant ``certbot-dns-websupportsk:`` prefix
is currently imposed by certbot for external plugins.)

---

Credentials file
----------------

An example ``credentials.ini`` file:

```ini
certbot_dns_websupportsk:dns_websupportsk_api_key = <api_key>
certbot_dns_websupportsk:dns_websupportsk_secret = <secret>
certbot_dns_websupportsk:dns_websupportsk_domain = example.com
```

The path to this file can be provided interactively or using the
``--certbot-dns-websupportsk:dns-websupportsk-credentials`` command-line argument. Certbot
records the path to this file for use during renewal, but does not store the
file's contents.

**CAUTION:** You should protect these API credentials as you would the
password to your websupport account. Users who can read this file can use these
credentials to issue arbitrary API calls on your behalf. Users who can cause
Certbot to run using these credentials can complete a ``dns-01`` challenge to
acquire new certificates or revoke existing certificates for associated
domains, even if those domains aren't being managed by this server.

Certbot will emit a warning if it detects that the credentials file can be
accessed by other users on your system. The warning reads "Unsafe permissions
on credentials configuration file", followed by the path to the credentials
file. This warning will be emitted each time Certbot uses the credentials file,
including for renewal, and cannot be silenced except by addressing the issue
(e.g., by using a command like ``chmod 600`` to restrict access to the file).

---

Direct command
--------------

To acquire a single certificate for both ``example.com`` and
``*.example.com``, waiting 600 seconds for DNS propagation:


```bash
certbot certonly \
    --authenticator certbot-dns-websupportsk:dns-websupportsk \
    --certbot-dns-websupportsk:dns-websupportsk-propagation-seconds "600" \
    --certbot-dns-websupportsk:dns-websupportsk-credentials "/etc/letsencrypt/.secrets/<domain>.<tld>.ini" \
    --email full.name@example.com \
    --agree-tos \
    --rsa-key-size 4096 \
    -d *.example.com -d example.com
```
**NOTE:** Don't forget to name your ini file

---

Docker
------

In order to create a docker container with a certbot-dns-websupport installation,
create an empty directory with the following ``Dockerfile``:

```dockerfile
FROM certbot/certbot
RUN pip3 install certbot-dns-websupportsk
```

<br>

Proceed to build the image:
```commandline
docker build -t certbot/dns-websupportsk .
```

<br>

Once that's finished, the application can be run as follows:
```commandline
sudo docker run -it --rm \
    -v /var/lib/letsencrypt:/var/lib/letsencrypt \
    -v /etc/letsencrypt:/etc/letsencrypt \
    certbot/dns-websupportsk \
    certonly \
    --authenticator certbot-dns-websupportsk:dns-websupportsk \
    --certbot-dns-websupportsk:dns-websupportsk-propagation-seconds "600" \
    --certbot-dns-websupportsk:dns-websupportsk-credentials "/etc/letsencrypt/.secrets/<domain>.<tld>.ini" \
    --email full.name@example.com \
    --agree-tos \
    --rsa-key-size 4096 \
    -d *.example.com -d example.com
```
**NOTE:** Check if your volumes on host system match this example (Depends if you installed your server on host system or inside docker). If not, you will have to edit this command.

<br>

It is suggested to secure the .ini folder as follows:
```commandline
chown root:root /etc/letsencrypt/.secrets
chmod 600 /etc/letsencrypt/.secrets
```

---