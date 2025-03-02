

while True:
    try:
        print(f"1. Set Start & Destination \n2. Nearby Destinations \n0. Exit")
        menu = int(input("Select menu: "))
        if menu == 1:
            print(f"menu 1")
        elif menu == 2:
            print(f"menu 2")
        elif menu == 0:
            print(f"Exit Program.")
            input("Please entar ...... ")
            break
        else:
            print(f"Please select menu again.")
    except:
        print(f"Error Invalid something.")