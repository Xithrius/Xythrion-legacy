    @comms.command()
    async def create_cog(self, ctx, new_cog):
        good_cog = False
        while not good_cog:
            cog_type = input('Type of cog (rack, requester, detector): ')
            cog_name = input('Name of the cog: ')
            if cog_type in ['rack', 'requester', 'detector']:
                good_cog = True
        cog_name = cog_name.lower()
        cog_file = f'{cog_name}.py'
        shutil.copy2(path('automation', 'template.py'), path('automation', 'new_cogs', cog_file))
        replacedata = {
            'placeholder_type': f'{cog_type.title()} cog for {cog_name.title()}',
            'PLACEHOLDER_COG': f'{cog_name.title()}_{cog_type.title()}',
            'PLACEHOLDER': cog_name.upper(),
            'Placeholder': cog_name.title(),
            'placeholder': cog_name
        }
        with open(path('automation', 'new_cogs', cog_file), 'r') as f:
            filedata = f.read()
            for k, v in replacedata.items():
                filedata = filedata.replace(k, v)
        with open(path('automation', 'new_cogs', cog_file), 'w') as f:
            f.write(filedata)