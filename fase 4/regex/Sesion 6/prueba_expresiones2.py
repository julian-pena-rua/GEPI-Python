import re
pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"
sequence = "luz@dominio.com"
if re.match(pattern, sequence):
    print("✅ Match!")
else: print("❌ Not a match!")
