import event_handlers


class UpdateObjectHandler(event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        sticker_id = kwargs['obj_id']
        kwargs.pop('obj_id')
        if 'font' in kwargs:
            kwargs['font'] = eval(kwargs['font'])
        ctx.objects_storage.get_by_id(sticker_id).update(ctx, **kwargs)
