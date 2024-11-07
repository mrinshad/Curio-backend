from reddit_service import get_top_posts_and_comments
from gemini_service import analyze_comments_with_gemini,analyze_category_of_query
from colorama import Fore, Style, init,Back


def main():

    print(f"{Fore.YELLOW}{Style.BRIGHT}Disclaimer: {Fore.WHITE}{Style.NORMAL}This may not be the best recommendation since the method of acquiring the correct community and posts may not be fully accurate.\n")
    print(f"{Back.GREEN}{Fore.BLACK} PLEASE BE PATIENT BECAUSE IT MAY TAKE UPTO 3min {Back.RESET}{Fore.RESET}\n")
    topic = input("Enter your search term (e.g., 'Top movies of all time'): ")
    # topic = "Top movies of all time"

    response = analyze_category_of_query(topic)
    print(f"POST Category is  {Fore.LIGHTBLUE_EX}{response}{Fore.WHITE}")

    # Get top posts and comments from Reddit
    post_data = get_top_posts_and_comments(topic)

    # Analyze comments with Gemini to create a tier list
    tier_list = analyze_comments_with_gemini(post_data)

    # loading_bar(100, "Completed!")
    print("\nTier List based on Reddit Comments:")

    # Display the tier list if available, otherwise show an error message

    if tier_list:
        for tier, items in tier_list.items():
            print(f"{tier} Tier:")
            for item in items:
                # Ensure item is a dictionary with 'title' and 'reason' keys
                if isinstance(item, dict) and 'title' in item and 'reason' in item:
                    print(f"  - {item['title']}: {item['reason']}")
                else:
                    print(f"  - {item}: No reason available")  # In case data is not structured properly
            print()  # Newline between tiers for clarity
    else:
        print("Failed to generate tier list.")


if __name__ == "__main__":
    main()
