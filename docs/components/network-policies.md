# Component: Network Policies

This component is responsible for configuring a set of default NetworkPolicy objects by creating a projectRequestTemplate.
Three default NetworkPolicies are created:
- `allow-same-namespace`
  This allows inter-pod communication in the same namespace
- `allow-from-openshift-ingress`
  This allows traffic to all pods from namespaces labeled: `policy-group.network.openshift.io/ingress: ''`
- `allow-from-openshift-monitoring`
  This allows traffic to all pods from namespaces labeled: `network.openshift.io/policy-group: monitoring`

## Part Of
- Component: `network-policies`
- Tags: `network-policies`
- Application: `network-policies`

# Index

<!-- vim-markdown-toc GFM -->

* [Gotchas](#gotchas)

<!-- vim-markdown-toc -->

# Gotchas

Setting default NetworkPolicies using a default projectRequestTemplate has a
couple of gotchas to be aware of:

- Existing namespaces are not updated
- Only namespaces created using a projectRequest object will be affected. Not
  namespaces created by instantiating a Project object, or by creating a
  namespace directly.
  - On a default OpenShift install regular users can only create namespaces by
    the use of a projectRequest object (`oc new-project <name>`), so this
    should not affect those installs.
