# Copyright (c) Simon Niederberger.
# Distributed under the terms of the MIT License.

import pytest


@pytest.fixture(autouse=True)
def reset_fn_interact_globals():
    """Clear global singletons between tests to prevent cross-test pollution."""
    from dash_fn_form._forms import _registered_config_ids
    from dash_fn_form._renderers import _RENDERERS

    before_ids = set(_registered_config_ids)
    before_renderers = dict(_RENDERERS)

    yield

    _registered_config_ids.clear()
    _registered_config_ids.update(before_ids)
    _RENDERERS.clear()
    _RENDERERS.update(before_renderers)
