import event_handlers


class AddPenHandler(event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        obj_id = kwargs['obj_id']
        x = list(map(int, kwargs['x'].split()))
        y = list(map(int, kwargs['y'].split()))
        width = float(kwargs['width'])
        color = kwargs['color']
        ctx.objects_storage.create('PEN', obj_id=obj_id, width=width, color=color, x=x, y=y)


class ChangeColorPenHandler(event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        obj_id = kwargs['obj_id']
        color = kwargs['color']
        ctx.objects_storage.update(obj_id, fill=color)
