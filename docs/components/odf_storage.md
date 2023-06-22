# Component: API Server

This component installs OpenShift Data Foundation. It is recommended that you
have at least **three** nodes, with 16 vCPUs and 32GiB of memory, in your
`storage` group in your Ansible inventory.

This component does a simple configuration. For a more advanced configuration
please edit the manifests in Git before applying to your cluster.


## Part Of
- Component: `odf_storage`
- Tags: `odf_storage`
- Application: `odf_storage`

# Index

<!-- vim-markdown-toc GFM -->

* [Warning](#warning)
    * [Block vs Filesystem](#block-vs-filesystem)
* [OpenShift Data Foundation Variables](#openshift-data-foundation-variables)

<!-- vim-markdown-toc -->

# Warning

This component automatically adds all (extra) disks and paritions of at least
10Gi on your Storage nodes into a LocalVolumeSet called `odf-local_storage`,
which is then used by the OpenShift Data Foundation to add backing storage to
ODF. This requires that you also install the `local_storage` component. Install
this component without the `local_storage` component will result in a
non-functioning setup until then `local_storage` component is added.

This component does not touch exiting LocalVolumes, so you could create
PhysicalVolumes beforehand and add them to the `odf-local-storage`
StorageClass. Remember that these volumes should of the volumeMode `Block`, and
**not** of the volumeMode `Filesystem`.

## Block vs Filesystem

There is sometimes some confusion over Block Storage vs Filesystem storage. Traditionally we have called things like iSCSI volumes and FC "Block Storage", and things like NFS File storage. While  technically true, Kubernetes has some ideas of its own. While things like iSCSI are provided to your nodes as Block storage, Kubernetes typically creates a filesystem on those devices before presenting them to your pods. This is called `volumeMode: Filesystem`. What the ODF operator wants is raw block devices, like `/dev/vdb`, `/dev/sdc3`, or an LVM Logical Volume. These are created by setting `volumeMode: Block` on a PhysicalVolume.

**TL;DR** Do not create your backing stores for ODF using the `local_storage`
inventory variable. Just create `extra_disks` for your machines (or make sure
those disks are already there for the `ilo` and `grub` `install_method`, and
let this component find them automatically.

# OpenShift Data Foundation Variables

You can configure this component using these variables:

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `odf_storage_operator_channel` | Optional | The Operator channel to use, defaults to `stable-{{ install_version }}`<br/>If you are using an `install_version` with an incremental revision, like `4.9.9` you **must** set this. |
| `odf_storage_cluster_disk_count` | Optional | The number of available disks per storage node. For safety this defaults to `1` if not set. |
| `odf_prefix` | Optional | For backwards compatibility with OCS labeled storage objects. Default value is 'odf'. |
| `odf_replica` | Optional | The number of storage replicas when you add more than 3 storage nodes. Defaults to `3` if not set. |

Clusters with OCS that have been upgraded to ODF still use ocs-* labeled storage system, storage class and local devicesets. With `odf_prefix` is it possible to keep using ocs-* names on existing clusters where openshift installer is introduced.
