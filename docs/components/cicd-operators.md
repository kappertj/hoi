# Component: CICD Operators

This component is responsible for installing two operators typically used by dev-teams:
- OpenShift Pipelines
- OpenShift Serverless

## Part Of
- Component: `cicd-operators`
- Tags: `cicd-operators`
- Application: `cicd-operators`

# Index

<!-- vim-markdown-toc GFM -->

* [CICD Operators Variables](#cicd-operators-variables)
* [CICD Operators Details](#cicd-operators-details)
  * [Tekton](#tekton)
  * [Knative](#knative)

<!-- vim-markdown-toc -->

# CICD Operators Variables

| Option | Required/Optional | Comments | Default |
|--------|-------------------|----------|---------|
| cicd_operators_install_tekton | Optional | Install Tekton (OpenShift Pipelines) Operator | True |
| cicd_operators_install_knative | Optional | Install Knative (OpenShift Serverless) Operator | True |

# CICD Operators Details

All of the configuration for this component is pulled from the upstream base. It does the following things:

## Tekton
- Create a subscription for the OpenShift Pipelines Operator.
- Configure the OpenShift Pipelines Operator to automatically clean old
  PipelineRuns and TaskRuns every fifteen minutes.

## Knative
- Create a namespace for the OpenShift Serverless Operator (`openshift-serverless`).
- Create an OperatorGroup in the `openshift-serverless` namespace.
- Create a subscription for the OpenShift Serverless Operator
- Create a KnativeEventing object to enable Eventing
- Create a KnativeServing object to enable Serving

