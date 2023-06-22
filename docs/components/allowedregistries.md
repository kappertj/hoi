# Component: Allowed Registries

This component is responsible for configuring the allowed registries on your
cluster.  This includes custom CA certificates for registries, insecure
registries, and allowing importing by regular users.

By default OpenShift allows users to pull images from any (secure) registry
they want. An administrator can close this off to a predefined list, and allow certain registries to be used over HTTP, or without a validated certificate.


## Part Of
- Component: `allowedregistries`
- Tags: `allowedregistries`
- Application: `allowedregistries`

# Index

<!-- vim-markdown-toc GFM -->

* [Allowed Registries Variables](#allowed-registries-variables)
    * [Allowed Registries Attributes](#allowed-registries-attributes)
    * [Allowed Registries Configuration Example](#allowed-registries-configuration-example)

<!-- vim-markdown-toc -->

# Allowed Registries Variables


You can set

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `removedefaultregistries` | Optional | Whether or not to remove the default list of allowed registries (`quay.io`, `registry.redhat.io`, `docker.io`, `k8s.gcr.io`, and the internal registry) from the list of allowed registries. Defaults to `false` |
| `allowedregistries` | Optional | A list of registries to be allowed on the cluster. Defaults to `[]`. See the explanation below for valid attributes. |

## Allowed Registries Attributes

Every entry in the `allowedregistries` variable can have a number of configuration options:

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `url` | **Required** | The hostname of the registry (can include a path). For example `quay.io` or `myregistry.example.com/myrepo/myapp:latest` |
| `ca` | Optional | A custom CA (in PEM format) to use for this registry. A full chain is recommendend. |
| `insecure` | Optional | Whether or not this is an insecure registry (HTTP or unvalidated HTTPS). Defaults to `False`. |
| `allowimport` | Optional | Whether or not regular users can create an ImageStreamImport from this registry. Defaults to `False`. |
| `samplesregistry` | Optional | The registry to use for the samples operator. Defaults to `registry.redhat.io`. |

## Allowed Registries Configuration Example
```yaml
removedefaultregistries: false
allowedregistries:
- url: internal.example.com
  ca: |
    CERTS GO HERE
    ...
    CERTS GO HERE
  allowimport: true
- url: insecure.example.com
  insecure: true
- url: registry.gitlab.com/wanderb/isitfriday:minimize
  allowimport: true
```
