# Round 7 Query Submission and Reflection

## Seventh-Round Query Submission

1. 0.206328-0.210881  
2. 0.924394-0.673650  
3. 0.886644-0.005283-0.864351  
4. 0.401284-0.390655-0.356079-0.375087  
5. 0.985576-0.955780-0.999493-0.303493  
6. 0.230255-0.573263-0.228581-0.991624-0.001223  
7. 0.002750-0.032985-0.989588-0.134703-0.279849-0.577616  
8. 0.004816-0.468454-0.084537-0.410556-0.988018-0.830312-0.494501-0.910814

## Reflection Responses

### 1) Which prompt patterns (zero-shot, few-shot, etc.) did you use, and why? What changed when you simplified vs structured the prompt?

I used a hybrid: zero-shot for quick ideation, then structured prompting for final decisions.
Zero-shot helped generate diverse candidate strategies quickly, but was inconsistent in formatting and sometimes too generic.
Structured prompts (fixed sections: objective, constraints, data summary, required output format) produced more stable, auditable choices and fewer off-target suggestions.
When simplified, prompts were faster but less reproducible. When structured, outputs were more coherent and easier to compare across rounds.

### 2) What temperature, top-p, top-k and max-tokens settings did you choose? How did they trade off coherence vs diversity? How did they affect your chosen query?

I used low temperature for decision-quality responses and stricter formatting:
- Temperature: 0.1-0.3 for final strategy text and query justification
- Top-p: 0.85-0.95 to keep some diversity without drifting
- Top-k: 40-80 where available, to prevent long-tail randomness
- Max tokens: sized to keep full reasoning plus checks, but capped to avoid verbose drift

Trade-off: lower temperature improved coherence and consistency; slightly higher top-p allowed alternative hypotheses. For final query selection, lower randomness reduced risk of unstable round-to-round behavior.

### 3) Did token boundaries or unusual input strings affect the model's behaviour? When did you notice token count limits or truncation influencing the outputs? If no such cases were observed, explain how you checked for those cases.

Yes, unusual input strings (long numeric arrays, scientific notation, mixed delimiters) can cause parsing or attention errors.
I checked this by:
- Enforcing one-line, delimiter-consistent output per function
- Validating dimension counts per function before acceptance
- Checking for dropped or duplicated numeric fields after generation

I did not observe hard truncation in final accepted outputs, because I kept prompt payloads compact and structured.

### 4) With 17 data points, what limitations did you encounter, such as prompt overfitting, attention focusing on irrelevant context or diminishing returns from longer inputs?

With 17 points total per function, key limitations were:
- Prompt overfitting to the most recent outcomes
- Attention bias toward dramatic outliers
- Sparse coverage in higher dimensions (6D and 8D)
- Diminishing returns from adding more context text without adding new signal

Longer prompts did not always improve quality; after a point, they increased noise and made outputs less focused.

### 5) Which strategies did you try to reduce hallucinations? For example, did you use tighter instructions, retrieval of prior relevant information or constrain the output format?

I used:
- Tighter instructions with explicit constraints and required output schema
- Retrieval of only relevant prior rounds (not full raw history every time)
- Deterministic post-checks (dimension count, bounds, delimiter consistency)
- Separating reasoning text from submission text so final output stayed machine-safe

This reduced fabrication risk and formatting errors significantly.

### 6) In future rounds, how would you scale your prompting and decoding strategies when working with larger data sets or more complex LLMs?

For larger datasets or more complex LLMs, I would:
- Switch to retrieval-first prompting (summaries plus top relevant rounds)
- Use schema-constrained outputs (JSON or strict templates)
- Decouple exploration strategy generation from final deterministic formatting
- Run multi-seed candidate generation, then aggregate by scoring rules
- Monitor context budget explicitly and prune low-value history

This keeps reasoning scalable while controlling latency and error rates.

### 7) How did these design choices for prompts and decoding help you think like a practitioner balancing exploration, risk and computational constraints in a black-box setting with incomplete information?

These choices reinforced practical ML behavior:
- Exploration must be intentional, not random
- Exploitation should be evidence-based, not recency-biased
- Compute budget is a real constraint, so prompt structure must be efficient
- Reliability and reproducibility matter as much as a single good score

In a black-box setting with incomplete information, the best process is disciplined uncertainty management: controlled diversity, strict validation and repeatable decision rules.
