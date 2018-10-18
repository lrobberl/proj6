import data_retrieval as dr
import file_utils as fu


def main_menu():
    print("Welcome to the program.\nThe system is now checking if there are samples already saved locally...\n")
    dr.check_local_files()
    print("That's all for now!! Thank you")


main_menu()
fu.get_data_from_files()