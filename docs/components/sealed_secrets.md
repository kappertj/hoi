# Component: Bitnami Sealed Secrets

This component is responsible for installing Bitnami Sealed Secrets on your cluster. It also installs the `kubeseal` tool on your `bastion_host`.

## Part Of
- Component: `sealed_secrets`
- Tags: `sealed_secrets`
- Application: `sealed_secrets`

# Index

<!-- vim-markdown-toc GFM -->

* [Warning](#warning)
* [Skipping the Download of the `kubeseal` tool](#skipping-the-download-of-the-kubeseal-tool)
* [Bitnami Sealed Secrets Configuration](#bitnami-sealed-secrets-configuration)

<!-- vim-markdown-toc -->

# Warning

Almost all components you can enable will attempt to add SealedSecrets to Git.
If you skip this component most others will fail, since they will be missing
both the CRD for SealedSecrets, and the necessary secrets for their operation.

# Skipping the Download of the `kubeseal` tool

If `/usr/local/bin/kubeseal` is already present on your `bastion_host` you can
skip the automatic download of the tool by adding `--skip-tags=download` to
your playbook command.

**N.B.** You will need to have `/usr/local/bin/kubeseal` present on your
`bastion_host`, although it can be in a different location. If your
`bastion_host` is not able to download it directly download a version manually
from the [Bitnami Sealed Secrets releases
page](https://github.com/bitnami-labs/sealed-secrets/releases) and place it on
your `bastion_host` manually **before** running this playbook.

# Bitnami Sealed Secrets Configuration

You do not typically need to change any of these settings, but you can if you
need to, for example to use a different (newer) version of `kubeseal`, or to
change the path to the `kubeseal` binary on your `bastion_host`.

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `kubeseal_version` | Optional | The version of the `kubeseal` tool to download. Defaults to a recent version. |
| `kubeseal_download_url` | Optional | The download path for the `kubeseal` tool. Defaults to `https://github.com/bitnami-labs/sealed-secrets/releases/download/v{{ kubeseal_version }}/kubeseal-{{ kubeseal_version }}-linux-amd64.tar.gz` |
| `kubeseal_cert_dir` | Optional | The directory where the _public_ Sealed Secrets encryption certificate will be stored. Defaults to `/opt/openshift_files/{{ cluster }}/kubeseal` |
| `kubeseal_cert` | Optional | The filename to store the _public_ Sealed Secrets encryption certificate. Defaults to `{{ kubeseal_cert_dir }}/kubeseal.pem` |
| `kubeseal_command` | Optional | The default `kubeseal` command to use, including default parameters. Defaults to  `/usr/local/bin/kubeseal --kubeconfig={{ openshift_kubeconfig }} --controller-namespace=openshift-sealed-secrets`. |

