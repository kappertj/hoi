# Component: Node Maintenance Operator

This component is responsible for installing the Node Maintenance Operator

## Part Of
- Component: `nodemaintenanceoperator`
- Tags: `nodemaintenanceoperator`
- Application: `nodemaintenanceoperator`

# Index

<!-- vim-markdown-toc GFM -->

* [Node Maintenance  Operator Variables](#node-maintenance--operator-variables)
* [Node Maintenance Operator Details](#node-maintenance-operator-details)
  * [Draining a Node](#draining-a-node)
  * [Uncordoning a node](#uncordoning-a-node)

<!-- vim-markdown-toc -->

# Node Maintenance  Operator Variables

| Option | Required/Optional | Comments | Default |
|--------|-------------------|----------|---------|
| nodemaintenanceoperator_channel | Optional | The subscription channel to use | `stable` |

# Node Maintenance Operator Details

This operator does not take any configuration.

## Draining a Node

To drain and cordon a node create the follwing CR:

```
apiVersion: nodemaintenance.medik8s.io/v1beta1
kind: NodeMaintenance
metadata:
  name: node-1.example.com
spec:
  nodeName: node-1.example.com
  reason: "Just because"
```

## Uncordoning a node

To uncording a node simply remove the NodeMaintenance CR that drained the node.
