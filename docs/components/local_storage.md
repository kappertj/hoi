# Component: Local Storage Operator

This component is responsible for installing and configuring the Local Storage
Operator. The Local Storage Operator can create PhysicalVolumes out of local
disks and partitions on your nodes. Using these PhysicalVolumes will provide an
implicit nodeSelector to the pods that use them, since these volumes are only
available to pods running on the node that has the actual disk backing the
Physical Volume.

A good use for these volumes is backing the persistent storage for the
OpenShift Logging stack and the OpenShift Monitoring stack.

## Part Of
- Component: `local_storage`
- Tags: `local_storage`
- Application: `local_storage`

# Index

<!-- vim-markdown-toc GFM -->

* [Local Storage Variables](#local-storage-variables)
  * [Example Local Storage Configuration](#example-local-storage-configuration)
* [Local Storage and OpenShift Data Foundation](#local-storage-and-openshift-data-foundation)

<!-- vim-markdown-toc -->

# Local Storage Variables

This playbook creates LocalVolume objects based on the content of the `local_storage` variable set for each host. This variable takes a list of objects using the following spec:

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `device` | **Required** | The full devicenode path on the node to use a backingstore, e.g. `/dev/vdb`  |
| `storageclass` | **Required** | The storageclass to which to assign this PhysicalVolume, if it does not exist it will be created for you. |

## Example Local Storage Configuration

```yaml
all:
ocp:
  children:
    infra:
      hosts:
        infra01.example.com:
          local_storage:
          - device: "/dev/vdb"
            storageclass: logging
          - device: "/dev/vdc"
            storageclass: metrics
```

# Local Storage and OpenShift Data Foundation

Physical Volumes created by the Local Storage Operator seem like a great fit
for the volumes needed by OpenShift Data Foundation, and indeed, that can be
done. In fact, it can be done so well that the `odf-storage` component does
exactly that. **BUT**, OpenShift Data Foundation want volumes of the `block`
type, and this component is only configured to provide volumes of the
`filesystem` type. **DO NOT** create the volumes for OpenShift Data
Foundation using this component,, but use the configuration options as
described in the [docs for the `odf_storage` component](odf_storage.md)
