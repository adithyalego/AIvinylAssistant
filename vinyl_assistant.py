print("Vinyl Tape Damage Diagnostic Assistant - Clean Start")
print("Type 'exit' to quit\n")

while True:
    user_input = input("You: ").strip()
    if user_input.lower() == "exit":
        print("Goodbye!")
        break

    text = user_input.lower()

    if any(word in text for word in ["stick", "peel", "lift", "adhes"]):
        print("\nAssistant: Sounds like adhesion failure.")
        print("Fixes: Clean with IPA, use primer, apply firm pressure.\n")
    elif any(word in text for word in ["bubble", "air", "blister"]):
        print("\nAssistant: Sounds like bubbles / air pockets.")
        print("Fixes: Puncture bubbles, use hinge method, apply heat.\n")
    elif any(word in text for word in ["wrinkle", "stretch", "crease"]):
        print("\nAssistant: Sounds like wrinkles or stretching marks.")
        print("Fixes: Heat the vinyl, make relief cuts, post-heat.\n")
    else:
        print("\nAssistant: Please describe the problem more clearly.")
        print("(Example: 'bubbles on the edge' or 'not sticking on plastic')\n")