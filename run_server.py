from asyncio import get_event_loop

from todobackend import init

loop = get_event_loop()
loop.run_until_complete(init(loop))

try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
