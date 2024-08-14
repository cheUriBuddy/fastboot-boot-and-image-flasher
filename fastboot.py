from tkinter import *
from tkinter import filedialog
import subprocess
import tkinter.messagebox as msg

def boot_fastboot():
    try:
        output_text.delete(1.0, END)  # Clear previous output
        result = subprocess.run(["adb", "reboot", "bootloader"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_text.insert(END, f"Command: adb reboot bootloader\n")
        output_text.insert(END, "Output: Device Booted To Fastboot Mode\n")
    except subprocess.CalledProcessError as e:
        output_text.insert(END, f"Error: {e.stderr}\n")
        msg.showerror("Error", f"Failed to boot to Fastboot mode:\n{e.stderr}")

def check_device_connected():
    try:
        cmd = subprocess.run(["fastboot", "devices"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if not cmd.stdout.strip():
            msg.showwarning("No Device", "No device detected in Fastboot mode. Attempting to boot device to Fastboot mode.")
            boot_fastboot()  # Attempt to boot to Fastboot mode
            cmd = subprocess.run(["fastboot", "devices"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            if not cmd.stdout.strip():
                msg.showerror("No Device", "Still no device detected. Please connect your device and try again.")
                return False
        return True
    except subprocess.CalledProcessError as e:
        output_text.insert(END, f"Error: {e.stderr}\n")
        msg.showerror("Error", f"Failed to check device connection:\n{e.stderr}")
        return False

def bootSystem():
    if not check_device_connected():
        return

    try:
        output_text.delete(1.0, END)  # Clear previous output
        result = subprocess.run(["fastboot", "reboot"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output_text.insert(END, f"Command: fastboot reboot\n")
        output_text.insert(END, "Output: Device rebooted to System\n")
    except subprocess.CalledProcessError as e:
        output_text.insert(END, f"Error: {e.stderr}\n")

def flash_boot_image():
    if not check_device_connected():
        return

    file_path = filedialog.askopenfilename(title="Select Boot Image", filetypes=[("Image Files", "*.img"), ("All Files", "*.*")])
    if file_path:
        try:
            output_text.delete(1.0, END)  # Clear previous output
            command = ["fastboot", "flash", "boot", file_path]
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output_text.insert(END, f"Command: {' '.join(command)}\n")
            output_text.insert(END, "Output: Boot image flashed successfully\n")
        except subprocess.CalledProcessError as e:
            output_text.insert(END, f"Error: {e.stderr}\n")

def flash_recovery_image():
    if not check_device_connected():
        return

    file_path = filedialog.askopenfilename(title="Select Recovery Image", filetypes=[("Image Files", "*.img"), ("All Files", "*.*")])
    if file_path:
        try:
            output_text.delete(1.0, END)  # Clear previous output
            command = ["fastboot", "flash", "recovery", file_path]
            result = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            output_text.insert(END, f"Command: {' '.join(command)}\n")
            output_text.insert(END, "Output: Recovery image flashed successfully\n")
        except subprocess.CalledProcessError as e:
            output_text.insert(END, f"Error: {e.stderr}\n")

app = Tk()
app.geometry("500x600")

Button(app, text="Fastboot mode", height="5", width="20", bg="yellow", command=boot_fastboot).pack(pady=10)
Button(app, text="Reboot to System", height="5", width="20", bg="yellow", command=bootSystem).pack(pady=10)
Button(app, text="Flash Boot Image", height="5", width="20", bg="yellow", command=flash_boot_image).pack(pady=10)
Button(app, text="Flash Recovery Image", height="5", width="20", bg="yellow", command=flash_recovery_image).pack(pady=10)

# Create a Text widget for displaying command output
output_text = Text(app, height=15, width=60, wrap=WORD, bg="lightgrey")
output_text.pack(pady=20)

# Initial device check at startup
if not check_device_connected():
    output_text.insert(END, "No device detected at startup. Attempting to boot device to Fastboot mode...\n")

app.mainloop()
