import event_handlers

def create_table(ctx, table, event):
    print("hi")
    table.show_table(ctx)
    # load the table
    # show the table
    return None


def check(ctx, table, event):
    print(table.check())
    # return None