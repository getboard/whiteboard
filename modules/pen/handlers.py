import events.event_handlers


class AddPenHandler(events.event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        obj_id = kwargs['obj_id']
        kwargs.pop('obj_id')
        ctx.objects_storage.create('PEN', obj_id=obj_id, **kwargs)
