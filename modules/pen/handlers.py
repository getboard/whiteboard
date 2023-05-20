import event_handlers


class AddPenHandler(event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        obj_id = kwargs['obj_id']
        kwargs.pop('obj_id')
        if 'points' in kwargs:
            kwargs['points'] = eval(kwargs['points'])
        ctx.objects_storage.create(
            'PEN',
            obj_id=obj_id,
            **kwargs
        )
