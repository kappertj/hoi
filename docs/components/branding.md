# Component: Branding

This component is responsible for custom branding. It does this in two places:
- The OpenShift Console [Docs](console.md)
- The OpenShift Authentication Operator [Docs](oauth.md)

There is no actual task file for this component, as it used as a conditional
inside the components named previously.

## Part Of
- Component: `branding`
- Tags: None
- Application: `oauth` and `console`

# Index

<!-- vim-markdown-toc GFM -->

* [Branding Variables - Authentication](#branding-variables---authentication)
* [Branding Variables - Console](#branding-variables---console)
* [Example Branding Files](#example-branding-files)

<!-- vim-markdown-toc -->

# Branding Variables - Authentication

These variables are used when both the `branding` and `oauth` components are
defined in the `openshift_components` list variable

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `custom_logo_file` | Optional | A file name on the Ansible controller pointing to a SVG file with a custom logo in it. |
| `custom_background_file` | Optional | A file name on the Ansible Controller containing a SVG file to use a a background icon on login pages. |
| `custom_product_name` | Optional | A string to use as the product name on login pages. |
| `custom_product_disclaimer_body` | Optional | A custom disclaimer to display alongside the login screens |
| `custom_product_disclaimer_footer` | Optional | A custom disclaimer to show underneath the login screen. |

# Branding Variables - Console

These variables are used when both the `branding` and `console` components are
defined in the `openshift_components` list variable

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `custom_logo_file` | Optional | A file name on the Ansible controller pointing to a SVG file with a custom logo in it, for use in the Console |
| `custom_product_name` | Optional | A string to use as the product name in the Console |

# Example Branding Files
![Custom Logo](../../roles/openshift_config_gitops/files/hcs-ocp-logo.svg "Custom Logo")*Custom Logo*

![Custom background](../../roles/openshift_config_gitops/files/hcs-ocp-background.svg "Custom Background")*Custom Background*
