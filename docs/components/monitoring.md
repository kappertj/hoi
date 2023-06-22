# Component: Monitoring

This component is responsible for configuring the OpenShift Monitoring stack.

Currently three sub-components can be configured
- Cluster Monitoring
- User Workload Monitoring
- AlertManager

## Part Of
- Component: `monitoring`
- Tags: `monitoring`
- Application: `monitoring`

# Index

<!-- vim-markdown-toc GFM -->

* [Configuring Monitoring](#configuring-monitoring)
  * [Cluster Monitoring Configuration Options](#cluster-monitoring-configuration-options)
  * [User Workload Monitoring Configuration Options](#user-workload-monitoring-configuration-options)
  * [AlertManager Monitoring Configuration Options](#alertmanager-monitoring-configuration-options)
    * [AlertManager Configuration example](#alertmanager-configuration-example)
  * [Moving Monitoring Components to Infra Nodes](#moving-monitoring-components-to-infra-nodes)

<!-- vim-markdown-toc -->

# Configuring Monitoring

## Cluster Monitoring Configuration Options

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `prometheus_retention` | Optional | The time to keep metrics. Defaults to `15d` |
| `prometheus_storageclass` | Optional | The StorageClass to use for persistent storage for Prometheus. if unset no persistent storage will be configured and old metrics will be lost on pod restarts. |
| `prometheus_storage_size` | Optional | The size to use for persistent volumes for Prometheus. if unset no persistent storage will be configured and old metrics will be lost on pod restarts. |

## User Workload Monitoring Configuration Options

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `monitoring_user_workload_enabled` | Optional | Whether or not to enable User Workload Monitoring, default to `False` |
| `prometheus_user_retention` | Optional | The time to keep metrics. Defaults to `15d` |
| `prometheus_user_storageclass` | Optional | The StorageClass to use for persistent storage for Prometheus. if unset no persistent storage will be configured and old metrics will be lost on pod restarts. |
| `prometheus_user_storage_size` | Optional | The size to use for persistent volumes for Prometheus. if unset no persistent storage will be configured and old metrics will be lost on pod restarts. |

## AlertManager Monitoring Configuration Options

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `alertmanager_storageclass` | Optional | The StorageClass to use for AlertManager persistent storage. If not defined AlertManager will run on **non-persistent** EmptyDir volumes. |
| `alertmanager_storage_size` | Optional | The StorageClass to use for AlertManager persistent storage. If not defined AlertManager will run on **non-persistent** EmptyDir volumes. |
| `alertmanager_config` | Optional | A complete AlertManager config. If not defined no AlertManager configuration will be applied. |

### AlertManager Configuration example
```yaml
alertmanager_storageclass: odf-storagecluster-cephfs
alertmanager_storage_size: 5Gi
alertmanager_config:
  global:
    resolve_timeout: 5m
  route:
    group_wait: 30s
    group_interval: 5m
    repeat_interval: 12h
    receiver: default
    routes:
    - match:
        alertname: Watchdog
      repeat_interval: 5m
      receiver: watchdog
  receivers:
  - name: default
    webhook_configs:
    - url: https://alerting.example.com/myorg/mytoken
      send_resolved: true
  - name: watchdog
```

## Moving Monitoring Components to Infra Nodes

If you have at least two nodes in your `infra` group in Ansible all components
will be automatically configured to run on your Infra nodes where possible.
