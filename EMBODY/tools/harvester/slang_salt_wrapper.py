from pathlib import Path
import json

def dummy_salt_translate(english_line):
    # Placeholder — Replace with real SALT later
    return f"MSA({english_line})"

def dummy_slang_rewrite(msa_line):
    # Placeholder — Replace with real SLANG later
    return f"EGY({msa_line})"

def enrich_with_salt_slang(harvest_dir):
    harvest_dir = Path(harvest_dir)
    filelist = Path(harvest_dir)
    output_json = Path("tools/harvester/harvest_output/enriched_metadata.jsonl")

    with filelist.open("r", encoding="utf-8") as f_in, output_json.open("w", encoding="utf-8") as f_out:
        for line in f_in:
            wav_path, eng_line = line.strip().split("|")
            msa = dummy_salt_translate(eng_line)
            egy = dummy_slang_rewrite(msa)
            entry = {
                "wav": wav_path,
                "eng": eng_line,
                "msa": msa,
                "egy": egy,
                "emotion": None  # To be filled later
            }
            f_out.write(json.dumps(entry, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    import sys
    enrich_with_salt_slang(sys.argv[1])
