# Component: Service Mesh

This component is responsible for installing the operators needed for Red Hat Service Mesh
- Kiali Operator
- Red Hat OpenShift Distributed Tracing Platform
- OpenShift Elasticsearch Operator (Optional)
- Red Hat OpenShift Service Mesh


## Part Of
- Component: `servicemesh`
- Tags: `servicemesh`
- Application: `servicemesh`

# Index

<!-- vim-markdown-toc GFM -->

* [Service Mesh Variables](#service-mesh-variables)

<!-- vim-markdown-toc -->

# Service Mesh Variables

This component only takes one variable, that controls whether or not the OpenShift Elasticsearch Operator should be installed as part of the Service Mesh installation or not. If you are also isntalling the `logging` component this variable will be ignnored, and the OpenShift Elasticsearch Operator will be isntalled as part of the `logging` instead.

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `servicemesh_install_elasticsearch` | Optional | Whether or not to install the OpenShift Elasticsearch Operator. Defaults to `True`, ignored if the `logging` component is also installed. |
