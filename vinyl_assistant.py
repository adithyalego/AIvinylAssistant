import os

PROBLEMS = {
    "adhesion_failure": {
        "keywords": ["not sticking", "peeling", "lifting", "edges curling", "adhesive failure"],
        "analysis": "Adhesion failure typically results from surface contamination (dust, oil, moisture), incompatible substrates (low-energy plastics), insufficient pressure during application, or temperature extremes.",
        "fixes": [
            "Clean surface thoroughly with 90%+ isopropyl alcohol and lint-free cloth.",
            "Use adhesion promoter/primer for difficult surfaces like polypropylene.",
            "Apply firm, even pressure with a squeegee or roller.",
            "Ensure application temperature is 60-90°F (15-32°C)."
        ]
    },
    "bubbles": {
        "keywords": ["bubbles", "air pockets", "trapped air", "blisters"],
        "analysis": "Bubbles form from trapped air during installation, rapid application, or applying over textured/uneven surfaces without proper technique.",
        "fixes": [
            "Use hinge method: Apply center first, then smooth outward.",
            "Puncture small bubbles with a pin and press air out toward edge.",
            "Apply heat (hairdryer/heat gun on low) to make vinyl more pliable.",
            "For large areas, use wet application with soapy water for repositioning."
        ]
    },
    "wrinkles": {
        "keywords": ["wrinkles", "creases", "folds", "stretching marks", "stretch marks", "scratches"],
        "analysis": "Wrinkles occur from over-stretching vinyl, applying on curves without relief cuts, or insufficient heat causing material to resist conforming.",
        "fixes": [
            "Heat vinyl to 100-120°F to increase flexibility before application.",
            "Make relief cuts at corners/curves for better conformity.",
            "Pull and reapply sections carefully—vinyl is repositionable when warm.",
            "Practice technique on scrap pieces first."
        ]
    },
    "edge_lifting": {
        "keywords": ["edges lifting", "corners peeling", "delamination"],
        "analysis": "Edge lifting is often due to poor initial adhesion at borders, mechanical stress, or environmental exposure (UV, heat cycles).",
        "fixes": [
            "Re-heat edges and press firmly with squeegee.",
            "Apply edge sealer or clear overlaminate for protection.",
            "Trim excess material to reduce stress points."
        ]
    },
    "fading": {
        "keywords": ["fading", "discoloration", "yellowing", "color loss"],
        "analysis": "Premature fading stems from UV exposure, low-quality pigments, or chemical degradation.",
        "fixes": [
            "Choose cast vinyl with UV inhibitors for outdoor use.",
            "Apply UV-protective clear laminate over the graphic.",
            "Limit direct sunlight exposure where possible."
        ]
    }
}

def identify_problems(description):
    text = description.lower()
    identified = []
    for problem, data in PROBLEMS.items():
        if any(keyword in text for keyword in data["keywords"]):
            identified.append(problem)
    return identified or ["unknown"]

def analyze_and_fix(problems):
    output = ""
    for problem in problems:
        if problem != "unknown":
            data = PROBLEMS.get(problem, {})
            output += f"\nDetected Problem: {problem.replace('_', ' ').title()}\n"
            output += f"Analysis: {data.get('analysis', 'No detailed analysis available.')}\n"
            output += "Recommended Fixes:\n"
            for fix in data.get("fixes", []):
                output += f"• {fix}\n"
        else:
            output += "\nUnknown Issue: The description doesn't match common problems. Provide more details or an image for better analysis.\n"
    return output

def analyze_image(image_path):
    try:
        import cv2
        import numpy as np
        
        if not os.path.exists(image_path):
            return "Image Analysis: File not found. Check the path and try again."
        
        img = cv2.imread(image_path)
        if img is None:
            return "Image Analysis: Could not read the image. Make sure it's a valid JPG/PNG file."
        
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edge_density = np.count_nonzero(edges) / gray.size
        
        blur_score = cv2.Laplacian(gray, cv2.CV_64F).var()
        
        result = "\nImage Analysis Results:\n"
        if edge_density > 0.08:
            result += "• High edge density detected — likely wrinkles or stretching marks.\n"
        if edge_density > 0.12:
            result += "• Very severe wrinkling visible.\n"
        if blur_score < 80:
            result += "• Possible large air bubbles or smooth lifted areas (low texture).\n"
        if 0.03 <= edge_density <= 0.08:
            result += "• Minor irregularities — early stretching or small creases.\n"
        if edge_density < 0.03 and blur_score > 100:
            result += "• Image looks clean — no obvious damage detected.\n"
        
        return result
    except Exception as e:
        return f"Image Analysis: Error processing image ({str(e)})."

print("Vinyl Tape Damage Assistant Ready!\nDescribe the issue (type 'exit' to quit):")
while True:
    user_input = input("\nYou: ").strip()
    if user_input.lower() == "exit":
        print("Goodbye!")
        break
    
    problems = identify_problems(user_input)
    response = analyze_and_fix(problems)
    print("\nAssistant:" + response)
    
    image_path = input("\nImage path (optional - e.g., /Users/ajithedakandi/Desktop/damaged.jpg, or press Enter to skip): ").strip()
    if image_path:
        image_result = analyze_image(image_path)
        print(image_result)