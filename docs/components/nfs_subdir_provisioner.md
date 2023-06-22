# Component: NFS SubDir Provisioner

This component is responsible for installing and configuring the out-of-tree NFS SubDir Provisioner. This provisioner creates a storageClass with dynamic provisioning by creating sub-directories on an existing NFS share.

## Part Of
- Component: `nfs_subdir_provisioner`
- Tags: `nfs_subdir_provisioner`
- Application: `nfs_subdir_provisioner`

# Index

<!-- vim-markdown-toc GFM -->

* [Warning](#warning)
* [NFS SubDir Provisioner Configuration](#nfs-subdir-provisioner-configuration)
  * [Example NFS SubDir Provisioner Configuration](#example-nfs-subdir-provisioner-configuration)

<!-- vim-markdown-toc -->

# Warning

This component should **never** be used for production data, since it provides not a single form of authentication or encryption on the storage. It is very easy to gain access to the data stored on any PhysicalVolume created by this provisioner.

# NFS SubDir Provisioner Configuration

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `nfs_subdir_provisioner_server` | **Required** | The hostname or IP address of the external NFS server hosting the root volume. |
| `nfs_subdir_provisioner_export` | **Required** | The export path of the root volume on `nfs_subdir_provisioner_server`. |

## Example NFS SubDir Provisioner Configuration
```yaml
nfs_subdir_provisioner_server: nfs.example.com
nfs_subdir_provisioner_export: /exports/openshift
```
