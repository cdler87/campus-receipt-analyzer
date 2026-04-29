from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Dict, List

from openai import OpenAI

from config.prompts import ZERO_SHOT_PROMPT, FEW_SHOT_PROMPT, SYSTEM_PROMPT
from src.parse.schema import ParsedReceipt


@dataclass
class ReceiptParser:
    api_key: str
    model_name: str

    def build_prompt(self, email_text: str, prompt_template: str = FEW_SHOT_PROMPT) -> str:
        return prompt_template.format(email_text=email_text)

    from openai import OpenAI

    def call_llm(self, prompt: str) -> str:
        client = OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0
        )

        return response.choices[0].message.content


    def parse_receipt(self, email: Dict, prompt_template: str = FEW_SHOT_PROMPT) -> Dict:
        prompt = self.build_prompt(email.get("body_text", ""), prompt_template)
        raw_output = self.call_llm(prompt)

        try:
            parsed_json = json.loads(raw_output)
            parsed_json["message_id"] = email["message_id"]
            parsed_json["parse_success"] = True
            parsed_json["raw_model_output"] = raw_output
            validated = ParsedReceipt(**parsed_json)
            return validated.model_dump()
        except Exception:
            return {
                "message_id": email.get("message_id"),
                "vendor": None,
                "timestamp": None,
                "location": None,
                "items": [],
                "subtotal": None,
                "tax": None,
                "total": None,
                "parse_success": False,
                "raw_model_output": raw_output,
            }

    def parse_batch(self, emails: List[Dict], prompt_template: str = FEW_SHOT_PROMPT) -> List[Dict]:
        return [self.parse_receipt(email, prompt_template) for email in emails]
