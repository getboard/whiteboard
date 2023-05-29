import time

import context
import state_machine
import objects_storage

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
    # The order is crucial here
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
    ON_EVENT_SYNCER = 'OnEventSyncer'
    if ctx.objects_storage.get_opt_by_id(ON_EVENT_SYNCER) is None:
        ctx.objects_storage.register_object_type(ON_EVENT_SYNCER, OnEventSyncer)
        ctx.objects_storage.create(ON_EVENT_SYNCER, obj_id=ON_EVENT_SYNCER)
    ctx.root.after(_SYNC_PERIOD_IN_SEC * _MS_IN_SEC, lambda ctx=ctx: sync_periodic(ctx))


class OnEventSyncer(objects_storage.Object):
    def __init__(self, ctx: context.Context, id: str, **kwargs):
        super().__init__(ctx, id, **kwargs)
        ctx.pub_sub_broker.subscribe(
            state_machine.StateMachine.STATE_CHANGED_NOTIFICATION,
            state_machine.StateMachine.PUB_SUB_ID,
            self.id,
        )

    def get_notification(self, ctx: context.Context, _, event: str, **kwargs):
        if event != state_machine.StateMachine.STATE_CHANGED_NOTIFICATION:
            return
        if kwargs['state_changed_to'] != state_machine.StateMachine.ROOT_STATE_NAME:
            return
        sync(ctx, apply_events=True, force=False)


def init_sync(ctx: context.Context):
    ctx.root.after(_SYNC_PERIOD_IN_SEC * _MS_IN_SEC, lambda ctx=ctx: sync_periodic(ctx))
