def patch_mm(version: str) -> str:
    """
    Normalize any Riot-ish version string to 'major.minor'.

    Examples:
      '16.4.1'         -> '16.4'
      '16.4.512.1234'  -> '16.4'
      '16.4'           -> '16.4'
    """
    if not version:
        raise ValueError("empty version")

    parts = version.split(".")
    if len(parts) < 2:
        raise ValueError(f"bad version: {version}")

    return f"{parts[0]}.{parts[1]}"