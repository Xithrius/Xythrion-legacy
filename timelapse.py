import imageio
import click


@click.command()
@click.argument('inFile', type=click.Path(exists=True))
@click.argument('outFile', type=click.Path())
@click.argument('factor', type=click.FLOAT)
def cli(infile, outfile, factor):
    vid = imageio.get_reader(infile, 'ffmpeg')

    fps = vid.get_meta_data()['fps']

    writer = imageio.get_writer(outfile, fps=fps)

    buildUp = factor

    for i, f in enumerate(vid):
        if buildUp >= factor:
            writer.append_data(f)
            buildUp -= factor
        buildUp += 1

    writer.close()

# @click.command()
# @click.argument('value')
# def cli(value):
#     print(value)


if __name__ == '__main__':
    cli()

