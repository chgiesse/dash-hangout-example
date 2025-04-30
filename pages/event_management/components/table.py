from ..models import EventsModel

from typing import List
import dash_mantine_components as dmc 


def create_events_table(events: List[EventsModel]):

    create_avatar = lambda name: dmc.Avatar(name, radius='xl')

    head = dmc.TableThead(dmc.TableTr(
        [dmc.TableTh(name) for name in EventsModel.get_column_names()] + [dmc.TableTh('Action')]
    ))
    rows = []
    for event in events:
        parties = dmc.AvatarGroup([create_avatar(name) for name in event.participants])
        row = dmc.TableTr([
            dmc.TableTd(event.id),
            dmc.TableTd(event.name),
            dmc.TableTd(event.location),
            dmc.TableTd(event.date),
            dmc.TableTd(parties),
            dmc.TableTd(dmc.Anchor('Open', href=f'/events/{event.id}'))
        ])
        rows.append(row)

    body = dmc.TableTbody(rows)
    table = dmc.Table(
        [head, body],
        highlightOnHover=True,
        withTableBorder=False,
        withColumnBorders=False
    )
    return table