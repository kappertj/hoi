# Component: Group Sync

This component is responsible for installing and configuring the Group Sync Operator. It does this by performing the following tasks:

- Install the Group Sync Operator into the `group-sync-operator` namespace.
- Loop over all configured authentication providers, and create a GroupSync object if requested

## Part Of
- Component: `groupsync`
- Tags: `groupsync`
- Application: `groupsync`

# Index

<!-- vim-markdown-toc GFM -->

- [Component: Group Sync](#component-group-sync)
  - [Part Of](#part-of)
- [Index](#index)
- [Group Sync Variables](#group-sync-variables)
- [Current Status](#current-status)

<!-- vim-markdown-toc -->

# Group Sync Variables

The configuration playbook looks at the `oauth` list variable in your
inventory. For each item that has an attribute named `groupsync` it will
attempt to create a GroupSync object using the configuration for that
authentication provider. Check the [documentation for the `oauth`
component](oauth.md) for more details. Currently three different types are
supported:

| `groupsync` | Details | Comments |
|-------------|---------|----------|
| `IPA` | Configures synchronizing group contents with Red Hat IDM and FreeIPA servers  using LDAP | |
| `AD` | Configures synchronizing group contents with Active Directory using LDAP | Not recently tested |
| `azure` | Configures synchronizing group contents with Azure using OpenID Connect (oidc) | |

You can limit which groups are synchronized by adding a list to your `oauth`
item called `groupsync_groups`. The contents of this list differ based on the
authentication provider:
- For `IPA` and `AD` this is a list of items containing two keys: `dn`, holding
  the fully-qualified distinguished name of the group, and `short` holding the
  desired name in OpenShift for the group.
- For `azure` it just a plain list of group names to synchronize.

# Current Status

The `IPA` path has been thoroughly tested. `azure` has been tested as well. If you have success with either
`AD` or `azure` please let us know by raising an issue or a Pull Request on
these docs. If you do not have success with either of those please raise an
issue as well, including details, and preferably a Pull Request.
