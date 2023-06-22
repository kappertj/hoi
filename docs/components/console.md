# Component: Console

This component is responsible for configuring the OpenShift Console. It has three major functions
- Configure a custom login in the console
- Configure a custom product name in the console
- Configure a custom URL for the console

## Part Of
- Component: `console`
- Tags: `console`
- Application: `console`

# Index

<!-- vim-markdown-toc GFM -->

* [Console Variables](#console-variables)
* [Custom Console URL Considerations](#custom-console-url-considerations)
* [Example Branding Files](#example-branding-files)
* [Footnotes](#footnotes)

<!-- vim-markdown-toc -->

# Console Variables 

These variables are used when both the `branding` and `console` components are
defined in the `openshift_components` list variable

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `custom_logo_file` | Optional | A file name on the Ansible controller pointing to a SVG file with a custom logo in it, for use in the Console |
| `custom_product_name` | Optional | A string to use as the product name in the Console |
| `custom_console_url` | Optional | A custom hostname to run the console on.[^updateneeded] |

# Custom Console URL Considerations

Any custom console URL will be added to the relevant Ingress Controllers. Make
sure that the DNS entries for your custom console URL points the corect
load-balancer or IngressController.

# Example Branding Files
![Custom Logo](../../roles/openshift_config_gitops/files/hcs-ocp-logo.svg "Custom Logo")*Custom Logo*

# Footnotes
[^updateneeded]: The current codebase uses the <=4.7 method for settings a
  custom console URL. This needs to be updated to the >=4.8 method. Being able
  to set custom certificates is also needed. Please feel free to create a
  pull-request.
