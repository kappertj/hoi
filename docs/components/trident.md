# Component: Trident

This component is responsible for installing and configuring the NetApp Trident
Operator. Once installed it creates and configure TridentBackendConfig and
Storageclass objects.

## Part Of
- Component: `trident`
- Tags: `trident`
- Application: `trident`

# Index

<!-- vim-markdown-toc GFM -->

* [Configuration Variables](#configuration-variables)
  * [Configuring Backends](#configuring-backends)
  * [Trident Example Configuration](#trident-example-configuration)

<!-- vim-markdown-toc -->

# Configuration Variables


| Option | Required/Optional | Comments |
|--------|-------------------|----------|
|`trident_version`| Optional | Defaults to `22.07.0` if unset |
|`trident_operator_download_url`| Optional | Defaults to `https://github.com/NetApp/trident/releases/download/v{{ trident_version }}/trident-installer-{{trident_version}}.tar.gz` if unset |
|`trident_backends` | Optional | Defaults to an empty dict if unset, see 

## Configuring Backends

Backends (and their associated storageclasses) are created using the `trident_backends` variable. This variable consists of a list with entries containing the following keys:

| Key | Required/Optional | Comments |
|-----|-------------------|----------|
| `name`| **Required** | The name for this backend/storageclass. It is used when creating the names for the different objects. |
| `data` | **Required** | An object detailing the settings for this backend. See [the upstream documentation](https://docs.netapp.com/us-en/trident/trident-use/backend-kubectl.html#tridentbackendconfig) for details |
| `storageclass` | Optional | Extra options for the storageclass. This can include a key called `name` with an optional name for the storageclass, and a dictionary called `parameters` with extra key-value pairs to be added to the `parameters:` section of the desired Storageclass. |
| `credentials` | **Required** | A dictionary containing two keys, `username` and `password`, that will be stored in a credentials secret for this backend. |


##  Trident Example Configuration
```yaml
trident_backends:
- name: ontap-nas
  data:
    version: 1
    storageDriverName: ontap-nas
    managementLIF: 10.0.0.1
    dataLIF: 10.0.0.2
    backendName: ontap-nas
    svm: trident_svm
    limitAggregateUsage: 80%
    limitVolumeSize: 50Gi
    nfsMountOptions: nfsvers=4
    defaults:
      spaceReserve: volume
      exportPolicy: myk8scluster
      snapshotPolicy: default
      snapshotReserve: '10'
    deletionPolicy: retain
  storageclass:
    parameters:
      media: "ssd"
      provisioningType: "thin"
  credentials:
    username: foo
    password: bar
- name: second_example
  data:
    version: 1
    storageDriverName: ontap-nas-economy
    managementLIF: 10.0.0.1
    dataLIF: 10.0.0.2
    backendName: example1
    svm: trident_svm
    limitAggregateUsage: 80%
    limitVolumeSize: 50Gi
    nfsMountOptions: nfsvers=4
    defaults:
      spaceReserve: volume
      exportPolicy: myk8scluster
      snapshotPolicy: default
      snapshotReserve: '10'
    deletionPolicy: retain
  storageclass:
    name: useme
    parameters:
      media: "ssd"
      provisioningType: "thin"
  credentials:
    username: foo
    password: bar
```
