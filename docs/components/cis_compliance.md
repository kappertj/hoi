# Component: CIS Compliance

This component is responsible for adding `machineConfigs` and `KubeletConfigs` that
enable your cluster to pass the CIS benchmark.

## Part Of
- Component: `cis_compliance`
- Tags: `cis_compliance`
- Application: `cis_compliance`

## See Also
- [Compliance Operator Component](compliance_operator.md)

# Index

<!-- vim-markdown-toc GFM -->

* [OpenShift CIS Compliance Variables](#openshift-cis-compliance-variables)
* [User Respsonsibility](#user-respsonsibility)

<!-- vim-markdown-toc -->

# OpenShift CIS Compliance Variables

This component currently has now configuration options.

# User Respsonsibility

Even though this component configures your cluster to (mostly) pass the CIS
benchmark, there are a couple of steps a cluster administrator will still need
to perform for themselves:

1. Ensure that there are no more `ComplianceCheckResults` that FAILed
   ```bash
   oc get -n openshift-compliance ComplianceCheckResult -l compliance.openshift.io/check-status=FAIL
   ```
2. Fix any remaining failures, especially:
   - Enable Cluster Audit Log Forwarding by creating a `ClusterLogForwarder` object.
   - Ensure that there are no remaining namespaces outside of `openshift-*`, `kube-*`, and `default` without `NetworkPolicies`
   - Disable `kubeadmin` login:
     ```bash
     oc delete -n kube-system secret kubeadmin
     ```

