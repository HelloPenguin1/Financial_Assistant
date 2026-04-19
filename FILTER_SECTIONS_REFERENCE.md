# Filter Sections Reference - Exact Names to Use

This document shows the exact section names the orchestrator LLM should output in `filter_sections` for proper metadata filtering.

## 10-K Filing - Most Financially Significant Items

### Primary Sections (Recommended for filter_sections)
- `Item 1: Business` - Core operations, revenue drivers
- `Item 1A: Risk Factors` - Long-term business risks  
- `Item 7: MD&A` - Financial trends, liquidity, capital resources
- `Item 8: Financial Statements` - Balance sheet, income statement, cash flows

### Secondary Sections (Use if relevant)
- `Item 1B: Unresolved Staff Comments`
- `Item 1C: Cybersecurity`
- `Item 2: Properties`
- `Item 3: Legal Proceedings`
- `Item 5: Market for Registrant's Common Equity`
- `Item 6: Selected Financial Data`
- `Item 7A: Quantitative and Qualitative Disclosures About Market Risk`
- `Item 9: Controls and Procedures`
- `Item 10: Directors, Executive Officers, and Corporate Governance`

---

## 10-Q Filing - Most Financially Significant Items

### Primary Sections (Recommended for filter_sections)
- `Item 1: Financial Statements` - Interim quarterly statements
- `Item 2: MD&A` - Quarterly trends, YoY comparisons
- `Item 1A: Risk Factors` - Emerging/changed risks
- `Item 3: Quantitative and Qualitative Disclosures About Market Risk` - Financial exposures

### Secondary Sections (Use if relevant)
- `Item 4: Controls and Procedures`
- `Item 5: Other Information`

---

## Selection Strategy for filter_sections

### Always Include (90%+ of queries):
1. **MD&A** (Item 7 for 10-K, Item 2 for 10-Q)
   - Provides management's interpretation of financial results
   - Essential for understanding trends and context

2. **Financial Statements** (Item 8 for 10-K, Item 1 for 10-Q)
   - Actual numbers, verifies MD&A claims
   - Required for detailed financial analysis

### Often Include (depending on query):
3. **Risk Factors** (Item 1A)
   - If analyzing risks, threats, forward-looking implications
   - Helps understand downside scenarios

4. **Business** (Item 1 for 10-K only)
   - If analyzing operations, market position, strategy
   - Provides operational context for financial results

---

## Example filter_sections Lists

### Financial Performance Analysis
```json
"filter_sections": [
  "Item 1: Business",
  "Item 7: MD&A",           // 10-K version
  "Item 8: Financial Statements"
]
```

### Risk & Forward-Looking Analysis
```json
"filter_sections": [
  "Item 1A: Risk Factors",
  "Item 7: MD&A",
  "Item 1: Business"
]
```

### Quarterly Trend Analysis
```json
"filter_sections": [
  "Item 2: MD&A",           // 10-Q version
  "Item 1: Financial Statements",
  "Item 1A: Risk Factors"
]
```

### Market Risk Analysis
```json
"filter_sections": [
  "Item 7A: Quantitative and Qualitative Disclosures About Market Risk",  // 10-K
  "Item 3: Quantitative and Qualitative Disclosures About Market Risk",   // 10-Q
  "Item 7: MD&A"
]
```

---

## Implementation Notes

- ✅ Each filter_sections list should contain 3-4 items
- ✅ Use exact names as shown above
- ✅ Prioritize based on analysis goal
- ✅ Avoid duplicates within a single filter_sections list
- ✅ MD&A is almost always included (highest retrieval value)
- ⚠️ If using unfamiliar section names, retriever may return 0 results (no metadata match)

---

## Validation

To test if orchestrator is generating correct filter_sections:

1. Check orchestrator output structure:
   ```python
   section.filter_sections  # Should be List[str]
   # Example: ["Item 1: Business", "Item 7: MD&A", "Item 8: Financial Statements"]
   ```

2. Verify in llm_call retriever filter:
   ```python
   "section": {"$in": section.filter_sections}
   # Should match your vectorstore's section metadata field
   ```

3. Monitor retrieval results:
   - If getting 0 docs: Check section name spelling/format
   - If getting wrong sections: Verify metadata in vectorstore matches expected names
