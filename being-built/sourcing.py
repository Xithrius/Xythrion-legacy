@comms.command()
async def source(self, ctx, url: None):
        """Gets the source for an image

        Args:
            url (str): if none, url is extracted from context.
        
        Returns:
            An embed with the source(s) of the image.

        Raises:
            An error when sauce cannot be found or server cannot be reached.

        """
        if len(ctx.message.attachments) > 1:
            raise ValueError('Cannot get more than one image at a time.')

        url = f'http://saucenao.com/search.php?db=999&url={url}'

        async with self.bot.session.get(url) as r:
            assert r.status == 200
            t = await r.text()
            func = functools.partial(self.bot.html_parser, t)
            info = await self.bot.loop.run_in_executor(None, func)
