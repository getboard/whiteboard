import typing

import objects_storage


class HumanObject(objects_storage.Object):
    _width: float
    _part_ids: typing.List[int]

    def __init__(self, ctx, id: str, **kwargs):
        super().__init__(ctx, id)
        self._width = 5

        x = kwargs['x']
        y = kwargs['y']

        self._part_ids = []

        self._part_ids.append(self._ctx.canvas.create_oval(x + 13, y,
                                                           x + 28, y + 15,
                                                           width=self._width, tags=id))  # head
        self._part_ids.append(self._ctx.canvas.create_oval(x + 8, y + 15,
                                                           x + 33, y + 60,
                                                           width=self._width, tags=id))  # torso
        self._part_ids.append(self._ctx.canvas.create_line(x + 20, y + 57,
                                                           x + 8, y + 80,
                                                           width=self._width, tags=id))  # left leg
        self._part_ids.append(self._ctx.canvas.create_line(x + 24, y + 55,
                                                           x + 33, y + 80,
                                                           width=self._width, tags=id))  # right leg
        self._part_ids.append(self._ctx.canvas.create_line(x + 9, y + 25,
                                                           x, y + 50,
                                                           width=self._width, tags=id))  # left hand
        self._part_ids.append(self._ctx.canvas.create_line(x + 30, y + 25,
                                                           x + 39, y + 50,
                                                           width=self._width, tags=id))  # right hand

    def update(self, **kwargs):
        pass

    def scale(self, scale_factor: float):
        self._width *= scale_factor
        self._ctx.canvas.itemconfig(self.id, width=int(self._width))
