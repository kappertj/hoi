# HCS OpenShift Installation, Configuration, and Detonation

## Index

<!-- vim-markdown-toc GitLab -->

* [About](#about)
* [Requirements](#requirements)
* [Supported Installation Methods](#supported-installation-methods)
* [Setting up your inventory](#setting-up-your-inventory)
* [Installation](#installation)
    * [Example Installation Command](#example-installation-command)
* [Adding Nodes to a Cluster](#adding-nodes-to-a-cluster)
    * [Adding Nodes to a Cluster Example](#adding-nodes-to-a-cluster-example)
* [Installation Inventory Variables](#installation-inventory-variables)
* [Installation Safeguards](#installation-safeguards)
* [Configuration Using GitOps](#configuration-using-gitops)
* [Legacy Configuration](#legacy-configuration)

<!-- vim-markdown-toc -->

## About

**HCS OpenShift Install** (these playbooks) aim to make installing and
configuring OpenShift using User Provisioned Infrastructure (UPI) easier. It is
a set of **strongly** opinionated playbooks, consisting of two main parts:
- `openshift_install.yml`
  A playbook to install, or expand, an OpenShift cluster.
- `openshift_config_gitops.yml`
  A playbook that configures an OpenShift cluster using the OpenShift GitOps
  Operator (ArgoCD) and Bitnami Sealed Secrets.

Furthermore there are some other playbooks provided in the `day2_playbooks`
namespace that can help with cluster operations.

An older configuration playbook that does not use GitOps is also still provided, called `openshift_config.yml`, but it is no longer under active development. The documentation for the legacy configuration can be found as [docs/legacy.md](docs/legacy.md).

## Requirements
- A RHEL8, or equivalent (RockyLinux, ALmaLinux, CentOs Stream), or a modern Fedora machine to run this on
  - required software
  - Ansible 2.9 or higher
  - python `jmespath` module, see [the installation section](#installation) for
    instructions on obtaining this module.
- Optionally, a RHEL8, or equivalent, bastion host.
  - Your Ansible Controller (or bastion host if using the same machine) will
    need to have the `dnspython` python module installed.

## Supported Installation Methods

This set of playbooks can perform an OpenShift User-Provisioned-Installation
(UPI) on a set of platforms not typically supported by
Installer-Provisioned-Infrastructure (IPI):

- LibVirt
- LibVirt emulating RedFish with `sushy-tools`
- VMWare UPI
- Bare Metal machines using HP ILO
- Existing Linux machines
- Manually using a generated `.iso` file

## Setting up your inventory

You will need an inventory set up with all your OpenShift nodes in it, at a minimum you will need:
- One group called `bastion`, with precisely one machine in it.
- One group called `masters`, preferably with three machines in it.
- One group called `workers`, preferably with at least three machines in it
- Optionally a group called `infra`, preferably with at least three machines in it
- Optionally a group called `storage`, preferably with at least three machines in
  it, when you want to install OpenShift Data Foundation.

Variables for the various groups and components are detailed in the
installation instructions, and the sections on the different components in the
configuration manual.

## Installation

After setting up your inventory run the `openshift_install.yml` playbook. Important options:
- Before you start the installation some ansible collections need to be
  installed; `ansible-galaxy collection install -r requirements.yml`.
- On your ansible control node you will need to have python `jmespath` module
  installed. On RHEL family systems (RHEL, CentOS, AlmaLinux, RockyLinux,
  Fedora) this can be done by installing the `python3-jmespath` package:
  ```bash
  sudo dnf install python3-jmespath
  ```
  On other distributions search for the package in your repositories, or install it using `pip3`:
  ```bash
  sudo pip3 install jmespath
  ```
- When installing a *new* cluster, add `-e create_new_cluster=True` to your
  command line. Do **not** add this to your inventory, as it will blow away your
  currently stored `system:admin` authentication and `kubeconfig`, and create a
  new set of manifests, even if you are just adding hosts to an existing
  cluster.
- If you have already once downloaded the exact version you are installing you
  can speed things up by adding `--skip-tags=download` to the command.

### Example Installation Command

```bash
ansible-playbook -i <hosts-file> -e create_new_cluster=True openshift_install.yml
```

## Adding Nodes to a Cluster

Adding nodes to a cluster is done with the same playbook as installing a new cluster, with a couple of remarks:
- You **must** limit the playbook to only the new nodes (`-l newnode1,newnode2`).
- You **must not** set the `create_new_cluster` variable to `True`, as this
  will blow away your current stored files for the existing cluster.
- If the API server certificates for your cluster have been updated from the
  default internal OpenShift CA certificates you must provide a valid
  `kubeconfig` for an account with admin credentials. You can either remove the
  `certificate-authority-data` entries from the
  `/opt/openshift_files/<cluster>/ignition/auth/kubeconfig` file on your
  `bastion_host` when using API Server certificates from a trusted CA, update
  that entry to have your own custom CA in it, or point to another `kubeconfig`
  file for an admin user with `-e
  openshift_kubeconfig=/path/to/kubeconfig/on/bastion`. If you have use the
  configuration playbook with your custom CA defined the default `kubeconfig`
  is already updated to include your custom CA.

### Adding Nodes to a Cluster Example
```bash
ansible-playbook -i <hosts-file> \
  -e openshift_kubeconfig=/path/to/kubeconfig/on/bastion \
  -l newnode1,newnode2 \
  openshift_install.yml
```

## Installation Inventory Variables

See the file [installation_options.md](docs/installation_options.md) for all options.

## Installation Safeguards

At the beginning of the installation playbooks a connection will be made to what should be the resulting Kubernetes API address. If this connection succeeds, and you are trying to define more than one control-plane node in the current run, the installation will be aborted to stop you from potentially destroying a running production cluster.

If you know what your are doing you can instruct the playbooks to do the wrong
thing anyway by setting the variable `do_as_i_say_not_what_i_want` variable to
the current date in the format `YYYY-MM-DD`. For example, if today is the 13th
of April 2022 you could add `-e do_as_i_say_not_what_i_want=2022-04-14` to the
end of your `ansible-playbook` commandline to bypass these checks.

## Configuration Using GitOps

A playbook is included that can set up OpenShift GitOps, point it to a Git
repository, and the fill that repository with configuration for your cluster.

Check the documentation at [docs/config_using_gitops.md](docs/config_using_gitops.md) for details.

## Legacy Configuration

See the file [docs/legacy.md](docs/legacy.md)
