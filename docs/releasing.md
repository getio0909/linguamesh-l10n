# Releasing

No localization release can be produced from the foundation checkpoint.

A future release must use semantic versioning and include canonical sources, generated platform bundles, compatibility metadata, checksums, license material, and updated third-party notices. Before tagging, validate every official locale, placeholder/plural/select compatibility, fallback behavior, pseudo-locales, RTL fixtures, and deterministic regeneration.

Record the localization version and compatible client/core versions in the central `linguamesh-project/release-manifest.toml`. Mark prereleases clearly. Do not publish a stable bundle until the central known-good release train and reproducible CI evidence agree.
