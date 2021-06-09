try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ModuleNotFoundError:
    pass

from xythrion.bot import Context, Xythrion

__all__ = ("Context", "Xythrion")
