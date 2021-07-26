certbot-dns-websupport
======================

Websupport DNS Authenticator plugin for Certbot

This plugin automates the process of completing a ``dns-01`` challenge by
creating, and subsequently removing, TXT records using the Websupport Remote API.


Installation
------------

    pip install certbot-dns-websupport
    
    
Named Arguments
---------------

To start using DNS authentication for Websupport, pass the following arguments on
certbot's command line:
| Syntax | test |


|   Command      | Description |
| ----------- | ----------- |
|  ``--authenticator certbot-dns-websupport:dns-websupport``| select the authenticator plugin (Required) |
|``--certbot-dns-websupport:dns-websupport-credentials``    | websupport Remote User INI file. (Required) |
| ``--certbot-dns-websupport:dns-websupport-propagation-seconds`` | waiting time  for DNS to propagate before the ACME server to verify the DNS (Default: 120, Recommended: >= 600) |

(Note that the verbose and seemingly redundant ``certbot-dns-websupport:`` prefix
is currently imposed by certbot for external plugins.)


Credentials
-----------

An example ``credentials.ini`` file:

```ini
certbot_dns_websupport:dns_websupport_api_key = <api_key>
certbot_dns_websupport:dns_websupport_secret = <secret>
certbot_dns_websupport:dns_websupport_domain = example.com
```
The path to this file can be provided interactively or using the
``--certbot-dns-websupport:dns-websupport-credentials`` command-line argument. Certbot
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


Examples
--------

To acquire a single certificate for both ``example.com`` and
``*.example.com``, waiting 900 seconds for DNS propagation:


```bash
certbot certonly \
    --authenticator certbot-dns-websupport:dns-websupport \
    --certbot-dns-websupport:dns-websupport-credentials /etc/letsencrypt/.secrets/domain.tld.ini \
    --certbot-dns-websupport:dns-websupport-propagation-seconds 900 \
    --agree-tos \
    --rsa-key-size 4096 \
    -d 'example.com' \
    -d '*.example.com'
```

Docker
------

In order to create a docker container with a certbot-dns-websupport installation,
create an empty directory with the following ``Dockerfile``:

```docker
FROM certbot/certbot
RUN pip install certbot-dns-websupport
```
Proceed to build the image::

    docker build -t certbot/dns-websupport .

Once that's finished, the application can be run as follows::

```docker
docker run --rm \
   -v /var/lib/letsencrypt:/var/lib/letsencrypt \
   -v /etc/letsencrypt:/etc/letsencrypt \
   --cap-drop=all \
   certbot/dns-websupport certonly \
   --authenticator certbot-dns-websupport:dns-websupport \
   --certbot-dns-websupport:dns-websupport-propagation-seconds 900 \
   --certbot-dns-websupport:dns-websupport-credentials \
       /etc/letsencrypt/.secrets/domain.tld.ini \
   --no-self-upgrade \
   --keep-until-expiring --non-interactive --expand \
   --server https://acme-v02.api.letsencrypt.org/directory \
   -d example.com -d '*.example.com'
```

It is suggested to secure the folder as follows::
chown root:root /etc/letsencrypt/.secrets
chmod 600 /etc/letsencrypt/.secrets
