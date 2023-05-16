from event_handlers import EventHandler


class AddConnectorHandler(EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        obj_id = kwargs['obj_id']
        start_id = kwargs['start_id']
        end_id = kwargs['end_id']
        start_position = eval(kwargs['start_position'])
        end_position = eval(kwargs['end_position'])
        start_x = kwargs['start_x']
        start_y = kwargs['start_y']
        end_x = kwargs['end_x']
        end_y = kwargs['end_y']
        snap_to = kwargs['snap_to']
        ctx.objects_storage.create(
            'CONNECTOR',
            obj_id=obj_id,
            start_id=start_id,
            start_position=start_position,
            end_id=end_id,
            end_position=end_position,
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            snap_to=snap_to
        )
