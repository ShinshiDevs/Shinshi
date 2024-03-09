import hikari

from shinshi.__main__ import bot


# TODO: Event manager
@bot.listen(hikari.ShardReadyEvent)
async def on_shard_ready(event: hikari.ShardReadyEvent) -> None:
    await event.shard.update_presence(
        activity=hikari.Activity(
            type=hikari.ActivityType.WATCHING,
            name=f"Shard #{event.shard.id}",
        ),
        status=hikari.Status.ONLINE,
    )
