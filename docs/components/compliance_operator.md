# Component: OpenShift Compliance Operator

This component is responsible for installing the OpenShift Compliance Operator

## Part Of
- Component: `compliance_operator`
- Tags: `compliance_operator`
- Application: `compliance_operator`

## See Also
- [CIS Compliance Component](cis_compliance.md)

# Index

<!-- vim-markdown-toc GFM -->

* [OpenShift Compliance  Operator Variables](#openshift-compliance--operator-variables)
* [OpenShift Compliance Operator Details](#openshift-compliance-operator-details)
    * [Tailored Profiles](#tailored-profiles)
    * [Default Scans](#default-scans)

<!-- vim-markdown-toc -->

# OpenShift Compliance  Operator Variables

| Option | Required/Optional | Comments | Default |
|--------|-------------------|----------|---------|
| compliance_operator_channel | Optional | The subscription channel to use | `release-0.1` |

# OpenShift Compliance Operator Details

This operator does not take any configuration.

## Tailored Profiles

This component contains a `TailoredProfile` called `ocp4-cis-hoi`. This profile inherits everything from the regular `ocp4-cis` profile, but extends the list of SCCs that are allowed to have more capabilities to include the SCCs used by ODF and Tekton.

## Default Scans

This component sets up a `ScanSetting` called `ocp4-cis-hoi` that uses the
TailoredProfile, and creates a `ScanSettingBinding` called `cis-compliance`
that enables that `ScanSetting`.
