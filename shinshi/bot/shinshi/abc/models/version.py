import attrs


@attrs.define(eq=False, kw_only=True, hash=False, weakref_slot=False)
class VersionInfo:
    version: str
    git_sha: str
