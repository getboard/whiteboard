import event_handlers


class AddTextHandler(event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        x = int(kwargs['x'])
        y = int(kwargs['y'])
        text = kwargs['text']
        obj_id = kwargs['obj_id']
        ctx.objects_storage.create(
            'TEXT', x=x, y=y, text=text, obj_id=obj_id)


class EditTextHandler(event_handlers.EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        text_id = kwargs['obj_id']
        new_text = kwargs['new_text']
        ctx.objects_storage.get_by_id(text_id).update(ctx, text=new_text)
