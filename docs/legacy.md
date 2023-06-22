# HCS OpenShift Installation, Configuration, and Detonation

## Index

<!-- vim-markdown-toc GitLab -->

* [Requirements](#requirements)
* [Usage](#usage)
* [Adding new nodes](#adding-new-nodes)
* [Where's the rest of the docs?](#wheres-the-rest-of-the-docs)
* [Inventory format](#inventory-format)
  * [Node variables](#node-variables)
  * [VMWare extras](#vmware-extras)
  * [Cluster settings](#cluster-settings)
    * [Encrypted router and api cert keys](#encrypted-router-and-api-cert-keys)
* [Selecting which components to run](#selecting-which-components-to-run)
* [Other settings](#other-settings)
  * [Download sources](#download-sources)
  * [bastion directories](#bastion-directories)
  * [OpenShift SDN settings](#openshift-sdn-settings)
  * [NFS Dynamic client provisioner defaults](#nfs-dynamic-client-provisioner-defaults)
  * [OpenShift container storage](#openshift-container-storage)
  * [Prometheus and AlertManager defaults](#prometheus-and-alertmanager-defaults)
  * [Registry storage defaults](#registry-storage-defaults)
  * [Logging and ElasticSearch defaults](#logging-and-elasticsearch-defaults)
  * [Groupsync Cronjob defaults](#groupsync-cronjob-defaults)
  * [Custom logos and login pages](#custom-logos-and-login-pages)
  * [Custom console URL](#custom-console-url)

<!-- vim-markdown-toc -->

## Requirements
- A RHEL8, CentOS8 or modern Fedora machine to run this on
- Ansible 2.8+   _* (Ansible 2.9+, when deploying VMware VM's)_

> _* The Ansible `vsphere_copy` module contains updated paramater names, that is the difference between Ansible v2.8x and v2.9x._

## Usage

1. Edit Inventory to taste
2. Run `openshift_install.yml` playbook
   - Add `-e create_new_cluster=true` if you actually want to create a new
     cluster, leave it off when using `-l` to add new hosts
3. Run `openshift_config.yml` to add all configurations, move stuff to infra
   nodes, add authentication providers, certificates, storage, etc. See
   the `openshift_components` variable to find out more. Make sure to provide
   a value for variable `bastion_host` as extra vars when running the
   playbook in order to point it to the specific host that executes the
   playbook. This can be `localhost` or a remote bastion node depending on
   which host is to execute the playbook.

N.B. If the `apiserver_certs` tasks has been run authentication using the
installer generated `kubeconfig` will no longer work. In those cases use the
`openshift_kubeconfig` variable (specified on the commandline) to point to a
valid Kube config for a user with `cluster-admin` credentials on the bastion
host.


## Adding new nodes
1. Add the new nodes to your inventory
1. Run the isntaller playbook, limiting it to the new hosts
   1. If you haven't already configured certificates on the cluster:
      `ansible-playbook -i <inventory> -l <new_hosts_pattern> openshift_install.yml`
   2. If you already configured new certificates:
      `ansible-playbook -i <inventory> -l <new_hosts_pattern> -e openshift_kubeconfig=<path to a logged in .kube/config with admin rights on the bastion> </path>openshift_install.yml`
1. ???
1. Profit

**N.B.** Make sure you do **NOT** specify `-e create_new_cluster=true` when
adding hosts, that's a recipe for happy funtimes bonus overtime pay.


## Where's the rest of the docs?

We're working on it. Feel free to contribute.

## Inventory format

### Node variables

We need a couple of things configured for nodes, this is from the
`host_vars/template` directory.
```yaml
# install_method can be 'ilo', 'grub', 'libvirt', or 'vmware'
install_method: vmware # Can be set per machine or for all machines group_vars

# Set the disk to install to, without `/dev/`
install_dev: sda

# A *list* of network interfaces
# Only one interface should have `is_default_gateway` set.
#
# network_config[*].mac, network)config[*].bridge, and virt_host, are
# only used for libvirt installations

# network_config[*].vmware_net is only used for vmware installations
# network_config[*].bridge is only used for libvirt installations

network_config:
- device: ens192
  mac: "52:54:00:00:01:29"
  address: 10.1.0.29
  netmask: 255.255.255.0
  gateway: 10.1.0.1
  is_default_gateway: True
  dns:
  - 10.1.0.10
  bridge: okd
  vmware_net: VL_OCP

- device: bond0
  # bonding_opts is only needed when they differ from the options below
  bonding_opts:
  - "mode=802.3ad"
  - "lacp_rate=0"
  - "miimon=100"
  - "updelay=1000"
  - "downdelay=1000"
  address: 10.1.0.30
  netmask: 255.255.255.0
  gateway: 10.1.0.1
  is_default_gateway: True
  dns:
  - 10.1.0.10
  slaves:
  - device: enp1s0
    mac: 01:02:04:04:05:06
    bridge: br1
    # mac and bridge onlyy needed for testing on libvirt, don't run bonding
    # on libvirt in the real world please.
  - device: eth3

# These settings are only for `libvirt` installations
image_size: 120G
virt_host: hypervisor.example.com
virt_memory: 16384
virt_vcpus: 4


# This is only for `install_method: vmware`
vmware:
  vcenter: dcr1
  template: OCP4-Template
  memory: 16384
  vcpu: 4
  disk: 120
  folder: OpenShift
  guest_id: rhel7_64Guest
  hardware_version: 13
  customvalues:
  - key: "disk.EnableUUID"
    value: "true"


# When using the local-storage operator
local_storage:
- storageclass: logging
  device: /dev/vdb
- storageclass: metrics
  device: /dev/vdc

# Extra labels to put on hosts, usefule for topology
# Remember to quote labels with periods and slashes
extra_node_labels:
  "topology.kubernetes.io/region": amersfoort
  "topology.kubernetes.io/zone": dc1
```

> `vmware.customvalues` is optional, can be used to specify specific VMware custom parameters for a machine. It's a key value store as described in the [ansible module vmware_guest_module](https://docs.ansible.com/ansible/latest/collections/community/vmware/vmware_guest_module.html#parameter-customvalues).

> `vmware.hardware_version` is optional, can be used to specify the specific VMware VM hardware version. It can be used to enforce a certain hardware version.

### VMWare extras

Since VMWare installations need to know about vcenters, datacenters, etc. a special variable called `vcenters` can be used:
```yaml
vcenters:
  dcr1:
    hostname: vcenter1.example.com
    username: "{{ encrypted_vcenter_username }}"
    password: "{{ encrypted_vcenter_password }}"
    datacenter: DCR2
    datastore: DCR1-STORE
    iso_datastore: DCR1-ISO
    cluster: CL-DCR1
  dcr2:
    hostname: vcenter2.example.com
    username: "{{ encrypted_vcenter_username }}"
    password: "{{ encrypted_vcenter_password }}"
    datacenter: DCR2
    datastore: DCR2-STORE
    iso_datastore: DCR2-ISO
    cluster: CL-DCR2

vmware_vm_name_notation: "{{ inventory_hostname_short | upper }}"

install_dev_type: thin
```

> `vmware_vm_name_notation` is an optional variable to override the VMware name notation (format). By design, it falls back to the default `"{{ inventory_hostname_short | upper }}"` to keep backward compatibility. Use this variable to define your own company wide policy on namingconventions.

> `install_dev_type` is an optional variable to override the VMware VM's primary disk type. By design, it falls back to the default `"thin"` to keep backward compatibility. Use this variable to override the default value for the type of disk. It goes together (complements) with the variable `install_dev` for the primary disk device name. Both variables can be defined in the Ansible group_vars or host_vars, depending on their scopes or where to them set eventually.

### Cluster settings

Quite a large number of settings can be configured, both for the installation
and the configuration playbook.

```yaml
# install_method can be one of ['libvirt', 'vmware', 'grub', 'ilo'], can also
# be overridden per host
install_method: vmware

# Select flavour ['okd', 'ocp'] and major version, e.g. '4.4'
# Warning, OKD install versions are not currently maintained
install_flavour: ocp
install_version: "4.8"

# VRRP/Keepalived for api(-int) and ingress
# IPs need to be reachable from the outside world
# Without specifying both keeaplived will _not_ be configured
# This works by half-faking a bare-metal IPI install
api_vip: 10.1.0.100
ingress_vip: 10.1.0.101

# The bastion host can be different than the ansible controller node.
# Just remember that most file lookups are performed on the ansible controller
# node
bastion_host: localhost

# List of ntp_servers to be applied to all nodes. Currently done with a
# machineConfig, and can _not_ be overriden per host.
ntp_servers:
- 10.0.0.1

# If bastion_host is localhost, uncomment this line and set it to the external
# hostname of your bastion. This is needed to create URLs for downloads
# of ignition files and metal iamges, among others.
#bastion_external_hostname: bastion.example.com

# Set cluster name
cluster: ocp

# base_domain, final domain names end up as api(-int).{{ cluster }}.{{ base_domain }} and
# *.apps.{{ cluster }}.{{ base_domain }}
base_domain: example.com

# Proxy settings. if http_proxy is not defined (not the same as empty) no proxy
# will be configured on the cluster.
http_proxy: http://proxy.example.com:8080
https_proxy: https://proxy.example.com:8080
no_proxy: .svc,localhost,localhost.localdomain,.localdomain,192.168.0.0/24,.example.com

# A list of edits to make to the cluster manifests before isntallation.
# Normally you will want the below:
openshift_manifest_customizations:
- file: cluster-scheduler-02-config.yml
  regexp: '^  mastersSchedulable:'
  line: '  mastersSchedulable: false'

# An SSH public key, and a RH pull-secret from cloud.redhat.com
# Paths are local on the ansible controller node when using a `file` lookup
like this
openshift_coreos_sshpubkey: "{{ lookup('file', '/path/to/public_key') }}"
openshift_pullsecret: "{{ lookup('file', 'path/to/pull_secret/file') }}"

# Ingress Definitions
# If you **DO NOT** define an Ingresscontroller named `default` you will still end up with one
# Everything except `name` and `replicas` is optional
# Some of these settings used to be in `routercerts_certificates`
  openshift_ingress_controllers:
  - name: default
    certfile: /opt/openshift_files/certs/{{ cluster }}/*.apps.{{ cluster }}.{{ base_domain }}.fullchain.pem
    keyfile: /opt/openshift_files/certs/{{ cluster }}/*.apps.{{ cluster }}.{{ base_domain }}.key
    replicas: "{{ groups['infra'] | length }}"
    nodeplacement:
      nodeSelector:
        matchLabels:
          node-role.kubernetes.io/infra: ""
    routeselector:
      matchLabels:
        type: sharded
    namespaceSelector
      matchExpressions:
      - key: phase
        operator: In
        values:
        - test
        - dev


# Wildcard certificates for the routers, these files are `slurp`ed from the
# bastion host. You will typically want to have an entry for `name: default`, as
# that is the default router created by the install.
routercerts_certificates:
- name: default
  certfile: /opt/openshift_files/certs/{{ cluster }}/*.apps.{{ cluster }}.{{ base_domain }}.fullchain.pem
  keyfile: /opt/openshift_files/certs/{{ cluster }}/*.apps.{{ cluster }}.{{ base_domain }}.key
  # Keys can be Ansible vault encrypted to increase security. Read the docs
  # in below this section and uncomment to set the value when required.
  # keyfile_is_vaultencrypted: true

# Organizational CA to be trusted, file needs to be present on the Ansible
# controller node.
custom_ca_file: /etc/ipa/ca.crt

# Custom certificate for api.{{ cluster }}.{{ base_domain }}, file paths on
# bastion host.
apiserver_certificate:
  name: custom-api-cert
  certfile: /opt/openshift_files/certs/{{ cluster }}/api.{{ cluster }}.{{ base_domain }}.fullchain.pem
  keyfile: /opt/openshift_files/certs/{{ cluster }}/api.{{ cluster }}.{{ base_domain }}.key
  # Keys can be Ansible vault encrypted to increase security. Read the docs
  # in below this section and uncomment to set the value when required.
  # keyfile_is_vaultencrypted: true

# iSCSI volumes to create PVs and storageclasses for
# Each PV can be assigned a different storageclass, these are created
# automatically.
# Extra portals and an initiatorname are optional.

iscsi_pvs:
- name: metrics-1
  portal: 10.1.0.10
  iqn: iqn.2020-06.com.example.bastion:metrics-1
  fstype: xfs
  capacity: 100Gi
  labels:
    usage: metrics
  storageclass: metrics
- name: alerts-1
  portal: 10.1.0.10
  iqn: iqn.2020-06.com.example.bastion:alerts-1
  fstype: xfs
  capacity: 5Gi
  labels:
    usage: alerts
  storageclass: metrics
- name: logging-1
  portal: 10.1.0.10
  portals:
  - 10.1.0.10:3260
  - 10.1.0.11:3260
  iqn: iqn.2020-06.com.example.bastion:logging-1
  initiatorname: iqn.2000-01.com.hcs-company:example
  fstype: xfs
  capacity: 150Gi
  labels:
    usage: logging
  storageclass: logging

# NFS server and export path for dynamic NFS client provisioner
# This export will be used to create other (dynamic) PVs using a strorageclass
nfs_client_provisioner_server: 1.2.3.4
nfs_client_provisioner_export: /exports/nfs

# ldap settings
# used in the oauths below
ldap_service_dn: uid=ldap-service,cn=sysaccounts,cn=etc,dc=example,dc=com
ldap_service_pass: secret_password

# Authentications to configure, keep what you need, delete the rest, all LDAP
# cafiles are local to the Ansible controller node.
oauths:
- name: example-ipa
  type: LDAP
  binddn: "{{ ldap_service_dn }}"
  bindpass: "{{ ldap_service_pass }}"
  scheme: ldap
  host: ipa.example.com
  base: cn=users,cn=accounts,dc=example,dc=com
  cafile: /etc/ipa/ca.crt
  attributes:
    id:
    - uid
    email:
    - mail
    name:
    - displayName
    preferredUsername:
    - uid
- name: example-AD
  type: LDAP
  binddn: "{{ ldap_service_dn }}"
  bindpass: "{{ ldap_service_pass }}"
  scheme: ldaps
  host: ad.example.com
  base: cn=users,cn=accounts,dc=example,dc=com
  urlfilter: '?samaccountname?sub'
  cafile: /path/to/AD/ca.crt
  attributes:
    id:
    - cn
    email:
    - mail
    name:
    - description
    preferredUsername:
    - sAMAccountName

# Removing default self-provisioner access
self_provisioners:
  remove_default: true
  users:
  - developer
  groups: []

# Settings for a groupsync cronjob that will run every minute.
groupsync_cronjob_ldap_user: "{{ ldap_service_dn }}"
groupsync_cronjob_ldap_password: "{{ ldap_service_pass }}"
groupsync_ldap_ca_file: /tmp/ca.crt
groupsync_cronjob_ldap_base_dc_groups: "cn=groups,cn=accounts,dc=example,dc=com"
groupsync_cronjob_ldap_base_dc_users: "cn=users,cn=accounts,dc=example,dc=com"
groupsync_cronjob_namespace: openshift-ops
groupsync_cronjob_ldap_url: ldap://bastion.example.com:389
groupsync_cronjob_cluster_admins_group: clusteradmin

# Set this one to 'ad' or 'ipa'
groupsync_cronjob_type: ad
#groupsync_cronjob_type: ipa

# List of groups to sync, with their desired OpenShift (`short`) name.
groupsync_groups:
- dn: "cn=clusteradmin,cn=groups,cn=accounts,dc=example,dc=com"
  short: clusteradmin

# Configure AlertManager. If no `alertmanager_config` is defined no action will
# be taken

#alertmanager_config:
#  global:
#    resolve_timeout: 5m
#  route:
#    group_wait: 30s
#    group_interval: 5m
#    repeat_interval: 12h
#    receiver: default
#    routes:
#    - match:
#        alertname: Watchdog
#      repeat_interval: 5m
#      receiver: watchdog
#  receivers:
#  - name: default
#    webhook_configs:
#    - url: https://some.webhook.receiver.com/mywebhook/id
#      send_resolved: true
#  - name: watchdog

```

> When using `oauths` and having to deal with old-fashioned secure LDAP, it's
> required to provide the `scheme`. Use `scheme: ldaps` for when secure LDAP
> is used over port 636, or scheme `ldap` for when LDAP is used over the
> standard port 389 (with or without STARTTLS).
> The default for `scheme` is `ldap`.

#### Encrypted router and api cert keys

`routercerts_certificates` and `apiserver_certificate` contain certificate
keys. One can choose to add additional security by encrypting keys with
Ansible vault. This changes the way it's deployed as it has to decrypt
and transform the Ansible encrypted key file and present it to the tasks
in charge of deploying it from jinja templates.

When using this option, make sure the value of the `keyfile` is something like
this example and `keyfile_is_vaultencrypted` is set to `true`. By default it
falls back to its original behaviour (reading an un encrypted keyfile).

```yaml
routercerts_certificates:
- name: default
  certfile: /opt/openshift_files/certs/{{ cluster }}/*.apps.{{ cluster }}.{{ base_domain }}.fullchain.pem
  keyfile: "{{ lookup('file', '/opt/openshift_files/certs/{{ cluster }}/*.apps.{{ cluster }}.{{ base_domain }}.key') | b64encode }}"
  keyfile_is_vaultencrypted: true

apiserver_certificate:
  name: custom-api-cert
  certfile: /opt/openshift_files/certs/{{ cluster }}/api.{{ cluster }}.{{ base_domain }}.fullchain.pem
  keyfile: "{{ lookup('file', '/opt/openshift_files/certs/{{ cluster }}/api.{{ cluster }}.{{ base_domain }}.key') | b64encode }}"
  keyfile_is_vaultencrypted: true
```

## Selecting which components to run

The `openshift_config.yml` playbook uses the content of the
`openshift_components` variable to select which tasks to run. Individual tasks
can also be run exclusively, or skipped, by using the Ansible `--tags` and
`--skip-tags` options respectively. All tag names are identical to the names
listed below.

```yaml
openshift_components:
- chrony
- iscsi_pvs
- local_storage
- nfs_client_provisioner
- ocs_storage
- monitoring_storage
- registry_storage
- cluster_logging
- network_policies
- deploy_tekton
- deploy_gitops
- imagepruner
- oauth
- self_provisioners
- groupsync
- alertmanager
- custom_logo
- custom_login
- custom_console_url
- routercerts
- apiserver_certs
```

## Other settings

### bastion directories
- `openshift_ignition_dir: /opt/openshift_files/{{ cluster }}/ignition`
- `openshift_installer_dir: /opt/openshift_files/{{ cluster }}/installer`
- `openshift_installer_binary: "{{ openshift_installer_dir }}/openshift-install"`
- `filetranspile_url: https://raw.githubusercontent.com/ashcrow/filetranspiler/master/filetranspile`
- `filetranspile_binary: "{{ openshift_installer_dir }}/filetranspile"`
- `coreos_iso_output_dir: /var/www/html`

### OpenShift SDN settings
The `openshift_networktype` settings determines which SDN plugin will be used.
This can be either `OpenShiftSDN` (the default if unset), or `OVNKubernetes`.
When using a SDN plugin other than `OpenShiftSDN` default networkpolicies will
include `ipBlock` allows for the `hostCIDR`s of the infra nodes.
From 4.7 onwards you can also set `enable_ipsec: true` when using OVNKubernetes
to enable full ipsec on the SDN transport

```yaml
openshift_servicenetworks:
- 172.30.0.0/16
openshift_clusternetworks:
- cidr: 10.128.0.0/16
  hostPrefix: 23
openshift_networktype: OVNKubernetes
enable_ipsec: true
```

### NFS Dynamic client provisioner defaults
```yaml
nfs_client_provisioner_serviceaccount: nfs-client-provisioner
nfs_client_provisioner_namespace: openshift-nfs-client-provisioner
nfs_client_provisioner_name: nfs-client-provisioner
nfs_client_provisioner_server: FIXME
nfs_client_provisioner_export: /a/path
nfs_client_provisioner_storageclass: managed-nfs-storage
nfs_client_provisioner_make_default: "true"
```

### OpenShift container storage

Component `ocs_storage` takes care of installing OpenShift Container Storage.
It uses the operator to install it and configure to ensure a base setup.
It relies on the component `local_storage` to provide one or more local disks
for OCS to utilize. Due to the workload and segregation of node roles it's
recommended to use dedicated storage nodes for this purpose. These nodes have
to be part of the Ansible inventory group `storage` so they can be addressed.

The following variables have to be set:

```yaml
ocs_storage_operator_channel: stable-4.7
ocs_storage_cluster_disk_count: 1
```

> Choose the right operator [subscription channel](https://access.redhat.com/documentation/en-us/red_hat_openshift_container_storage/4.7/html-single/updating_openshift_container_storage/index#openshift-container-storage-upgrade-channels-and-releases_rhocs) that fit's your cluster.
> _Changing the version will cause the operator to update when available._

> To ensure that the OSDs have a guaranteed size across the nodes, the storage
> size for `storageDeviceSets` must be specified as less than or equal to the
> size of the desired PVs created on the nodes. The disk count is based on the
> formula: `(nodes * disks) / 3`. This means; if you have 3 nodes of which each
> contains 1 local storage disk you will end up with a value of 1. If you have
> 3 nodes with each 2 local disks, the value for the disk count will be 2. Yes
> This does apply when extending storage by adding more disks to the nodes.

Make sure to use the the correct storage class for the `local_storage`
component on each Ansible `host_var` file of the nodes that with contain OCS.

For example:

```yaml
local_storage:
- storageclass: ocs-local-storage
  device: /dev/sdb
- storageclass: ocs-local-storage
  device: /dev/sdc
```

> Do understand that each Ceph OSD pod (disk) requires 5G memory on the node
> it is running on. This will have impact to the sizing of the storage nodes.
> Insufficient resources will end up in a non operational OCS state.

### Prometheus and AlertManager defaults
```yaml
prometheus_storageclass: metrics
prometheus_storage_size: 100Gi
alertmanager_storageclass: metrics
alertmanager_storage_size: 5Gi
```

### Registry storage defaults
```yaml
registry_management_state: Managed
registry_storage_claim_name: "{{ cluster }}-registry-claim"

# Set this one to True if your registry storage can support RWX, thus making
# your regsitry capable of being HA.
registry_storage_supports_rwx: False

# Set the ammount of image registry replica's.
# Part of config in: "oc describe configs.imageregistry.operator.openshift.io"
registry_replicas: 1

# Set the image registry storage type
# Choose one and disable the other. Defaults to use of PVC:
# - "registry_storage_type_pvc" => PVC (Perstent Volume Claim)
# - "registry_storage_type_obc" => OBC (Object Bucket Claim)
registry_storage_type_pvc: true
registry_storage_type_obc: false
```

> When using an Object Bucket Claim, `registry_storage_type_obc: true` AND
> `registry_storage_type_pvc: false`, you should set
> `registry_storage_supports_rwx: true`.

### Logging and ElasticSearch defaults
```yaml
elasticsearch_replicas: 3
elasticsearch_storageclass: logging
elasticsearch_storage_size: 150Gi
elasticsearch_redundancy_policy: SingleRedundancy
elasticsearch_memory_limit: 8Gi
elasticsearch_cpu_request: 200m
elasticsearch_memory_request: 8Gi

kibana_memory_limit: 1Gi
kibana_cpu_request: 500m
kibana_memory_request: 1Gi

curator_memory_limit: 200Mi
curator_memory_request: 200Mi
curator_cpu_request: 200m
curator_schedule: "30 3 * * *"
curator_default_retention_days: 14

fluentd_memory_limit: 1Gi
fluentd_memory_request: 1Gi
fluentd_cpu_request: 200m

# By default audit logs are not sent to the built-in elasticsearch
# Set this one to true to collect audit logs on the cluster itself.
clusterlogging_forward_audit: true
```

### Groupsync Cronjob defaults
```yaml
# valid choices: ipa, ad
groupsync_cronjob_type: ipa
groupsync_cronjob_ldap_user: 'cn=example,OU=example,dc=example,dc=com'
groupsync_cronjob_ldap_password: FIXME
groupsync_ldap_ca_file: /path/to/ca/on/bastion
groupsync_cronjob_ldap_base_dc_groups: "dc=example,dc=com"
groupsync_cronjob_ldap_base_dc_users: "dc=example,dc=com"
groupsync_cronjob_namespace: openshift-ops
groupsync_cronjob_ldap_url: ldap://ldap.example.com:389
groupsync_cronjob_image: image-registry.openshift-image-registry.svc:5000/openshift/cli
groupsync_cronjob_image_version: latest
groupsync_cronjob_cluster_admins_group: openshift-admins
groupsync_groups: []
```

### Custom logos and login pages
```yaml
custom_logo_file: hcs-ocp-logo.svg
custom_background_file: hcs-ocp-background.svg
custom_product_name: HCS OpenShift Container Platform
custom_product_disclaimer_body: ""
custom_product_disclaimer_footer: ""
```

The disclaimer values are empty by default, but can be filled in with company
specific text. This feature should be used for security centric information
provided by the security team. For example:

```yaml
custom_product_disclaimer_body: >
  Access to this system is restricted to authorized users. Unauthorized or
  improper use of this system may result in administrative disciplinary
  action, civil and/or criminal penalties. By continuing to Login, I am
  indicating my awareness of and consent to these terms and conditions of use.
custom_product_disclaimer_footer: Leave this site immediately if you do not agree to these conditions.
```

### Custom console URL

Beside customizing logo's and login pages, it is also possible to customize
the OpenShift Console URL. Just to be clear, this does not replace the existing
URL. It adds and alias route that points to the original console URL.

This setting follows the guide as described in the [docs](https://docs.openshift.com/container-platform/4.7/web_console/customizing-the-web-console.html#customizing-the-web-console-url_customizing-web-console) and [solution](https://access.redhat.com/solutions/5143911),
except for adding a custom certificate. This specific custom certificate job is
taken care of by other components.

Use the below inventory variable to define the URL.

```yaml
custom_console_url: "my_special_console_url.apps.{{ cluster }}.{{ base_domain }}"
```
