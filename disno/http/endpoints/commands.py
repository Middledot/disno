"""
MIT License

Copyright (c) 2021-present Qwire Development Team

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from ..route import Route


class ApplicationCommandEndpoints:
    def get_global_application_commands(self, application_id: int):
        r = Route("GET", "/applications/{application_id}/commands", application_id=application_id)
        return self.request(r)

    def get_global_application_command(self, application_id: int, command_id: int):
        r = Route("GET", "/applications/{application_id}/commands/{command_id}", application_id=application_id, command_id=command_id)
        return self.request(r)

    def upsert_global_application_command(
        self,
        application_id: int,
        *,
        name: str,
        description: str,
        options = None,
        default_permission: bool = True,
        type: int = 1
    ):
        r = Route("POST", "/applications/{application_id}/commands", application_id=application_id)
        payload = {
            "name": str(name),
            "description": str(description),
            "options": options,
            "default_permission": int(default_permission),
            "type": int(type),
        }

        return self.request(r, payload=payload)

    def edit_global_application_command(
        self,
        application_id: int,
        *,
        name: str,
        description: str,
        options = None,
        default_permission: bool = True,
    ):
        r = Route("PATCH", "/applications/{application_id}/commands", application_id=application_id)
        payload = {
            "name": str(name),
            "description": str(description),
            "options": options,
            "default_permission": int(default_permission),
        }

        return self.request(r, payload=payload)

    def delete_global_application_command(self, application_id: int, command_id: int):
        r = Route("DELETE", "/applications/{application_id}/commands/{command_id}", application_id=application_id, command_id=command_id)
        return self.request(r)

    def bulk_overwrite_global_application_commands(self, application_id: int, *, commands):
        r = Route("PUT", "/applications/{application_id}/commands", application_id=application_id)
        return self.request(r, payload=commands)

    def get_guild_application_commands(self, application_id: int, guild_id: int):
        r = Route("GET", "/applications/{application_id}/guilds/{guild_id}/commands", application_id=application_id, guild_id=guild_id)
        return self.request(r)

    def get_guild_application_command(self, application_id: int, guild_id: int, command_id: int):
        r = Route("GET", "/applications/{application_id}/guilds/{guild_id}/commands/{command_id}", application_id=application_id, guild_id=guild_id, command_id=command_id)
        return self.request(r)

    def upsert_guild_application_command(
        self,
        application_id: int,
        guild_id: int,
        *,
        name: str,
        description: str,
        options = None,
        default_permission: bool = True,
        type: int = 1
    ):
        r = Route("POST", "/applications/{application_id}/guilds/{guild_id}/commands", application_id=application_id, guild_id=guild_id)
        payload = {
            "name": str(name),
            "description": str(description),
            "options": options,
            "default_permission": int(default_permission),
            "type": int(type),
        }

        return self.request(r, payload=payload)

    def edit_guild_application_command(
        self,
        application_id: int,
        guild_id: int,
        command_id: int,
        *,
        name: str,
        description: str,
        options = None,
        default_permission: bool = True,
    ):
        r = Route("PATCH", "/applications/{application_id}/guilds/{guild_id}/commands", application_id=application_id, guild_id=guild_id, command_id=command_id)
        payload = {
            "name": str(name),
            "description": str(description),
            "options": options,
            "default_permission": int(default_permission),
        }

        return self.request(r, payload=payload)

    def delete_guild_application_command(self, application_id: int, guild_id: int, command_id: int):
        r = Route("DELETE", "/applications/{application_id}/guilds/{guild_id}/commands/{command_id}", application_id=application_id, guild_id=guild_id, command_id=command_id)
        return self.request(r)

    def bulk_overwrite_guild_application_commands(self, application_id: int, guild_id: int, *, commands = []):
        r = Route("PUT", "/applications/{application_id}/guilds/{guild_id}/commands", application_id=application_id, guild_id=guild_id)
        return self.request(r, payload=commands)

    def get_guild_application_command_permissions(self, application_id: int, guild_id: int):
        r = Route("GET", "/applications/{application_id}/guilds/{guild_id}/commands/permissions", application_id=application_id, guild_id=guild_id)
        return self.request(r)

    def get_all_guild_application_commands_permissions(self, application_id: int, guild_id: int, command_id: int):
        r = Route("GET", "/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions", application_id=application_id, guild_id=guild_id, command_id=command_id)
        return self.request(r)

    def upsert_guild_application_command_permissions(
        self,
        application_id: int,
        guild_id: int,
        command_id: int,
        *,
        permissions
    ):
        r = Route("PUT", "/applications/{application_id}/guilds/{guild_id}/commands/{command_id}/permissions", application_id=application_id, guild_id=guild_id, command_id=command_id)
        return self.request(r, payload=permissions)

    def bulk_overwrite_guild_application_command_permissions(
        self,
        application_id: int,
        guild_id: int,
        *,
        permissions
    ):
        r = Route("PUT", "/applications/{application_id}/guilds/{guild_id}/commands/permissions", application_id=application_id, guild_id=guild_id)
        return self.request(r, payload=permissions)
