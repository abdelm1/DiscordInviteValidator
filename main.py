import os
import re
import requests
from colorama import Fore, Style

print(Fore.RED + '''
██╗███╗   ██╗██╗   ██╗██╗████████╗███████╗ ██████╗██╗  ██╗███████╗ ██████╗██╗  ██╗███████╗██████╗ 
██║████╗  ██║██║   ██║██║╚══██╔══╝██╔════╝██╔════╝██║  ██║██╔════╝██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║██╔██╗ ██║██║   ██║██║   ██║   █████╗  ██║     ███████║█████╗  ██║     █████╔╝ █████╗  ██████╔╝
██║██║╚██╗██║╚██╗ ██╔╝██║   ██║   ██╔══╝  ██║     ██╔══██║██╔══╝  ██║     ██╔═██╗ ██╔══╝  ██╔══██╗
██║██║ ╚████║ ╚████╔╝ ██║   ██║   ███████╗╚██████╗██║  ██║███████╗╚██████╗██║  ██╗███████╗██║  ██║
╚═╝╚═╝                              Discord: @zpi. ''' + Style.RESET_ALL)

# Prompt the user to enter the name of the input file.
input_file = input("Invite list file: ")

# Prompt the user to enter the URL of the license validation API.
api_url = "https://keyauth.win/api/seller/?sellerkey=2bed2e535b6d74d0542582e5ec7ab303&type=verify"

# Prompt the user to enter their license key.
license_key = input("Enter your license key: ")

# Create a directory to store the output files.
output_dir = "Data"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Open the output files for writing.
valid_file = open(f"{output_dir}/valid_links.txt", "w")
invalid_file = open(f"{output_dir}/invalid_links.txt", "w")

# Make a GET request to the license validation API.
response = requests.get(api_url, params={"key": license_key})

# Check the response status code to determine if the license key is valid.
if response.status_code == 200:
    data = response.json()
    if data["success"]:
        print(Fore.GREEN + "License key is valid." + Style.RESET_ALL)
    else:
        print(Fore.RED + "License key is invalid." + Style.RESET_ALL)
        exit()
else:
    print(Fore.RED + "License key is invalid." + Style.RESET_ALL)
    exit()

# Open the input file and read the invite links.
with open(input_file, "r") as file:
    invite_links = file.readlines()

# Process each invite link.
for invite_link in invite_links:
    # Strip any leading or trailing whitespace from the invite link.
    invite_link = invite_link.strip()

    # Parse the invite code from the link.
    match = re.search(r"(discord\.gg|discordapp\.com/invite)/([a-zA-Z0-9]+)", invite_link)
    if not match:
        invalid_file.write(f"{invite_link}\n")
        print(Fore.RED + f"Invalid invite link: {invite_link}" + Style.RESET_ALL)
        continue

    # Construct the invite endpoint URL.
    invite_code = match.group(2)
    invite_url = f"https://discord.com/api/v9/invites/{invite_code}"

    # Make a GET request to the invite endpoint URL.
    response = requests.get(invite_url)

    # Check the response status code to determine if the invite is valid or not.
    if response.status_code == 200:
        data = response.json()
        server_name = data["guild"]["name"]
        valid_file.write(f"{invite_link}\n")
        print(Fore.GREEN + f"[VALID INVITE] {server_name}: {invite_link}" + Style.RESET_ALL)
    else:
        invalid_file.write(f"{invite_link}\n")
        print(Fore.RED + f"[INVALID INVITE] {invite_link}" + Style.RESET_ALL)

# Close the output files.
valid_file.close()
invalid_file.close()

# Notify the user that the output files have been saved.
print()
print(Fore.YELLOW + f"Valid invite links have been saved to {output_dir}/valid_links.txt" + Style.RESET_ALL)
print(Fore.YELLOW + f"Invalid invite links have been saved to {output_dir}/invalid_links.txt" + Style.RESET_ALL)

# Prompt the user to press Enter before exiting.
input("Press Enter to exit...")
