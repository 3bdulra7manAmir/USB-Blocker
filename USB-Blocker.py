import subprocess
import re


class UsbBlocker:

    @staticmethod
    def blocker():
        # Fetch the list of all USB devices using devcon
        try:
            result = subprocess.run(['devcon', 'hwids', '=usb'], capture_output=True, text=True, check=True)

            # Use regex to find hardware IDs from the result (assuming hwid lines contain 'USB')
            hwid_pattern = re.compile(r'USB\\[^\\]+')
            hwids = hwid_pattern.findall(result.stdout)

            if not hwids:
                print("No USB devices found.")
                return

            # Assume we want to block the first matching USB device (for example)
            parsed_hwid = hwids[0]
            print(f"Found USB device with HWID: {parsed_hwid}")

            # Disable the USB device
            disable_result = subprocess.run(['devcon', 'disable', parsed_hwid], capture_output=True, text=True)
            print(f"Disable result: {disable_result.stdout}")

            # Optionally, enable it again later (uncomment if needed)
            # enable_result = subprocess.run(['devcon', 'enable', parsed_hwid], capture_output=True, text=True)
            # print(f"Enable result: {enable_result.stdout}")

        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# Call the static method
UsbBlocker.blocker()
