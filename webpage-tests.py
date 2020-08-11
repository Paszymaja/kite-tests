import pytest

from scripts import drivers_setup

# needed for pytest fixtures
driver_init = drivers_setup.driver_init


@pytest.mark.usefixtures('driver_init')
class TestWebpage:
    pass
