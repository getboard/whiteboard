import context


def prepare_for_applying(ctx: context.Context):
    ctx.pub_sub_broker.reset()
    ctx.objects_storage.reset()
    ctx.canvas.delete('all')
    ctx.state_machine.reset()

def sync(ctx: context.Context, apply_events=True):
    ctx.events_history.sync(ctx)
    if apply_events:
        prepare_for_applying(ctx)
        ctx.events_history.apply_all(ctx)