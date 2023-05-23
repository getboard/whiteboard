import context


def sync(ctx: context.Context, apply_events=True):
    ctx.events_history.sync(ctx)
    if apply_events:
        # TODO: clean here
        ctx.events_history.apply_all(ctx)