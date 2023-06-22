# Component: API Server

This component is responsible for configuring the OpenShift API Server.
Currently two modifications are supported:
- Custom Serving Certificates
- Etcd encryption

This component also sets the cluster-wide default nodeSelector to
`node-role.kubernetes.io/worker=""` to ensure that no user workloads land on
Infra, Storage, or Master nodes.

## Part Of
- Component: `apiserver`
- Tags: `apiserver`
- Application: `apiserver`

# Index

<!-- vim-markdown-toc GFM -->

* [API Server Certificate Variables](#api-server-certificate-variables)
  * [API Server Certificate Considerations](#api-server-certificate-considerations)
  * [API Server Certificate example](#api-server-certificate-example)
* [Etcd Encryption](#etcd-encryption)

<!-- vim-markdown-toc -->

# API Server Certificate Variables

The API Server serving certificate is configured if the variable
`apiserver_certificate` is set. Certificate and key contents can be provided in
two ways, by means of a file on your `bastion_host`, or by having the actual
content in your inventory. having the contents in in files makes things easier
with certificate updates, while having the contents in yoiur inventory allows
for encryption using vault, or even autoamtic retrieval from external secret
providers using lookup plugins.

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `name` | **Required** | The name to give to the secret holding the certificate |
| `certfile` | Optional | The file on the `bastion_host` holding then public part of the certificate. |
| `cert_content` | Optional | The contents of the APIServer public certificate, in PEM format. |
| `keyfile` | Optional | The file on the `bastion_host` holding the private key of the certificate. |
| `key_content` | Optional | The contents of the APIServer certificate private key, in PEM format. |

**N.B.** At least one of `certfile` or `cert_content` needs to be provided. If
both are provided `cert_content` takes precedence.  Similarily, at least one of
`keyfile` or `key_content` needs to be provided. If both are provided
`key_content` wins.


## API Server Certificate Considerations

The certificate you provide must be valid for the domain `api.{{ cluster }}.{{ base_domain }}`.
At the time of running the playbook it should be valid for at least another 30
days. (Configurable using the variable `certificate_expiry_limit_days`).

## API Server Certificate example
```yaml
apiserver_certificate:
  name: example-api-cert
  certfile: /opt/openshift_files/certs/{{ cluster }}/api.{{ cluster }}.{{ base_domain }}.fullchain.pem
  keyfile: /opt/openshift_files/certs/{{ cluster }}/api.{{ cluster }}.{{ base_domain }}.key
```

# Etcd Encryption

Encryption of sensitive data in Etcd can be controlled using the following variables:
| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `etcd_encryption` | Optional | Whether or not to encrypt sensitive data in Etcd. Defaults to `true` |
