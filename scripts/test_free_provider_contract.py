#!/usr/bin/env python3
"""No-network, no-key contract tests for opt-in SSE provider smoke tool."""
import io
import unittest
from free_provider_contract import sse_data_lines, extract_text, MODELS

class ProviderContractTests(unittest.TestCase):
    def test_openrouter_free_id(self):
        self.assertEqual(MODELS["openrouter"], "openrouter/free")

    def test_current_gemini_id(self):
        self.assertEqual(MODELS["gemini"], "gemini-3.5-flash-lite")

    def test_groq_id(self):
        self.assertEqual(MODELS["groq"], "openai/gpt-oss-20b")

    def test_openai_compatible_stream(self):
        data = {"choices":[{"delta":{"content":"hello"}}]}
        self.assertEqual(extract_text("groq", data), "hello")
        self.assertEqual(extract_text("openrouter", data), "hello")

    def test_google_native_stream(self):
        data = {"candidates":[{"content":{"parts":[{"text":"Hi"},{"text":" there"}]}}]}
        self.assertEqual(extract_text("gemini", data), "Hi there")

    def test_sse_parser_skips_comments(self):
        raw = io.BytesIO(b': keep alive\n\nevent: message\ndata: {"x":1}\n\ndata: [DONE]\n\n')
        self.assertEqual(list(sse_data_lines(raw)), ['{"x":1}', "[DONE]"])

if __name__=="__main__":
    unittest.main()
