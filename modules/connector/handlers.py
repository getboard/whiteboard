from event_handlers import EventHandler


class AddConnectorHandler(EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        start = ctx.objects_storage.get_opt_by_id(kwargs['start_id'])
        end = ctx.objects_storage.get_opt_by_id(kwargs['end_id'])
        snap_to = kwargs['snap_to']
        obj_id = kwargs['obj_id']
        ctx.objects_storage.create(
            ctx,
            'CONNECTOR',
            obj_id=obj_id,
            snap_to=snap_to,
            start=start,
            end=end
        )


class EditConnectorHandler(EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        start = ctx.objects_storage.get_opt_by_id(kwargs['start_id'])
        end = ctx.objects_storage.get_opt_by_id(kwargs['end_id'])
        snap_to = kwargs['snap_to']
        obj_id = kwargs['obj_id']
        ctx.objects_storage.get_by_id(obj_id).update(snap_to=snap_to, start=start, end=end)
