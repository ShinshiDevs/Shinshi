from hikari import Snowflakeish

from shinshi.abc.config.iconfiguration_service import IConfigurationService


def get_emoji(
    configuration_service: IConfigurationService, name: str, *, config_name: str = "emojis"
) -> Snowflakeish | None:
    return configuration_service.get_config(config_name).get(name)
