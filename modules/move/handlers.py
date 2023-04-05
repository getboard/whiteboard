import context
from event_handlers import EventHandler


class MoveObjectHandler(EventHandler):
    @classmethod
    def apply(cls, ctx: context.Context, **kwargs):
        obj_id = kwargs['obj_id']
        x = int(kwargs['x'])
        y = int(kwargs['y'])
        ctx.objects_storage.get_by_id(obj_id).move_to(ctx, x, y)
