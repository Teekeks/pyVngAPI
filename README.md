# VNG-API

A async API client for the game "[Von Neumann Game](https://neumann-probe.net)" by Gnieark

## Example use

Start crafting Steel Bars with all free mannies on Probe with ID `420`
```python
from vng_api.client import APIClient
import asyncio

async def main():
    client = APIClient('my_token')
    # get all mannies of the probe with ID 420
    ret, mannies = await client.probe.manny.get_all(420)
    # check if the API call was successfull
    if not ret.success:
        raise Exception(f'Failed to get mannies of probe: {ret.error_code}: {ret.error_message}')
    # create context manager for mannie tasks on probe 420
    tasks = client.probe.manny.tasks(420)
    async with tasks:
        # queue the crafting task for each manny
        for manny in mannies.values():
            if manny.currentTask is None and manny.location.type == 'probe':
                await tasks.craft(manny.id, 'steel_bar')
    # check if the API calls of the task batching where successfull
    if not tasks.results.success:
        # get the batches that failed and compile error message
        failed = filter(lambda inp: not inp.success, tasks.results.responses)
        raise Exception(f'Failed to tasks mannies:\n{'\n'.join([f'- {f.error_code}: {f.error_message}' for f in failed])}')

asyncio.run(main())
```

## Basic Principles

TODO
