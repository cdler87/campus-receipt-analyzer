SYSTEM_PROMPT = """
Extract structured purchase receipt information from Duke university mobile order emails.
Return valid JSON only.
""".strip()

ZERO_SHOT_PROMPT = """
Extract the following fields from this receipt email:
- vendor
- timestamp
- location
- items: list of {{name, quantity, price}}
- subtotal
- tax
- total

If a field is missing, return null.
Return valid JSON only.

EMAIL:
{email_text}
""".strip()

FEW_SHOT_PROMPT = """
Extract receipt information and return valid JSON only.

Example:
EMAIL:
Thanks for your mobile order at Bella Union.
1 Latte $4.50
1 Blueberry Muffin $3.25
Tax $0.55
Total $8.30
Ordered at 2026-03-12 09:14 AM

JSON:
{{
  "vendor": "Bella Union",
  "timestamp": "2026-03-12T09:14:00",
  "location": "Bella Union",
  "items": [
    {{"name": "Latte", "quantity": 1, "price": 4.50}},
    {{"name": "Blueberry Muffin", "quantity": 1, "price": 3.25}}
  ],
  "subtotal": 7.75,
  "tax": 0.55,
  "total": 8.30
}}

EMAIL:
{email_text}
""".strip()

STRICT_JSON_PROMPT = """
You must return ONLY valid JSON matching this schema:
{{
  "vendor": str | null,
  "timestamp": str | null,
  "location": str | null,
  "items": [{{"name": str, "quantity": int | null, "price": float | null}}],
  "subtotal": float | null,
  "tax": float | null,
  "total": float | null
}}

EMAIL:
{email_text}
""".strip()
