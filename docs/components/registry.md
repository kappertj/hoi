# Component: Registry

This component is responsible for configuring the internal image registry used by the cluster.

You can configure the OpenShift internal registry to have persistent storage.
In the cases where you  want to use the internal registry having persistent
storage is generally thought of as a good idea, since nobody wants to re-run
all their builds every single time the registry pod restarts.

Having persistent storage underneath the registry also allows the registry to
run in HA mode, as long as the underlying PhysicalVolumeClaim supports
ReadWriteMany(rwx) mode.

When your storage supports ReadWriteMany, and there are Infra nodes available,
this component automatically configures the registry to run on Infra nodes
only, with as many replicas as there are Infra nodes.

## Part Of
- Component: `registry`
- Tags: `registry`
- Application: `registry`

# Index

<!-- vim-markdown-toc GFM -->

* [Registry Variables](#registry-variables)
  * [Registry Configuration Example](#registry-configuration-example)
* [Enhancement Ideas](#enhancement-ideas)

<!-- vim-markdown-toc -->

# Registry Variables


You can set

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `registry_storage_claim_name` | Optional | The name of the PersistentVolumeClaim to configure for registry storage. If not set the name `{{ cluster }}-registry-claim` is used. |
| `registry_storage_claim_storageclass` | Optional | The StorageClass to use for the PVC. If not set the default storageclass will be used. |
| `registry_storage_claim_size` | Optional | The size to use for the PVC. If not set it defaults to `100Gi` |
| `registry_storage_supports_rwx` | Optional | Whether or not your storage claim can be mounted by multiple nodes simultaneously (ReadWriteMany), defaults to `False`. If your storage does not support ReadWriteMany mode the registry is limited to a single pod, without HA. |

## Registry Configuration Example
```yaml
registry_storage_claim_storageclass: odf-storagecluster-cephfs
registry_storage_claim_size: 250Gi
registry_storage_supports_rwx: True
```

# Enhancement Ideas

Having the registry use an S3 bucket from OpenShift Data Foundation would be
really nice. Unfortunately the current implementation makes it almost
impossible to talk directly to the S# service using TLS without some dirty
registry hacking, and using an external route causes unnecessary overhead on
the IngressControllers. If you have a good idea feel free to raise an issue
with your solution, or file a Pull Request.
