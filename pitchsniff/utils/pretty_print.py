def pretty_print_swot(swot):
    print("\n" + "="*40)
    print("         SWOT ANALYSIS")
    print("="*40)

    for section in ["strengths", "weaknesses", "opportunities", "threats"]:
        print(f"\n{section.upper()}:")
        for point in swot.get(section, []):
            print(f"  • {point}")