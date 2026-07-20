# Configuration

- `base/` — shared configuration: the data catalog and pipeline parameters. Safe to version control.
- `local/` — machine-specific overrides and credentials. Excluded from version control via `.gitignore`.

See [Kedro's configuration documentation](https://docs.kedro.org/en/stable/configure/configuration_basics/#configuration) for details on how the two are merged at runtime.
