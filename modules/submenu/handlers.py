import context
import events.event_handlers


class UpdateObjectHandler(events.event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx: context.Context, **kwargs):
        obj_id = kwargs['obj_id']
        kwargs.pop('obj_id')
        obj = ctx.objects_storage.get_by_id(obj_id)
        for prop_name, prop_value in kwargs.items():
            obj.properties[prop_name].setter(ctx, prop_value)
        ctx.table.update_object(ctx, obj_id)
