import subprocess
import re


class UsbBlocker:

    @staticmethod
    def blocker():
        """Fetch and disable the first detected USB device using DevCon."""
        try:
            # Fetch the list of all USB devices using devcon
            result = subprocess.run(['devcon', 'hwids', '=usb'], capture_output=True, text=True, check=True)

            # Use regex to find hardware IDs from the result (assuming hwid lines contain 'USB')
            hwid_pattern = re.compile(r'USB\\[^\\]+')
            hwids = hwid_pattern.findall(result.stdout)

            if not hwids:
                print("No USB devices found.")
                return

            # Assume we want to block the first matching USB device
            parsed_hwid = hwids[0]
            print(f"Found USB device with HWID: {parsed_hwid}")

            # Disable the USB device
            disable_result = subprocess.run(['devcon', 'disable', parsed_hwid], capture_output=True, text=True)
            if disable_result.returncode == 0:
                print(f"Successfully disabled USB device: {parsed_hwid}")
            else:
                print(f"Failed to disable USB device: {parsed_hwid}\n{disable_result.stderr}")

        except subprocess.CalledProcessError as e:
            print(f"Error while executing DevCon command: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


# Call the static method
if __name__ == "__main__":
    UsbBlocker.blocker()
