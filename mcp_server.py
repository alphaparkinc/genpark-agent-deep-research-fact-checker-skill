import sys
import json
import re

class FactChecker:
    @staticmethod
    def verify(claim, source_docs):
        claim_tokens = set(re.findall(r"\w+", claim.lower()))
        supporting = []
        for src_id, text in source_docs.items():
            doc_tokens = set(re.findall(r"\w+", text.lower()))
            overlap = claim_tokens & doc_tokens
            if len(overlap) >= min(3, len(claim_tokens)):
                score = round(len(overlap) / len(claim_tokens), 3)
                supporting.append({"source": src_id, "overlap_score": score})

        total_sources = max(1, len(source_docs))
        confidence = round(sum(s["overlap_score"] for s in supporting) / total_sources, 3)
        verified = len(supporting) >= 2 and confidence >= 0.35

        return {
            "claim": claim,
            "verified": verified,
            "corroborating_sources_count": len(supporting),
            "confidence_score": confidence,
            "supporting_sources": supporting
        }

def handle_rpc(request):
    method = request.get("method")
    req_id = request.get("id")
    params = request.get("params", {})

    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "verify_claim",
                        "description": "Cross-reference claim across multiple source documents.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "claim": {"type": "string"},
                                "source_docs": {"type": "object"}
                            },
                            "required": ["claim", "source_docs"]
                        }
                    }
                ]
            }
        }

    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments", {})
        if name == "verify_claim":
            res = FactChecker.verify(args.get("claim", ""), args.get("source_docs", {}))
            return {"jsonrpc": "2.0", "id": req_id, "result": {"content": [{"type": "text", "text": json.dumps(res)}]}}

    return {"jsonrpc": "2.0", "id": req_id, "error": {"code": -32601, "message": "Method not found"}}

if __name__ == "__main__":
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            resp = handle_rpc(req)
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "error": {"code": -32000, "message": str(e)}}) + "\n")
            sys.stdout.flush()
