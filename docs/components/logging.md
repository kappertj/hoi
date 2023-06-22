# Component: Logging

This component is responsible for installing and configuring the OpenShift Logging stack.
You can choose between isntalling the (default) Elastic stack, or the new-fangled Loki stack.

## Part Of
- Component: `logging`
- Tags: `logging`
- Application: `logging`

# Index

<!-- vim-markdown-toc GFM -->

* [Logging Variables](#logging-variables)
    * [Logging Stack Choice](#logging-stack-choice)
    * [ElasticSearch Options](#elasticsearch-options)
        * [Data Retention Options](#data-retention-options)
        * [Storage and Redundancy](#storage-and-redundancy)
        * [Memory and CPU Settings](#memory-and-cpu-settings)
    * [Loki Options](#loki-options)
        * [S3 settings](#s3-settings)
    * [Moving Logging Components to Infra Nodes](#moving-logging-components-to-infra-nodes)

<!-- vim-markdown-toc -->

# Logging Variables

While just enabling this component will install and configure the OpenShift
Logging stack, there are a lot of settings you can fine-tune for your cluster:

## Logging Stack Choice

You can select your desired logging stack using the following variable:

| Option | Required/Optional | Defaults | Comments |
|--------|-------------------|----------|----------|
| `logging_type` | Optional | `elastic` | Set this to `loki` to select the Loki logging stack, leave it unset, or set it to `elastic` to select the ElasticSearch logging stack. |

## ElasticSearch Options

When using the `logging_type: elastic` setting there are a number of choices you can make:

### Data Retention Options

| Option | Required/Optional | Defaults | Comments |
|--------|-------------------|----------|----------|
| `logging_application_retention` | Optional | 21d | |
| `logging_infra_retention` | Optional | 10d | |
| `logging_audit_retention` | Optional | 7d | |


### Storage and Redundancy
| Option | Required/Optional | Defaults | Comments |
|--------|-------------------|----------|----------|
| `elasticsearch_replicas` | Optional | `3` | If you have at least three `infra` nodes this playbook automatically configures Elasticsearch  to run on those nodes. Make sure you do **not** set your replicas to more than your actual amount of `infra` nodes. |
| `elasticsearch_storageclass` | Optional |  `logging` | This should be an existing StorageClass |
| `elasticsearch_storage_size` | Optional | `150Gi` | Make sure your StorageClass has enough room for `elasticsearch_replicas` × `elasticsearch_storage_size` |
| `elasticsearch_redundancy_policy` | Optional | `SingleRedundancy` | `SingleRedudancy` implies that Elasticsearch stores every document twice. Valid options are: `FullRedudancy`, `MultipleRedundancy`, `SingleRedundancy`, and `ZeroRedundancy`. |


### Memory and CPU Settings

For each sub-component (`elasticsearch`, `kibana`, and `fluentd`) you can set both the CPU and Memory requests and limits. If you do not set these defaults are applied.

| Option | Required/Optional | Defaults | Comments |
|--------|-------------------|----------|----------|
| `elasticsearch_cpu_limit` | Optional | `4` | |
| `elasticsearch_memory_limit` | Optional | `8Gi` | For production workloads it is recommended to set this to at least `16Gi` |
| `elasticsearch_cpu_request` | Optional | `500m` | |
| `elasticsearch_memory_request` | Optional | `8Gi` | For production workloads it is recommended to set this to at least `16Gi` |
| `kibana_cpu_limit` | Optional | `1` | |
| `kibana_memory_limit` | Optional | `1Gi` | |
| `kibana_cpu_request` | Optional | `500m` | |
| `kibana_memory_request` | Optional | `1Gi` | |
| `fluentd_memory_limit` | Optional | `1Gi` | |
| `fluentd_memory_request` | Optional | `1Gi` | |
| `fluentd_cpu_limit` | Optional | `1` | |
| `fluentd_cpu_request` | Optional | `200m` | |

## Loki Options

When using the `logging_type: elastic` setting there are a number of choices you can make:

| Option | Required/Optional | Defaults | Comments |
|--------|-------------------|----------|----------|
| `loki_retention` | Optional | None | The amount of days (as an integer) for which to keep logs. If not set all logs are kept forever. |
| `loki_size` | Optional | `1x.extra-small` | Choose from `1x.extra-small`, `1x.small`, or `1x.medium`. See the upstream documentation for more information. |
| `loki_storageclass` | Optional | `odf-storagecluster-cephfs` | The storageclass to use for log storage. Indices are stored on S3. |
| `loki_use_odf` | Optional | `True` | When set to `True` (Default) an ObjectBucketClaim will be made on the installed OpenShift Data Foundation to provide S3 storage for search indices. |

### S3 settings

If you set `loki_use_odf` to `false` you will have to provide a S3 bucket to store log indices.

| Option | Required/Optional | Defaults | Comments |
|--------|-------------------|----------|----------|
| `loki_s3_access_key_id` | **Required** | None | Your S3 credentials username. |
| `loki_s3_access_key_secret` | **Required** | None | Your S3 credentials access key. |
| `loki_s3_bucket_name` | **Required** | None | The name of the S3 bucket to use. |
| `loki_s3_endpoint` | **Required** | None | The URL to an S3 endpoint serving your bucket. |

## Moving Logging Components to Infra Nodes

If you have enough nodes in your `infra` group in Ansible components will be
automatically configured to exclusively (apart from the collectors of course)
run on Infra nodes. The minimum when using `logging_type: elastic` is three
nodes for the Elasticsearch components and two nodes for everything else. When
using `logging_type: loki` it depends on your `loki_size` setting.
