# Index
<!-- vim-markdown-toc GFM -->

* [Cluster Wide Installation Options](#cluster-wide-installation-options)
    * [Cluster Name](#cluster-name)
    * [Bastion Options](#bastion-options)
        * [Defining Your Bastion Host](#defining-your-bastion-host)
        * [Bastion Host Examples](#bastion-host-examples)
    * [Installation Version](#installation-version)
    * [Pull Secret](#pull-secret)
    * [Node SSH Access](#node-ssh-access)
    * [Auxiliary Services](#auxiliary-services)
    * [OpenShift Networking](#openshift-networking)
    * [Automagic Loadbalancer for API and Ingress](#automagic-loadbalancer-for-api-and-ingress)
    * [Customizing Default Manifests](#customizing-default-manifests)
* [Per Machine Installation Options](#per-machine-installation-options)
    * [Installation Method](#installation-method)
    * [Node Network Configuration](#node-network-configuration)
            * [LibVirt Example](#libvirt-example)
            * [VMWare Example](#vmware-example)
            * [Bonding Example with VLAN](#bonding-example-with-vlan)
    * [LibVirt Specific Settings](#libvirt-specific-settings)
        * [LibVirt Example](#libvirt-example-1)
    * [VMWare Specific Settings](#vmware-specific-settings)
        * [VMWare CSI integration](#vmware-csi-integration)
        * [Configuring VMWare Vcenters](#configuring-vmware-vcenters)
        * [A Note on Datastores](#a-note-on-datastores)
            * [VMWare VCenters Configuration Example](#vmware-vcenters-configuration-example)
        * [VMWare  Example](#vmware--example)
    * [HP ILO Specific Settings](#hp-ilo-specific-settings)
        * [HP ILO Example](#hp-ilo-example)
    * [Extra Node Labels](#extra-node-labels)

<!-- vim-markdown-toc -->
# Cluster Wide Installation Options

A number of options are used during the installation that affect the entire
cluster. It is recommended you configure these in your inventory `all` group,
or a parent group of your `master`, `infra`, `worker`, and `storage` groups.

## Cluster Name

Your cluster will need a name. This name is used for directory names on your bastion host, as well as in the generation of hostnames and URIs for various cluster components. This setting does **not** have a default, and must be set in your inventory at a level where all hosts, including the bastion, will see the _same_ value.

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `cluster` | **Required** | The name for our cluster, used in directories on the bastion host as well as in URIs. |
| `base_domain` | **Required** | The base DNS domain name for your cluster. The API Server will be available at `api.{{ cluster }}.{{ base_domain }}`, and applications at `*.apps.{{ cluster }}.{{ base_domain }}` |

**N.B.** Ensure that the DNS names reference in the preceding table are available on your network and point to the correct IP addresses or load-balancers.
1. It's not DNS
2. It can't be DNS
3. ???
4. It was DNS

## Bastion Options

### Defining Your Bastion Host

The `openshift_install.yml` playbook assumes that you are using a bastion host
to connect to your OpenShift cluster, virtualization nodes, ILO cards, etc. You
can configure which host this is with the `bastion_host` setting. If you want
this to be the same host as from which you run the playbook itself set this
variable to `localhost`.

You can also define some file locations on your bastion host, these default to directories underneath `/opt/openshift_files/{{ cluster }}

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `bastion_host` | **Required** | The machine to use as bastion. This host **must** exist in your Ansible inventory |
| `bastion_external_hostname` | Optional | The name that your nodes should use to download materials from the bastion. Only needed when that hostname/ip is different from your `bastion_host` setting. |
| `installer_tmpdir` | Optional | In case Ansible tmp directory (/tmp) is not large enough for creating iso's. The installer needs ~1 GB temp diskspace per node. `installer_tmpdir: /opt/openshift_files/tmp`
| `openshift_ignition_dir` | Optional | The directory on the bastion host where ignition and authentication files will be stored. Defaults to `/opt/openshift_files/{{ cluster }}/ignition`. **N.B.** Make sure you backup this directory after a successful installation, as it holds your `kubeadmin` and `system:admin` credentials, as well as the `kubeconfig` used by the configuration and Day 2 playbooks. |
| `openshift_installer_dir` | Optional | The directory where installer files and clients will be downloaded to. Default to `/opt/openshift_files/{{ cluster }}/installer` |

### Bastion Host Examples

Bastion is localhost:
```yaml
bastion_host: localhost
```

bastion is external:
```yaml
bastion_host: bastion.example.com
```

## Installation Version

These playbooks support installing multiple version of OpenShift. When newer
version are added older versions are removed. The playbooks also support
setting a specific revision version.

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `install_flavour` | Optional | The flavor to install. Can be `ocp`(Default), or `okd`(Currently Unmaintained, feel free to step up) |
| `install_version` | **Required** | The version to install. Can be major.minor version, like `"4.11"`, or a specific revision like `"4.11.5"`. When using only major.minor the most recent stable incremental version will be used. **N.B.** Make sure to quote your version, ansible might treat it like a number instead of a string otherwise, causing some weird errors down the line. |

## Pull Secret

OpenShift needs a "Pull Secret" to access OpenShift content in the upstream registries. You can obtain a Pull Secret by visiting [http://cloud.redhat.com](https://cloud.redhat.com)
| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `openshift_pullsecret` | **Required** | The contents of a pull secret that can access OpenShift content on the upstream registries. |
| `disable_remote_health`| Optional | Disables remote health reporting of the cluster if so required. Defaults to `false`. |

## Node SSH Access

During installation a SSH Public Key is added to the `core` user on all nodes. This key can later be changed using a MachineConfig.

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `openshift_coreos_sshpubkey` | **Required** | The content of a SSH Public Key that should be added to the `authorized_keys` for the `core` user on all nodes. |

## Auxiliary Services

In most environments you have to deal with external services, like a company
wide Certificate Authority (CA), or proxy servers to reach the outside world.
You can use the following options to configure these:

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `custom_ca_file` | Optional | A file path (on your bastion host) containing a list of additional Certificate Authorities (in PEM format) that should be added to the cluster trust store. These CAs will be trusted by the cluster, but not automatically by additional applications you deploy on your cluster. |
| `http_proxy` | Optional | The URL, including protocol and port, of an optional proxy server to use for http requests. Automatically honored by most cluster components, not by extra applications you deploy yourself. |
| `https_proxy` | Optional | The URL, including protocol and port, of an optional proxy server to use for https requests. Automatically honored by most cluster components, not by extra applications you deploy yourself. |
| `no_proxy` | Optional | A list of URL patterns, host names, IP addresses, and IP ranges that should not be sent to the proxy. Your cluster networks and local cluster service names are automatically added to this list. Honored by most cluster components, but not by additional applications you deploy yourself. |

## OpenShift Networking

During installation you can set some options for the internal OpenShift networks. Most of these options can **not** be changed after installation.

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `openshift_networktype` | Optional | The OpenShift SDN provider. Valid values: `OpenShiftSDN`(Default) and `OVNKubernetes` |
| `openshift_servicenetworks` | Optional | A list of CIDRs that can be used for the internal service network. Kubernetes Service objects will receive an IP from these ranges. Defaults to:<br/>`- 172.30.0.0/16`
| `openshift_clusternetworks` | Optional | A list of CIDRs from which to assign IPs to pods, including a `hostPrefix` that determines how different nodes will assign these IPs. Defaults to:<br/>`- cidr: 10.128.0.0/16`<br/>`  hostPrefix: 23` |
| `enable_ipsec` | Optional | Whether or not to enable IPSec on the SDN layer. Can only be enabled with `openshift_networktype: OVNKubernetes`, defaults to `False` |
| `disable_multus` | Optional | Whether or not to disable the Multus component in the networking stack. Disabling Multus can speed up pod creation and cluster updates, but can not be enabled later if you need it. Defaults to `False` |
| `ovnkubernetes_mtu` | Optional | The MTU to set for the OVNKubernetes SDN, defaults to `1400` |
| `ovnkubernetes_geneveport` | Optional | The port to use for the OVNKubernetes SDN, defaults to `6081` |


## Automagic Loadbalancer for API and Ingress

OpenShift is capable of self-hosting load-balancers/keepalived for both the API
and Ingress. During some forms of IPI deployments this is configured
automatically, but these playbooks can fake those conditions as well.

**N.B.** This configuration is **NOT** supported by Red Hat in this manner, if
it breaks you get to keep both pieces.

**N.B.** Defining an Ingress VIP is not compatible with hosting multiple Ingress controllers, e.g. router-sharding. Do **NOT** use this if you plan on running multiple routers, but use an external load-balancer instead.

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `api_vip` | Optional | The floating IP address to use for the API load-balancer. |
| `ingress_vip` | Optional | The floating IP address to use for the Ingress load-balancer |

## Customizing Default Manifests

These playbooks allow you to directly modify the main manifests generated by the OpenShift installer. Normally this should not be necessary.

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `openshift_manifest_customizations` | Optional | A list of `file`, `regexp`, and `line` attributes that are passed to the `lineinfile` ansible modules. Defaults to:<br/>`- file: cluster-scheduler-02-config.yml`<br/>`  regexp: '^  mastersSchedulable:'`<br/>`  line: '  mastersSchedulable: false'` |


# Per Machine Installation Options

A number of options can be specified _per_ machine. A template is available is
in the [`host_vars/template`](../hosts-example/host_vars/template/main.yml) file.

## Installation Method

- `install_method` (**required**)
  The installation method to use, choose one of
  - `grub`

    This method connects to existing hosts, and updates the bootloader
    configuration to boot into the installer image.
  - `ilo`

    This method connects to an HP ILO card, and either attaches a temporary boot image
    to start the installer from, or it configures a network card to do a
    UEFI Boot from URL to fetch a boot image from a webserver/bastion.

  - `libvirt`

    This method boots a **new** virtual machine straight into the installer
    kernel and initial ramfs.
  - `vmware`

    This methods boots a VMWare virtual machine into a custom boot iso to start the installer.

    **Warning:** It will automatically delete any previous instances of the same machine.

  - `iso`

    This method only creates a bootable ISO file for the selected machines, containing
    network configuration, basic ignition file, and more. Simply booting a machine from this
    image should be enough to install a machine, if no other installation options are available.

    The installation playbook will pause, waiting for you to manually boot these machines.

  Example: `install_method: libvirt`

- `install_dev` (**required**)
  The primary disk to install on, **without** `/dev/`.

  Example: `install_dev: sda`

- `additional_kernel_args`
  In case a node needs additional kernel arguments.

  Example: `additional_kernel_args: rd.net.timeout.carrier=15`

## Node Network Configuration

- `network_config` (**required**)
  A _list_ of network devices to configure on the nodes. Some sub-options are
  specific to the `libvirt` and `vmware` installation methods.
  | Option | Required / Optional | Comments |
  |--------|---------------------|----------|
  | `device` | **Required** | The name of the network interface to use. On bare-metal this depends on your hardware, on LibVirt you typically start with `enp1s0`, on VMWare you typically start with `ens192`. |
  | `vlan` | Optional | A vlanId to use for the desired interface. |
  | `mac` | Optional | (LibVirt only) The MAC address for the specified interface |
  | `address` | **Required** | The IP address for this interface |
  | `netmask` | **Required** | The netmask for this interface |
  | `gateway` | Optional | The default gateway, reachable by this interface |
  | `is_default_gateway` | Optional | If this interface's default gateway should be the system default gateway. Do **NOT** specify this as `true` on more than one interface per machine. |
  | `dns` | Optional | A _list_ of nameservers to use. While optional, things will most likely break if you machines do not have at least one nameserver configured |
  | `create_nmconnection_files` | Optional | Set this option to `True` to include generated NetworkManager configuration files in your ignition. Typically **not** needed, except in some weird cases. |
  | **LibVirt only** |
  | `bridge` | **Required** | The bridge/virtual network to create the interface on |
  | **VMWare only** |
  | `vmware_net` | **Required** | The virtual network to create the interface on |
  | **Bonding** |
  | `slaves` | Optional | You can enable network bonding by setting this option. The format is a list of `device: <devicename>` (**required**), `mac: <MAC address>` (Optional)(LibVirt only), and `bridge: <libvirt_bridge>` (Optional, LibVirt only)
  | `bonding_opts` | Optional | The bonding options to use for this bond (as a list). By default the following options will be used:<br/>`- "mode=802.3ad"`<br/>`- "lacp_rate=0"`<br/>`- "miimon=100"`<br/>`- "updelay=1000"`<br/>`- "downdelay=1000"` |
  | **iLO Boot_from_url only** |
  | `nicboot` | Optional | Interface name of the nic to boot from with UEFI Boot from URL. Example: NicBoot1 |
  | `initial_boot_from_network` | Optional | If this interface's ip configuration is used to configure network config for UEFI Pre Boot Environment |

#### LibVirt Example
  ```yaml
  network_config:
  - device: enp1s0
    mac: "52:54:00:00:01:20"
    address: 10.1.0.20
    netmask: 255.255.255.0
    gateway: 10.1.0.1
    is_default_gateway: True
    dns:
    - 10.1.0.10
    bridge: br1
  ```

#### VMWare Example
  ```yaml
  network_config:
  - device: ens192
    address: 10.1.0.20
    netmask: 255.255.255.0
    gateway: 10.1.0.1
    is_default_gateway: True
    dns:
    - 10.1.0.10
    - 10.1.0.11
    vmware_net: OCPNet
  ```

#### Bonding Example with VLAN
  ```yaml
  network_config:
  - device: bond0
    vlan: 132
    slaves:
    - device: en1ps0
    - device: en2ps0
    bonding_opts:
    - "mode=802.3ad"
    - "lacp_rate=0"
    - "miimon=100"
    - "updelay=500"
    - "downdelay=500"
    address: 10.1.0.20
    netmask: 255.255.255.0
    gateway: 10.1.0.1
    is_default_gateway: True
    dns:
    - 10.1.0.10
    - 10.1.0.11
  - device: eno1
    address: 10.2.0.10
    netmask: 255.255.255.0
    gateway: 10.2.0.1
    nicboot: NicBoot1
    initial_boot_from_network: True
  ```

## LibVirt Specific Settings

Some machine specific settings are only relevant for LibVirt installations:

| Option | Required / Optional | Comments |
|--------|---------------------|----------|
| `extra_disks` | Optional | A list of extra disks to create and assign to the machine. Each entry should have a `name` and a `size` in a format supported by `qemu-img`. For example:<br/>`extra_disks:`<br/>`- name: odf`<br/>`  size: 200G`
| `image_size` | **Required** | The (virtual) size of the primary disk, specified in a format that `qemu-img` likes, for example: `200G` |
| `virt_host` | **Required** | The hostname of the hypervisor on which to create this machine. The hypervisor must be known in the Ansible inventory, and Ansible should be able to connect to that machine with full sudo privileges. |
| `virt_memory` | **Required** | The amount of memory in Mebibytes to allocate to this VM. |
| `virt_vcpus` | **Required** | The number of vCPUs to allocate to this machine |

### LibVirt Example
```yaml
master01.example.com:
  network_config:
  - device: enp1s0
    mac: "52:54:00:00:01:20"
    address: 10.1.0.20
    netmask: 255.255.255.0
    gateway: 10.1.0.1
    is_default_gateway: True
    dns:
    - 10.1.0.10
    - 10.1.0.11
    bridge: br1
  image_size: 120G
  virt_host: vmhost03.example.com
  virt_memory: 32768
  virt_vcpus: 8
  extra_node_labels:
    "topology.kubernetes.io/region": amersfoort
    "topology.kubernetes.io/zone": dc1
```

## VMWare Specific Settings

Some machine specific settings are only relevant to machines on VMWare. This machines should have a `vmware` variable with the following children:

| Option | Required / Optional | Comments |
|--------|---------------------|----------|
| `extra_disks` | Optional | A list of extra disks to create and assign to the machine. Each entry should have a `size_gb` and optionally a `datastore` and/or a `type` setting. You can also add any other options allowed by the `vmware_guest` Ansible module. For example:<br/>`extra_disks:`<br/>`- size_gb: 200`<br/>`  datastore: MyDataStore`<br/>`  type: thick`<br/>`    scsi_controller: 0`<br/>`  unit_number: 2`<br/>Note: `scsi_controller` and `unit_number` are temporarily mandatory due to a defect in the [vmware_guest module](https://github.com/ansible-collections/community.vmware/issues/931). Increase unit_number for each extra disk (starting from 2)
| `vcenter` | **Required** | The name of the VMWare VCenter to use, as defined in [the section on configuring your vcenters](#configuring-vmware-vcenters) |
| `memory`| **Required** | Amount of memory in Mebibytes |
| `vcpu`| **Required** | Number of vCPUs to assign |
| `disk` | **Required** | Primary disk size, in GiB |
| `folder` | **Required** | Folder to create the machine in |
| `guest_id` | **Required** | VMware machine type, e.g. `rhel7_64Guest` |
| `hardware_version` | **Required** | VMWare hardware revision to use, e.g. `13` |
| `boot_firmware` | **Optional** | VMWare bios boot option `bios` or `efi`, default is `bios` |
| `customvalues` | Optional | DEPRECATED: A list of `key` and `value` pairs to assign to the VMWare custom values, for example:<br/>`- key: "disk.EnableUUID"`<br/>`  value: "true"`
| `advanced_settings` | Optional | A list of `key` and `value` pairs to assign to the VMWare advanced settings, for example:<br/>`- key: "disk.EnableUUID"`<br/>`  value: "TRUE"`
| `datastore` | Optional | If defined this will override the VMWare Datastore for the primary disk from the `vcenter` setting. |

Furthermore two optional variables can be set directly on your machines:
| Option | Required / Optional | Comments |
|--------|---------------------|----------|
| `vmware_vm_name_notation` | Optional | The name you want for this machine in the VMWare console. This defaults to an all uppercase version of the short hostname, for example the hostname `node01.example.com` would become `NODE01`. |
| `install_dev_type` | Optional | How to allocate the primary disk for this machine. By default VMWare thin provisioning will be used, but you can set this to `thin`(default), `thick`, or `eagerzeroedthick`.

### VMWare CSI integration

During install some paltform options can be set that enable VMWare Storage integration using CSI drivers. This will use the VMWare settings for your `bastion_host`. To enable this set the `vmware_csi` variable to anything.

| Option | Required / Optional | Comments |
|--------|---------------------|----------|
| `vmware_csi` | Optional | Set to anything to enable VMWare CSI storage integration |

### Configuring VMWare Vcenters

In order to speak to VMWare Ansible the playbooks should know about your
VCenters on which you wish to deploy. These should probably be configured for
your `all` group, or at least in such a way that they exist for all the
machines you wish to deploy. They should be configured as children of the `vcenters` variable, with the following options:

| Option | Required / Optional | Comments |
|--------|---------------------|----------|
| `hostname` | **Required** | The management hostname of your VCenter. |
| `username` | **Required** | The username to use when connecting |
| `password` | **Required** | The password to use when connecting. It is recommended to not put this one directly in your inventory, but to use a vault or other secure way of password lookup. |
| `datacenter` | **Required** |  The datacenter to create the machine on |
| `datastore` | Optional | The datastore for the machine image |
| `iso_datastore` | **Required** | The datastore for the temporary boot ISO image |
| `cluster` | **Required** | The cluster to create the machine on |
| `copy_timeout` | Optional | The timeout in seconds for the upload to the datastore |

### A Note on Datastores
The datastore for the primary disk can be selected using either the
machine-specific `vmware.datastore` option, or by the `datastore` option in the
specified VCenter. If both are set the machine-specific setting takes
precedence.

If **neither** is set these playbooks will automatically enable the
`autoselect_datastore` option in the `vmware_guest` Ansible module. For disk
specified in `extra_disks` this can be done manually in your inventory.

#### VMWare VCenters Configuration Example
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
```
### VMWare  Example
```yaml
master01.example.com:
  network_config:
  - device: enp1s0
    mac: "52:54:00:00:01:20"
    address: 10.1.0.20
    netmask: 255.255.255.0
    gateway: 10.1.0.1
    is_default_gateway: True
    dns:
    - 10.1.0.10
    - 10.1.0.11
    bridge: br1
  image_size: 120G
  vmware:
    vcenter: dcr1
    template: OCP4-Template
    memory: 32768
    vcpu: 8
    disk: 120
    folder: OpenShift
    guest_id: rhel7_64Guest
    hardware_version: 13
    boot_firmware: bios
    customvalues:
    - key: "disk.EnableUUID"
      value: "true"
  vmware_vm_name_notation: "{{ inventory_hostname_short }}"
  install_dev_type: eagerzeroedthick
  extra_node_labels:
    "topology.kubernetes.io/region": amersfoort
    "topology.kubernetes.io/zone": dc1
```

## HP ILO Specific Settings
In order to connect to HP ILO management cards the following options will need
to be set for a machine, along with `install_method: ilo`:

| Option | Required/Optional | Comment |
|--------|-------------------|---------|
| `ilo_user` | **Required** | The ILO username to use |
| `ilo_password` | **Required** | The password for the ILO user. It is recommended to store this setting in a vault, or another external secret management tool. |
| `ilo_address` | **Required** | The hostname or IP address of the ILO management card for this machine. |
| `ilo_version` | Optional | The version of ILO that's being used. Currently ILO 4 and 5 are supported. Default(4). |
| `ilo_use_proxy` | Optional | Follow http_proxy, https_proxy and no_proxy settings to connect to an iLO interface. A 'no' explicitly adds ilo_address to no_proxy. Default(yes) |
| `ilo_boot_from_url` | Optional | no = iLO boot from virtual cdrom. yes = Boot from URL. Default(no) |


### HP ILO Example
```yaml
master01.example.com:
  install_method: ilo
  ilo_user: Administrator
  ilo_password: swordfish
  ilo_version: 5
  ilo_address: 10.1.0.201
  ilo_use_proxy: yes
  ilo_boot_from_url: no
```

## Extra Node Labels

It is possible to assign extra node labels directly during the install. This
can for example be useful to set Kubernetes topology labels. You can specify
these label per node with the `extra_node_labels` variable. This variable is a
dictionary of `<label>: <value>` pairs, for example:

```yaml
extra_node_labels:
  "topology.kubernetes.io/region": amersfoort
  "topology.kubernetes.io/zone": dc1
```
It is **not** necessary to set `node-role.kubernetes.io/<role>: ''` labels for the following roles:
- master
- worker
- infra
- storage

These are set automatically by the installation playbooks based on the group
memberships of your machines.

**N.B.** Remember to quote labels with periods and slashes.
