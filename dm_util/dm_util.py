from maubot import Plugin
from maubot.handlers import event
from mautrix.errors import MNotFound
from mautrix.types import EventType, StateEvent, Membership, RoomID


class DMUtilPlugin(Plugin):
    async def start(self) -> None:
        rooms = await self.client.get_joined_rooms()
        for room in rooms:
            await self.check_room_members(room)

    @event.on(EventType.ROOM_MEMBER)
    async def on_room_member(self, evt: StateEvent):
        if evt.content.membership == Membership.INVITE and evt.content.is_direct:
            try:
                direct = await self.client.get_account_data(EventType.DIRECT)
            except MNotFound:
                direct = {}
            if evt.sender not in direct:
                direct[evt.sender] = []
            if evt.room_id not in direct[evt.sender]:
                direct[evt.sender].append(evt.room_id)
                await self.client.set_account_data(EventType.DIRECT, direct)
                self.log.debug(f"Joined new DM room: {evt.room_id}")

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
            account_data = await self.client.get_account_data(EventType.DIRECT)
            for user in account_data:
                if room in user:
                    account_data[user].remove(room)
                    if len(account_data[user]) == 0:
                        del account_data[user]
            self.client.set_account_data(EventType.DIRECT, account_data)
