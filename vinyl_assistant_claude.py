import os
import base64
import ollama
client = ollama.Client(host="http://localhost:11434")
# ─── Knowledge Base ───────────────────────────────────────────────────────────
# Injected into the system prompt so llama3 reasons with domain expertise.

KNOWLEDGE_BASE = """
You are an expert vinyl wrap and vinyl tape technician. You diagnose damage issues
and provide clear, actionable repair strategies. Use the reference knowledge below.

--- KNOWN PROBLEMS & FIXES ---

ADHESION FAILURE (not sticking, peeling, lifting, edges curling):
  Causes: surface contamination (dust, oil, moisture), incompatible substrate
          (low-energy plastics like PP/PE), insufficient pressure, temperature extremes.
  Fixes:
    - Clean surface with 90%+ isopropyl alcohol and a lint-free cloth.
    - Use adhesion promoter/primer for difficult surfaces (polypropylene, polyethylene).
    - Apply firm, even pressure with a squeegee or rubber roller.
    - Ensure application temperature is 60–90°F (15–32°C).

BUBBLES / AIR POCKETS (bubbles, blisters, trapped air):import ollama
  Causes: trapped air during installation, rapid application, textured surfaces.
  Fixes:
    - Use the hinge method — apply center first, smooth outward to edges.
    - Puncture small bubbles with a fine pin and press air toward edge.
    - Apply low heat (hair dryer / heat gun on low) to make vinyl more pliable.
    - Use wet application (diluted soapy water) for large panels to allow repositioning.

WRINKLES / CREASES (wrinkles, folds, stretch marks, over-stretching):
  Causes: over-stretching vinyl, applying curves without relief cuts, insufficient heat.
  Fixes:
    - Heat vinyl to 100–120°F before application to increase flexibility.
    - Make relief cuts at corners and curves for better conformity.
    - Reheat and reapply sections — vinyl is repositionable when warm.
    - Practice on scrap material before tackling complex curves.

EDGE LIFTING / DELAMINATION (corner peeling, edges coming up):
  Causes: poor initial adhesion at borders, mechanical stress, UV/heat cycling.
  Fixes:
    - Reheat edges and press firmly with a squeegee.
    - Apply edge sealer or clear overlaminate for long-term protection.
    - Trim excess material flush to reduce mechanical stress points.

FADING / DISCOLORATION (fading, yellowing, color loss, UV damage):
  Causes: UV exposure, low-quality pigments, chemical degradation.
  Fixes:
    - Use cast vinyl with built-in UV inhibitors for any outdoor application.
    - Apply a UV-protective clear laminate over the graphic.
    - Avoid prolonged direct sunlight where possible.

SCRATCHES / SURFACE DAMAGE (surface scratches, scuffs, abrasion marks):
  Causes: abrasive contact, improper cleaning tools, sharp objects.
  Fixes:
    - Apply heat to minor scratches — vinyl has memory and may self-heal slightly.
    - Use a paint correction compound lightly on deep scuffs before reapplying.
    - For severe scratches, patch with matching vinyl or replace the section entirely.

--- RESPONSE FORMAT ---
1. Identify the most likely problem(s) based on the description.
2. Briefly explain the likely cause (1–2 sentences).
3. List 3–5 concrete, numbered fixes the user can perform right now.
4. End with a short confidence note if the description is ambiguous.

Keep your tone professional but approachable. Be specific — avoid vague advice.
"""

# ─── Text Diagnosis (llama3) ───────────────────────────────────────────────────

def diagnose_text(description: str) -> str:
    """Send the user's problem description to llama3 for AI-powered diagnosis."""
    try:
        response = client.chat(
            model="llama3",
            messages=[
                {"role": "system", "content": KNOWLEDGE_BASE},
                {"role": "user",   "content": f"My vinyl issue: {description}"}
            ]
        )
        return response["message"]["content"]
    except ollama.ResponseError as e:
        return f"[Ollama error] {e.error}\nMake sure llama3 is pulled: `ollama pull llama3`"
    except Exception as e:
        return f"[Unexpected error] {e}"


# ─── Image Analysis (llava) ────────────────────────────────────────────────────

def diagnose_image(image_path: str) -> str:
    """Send the image to llava for visual damage analysis."""
    if not os.path.exists(image_path):
        return f"[File not found] Check the path: {image_path}"

    ext = os.path.splitext(image_path)[1].lower()
    if ext not in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
        return f"[Unsupported format] Please use JPG, PNG, BMP, or WEBP."

    try:
        with open(image_path, "rb") as f:
            image_b64 = base64.b64encode(f.read()).decode("utf-8")

        image_prompt = (
            "You are a vinyl wrap technician inspecting a damage photo. "
            "Identify visible issues (bubbles, wrinkles, peeling, fading, scratches, etc.), "
            "assess their severity (minor / moderate / severe), and suggest the top 3 fixes. "
            "Be specific about what you see in the image."
        )

        response = client.chat(
            model="llava",
            messages=[
                {
                    "role": "user",
                    "content": image_prompt,
                    "images": [image_b64]
                }
            ]
        )
        return response["message"]["content"]

    except ollama.ResponseError as e:
        return f"[Ollama error] {e.error}\nMake sure llava is pulled: `ollama pull llava`"
    except Exception as e:
        return f"[Unexpected error during image analysis] {e}"


# ─── CLI Loop ──────────────────────────────────────────────────────────────────

def main():
    print("=" * 60)
    print("  🎛  Vinyl Damage AI Assistant  (llama3 + llava)")
    print("  Powered by Ollama  |  Type 'exit' to quit")
    print("=" * 60)

    while True:
        print()
        description = input("Describe your vinyl issue: ").strip()

        if description.lower() in ("exit", "quit", "q"):
            print("Goodbye! 👋")
            break

        if not description:
            print("Please enter a description to continue.")
            continue

        # ── Text diagnosis ──
        print("\n⏳ Analysing with llama3...\n")
        text_result = diagnose_text(description)
        print("─" * 50)
        print("🧠 AI Diagnosis:\n")
        print(text_result)
        print("─" * 50)

        # ── Optional image analysis ──
        image_path = input(
            "\n📷 Image path for visual analysis (or press Enter to skip): "
        ).strip().strip('"').strip("'")

        if image_path:
            print("\n⏳ Analysing image with llava...\n")
            image_result = diagnose_image(image_path)
            print("─" * 50)
            print("🔍 Visual Analysis:\n")
            print(image_result)
            print("─" * 50)

        again = input("\nAnalyse another issue? [Y/n]: ").strip().lower()
        if again == "n":
            print("Goodbye! 👋")
            break


if __name__ == "__main__":
    main()