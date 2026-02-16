import os

def check_file():
    print(f"Current working directory: {os.getcwd()}")
    if os.path.exists("landing_page.html"):
        print("landing_page.html exists")
    else:
        print("landing_page.html does not exist")

check_file()
