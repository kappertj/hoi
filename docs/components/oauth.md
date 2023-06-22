# Component: Authentication

This component is responsible for configuring the OpenShift Authentication
Operator. It currently supports multiple authentication providers:
- LDAP (e.g. FreeIPA, OpenLDAP, Red Hat IDM)
- Microsoft Active Directory (Using LDAP)
- OpenID Connect (oidc)

This component is also responsible for applying the custom login screen
branding you may have configured. For the documentation on how to configure
that see the [docs for the `branding` component](branding.md).

## Part Of
- Component: `oauth`
- Tags: `oauth`
- Application: `oauth`

## Related Components
- `groupsync`
- `branding`

# Index

<!-- vim-markdown-toc GFM -->

- [Component: Authentication](#component-authentication)
  - [Part Of](#part-of)
  - [Related Components](#related-components)
- [Index](#index)
- [Authentication Variables](#authentication-variables)
  - [Authentication Configuration Examples](#authentication-configuration-examples)
    - [LDAP (FreeIPA)](#ldap-freeipa)
    - [Active Directory](#active-directory)
    - [OpenID Connect](#openid-connect)
- [Branding Configuration Variables](#branding-configuration-variables)
- [Managing Self-Provisioners](#managing-self-provisioners)
  - [Managing Self-Provisioners Example Configuration](#managing-self-provisioners-example-configuration)
- [Setting Cluster Admins](#setting-cluster-admins)
  - [Cluster Admin Groups Example](#cluster-admin-groups-example)

<!-- vim-markdown-toc -->

# Authentication Variables

You can configure authentication providers using the `oauth` variable, this is
a list of objects with the following specification.

| Option | Required/Optional | Type | Comments |
|--------|-------------------|------|----------|
| `type` | Optional | All | Whether this is for `LDAP` (and AD), or `OpenID`, defaults to `LDAP` if not specified. |
| `name` | **Required** | All | The name for this provider, used in the name of other objects. |
| `cafile` | Optional | All | A file on the `bastion_host` holding a custom CA used to verify the connection when talking to this provider. |
| `groupsync` | Optional | All | The type of Group Sync to perform, supported values are `IPA`, `AD` and `azure`. Only used by the `groupsync` component. |
| `groupsync_groups` | Optional | All | A list of groups to synchronize from your authentication provider. Only used by the `groupsync` component. The format differs per provider, see the [Group Sync Component docs](groupsync.md) for more information. |
| `binddn` | **Required** | `LDAP` | The LDAP Distinguished Name of the account used to connect to the LDAP Server. |
| `bindpw` | **Required** | `LDAP` | The password of the LDAP user used to connect to the LDAP server. |
| `host` | **Required** | `LDAP` | The hostname of the LDAP server. |
| `scheme` | Optional | `LDAP` | The scheme to use when talking to LDAP. By default `ldap` (with STARTTLS) is used. If your LDAP provider still lives in the '90s you can use `ldaps` to force connections TLS on a separate port. |
| `base` | **Required** | `LDAP` | The LDAP search base for users |
| `urlfilter` | Optional | `LDAP` | An empty URL filter to append to the LDAP queries sent for users. Useful to limit the amount of responses to only those objects that actually match users. |
| `group_base` | Optional | `LDAP` | The LDAP search base for groups.Only used for the `groupsync` component. |
| `attributes` | **Required** | `LDAP` | A dictionary of four items (`id`, `email`, `name`, and `preferredUsername`, each containing a list of the LDAP attribute names to map to those OpenShift user attributes. |
| `openid_clientid` | **Required** | `OpenID` | The OpenID client ID to use when connecting. |
| `openid_tenantid` | **Required** | `OpenID` | The Azure Tenant ID to use when connecting. `groupsync` uses tenant id |
| `openid_issuer` | **Required** | `OpenID` | The OpenID issuer URL. The URL includes the tenant id. Oauth uses issuer URL |
| `openid_client_secret` | **Required** | `OpenID` | The OpenID clientSecret to use when talking to the issuer. |
| `oauth_token_lifetime_seconds` | Optional | The maximum lifetime of an Oauth token, in seconds. Defaults to 24 hours, or `86400`. |
| `oauth_token_inactivity_timeout` | Optional | The default inactivity time aftger which an Oauth token losses validity, can be overriden by client. Default: None |
oauth_token_lifetime_seconds is defined) or (oauth_token_inactivity_timeout


## Authentication Configuration Examples

### LDAP (FreeIPA)
```yaml
oauths:
- name: example-ipa
  type: LDAP
  binddn: "{{ ldap_service_dn }}"
  bindpass: "{{ ldap_service_pass }}"
  scheme: ldap
  host: ipa.example.com
  base: cn=users,cn=accounts,dc=example,dc=com
  cafile: /etc/ipa/ca.crt
  attributes:
    id:
    - uid
    email:
    - mail
    name:
    - displayName
    preferredUsername:
    - uid
```

### Active Directory
```yaml
oauths:
- name: example-AD
  type: LDAP
  binddn: "{{ ldap_service_dn }}"
  bindpass: "{{ ldap_service_pass }}"
  scheme: ldaps
  host: ad.example.com
  base: cn=users,cn=accounts,dc=example,dc=com
  urlfilter: '?samaccountname?sub'
  cafile: /path/to/AD/ca.crt
  attributes:
    id:
    - cn
    email:
    - mail
    name:
    - description
    preferredUsername:
    - sAMAccountName
```

### OpenID Connect
```yaml
oauths:
- name: example-openid-azure
  type: OpenID
  openID:
    claims:
      email:
      - email
      name:
      - name
      preferredUsername:
      - upn
  openid_clientid: "{{ openid_clientid }}"
  openid_tenantid: "{{ openid_tenantid }}"
  openid_issuer: "https://login.microsoftonline.com/{{ openid_tenantid }}"
  openid_client_secret: "{{ openid_client_secret }}"
  cafile: "/path/to/custom/ca.pem"
```

# Branding Configuration Variables

For custom login branding configuration check the [docs for the `branding` component](branding.md)

# Managing Self-Provisioners

By default an OpenShift cluster allows every single authenticated user to
create new Projects. In many environments this can be unwanted.You can control
who can create Projects using the `self_provisioners` variable. This variable
has a default (which does nothing). If you decide to set it all three
attributes must be set on it. The "Default" column in the following table show
the settings if you do not define this variable yourself.

Cluster Admins always have the right to provision namespaces and Projects.

| Option | Comments | Default |
|--------|----------|---------|
| `remove_default` | Whether or not to remove the self-provisioner access from all authenticated users. | `False` |
| `users` | A list of users that should have self-provisioning access granted. If other than an empty list (`[]`) `remove_default` will be set to `True` | `[]` |
| `groups` | A list of groups that should have self-provisioning access granted. If other than an empty list (`[]`) `remove_default` will be set to `True` | `[]` |


## Managing Self-Provisioners Example Configuration
```yaml
self_provisioners:
  remove_default: True
  users:
  - trusted_team_member
  - operations_manager
  - system:serviceaccount:app-cicd:tekton
  groups:
  - trusted_devteam
  - teamleads
```

# Setting Cluster Admins

You can configure which groups automatically get assigned `cluster-admin` privileges.

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `openshift_cluster_admin_groups` | Optional | A list of group names that should be assigned cluster-admin privileges. |

## Cluster Admin Groups Example
```yaml
openshift_cluster_admin_groups:
- cluster-admin
```
