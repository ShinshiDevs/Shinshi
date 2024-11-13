from hikari.guilds import Member


def get_audit_reason(moderator: Member, reason: str) -> str:
    suffix: str = f"[@{str(moderator)} (ID: {moderator.id})]"
    return f"{reason} {suffix}"
