from api.sql_operator import db_operator
from api.models.events import Event, EventInfo, Participant
from .models import EventFormModel

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime


@db_operator(verbose=True)
async def add_event(db: AsyncSession, form: EventFormModel):
    event = EventInfo(
        EventName = form.name,
        EventLocation = form.location,
        EventDate = form.date,
        CreateDate = datetime.now(),
        CreatedBy = 'Me - this should be the current user defined by the Session'
    )
    
    try:
        db.add(event)
        await db.commit()
    
    except Exception as e:
        return e

    return True     


@db_operator(verbose=True)
async def get_events(db: AsyncSession, search_value: int | str):
    query = (
        select(
            EventInfo.EventId
            , EventInfo.EventName
            , EventInfo.EventLocation
            , EventInfo.EventDate
            , func.array_agg(Participant.LastName)
        )
        .select_from(EventInfo)
        .join(Event, EventInfo.EventId == Event.EventId, full=True)
        .join(Participant, Event.UserId == Participant.UserId, full=True)
        .group_by(EventInfo.EventId, EventInfo.EventName, EventInfo.EventLocation, EventInfo.EventDate)
    )
    print('search_value', search_value, type(search_value), flush=True)
    if isinstance(search_value, int):
        query = query.filter(EventInfo.EventId == search_value)
    
    if isinstance(search_value, str):
        query = query.filter(EventInfo.EventName.ilike(f'%{search_value}%'))

    result = await db.execute(query)
    data = result.fetchall()
    return data