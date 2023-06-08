from events.event_handlers import EventHandler


class AddConnectorHandler(EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        obj_id = kwargs['obj_id']
        kwargs['start_position'] = kwargs['start_position']
        kwargs['end_position'] = kwargs['end_position']
        kwargs.pop('obj_id')
        ctx.objects_storage.create(
            'CONNECTOR',
            obj_id=obj_id,
            **kwargs
        )
