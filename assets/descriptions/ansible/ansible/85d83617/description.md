# Title

Standardize TLS Connection Parameters Across All Modules, Plugins, and Connections

# Summary

Standardize parameter names for TLS/SSL connections across the Ansible codebase to provide a consistent interface. Many modules, plugins, and connections use varying names for similar TLS configuration options, causing confusion and inconsistency.

# Why

- **Inconsistency**: Different modules use different parameter names for identical purposes
  - `ssl_cert` vs `certfile` vs `cert_file` vs `client_cert`
  - `ssl_verify` vs `verify_ssl` vs `validate_certs` vs `ssl_check_peer`
  - `ssl_ca` vs `cacert` vs `ca_certs` vs `ssl_ca_cert`
  - ... and many more variations
- **User Experience**: Users must learn different parameter names for each module
- **Maintainability**: Harder to maintain and document

# Standard Parameters

Define four canonical TLS parameters:

- **`client_cert`**: Certificate for client identity (may include private key)
- **`client_key`**: Private key for `client_cert`
- **`ca_cert`**: CA certificate(s) to validate server identity
- **`validate_certs`**: Boolean to enable/disable certificate validation

# Changes

Apply standardization across:

- **Modules**: openstack, tower, docker, k8s, mysql, postgresql, rabbitmq, ingate, manageiq, nios, zabbix, bigip, vdirect, mqtt, pulp, rhn, yum, lxd, kubevirt, get_certificate, gitlab, ...
- **Connections**: kubectl, oc, psrp
- **Inventory plugins**: docker_swarm, k8s, openshift, tower
- **Lookup plugins**: hashi_vault, k8s, laps_password
- **Callbacks**: foreman, grafana_annotations, nrdp

# Backward Compatibility

- Old parameter names remain as **aliases**
- New names take precedence if both specified
- No breaking changes for existing playbooks

# Implementation Notes

- Update all affected `argument_spec` definitions
- Add proper aliases mapping
- Update documentation fragments
- Add changelog entry
- Handle special cases where internal logic references old names