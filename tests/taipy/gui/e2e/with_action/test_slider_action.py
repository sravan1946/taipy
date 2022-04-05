import inspect
import logging
from importlib import util

import pytest

if util.find_spec("playwright"):
    from playwright._impl._page import Page

from taipy.gui import Gui


@pytest.mark.teste2e
def test_slider_action(page: "Page", gui: Gui, helpers):
    page_md = """
<|{x}|id=text1|>

<|{x}|slider|id=slider1|>
"""
    x = 10
    gui._set_frame(inspect.currentframe())
    gui.add_page(name="test", page=page_md)
    helpers.run_e2e(gui)
    page.goto("/test")
    page.expect_websocket()
    page.wait_for_selector("#text1")
    text1 = page.query_selector("#text1")
    assert text1.inner_text() == "10"
    page.wait_for_selector("#slider1")
    page.fill("#slider1 input", "20")
    function_evaluated = True
    try:
        page.wait_for_function("document.querySelector('#text1').innerText !== '10'")
    except Exception as e:
        function_evaluated = False
        logging.getLogger().debug(f"Function evaluation timeout.\n{e}")
    if function_evaluated:
        text1_2 = page.query_selector("#text1")
        assert text1_2.inner_text() == "20"


@pytest.mark.teste2e
def test_slider_action_on_change(page: "Page", gui: Gui, helpers):
    d = {"v1": 10, "v2": 10}

    def on_change(state, var, val):
        if var == "d.v2":
            d = {"v1": 2 * val, "v2": val}
            state.d.update(d)

    page_md = """
Value: <|{d.v1}|id=text1|>

Slider: <|{d.v2}|slider|id=slider1|>
"""
    gui._set_frame(inspect.currentframe())
    gui.add_page(name="test", page=page_md)
    helpers.run_e2e(gui)
    page.goto("/test")
    page.expect_websocket()
    page.wait_for_selector("#text1")
    text1 = page.query_selector("#text1")
    assert text1.inner_text() == "10"
    page.wait_for_selector("#slider1")
    page.fill("#slider1 input", "20")
    function_evaluated = True
    try:
        page.wait_for_function("document.querySelector('#text1').innerText !== '10'")
    except Exception as e:
        function_evaluated = False
        logging.getLogger().debug(f"Function evaluation timeout.\n{e}")
    if function_evaluated:
        text1_2 = page.query_selector("#text1")
        assert text1_2.inner_text() == "40"
