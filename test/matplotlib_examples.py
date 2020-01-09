def adv_python():
    # x[6] and x[8] are tuition and fees and room and board costs, so x[0] and x[2] removes fees and tuition
    plt.plot([(x[6] - x[0]) for x in self.arr], '-o', label='Private 4-year', markevery=1)
    plt.plot([(x[8] - x[2]) for x in self.arr], '-o', label='Public 4-year', markevery=1)
    plt.xticks(np.arange(0, int(self.arr.shape[0])), np.arange(self.start_year, self.end_year + 1, 1), rotation='vertical')
    plt.subplots_adjust(bottom=0.15)
    plt.title("Room and board trend")
    plt.legend(loc='best')
    plt.xlabel("Year")
    plt.ylabel("Room and board cost (dollars)")

    indexes = (np.where(np.arange(self.start_year, self.end_year + 1) == year))[0][-1]
    arr = self.arr[indexes - 3:indexes + 1, 0:9:2]
    # Costs include tuition, fees, room, and board
    public = arr[0:4, 3]
    private = arr[0:4, 4]
    # 2 year public added to 2 year public and 2 year private
    publicAndPublic = np.concatenate((arr[0:2, 2], arr[2:4, 3]))
    publicAndPrivate = np.concatenate((arr[0:2, 2], arr[2:4, 4]))

    for k, v in {'Public 4-year': public, 'Private 4-year': private, 'Public 2-year and public 4-year': publicAndPublic, 'Public 2-year and private 4-year': publicAndPrivate}.items():
        plt.plot(v, '-o', label=k, markevery=1)

    plt.xticks(np.arange(0, 4), np.arange(year - 3, year + 1, 1), rotation='vertical')
    plt.subplots_adjust(bottom=0.15)
    plt.title("Tuition, fees, room, and board cost trend")
    plt.legend(loc='best')
    plt.xlabel("Year")
    plt.ylabel("Tuition, fees, room, and board cost (dollars)")


def old_weather():
    dates = [[v for k, v in _dict.items() if k in requests] for _dict in info]
    highs = [x[1] for x in dates]
    lows = [x[2] for x in dates]
    plt.plot([x[0] for x in dates], highs, linestyle='solid', label="high")
    plt.plot([x[0] for x in dates], lows, linestyle='solid', label="low")
    max_temp, min_temp = max(highs), min(lows)
    plt.xticks(rotation='vertical')
    plt.yticks(ticks=np.arange(min_temp, max_temp + 1, 5))
    plt.legend()
    plt.grid()
    plt.xlabel("Date")
    plt.ylabel("Temperature (°F)")
    plt.title(f"Zip {zip_code}, {country}: High/low temperatures")
    plt.gcf().autofmt_xdate()
    filename = get_filename(ctx.message.author.id, '.png')
    plt.savefig(path('repository', 'tmp', filename))
    plt.clf()
    await ctx.send(file=discord.File(path('repository', 'tmp', filename)))
    os.remove(path('repository', 'tmp', filename))