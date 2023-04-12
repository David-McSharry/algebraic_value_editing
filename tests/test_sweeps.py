""" Test suite for sweeps.py """

# %%
import pickle

import pytest
import numpy as np
import pandas as pd

from transformer_lens import HookedTransformer

from algebraic_value_editing import sweeps
from algebraic_value_editing import prompt_utils
from algebraic_value_editing.prompt_utils import RichPrompt

try:
    from IPython import get_ipython

    get_ipython().run_line_magic("reload_ext", "autoreload")
    get_ipython().run_line_magic("autoreload", "2")
except AttributeError:
    pass

# Filename for pre-pickled assets
SWEEP_OVER_PROMPTS_CACHE_FN = "tests/sweep_over_prompts_cache.pkl"


@pytest.fixture(name="model")
def fixture_model() -> HookedTransformer:
    """Test fixture that returns a small pre-trained transformer used
    for fast sweep testing."""
    return HookedTransformer.from_pretrained(
        model_name="attn-only-2l", device="cpu"
    )


def test_make_rich_prompts():
    """Test for make_rich_prompts() function.  Provides a simple set of
    phrases+coeffs, activation names and additional coeffs that the
    function under test will expand into all permutations, in the style
    of np.ndgrid.  The return value is compared against a pre-prepared
    reference output."""
    # Call the function under test
    rich_prompts_df = sweeps.make_rich_prompts(
        [[("Good", 1.0), ("Bad", -1.0)], [("Amazing", 2.0)]],
        [prompt_utils.get_block_name(block_num=num) for num in [6, 7, 8]],
        np.array([1.0, 5, 10.0, 20.0]),
    )
    # Compre to pre-defined target
    pd.testing.assert_frame_equal(rich_prompts_df, MAKE_RICH_PROMPTS_TARGET)


def test_sweep_over_prompts(model):
    """Test for sweep_over_prompts().  Uses a toy model fixture, passes
    a handful of RichPrompts and prompts, and compares results to a
    pre-cached reference output."""
    act_name = prompt_utils.get_block_name(block_num=0)
    normal_df, patched_df = sweeps.sweep_over_prompts(
        model,
        [
            "Roses are red, violets are blue",
            "The most powerful emotion is",
            "I feel",
        ],
        [
            [
                RichPrompt(1.0, act_name, "Love"),
                RichPrompt(-1.0, act_name, "Fear"),
            ],
            [
                RichPrompt(10.0, act_name, "Love"),
                RichPrompt(-10.0, act_name, "Fear"),
            ],
        ],
        num_normal_completions=4,
        num_patched_completions=4,
        seed=42,
    )
    with open(SWEEP_OVER_PROMPTS_CACHE_FN, "rb") as file:
        normal_target, patched_target = pickle.load(file)
    pd.testing.assert_frame_equal(normal_df, normal_target)
    pd.testing.assert_frame_equal(patched_df, patched_target)


# Assets
MAKE_RICH_PROMPTS_TARGET = pd.DataFrame(
    {
        "rich_prompts": [
            [
                RichPrompt(
                    prompt="Good",
                    coeff=1.0,
                    act_name="blocks.6.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-1.0,
                    act_name="blocks.6.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=5.0,
                    act_name="blocks.6.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-5.0,
                    act_name="blocks.6.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=10.0,
                    act_name="blocks.6.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-10.0,
                    act_name="blocks.6.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=20.0,
                    act_name="blocks.6.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-20.0,
                    act_name="blocks.6.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=1.0,
                    act_name="blocks.7.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-1.0,
                    act_name="blocks.7.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=5.0,
                    act_name="blocks.7.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-5.0,
                    act_name="blocks.7.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=10.0,
                    act_name="blocks.7.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-10.0,
                    act_name="blocks.7.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=20.0,
                    act_name="blocks.7.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-20.0,
                    act_name="blocks.7.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=1.0,
                    act_name="blocks.8.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-1.0,
                    act_name="blocks.8.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=5.0,
                    act_name="blocks.8.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-5.0,
                    act_name="blocks.8.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=10.0,
                    act_name="blocks.8.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-10.0,
                    act_name="blocks.8.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Good",
                    coeff=20.0,
                    act_name="blocks.8.hook_resid_pre",
                ),
                RichPrompt(
                    prompt="Bad",
                    coeff=-20.0,
                    act_name="blocks.8.hook_resid_pre",
                ),
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=2.0,
                    act_name="blocks.6.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=10.0,
                    act_name="blocks.6.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=20.0,
                    act_name="blocks.6.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=40.0,
                    act_name="blocks.6.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=2.0,
                    act_name="blocks.7.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=10.0,
                    act_name="blocks.7.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=20.0,
                    act_name="blocks.7.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=40.0,
                    act_name="blocks.7.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=2.0,
                    act_name="blocks.8.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=10.0,
                    act_name="blocks.8.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=20.0,
                    act_name="blocks.8.hook_resid_pre",
                )
            ],
            [
                RichPrompt(
                    prompt="Amazing",
                    coeff=40.0,
                    act_name="blocks.8.hook_resid_pre",
                )
            ],
        ],
        "phrases": [
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Good", 1.0), ("Bad", -1.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
            [("Amazing", 2.0)],
        ],
        "act_name": [
            "blocks.6.hook_resid_pre",
            "blocks.6.hook_resid_pre",
            "blocks.6.hook_resid_pre",
            "blocks.6.hook_resid_pre",
            "blocks.7.hook_resid_pre",
            "blocks.7.hook_resid_pre",
            "blocks.7.hook_resid_pre",
            "blocks.7.hook_resid_pre",
            "blocks.8.hook_resid_pre",
            "blocks.8.hook_resid_pre",
            "blocks.8.hook_resid_pre",
            "blocks.8.hook_resid_pre",
            "blocks.6.hook_resid_pre",
            "blocks.6.hook_resid_pre",
            "blocks.6.hook_resid_pre",
            "blocks.6.hook_resid_pre",
            "blocks.7.hook_resid_pre",
            "blocks.7.hook_resid_pre",
            "blocks.7.hook_resid_pre",
            "blocks.7.hook_resid_pre",
            "blocks.8.hook_resid_pre",
            "blocks.8.hook_resid_pre",
            "blocks.8.hook_resid_pre",
            "blocks.8.hook_resid_pre",
        ],
        "coeff": [
            1.0,
            5.0,
            10.0,
            20.0,
            1.0,
            5.0,
            10.0,
            20.0,
            1.0,
            5.0,
            10.0,
            20.0,
            1.0,
            5.0,
            10.0,
            20.0,
            1.0,
            5.0,
            10.0,
            20.0,
            1.0,
            5.0,
            10.0,
            20.0,
        ],
    }
)
