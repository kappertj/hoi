# Component: Machine Configs

This component is responsible for adding extra MachineConfig object to your
cluster. Currently the playbook only add a single MachineConfig to both the
`master` and `worker` role: A `chrony` configuration for timekeeping. While
this seems like something that could be done during machine install time, this
setup allows you to change the timeservers in use on your cluster at runtime.

But the main purpose of this component is to give your Git repo a starting
point for adding your own MachineConfigs.

## Part Of
- Component: `machineconfigs`
- Tags: `machineconfigs`
- Application: `machineconfigs`

# Index

<!-- vim-markdown-toc GFM -->

* [Machine Config Variables](#machine-config-variables)

<!-- vim-markdown-toc -->

# Machine Config Variables

This component only takes a single variable:

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `ntp_servers` | Optional | A list of time servers to configure on each node. Defaults to a list of `pool.ntp.org` servers if unset. To set no time servers specify an empty list in your inventory. |
