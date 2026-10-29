# VNG-API

A async API client for the game "[Von Neumann Game](https://neumann-probe.net)" by Gnieark

This library implements both the normal user API as well as the Others NPC API.

## Basic Principles

### Statistics

`APIClient.stats` keeps a up to date list of statistics as reported by the API, this includes the current remaining calls in the rate limit bucket as well as the total bucket size.

### APIResponse

Almost all requests return a `vng_api.base.APIResponse` object.
You can check if your request suceeded by checking the `success` value. The data that was returned is put into `data`.
You can also use var unpacking on APIResponse to get both the normal APIResponse object and the contents of `data` at the same time.

The general HTTP response code can be acessed via `status`.

Example:
```python
ret, version = await client.version()
# raise exception if the api call failed
ret.may_raise()
print(ret.suceess)
# -> True
print(version)
# -> 140
# var unpacking still leaves the data in the original object untouched and can be acessed as normal:
print(ret.data)
# -> 140
print(ret.status)
# -> 200
```

In case of a unsucessfull API call, you can use `error_code` and `error_message` to get the reason.  
Note that Error 500, 503 and similar will leave those fields empty.

You may use `APIResponse.may_rise()` to raise a descriptive exception whenever a API call failed.

### APIBatchResult

In the case of batched requests (as used by `APIClient.probe.manny.tasks()`), it will return a `vng_api.base.APIBatchResult` object.
This behaves similar to `APIResponse` in that the overall success of the batch is checkable via `success`.

The individual `APIResponse` objects of each API call in the batch are stored in `responses`.


## Example use

Following are some complete example usages for the library.

### Batch crafting

Start crafting Steel Bars with all free mannies on Probe with ID `420`
```python
from vng_api.client import APIClient
import asyncio

async def main():
    client = APIClient('my_token')
    # get all mannies of the probe with ID 420
    ret, mannies = await client.probe.manny.get_all(420)
    # raise exception if api call failed
    ret.may_rise()
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

### Sector searching

Will search the current sector of probe `420` for any object with minable `deuterium`

```python
from vng_api.client import APIClient
from vng_api.helper import get_manny_minable
import asyncio

async def main():
    client = APIClient('my_token')
    ret, sector_response = await client.probe.sector.get(420)
    ret.may_rise()
    found = False
    # use helper function to extract minable objects from sector observation
    minable_objects = get_manny_minable(sector_response.sector)
    # look through objects to search for the ones with deuterium
    for mo in minable_objects:
        if mo.resourceAmounts is not None:
            if mo.ResourceAmounts.deuterium > 0:
                print(f'object {mo.id} of type {mo.type} has {mo.resourceAmounts.deuterium:.2f} deuterium!')
                found = True
    if not found:
        print('no deuterium in this system :(')
    
asyncio.run(main())
```

### Others NPCs

This will start a resource harvest on the first available planet with all available auxiliaries.  
Note that for simplicity this example will assume that all auxiliaries are free and that you already know the ID of your fleet.

```python
from vng_api.client import APIClient
from vng_api.types.others import OthersShip
from vng_api.helper import get_harvestable
import asyncio
from pprint import pprint

async def main():
    client = APIClient('my_token')
    # get fleet ships
    ret, fleet_info = await client.others.fleet.get('my_fleet_id')
    ret.may_rise()
    # find mothership in list
    mothership: OthersShip = list(filter(lambda f: f.type == 'mothership', fleet_info.ships))[0]
    # ensure that mothership is in sector
    assert mothership.location.state == 'in_sector'
    # get first available harvestable planet
    ret = await client.others.sector.get(mothership.id, mothership.sector.relative)
    ret.may_rise()
    # use helper function to extract all harvestable sector objects from sector observation
    planets = get_harvestable(ret.data)
    assert len(planets) > 0
    # start harvest
    ret, action = await client.others.ship.harvest(mothership.id, planets[0].id, mothership.auxiliaryCount)
    ret.may_rise()
    pprint(action)
    
asyncio.run(main())
```
