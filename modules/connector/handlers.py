from event_handlers import EventHandler


class AddConnectorHandler(EventHandler):
    @classmethod
    def apply(cls, ctx, **kwargs):
        start = kwargs['start'].split('; ')
        end = kwargs['end'].split('; ')
        if len(start) > 1:
            start = (int(start[0]), int(start[1]))
        else:
            start = ctx.objects_storage.get_by_id(start[0])

        if len(end) == 2:
            end = (int(end[0]), int(end[1]))
        else:
            end = ctx.objects_storage.get_by_id(end[0])

        snap_to = kwargs['snap_to']
        obj_id = kwargs['obj_id']
        start_x, start_y = map(int, kwargs['start_pos'].split('; '))
        end_x, end_y = map(int, kwargs['end_pos'].split('; '))
        ctx.objects_storage.create(
            'CONNECTOR',
            obj_id=obj_id,
            start=start,
            end=end,
            start_x=start_x,
            start_y=start_y,
            end_x=end_x,
            end_y=end_y,
            snap_to=snap_to
        )
