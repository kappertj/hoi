# Component: MetalLB

This component is responsible for installing and configuring a MetalLB
LoadBalancer instance on your cluster.

## Part Of
- Component: `metallb`
- Tags: `metallb`
- Application: `metallb`

# Index

<!-- vim-markdown-toc GFM -->

* [Configuration Variables](#configuration-variables)
  * [Configuring MetalLb](#configuring-metallb)
    * [Configuring AddressPools](#configuring-addresspools)
    * [Configuring BGP Peers](#configuring-bgp-peers)
    * [Configuring BGP Advertisements](#configuring-bgp-advertisements)
    * [Configuring L2  Advertisements](#configuring-l2--advertisements)
  * [Replacing the Default IngressController](#replacing-the-default-ingresscontroller)
    * [Caveats](#caveats)
    * [Procedure when not using `api_vip` and `ingress_vip`](#procedure-when-not-using-api_vip-and-ingress_vip)
    * [Procedure when not using `api_vip` and `ingress_vip`](#procedure-when-not-using-api_vip-and-ingress_vip-1)
  * [MetalLB Example Configuration](#metallb-example-configuration)

<!-- vim-markdown-toc -->

# Configuration Variables


| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `metallb` | **Required** | A set of configuration options for MetalLB|

## Configuring MetalLb

The `metallb` variable takes a number of children, all of which are optional:

| Key | Required/Optional | Comments |
|-----|-------------------|----------|
| `asn`| Optional | The Autonomous System Number (ASN) for this MetalLB instance. This item becomes **Required** when `metallb.bgpadvertisements` is non-empty. |
| `addresspools` | Optional | A list of addresspools to configure, see [Configuring AddressPools](#configuring-address-pools) |
| `peers` | Optional | A list of BGP peers to configure, see [Configuring BGP Peers](#configuring-bgp-peers) |
| `bgpadvertisements` | Optional | A list of BGP Advertisements to configure, see [Configuring BGP Advertisements](#configuring-bgp-advertisements) |
| `l2advertisements` | Optional | A list of L2 Advertisements to configure, see [Configuring L2 Advertisements](#configuring-l2-advertisements) |
| `add_default_ingress_service` | Optional | Add an extra LoadBalancerService to the default IngressController. Needed when using `api_vip` and `ingress_vip`. Defaults to `false` |
| `default_ingress_ip` | Optional | An optional IP address to assign to the extra default Ingress Service. Only useful when `add_default_ingress_service: true`. Defaults to unset. |

### Configuring AddressPools

In `metallb.addresspools` you can configure a list of addresspools with the following attributes:

| Key | Required/Optional | Description |
|-----|-------------------|-------------|
| `name` | **Required** | The name for this Adress Pool |
| `addresses` | **Required** | A *list* of address and address ranges |
| `autoassign` | Optional | Whether or not address from this range can be assigned autoamtically, defaults to `true` |

### Configuring BGP Peers

In `metalb.peers` you can configure a list of BGP Peers using the following attributes:

| Key | Required/Optional | Description |
|-----|-------------------|-------------|
| `name` | **Required** | A name for the remote peer |
| `asn` | **Required** | The Autonomous System Number for the remote peer |
| `address` | **Required** | The IP address of the remote peer |

### Configuring BGP Advertisements

In `metallb.bgpadvertisements` you can configure from which address pools IP addresses should be advertised over BPG.

| Key | Required/Optional | Description |
|-----|-------------------|-------------|
| `name` | **Required** | A name for the advertisements |
| `addresspools` | **Required** | A *list* of Address Pool names to be advertised |

### Configuring L2  Advertisements

In `metallb.l2advertisements` you can configure from which address pools IP addresses should be advertised using simple Layer 2 failover with VRRP.

| Key | Required/Optional | Description |
|-----|-------------------|-------------|
| `name` | **Required** | A name for the advertisements |
| `addresspools` | **Required** | A *list* of Address Pool names to be advertised |


## Replacing the Default IngressController

Replacing the (Default) IngressController with one that uses a
LoadBalancerService from MetalLB currently takes some manual work. If you want
to create a (Post)SyncHook for this we will happily take your MergeRequest.

### Caveats

If you use `api_vip` and `ingress_vip` you **CAN NOT** update the default
ingresscontroller to use a LoadBalancerService. You can however add an extra
LoadBalancerService that points to the same IngressController.

This is because the `ingress_vip` gets hardcoded into your cluster at multiple
places, including the configuration for CoreDNS (`Corefile`). Updating the
default Service would make `ingress_vip` unusable, resulting in features like
oauth logins for the console and ArgoCD becoming unavailable.

### Procedure when not using `api_vip` and `ingress_vip`
1. Forcefully replace the default `IngressController`:
   ```
   $ oc replace --force --wait -f <path/to/gitops>/ingress/assets/ingresscontroller-default.yaml
   ```
2. Wait for the `ingress-default` service to get an IP address from one of the
   `IPAddressPools` you configure for MetalLB. This is your new Ingress IP.
3. Update your DNS server with the new address for `*.apps.<cluster>.<domain>`.

### Procedure when not using `api_vip` and `ingress_vip`
1. Configure `metallb.add_default_ingress_service` and optionally `metallb.default_ingress_ip`
2. When not using `metallb.default_ingress_ip`: Wait for the
   `router-metallb-default` service to get an IP address from one of the
   `IPAddressPools` you configure for MetalLB. This is your new Ingress IP.
3. Update your DNS server with the new address for `*.apps.<cluster>.<domain>`.

##  MetalLB Example Configuration
```yaml
metallb:
  asn: 64513
  addresspools:
  - name: ocp
    addresses:
    - 10.1.0.102-10.1.0.110
  peers:
  - name: router
    asn: 64512
    address: 10.1.0.1
  bgpadvertisements:
  - name: router
    addresspools:
    - ocp
  l2advertisements: []
```
