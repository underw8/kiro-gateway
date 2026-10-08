# -*- coding: utf-8 -*-

"""
Unit tests for converters_responses module.
"""

import pytest
from unittest.mock import patch

from kiro.converters_responses import build_kiro_payload
from kiro.models_responses import ResponsesRequest


class TestBuildKiroPayloadModelAliases:
    """Tests for MODEL_ALIASES resolution in the Responses API payload builder."""

    @pytest.mark.parametrize("alias,expected", [("auto-kiro", "auto"), ("claude-sonnet-4-5", "claude-sonnet-4.5")])
    def test_resolves_model_alias_before_sending(self, alias, expected):
        """
        What it does: Verifies MODEL_ALIASES is applied to the modelId sent to Kiro.
        Purpose: An advertised alias (auto-kiro) must reach Kiro as its target, not verbatim.
        """
        request = ResponsesRequest(model=alias, input="Hello")

        with patch("kiro.converters_responses.MODEL_ALIASES", {"auto-kiro": "auto"}):
            result = build_kiro_payload(request, "conv-123", "")

        assert result["conversationState"]["currentMessage"]["userInputMessage"]["modelId"] == expected
