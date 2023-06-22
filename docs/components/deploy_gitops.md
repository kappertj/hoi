# Component: Deploy GitOps

This component is responsible for installing and configuring ArgoCD in the
`openshift-gitops` namespace.

## Part Of
- Component: `deploy_gitops`
- Tags: `deploy_gitops`
- Application: None

## Index

<!-- vim-markdown-toc GFM -->

* [Important Variables](#important-variables)
* [Git Variables](#git-variables)

<!-- vim-markdown-toc -->

## Important Variables

You can configure this component using the following variables:

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `openshift_gitops_admin_groups` | Optional | A list of OpenShift group names that should be given admin access to ArgoCD. This defaults to `[]`, allowing only `system:cluster-admins` admin access (i.e. the `kubeadmin` user) |
| `openshift_gitops_default_role` | Optional | The role that should be given to ArgoCD users not in an admin group. Defaults to `role:readonly`, but can be set to `''` for added security. or `role:admin` for extra fun with your auditors. |
| `gitops_operator_channel` | Optional | The Operator channel to subscribe to, defaults to `stable`. There is typically no reason to change this. |


## Git Variables

The following variables can be used to configure this component. Note that some of these
variables are also documented under [Component: Create
ApplicationSet](create_applicationset.md) and [Component: Setup Git](setup_git.md) as well
since they overlap.

| Option | Required/Optional | Comments |
|--------|-------------------|----------|
| `openshift_gitops_dir` | Optional | The directory where to store and modify the Git checkout. Defaults to `/opt/openshift_files/{{ cluster }}/gitops` |
| `openshift_gitops_repo_url` | **Required** | The **SSH** URL to your custom GitOps repository, for example: `git@git.example.com:ocp/gitops.git`
| `openshift_gitops_repo_version` | Optional | The Git branch to use, defaults to `main` |
| `openshift_gitops_repo_ssh_privkey_file` | Optional | The file location _on your bastion host_ of the SSH private key to use. Defaults to `/opt/openshift_files/{{ cluster }}/keys/gitops.rsa` |
| `openshift_gitops_repo_name` | **Required** | The name to use in ArgoCD for your repository.
| `openshift_gitops_repo_known_hosts` | **Required** | Extracts of a SSH `known_hosts` file detailing the host keys of your Git server(s). These values can be easily obtained by running `ssh-keyscan <gitserver> 2> /dev/null`. Example:<br/>`openshift_gitops_repo_known_hosts: \|`<br/>`  git.example.com ssh-rsa AAAAAsdsgy4qwtgw4gerghw.....`<br/>`  git.example.com ecdsa-sha2-nistp256 AAAAAsdghsrahera`<br/>...
| `openshift_gitops_upstream_base` | Optional | The Git URL for your upstream base. Defaults to `https://gitlab.com/hcs-company/openshift-gitops-base.git`. If your upstream fork is private this will need to be a SSH url, using the same private key as `openshift_gitops_repo_url`, and the SSH host keys should be included in `openshift_gitops_repo_known_hosts`. |
| `openshift_gitops_upstream_ref` | Optional | The Git reference to use (e.g. a branch name or a tag name) for the `openshift_gitops_upstream_base` repository. Not used when not set. |
