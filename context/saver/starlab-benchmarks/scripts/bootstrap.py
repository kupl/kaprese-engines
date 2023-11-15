import json
import sys
from pathlib import Path

argv = sys.argv
if len(argv) < 2:
    print("Usage: python bootstrap.py <metadata.json>")
    exit(1)

metadata = json.loads(Path(argv[1]).read_text())
if (
    "memory-leak" not in metadata["categories"]
    and "resource-leak" not in metadata["categories"]
):
    print("This benchmark is not supported by SAVER.")
    exit(1)

basedir = Path() / metadata["buggyPath"]

report = {
    "err_type": "MEMORY_LEAK",
    "source": {
        "filepath": metadata["leak"]["source"]["file"],
        "line": metadata["leak"]["source"]["line"],
    },
    "sink": {
        "filepath": metadata["leak"]["sink"]["file"],
        "line": metadata["leak"]["sink"]["line"],
    },
}
report_json = basedir / "report.json"
report_json.write_text(json.dumps(report, indent=4))

def remove_prefix(text, prefix):
    if text.startswith(prefix):
        return text[len(prefix):]
    return text

def make_effect(event, effect, reference_depth):
    return {
        "deref": reference_depth > 0,
        "event": event,
        "idx": 0 if effect == "$return" else int(remove_prefix(effect, "$param")),
    }


if "resource-leak" in metadata["categories"]:
    apispec = []
    for kind, spec in metadata["api"].items():
        api = {
            "resource-type": kind,
            "allocators": [],
            "deallocators": [],
        }
        for alloc in spec["allocators"]:
            allocator = {
                "method_name": alloc["func"],
                "param_effects": [],
                "param_types": [],
                "return_effect": None,
            }
            effect = make_effect("Alloc", alloc["effect"], alloc["reference_depth"])
            if alloc["effect"] != "$return":
                allocator["param_effects"].append(effect)
                allocator["return_effect"] = {"deref": False, "event": "", "idx": 0}
            else:
                allocator["return_effect"] = effect
            api["allocators"].append(allocator)
        for dealloc in spec["deallocators"]:
            deallocator = {
                "method_name": dealloc["func"],
                "param_effects": [],
                "param_types": [],
                "return_effect": None,
            }
            effect = make_effect("Free", dealloc["effect"], dealloc["reference_depth"])
            if dealloc["effect"] != "$return":
                deallocator["param_effects"].append(effect)
                deallocator["return_effect"] = {"deref": False, "event": "", "idx": 0}
            else:
                deallocator["return_effect"] = effect
            api["deallocators"].append(deallocator)
        apispec.append(api)
    apispec_json = basedir / "api.json"
    apispec_json.write_text(json.dumps(apispec, indent=4))
