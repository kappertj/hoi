# Component: Proxy

This component is responsible for configuring both the proxy used by the
cluster, and the trusted CAs.

Normally, this is all configured during install time, but there is a caveat:

> :warning: When you do not have a system-wide proxy configured, a ConfigMap called
> `user-ca-bundle` is still configured in the `openshift-config` namespace, but
> it is not referenced anywhere. Using this component you can enable the trust
> for your local CA, without configuring a proxy.

## Part Of
- Component: `proxy`
- Tags: `proxy`
- Application: `proxy`

# Index

<!-- vim-markdown-toc GFM -->

* [Proxy Variables](#proxy-variables)
    * [Proxy Configuration Example](#proxy-configuration-example)

<!-- vim-markdown-toc -->

# Proxy Variables

You can set

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `custom_ca_file` | Optional | A file path (on your bastion host) containing a list of additional Certificate Authorities (in PEM format) that should be added to the cluster trust store. These CAs will be trusted by the cluster, but not automatically by additional applications you deploy on your cluster. |
| `http_proxy` | Optional | The URL, including protocol and port, of an optional proxy server to use for http requests. Automatically honored by most cluster components, not by extra applications you deploy yourself. |
| `https_proxy` | Optional | The URL, including protocol and port, of an optional proxy server to use for https requests. Automatically honored by most cluster components, not by extra applications you deploy yourself. |
| `no_proxy` | Optional | A comma-separated list of URL patterns, host names, IP addresses, and IP ranges that should not be sent to the proxy. Your cluster networks and local cluster service names are automatically added to this list. Honored by most cluster components, but not by additional applications you deploy yourself. |
| `proxy_readiness_endpoints` | Optional | A *list* of URLs (starting with `http://` or `https://` that should be successfully accessed through the proxy before activating it. |


## Proxy Configuration Example
```yaml
http_proxy: http://proxy.example.com:8080
https_proxy: https://proxy.example.com:8443
no_proxy: .example.com,10.0.0.0/8
proxy_readiness_endpoints:
- https://google.com
- https://techblog.hcs-company.com
```
