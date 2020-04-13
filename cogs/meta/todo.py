"""
> Xythrion
> Copyright (c) 2020 Xithrius
> MIT license, Refer to LICENSE for more info
"""


from datetime import datetime
import typing as t

from discord.ext import commands as comms

from modules import quick_block


class Todo(comms.Cog):
    """Saving people's things that they need to do in the database.

    Attributes:
        bot (:obj:`comms.Bot`): Represents a Discord bot.

    """

    def __init__(self, bot):
        """Creating important attributes for this class.

        Args:
            bot (:obj:`comms.Bot`): Represents a Discord bot.

        """
        self.bot = bot

    @comms.group()
    async def todo(self, ctx):
        """The group command for todo.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]todo [subcommand]

        """
        if ctx.invoked_subcommand is None:
            await ctx.send('`Invalid todo command passed.`')

    @todo.command(aliases=['insert'])
    async def add(self, ctx, todo_lst_name: str, *, item: str):
        """Creates a todo if one doesn't exist, and adds an entry to that todo.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            todo_lst_name (str): The name of the todo to be created or for an item to be inserted into.
            item (str): The item(s) that the todo will recieve (split by a newline).

        Command examples:
            >>> [prefix]todo add "stuff and things" Do this tomorrow.
            >>> [prefix]todo add nope nah

        """
        item = item.split('\n')
        item = [item] if not isinstance(item, list) else item
        async with self.bot.pool.acquire() as conn:
            todos = await conn.fetch(
                '''SELECT todo_lst_name, lst FROM Todos WHERE id = $1''',
                ctx.author.id
            )
            if len(todos) == 10:
                await ctx.send('`You have reached maximum amount of todo lists (10).`')

            # Update an existing todo
            elif todo_lst_name in [x['todo_lst_name'] for x in todos]:
                lst = [t['lst'] for t in todos if t['todo_lst_name'] == todo_lst_name][0]
                if len(lst) == 30:
                    return await ctx.send('`Cannot update list anymore, max entries hit (30).`')

                lst.extend(item)
                await conn.execute(
                    '''UPDATE Todos SET t_updated = $3, lst = $4 WHERE id = $1 AND todo_lst_name = $2''',
                    ctx.author.id, todo_lst_name, datetime.now(), lst
                )

            # Create a new todo
            else:
                await conn.execute(
                    '''INSERT INTO Todos(
                        t_creation, t_updated, id, todo_lst_name, lst) VALUES ($1, $2, $3, $4, $5)''',
                    datetime.now(), datetime.now(), ctx.author.id, todo_lst_name, item
                )

    @todo.command(aliases=['remove', 'uninsert'])
    async def delete(self, ctx, todo_lst_name: str, *, item: t.Union[str, int]):
        """Deletes a entry from a todo, and if there are none left, the todo is deleted.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            todo_lst_name (str): The name of the todo to have a specific entry deleted from.
            item (:obj:`t.Union[str, int]`): The index of the entry or the index of the entry within the todo.

        Command examples:
            >>> [prefix]todo delete "stuff and things" Do this tomorrow.
            >>> [prefix]todo delete nope nah

        """
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT lst FROM Todos WHERE id = $1 AND todo_lst_name = $2''',
                ctx.author.id, todo_lst_name
            )

            if len(info):
                lst = info[0]['lst']
                try:
                    if not item.isdigit():
                        lst.pop(lst.index(item))
                    else:
                        lst.pop(int(item))

                    # Updating todo with removed item.
                    if len(lst):
                        await conn.execute(
                            '''UPDATE Todos SET t_updated = $3, lst = $4
                            WHERE id = $1 AND todo_lst_name = $2''',
                            ctx.author.id, todo_lst_name, datetime.now(), lst
                        )

                    # If the todo is empty
                    else:
                        await conn.execute(
                            '''DELETE FROM Todos WHERE id = $1 AND todo_lst_name = $2''',
                            ctx.author.id, todo_lst_name
                        )
                        return await ctx.send(
                            f'`Todo "{todo_lst_name}" automatically deleted because of emptyness.`')

                except IndexError:
                    return await ctx.send('`Could not locate and delete entry within todo.`')

            await ctx.send(f'`Could not find todo named "{todo_lst_name}"`')

    @todo.command()
    async def view(self, ctx, todo_lst_name: str):
        """Views the items within a specific todo.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.
            todo_lst_name (str): The name of the todo to be viewed.

        Command examples:
            >>> [prefix]todo view "stuff and things"
            >>> [prefix]todo view nope

        """
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT lst FROM Todos WHERE id = $1 AND todo_lst_name = $2''',
                ctx.author.id, todo_lst_name
            )

        if len(info):
            info = info[0]['lst']
            block = await quick_block(
                [[x.replace("'", '')] for x in info], title=f'Todo "{todo_lst_name}":', index=True)
            return await ctx.send(block)

        await ctx.send(f'`Could not find todo named "{todo_lst_name}"`')

    @todo.command(name='list')
    async def _list(self, ctx):
        """Lists all the todos that belong to you.

        Args:
            ctx (:obj:`comms.Context`): Represents the context in which a command is being invoked under.

        Command examples:
            >>> [prefix]todo list

        """
        async with self.bot.pool.acquire() as conn:
            info = await conn.fetch(
                '''SELECT todo_lst_name, lst FROM Todos WHERE id = $1''',
                ctx.author.id
            )

        if len(info):
            info = {x['todo_lst_name']: len(x['lst']) for x in info}
            block = await quick_block(info, ['Todo', 'Length'])
            return await ctx.send(block)

        await ctx.send('`You do not own any todos.`')


def setup(bot):
    bot.add_cog(Todo(bot))
