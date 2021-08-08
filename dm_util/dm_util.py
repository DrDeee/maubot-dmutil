from maubot import Plugin
from maubot.handlers import event
from mautrix.types import EventType, StateEvent, Membership, RoomID


class DMUtilPlugin(Plugin):
    async def start(self) -> None:
        rooms = await self.client.get_joined_rooms()
        for room in rooms:
            await self.check_room_members(room)

    @event.on(EventType.ROOM_MEMBER)
    async def on_room_member(self, evt: StateEvent):
        if evt.content.membership == Membership.LEAVE and evt.state_key != self.client.mxid:
            await self.check_room_members(evt.room_id)

    async def check_room_members(self, room: RoomID):
        all_members = await self.client.get_members(room)
        members = []
        for member in all_members:
            if member.content.membership == Membership.JOIN and member.state_key != self.client.mxid:
                members.append(member)
        if len(members) == 0:
            await self.client.leave_room(room)
            self.log.debug(f"Leaving room {room}: No more members")
