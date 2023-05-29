import time

import context
import state_machine

_SYNC_PERIOD_IN_SEC = 5
_MS_IN_SEC = 1000


def _last_sync_was_long_ago(ctx: context.Context) -> bool:
    cur_ts = time.time()
    last_sync_ts = ctx.events_history.get_last_sync_ts()
    return last_sync_ts is None or last_sync_ts + _SYNC_PERIOD_IN_SEC < cur_ts


def _is_sync_needed(ctx: context.Context) -> bool:
    if ctx.state_machine.get_cur_state_name() != state_machine.StateMachine.ROOT_STATE_NAME:
        ctx.logger.debug('State machine is not in the root state, skipping sync')
        return False
    if not _last_sync_was_long_ago(ctx):
        ctx.logger.debug('too soon to sync events')
        return False
    return True


def prepare_for_applying(ctx: context.Context):
    ctx.pub_sub_broker.reset()
    ctx.objects_storage.reset()
    ctx.canvas.delete('all')
    ctx.state_machine.reset()


def sync(ctx: context.Context, apply_events=True, force=False):
    if not force and not _is_sync_needed(ctx):
        return

    ctx.events_history.sync(ctx)
    if apply_events:
        prepare_for_applying(ctx)
        ctx.events_history.apply_all(ctx)


def sync_periodic(ctx: context.Context):
    sync(ctx, apply_events=True, force=False)
    ctx.root.after(_SYNC_PERIOD_IN_SEC * _MS_IN_SEC, lambda ctx=ctx: sync_periodic(ctx))


def start_sync_periodic_task(ctx: context.Context):
    ctx.root.after(_SYNC_PERIOD_IN_SEC * _MS_IN_SEC, lambda ctx=ctx: sync_periodic(ctx))
