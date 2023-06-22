# Component: Ingress

This component is responsible for configuring the OpenShift Ingress Operator, and any defined IngressControllers

## Part Of
- Component: `ingress`
- Tags: `ingress`
- Application: `ingress`

# Index

<!-- vim-markdown-toc GFM -->

* [Ingress Overview](#ingress-overview)
* [Ingress Variables](#ingress-variables)
  * [Configuration Example](#configuration-example)
* [Possible Enhancements](#possible-enhancements)

<!-- vim-markdown-toc -->

# Ingress Overview

By default the OpenShift Installer creates an IngressController called
`default`, allowed to run on all worker nodes, using a wildcard certificate for
`*.apps.{{ cluster }}.{{ base_domain }}`. In most cases you will want to
replace this one with a new one that uses certificates signed by a Certificate
Authority trusted by your organization, and a NodeSelector that forces it onto
nodes where your (external) load-balancer can find it.

You can also create extra IngressControllers, for use with router-sharding, but
be careful that a single node can only run a single instance of **any** router.


# Ingress Variables

You can configure your IngressControllers using the
`openshift_ingress_controllers` variable. This variable is list of objects
using the following specification:

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `name` | **Required** | The name to give to this IngressController, also used in the name of certificate secret if a custom certificate is defined. |
| `force_loadbalancer` | Optional | Forces the creation of a LoadBalancer service. This can be useful when adding extra ingresses when running something like MetalLB on a platform that does not natively have LoadBalancer Services available. Default to `false` **Do not** use this on your `default` IngressController when using `ingress_vip` and `api_vip`, instead use `metallb.dd_default_ingress_service`. |
| `certfile` | Optional | The file on the `bastion_host` holding then public part of the certificate. |
| `cert_content` | Optional | The contents of the public certificate, in PEM format. |
| `keyfile` | Optional | The file on the `bastion_host` holding the private key of the certificate. |
| `key_content` | Optional | The contents of the certificate private key, in PEM format. |
| `domain` | Optional | The domain to use for this IngressController. If unspecified defaults to `*.apps.{{ cluster }}.{{ base_domain }}` |
| `nodePlacement` | Optional | A selector for which nodes this IngressController can schedule pods on. Can have `nodeSelector` and `tolerations` attributes. |
| `replicas` | Optional | The number of replicas for this IngressController, defaults to `2`. |
| `namespaceSelector` | Optional | A selector detailing for which namespace this IngressController should monitor routes.Can use `matchExpressions` and `matchLabels` attributes. Defaults to all namespaces. |
| `routeSelector` | Optional | A selector for which Route object to monitor. Can use `matchExpressions` and `matchLabels` attributes. Defaults to all routes. |

**N.B.** While providing a custom wildcard certificate is optional, if you do
want to provide one at least one of `certfile` or `cert_content` needs to be
provided. If both are provided `cert_content` takes precedence.  Similarly, at
least one of `keyfile` or `key_content` needs to be provided. If both are
provided `key_content` wins.


## Configuration Example

The following example overrides some settings for the `default` IngressController:

```yaml
openshift_ingress_controllers:
- name: default
  certfile: /opt/openshift_files/certs/{{ cluster }}/*.apps.{{ cluster }}.{{ base_domain }}.fullchain.pem
  keyfile: /opt/openshift_files/certs/{{ cluster }}/*.apps.{{ cluster }}.{{ base_domain }}.key
  replicas: "{{ groups['infra'] | length }}"
  nodeplacement:
    nodeSelector:
      matchLabels:
        node-role.kubernetes.io/infra: ""
```

# Possible Enhancements

An OpenShift IngressController can take more configuration than what is exposed
through this playbook. if you need these features you have two options:
1. Modify your IngressController objects in Git before applying to your cluster
2. Modify this playbook and create a Pull Request for your changes.
