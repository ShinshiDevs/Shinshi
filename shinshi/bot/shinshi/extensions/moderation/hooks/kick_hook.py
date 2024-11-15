from aurum.hooks import HookResult, hook
from hikari.guilds import Member

from shinshi.framework.interaction.context import Context


@hook()
async def kick_hook(context: Context) -> HookResult:
    bot: Member = context.guild.get_my_member()
    moderator: Member = context.member
    target: Member = context.arguments["member"]

    if context.bot.get_me().id == target.id:
        await context.create_warning_response(context.locale.get("commands.kick.errors.target_is_bot"))
        return HookResult(stop=True)

    if moderator.id == target.id:
        await context.create_warning_response(context.locale.get("commands.kick.errors.target_is_moderator"))
        return HookResult(stop=True)

    if bot.get_top_role().position <= target.get_top_role().position:
        await context.create_warning_response(context.locale.get("commands.kick.errors.target_too_high_for_bot"))
        return HookResult(stop=True)

    if moderator.id != context.guild.owner_id and moderator.get_top_role().position <= target.get_top_role().position:
        await context.create_warning_response(context.locale.get("commands.kick.errors.target_too_high_for_moderator"))
        return HookResult(stop=True)

    return HookResult(stop=False)
