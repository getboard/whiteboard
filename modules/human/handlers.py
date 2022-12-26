import event_handlers


class AddHumanHandler(event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        x = int(kwargs['x'])
        y = int(kwargs['y'])
        obj_id = kwargs['obj_id']
        ctx.objects_storage.create(ctx, 'HUMAN', x=x, y=y, obj_id=obj_id)
