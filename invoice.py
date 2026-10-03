#!/usr/bin/env python3
from __future__ import annotations
from dataclasses import dataclass
import argparse
import json
from pathlib import Path


@dataclass
class LineItem:
    name: str
    qty: float
    unit_price: float

    @property
    def subtotal(self) -> float:
        return self.qty * self.unit_price


def calc(items: list[LineItem], vat_rate: float = 0.15, discount: float = 0.0) -> dict:
    subtotal = sum(i.subtotal for i in items)
    discount_amount = subtotal * discount
    taxable = subtotal - discount_amount
    vat = taxable * vat_rate
    total = taxable + vat
    return {
        "subtotal": round(subtotal, 2),
        "discount": round(discount_amount, 2),
        "vat": round(vat, 2),
        "total": round(total, 2),
        "items": [
            {
                "name": i.name,
                "qty": i.qty,
                "unit_price": i.unit_price,
                "line_total": round(i.subtotal, 2),
            }
            for i in items
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", default="sample_invoice.json")
    parser.add_argument("--vat", type=float, default=0.15)
    parser.add_argument("--discount", type=float, default=0.0)
    args = parser.parse_args()
    payload = json.loads(Path(args.file).read_text(encoding="utf-8"))
    items = [LineItem(**row) for row in payload["items"]]
    print(json.dumps(calc(items, args.vat, args.discount), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
