import data_retrieval


def main_menu():
    print("Welcome to the program.\nThe system is now checking if there are samples already saved locally...\n")
    data_retrieval.check_local_files()
    print("That's all for now!! Thank you")


main_menu()
