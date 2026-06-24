from pathlib import Path
import os

root = Path(r"C:\Users\Administrator\.qclaw\workspace-37i6raipm851ul5j\gudaoqihuo")

# Check environment
print("ZHIPU_API_KEY in env:", bool(os.environ.get("ZHIPU_API_KEY")))

# Check .env file
for name in [".env", "config.py", "secrets.py", ".env.local", "env.txt"]:
    f = root / name
    if f.exists():
        print(f"\nFound: {f}")
        content = f.read_text(encoding="utf-8", errors="ignore")
        # Show lines that might contain API key
        for line in content.splitlines():
            if "API" in line.upper() or "KEY" in line.upper() or "ZHIPU" in line.upper():
                print("  ", line[:80])

# Also check scripts/config
print("\n--- Checking generate_content.py for key config ---")
gc = root / "scripts" / "generate_content.py"
if gc.exists():
    content = gc.read_text(encoding="utf-8", errors="ignore")
    for i, line in enumerate(content.splitlines()[:50], 1):
        if "API" in line.upper() or "KEY" in line.upper():
            print(f"  Line {i}: {line[:100]}")
