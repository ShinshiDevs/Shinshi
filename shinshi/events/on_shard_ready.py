from hikari import ActivityType
from hikari.events import ShardReadyEvent

from shinshi.framework.bot import bot


@bot.listen(ShardReadyEvent)
async def callback(event: ShardReadyEvent) -> None:
    await event.shard.update_presence(
        activity=Activity(
            activity_type=ActivityType.PLAYING,
            name=""
        )
    )
