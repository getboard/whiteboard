import context
import event_handlers


class UpdateObjectHandler(event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx: context.Context, **kwargs):
        obj_id = kwargs['obj_id']
        kwargs.pop('obj_id')
        obj = ctx.objects_storage.get_by_id(obj_id)
        for prop_name, prop_value in kwargs.items():
            obj.properties[prop_name].setter(ctx, prop_value)


class DeleteObjectHandler(event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx: context.Context, **kwargs):
        obj_id = kwargs['obj_id']
        ctx.objects_storage.remove(obj_id)
