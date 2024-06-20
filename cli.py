import tkinter as tk
from tkinter import messagebox, simpledialog
import customtkinter
import netmiko
from customtkinter import *
import os

# Global variable to hold the connection object
connection = None

def connect_to_device():
    global connection
    device = {
        'device_type': 'cisco_ios',
        'host': entry_hostname.get(),
        'username': entry_username.get(),
        'password': entry_password.get(),
        'port': 22,
        'secret': entry_password.get()
    }

    try:
        connection = netmiko.ConnectHandler(**device)
        connection.enable()  # Enter enable mode
        messagebox.showinfo("Success", "Connection established!")
    except netmiko.NetMikoTimeoutException:
        messagebox.showerror("Error", "Connection timed out.")
    except netmiko.NetMikoAuthenticationException:
        messagebox.showerror("Error", "Authentication failed.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to connect: {e}")

def vlan():
    if connection is None:
        messagebox.showerror("Error", "No connection established. Please connect first.")
        return

    vlanNew = entry_vlan_id.get()

    if vlanNew:
        commands = [f"interface vlan {vlanNew}"]
        try:
            connection.send_config_set(commands)  # Send config commands
            messagebox.showinfo("Success", "vlan added successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add vlan: {e}")
    else:
        messagebox.showerror("Error", "Please enter a new vlan.")


def configure_interface():
    if connection is None:
        messagebox.showerror("Error", "No connection established. Please connect first.")
        return

    interface = entry_interface.get()
    new_vlan = entry_vlan_id.get()
    mode = mode_var.get()

    commands = []
    if mode == "Access":
        commands = [
            f"interface {interface}",
            "switchport mode access",
            f"switchport access vlan {new_vlan}",
            "no shutdown"
        ]
    elif mode == "Trunk":
        commands = [
            f"interface {interface}",
            "switchport mode trunk",
            f"switchport trunk allowed vlan {new_vlan}",
            "no shutdown"
        ]

    try:
        connection.send_config_set(commands)  # Send config commands
        messagebox.showinfo("Success", "Interface configuration applied successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to configure interface: {e}")

def change_hostname():
    if connection is None:
        messagebox.showerror("Error", "No connection established. Please connect first.")
        return

    new_hostname = entry_name.get()
    if new_hostname:
        commands = [f"hostname {new_hostname}"]
        try:
            connection.send_config_set(commands)  # Send config commands
            messagebox.showinfo("Success", "Hostname changed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change hostname: {e}")
    else:
        messagebox.showerror("Error", "Please enter a new hostname.")

# Initialize the main window
window = tk.Tk()
window.title('Automated Cisco Switch Configurator')
window.geometry('860x400')
window.configure(bg='#000D0C')

# Welcome Label
welcome_label = customtkinter.CTkLabel(window, text='Welcome to Automated Cisco Switch Interface', font=("Arial Rounded MT Bold", 18))
welcome_label.grid(row=0, pady=10, padx=8, columnspan=3)

# Frame for Login
frame = customtkinter.CTkFrame(window, corner_radius=10, fg_color='#2F403E')
frame.grid(row=1, column=0, pady=0, padx=30)

login_label = customtkinter.CTkLabel(frame, text='Login SSH Connection', font=("Arial Rounded MT Bold", 15), text_color='#F2F1E9')
login_label.grid(row=0, padx=19, columnspan=3, pady=15)

# Hostname Label and Entry
label_hostname = customtkinter.CTkLabel(frame, text="Hostname:", text_color='#F2F1E9')
label_hostname.grid(row=1, column=0, padx=10, pady=10)
entry_hostname = customtkinter.CTkEntry(frame)
entry_hostname.grid(row=1, column=1, padx=10, pady=5)

# Username Label and Entry
label_username = customtkinter.CTkLabel(frame, text="Username:", text_color='#F2F1E9')
label_username.grid(row=2, column=0, padx=10, pady=10)
entry_username = customtkinter.CTkEntry(frame)
entry_username.grid(row=2, column=1, padx=10, pady=5)

# Password Label and Entry
label_password = customtkinter.CTkLabel(frame, text="Password:", text_color='#F2F1E9')
label_password.grid(row=3, column=0, padx=10, pady=10)
entry_password = customtkinter.CTkEntry(frame, show="*")
entry_password.grid(row=3, column=1, padx=10, pady=5)

# Connect Button
connect_button = customtkinter.CTkButton(frame, text="Connect", fg_color='#A66851', text_color='#F2F1E9', hover_color='#A0A603', command=connect_to_device)
connect_button.grid(row=4, columnspan=2, pady=15)

tabview = CTkTabview(master=window, fg_color='#EAF205', segmented_button_fg_color='#030640', segmented_button_selected_color='#A66851', segmented_button_selected_hover_color='#A66851', segmented_button_unselected_color='#010326')
tabview.grid(row=1, column=1, padx=20, pady=20)

tabview.add("Interface")
tabview.add("Access List")
tabview.add("Profile")


configure_label = customtkinter.CTkLabel(master=tabview.tab('Interface'), text='Configure Switch', font=("Arial Rounded MT Bold", 15), text_color='#262626')
configure_label.grid(row=0, padx=19, column=1, pady=10)

# Interface Label and Entry
label_interface = customtkinter.CTkLabel(master=tabview.tab('Interface'), text="Interface:", text_color='#262626')
label_interface.grid(row=1, column=0, padx=15, pady=15)
entry_interface = customtkinter.CTkEntry(master=tabview.tab('Interface'))
entry_interface.grid(row=1, column=1, padx=10, pady=5)

# VLAN ID Label and Entry
label_vlan_id = customtkinter.CTkLabel(master=tabview.tab('Interface'), text="VLAN ID:", text_color='#262626')
label_vlan_id.grid(row=3, column=0, padx=15, pady=5)
entry_vlan_id = customtkinter.CTkEntry(master=tabview.tab('Interface'))
entry_vlan_id.grid(row=3, column=1, padx=10, pady=5)

# Mode Label and Radiobuttons
label_mode = customtkinter.CTkLabel(master=tabview.tab('Interface'), text="Mode:", text_color='#262626')
label_mode.grid(row=2, column=0, padx=15, pady=5)
mode_var = tk.StringVar(value="Access")
radio_access = customtkinter.CTkRadioButton(master=tabview.tab('Interface'), text="Access", variable=mode_var, value="Access", text_color='#262626')
radio_access.grid(row=2, column=1, padx=10, pady=5, sticky='e')
radio_trunk = customtkinter.CTkRadioButton(master=tabview.tab('Interface'), text="Trunk", variable=mode_var, value="Trunk", text_color='#262626')
radio_trunk.grid(row=2, column=2, padx=10, pady=5, sticky='w')

# Change Hostname Label and Entry
label_name = customtkinter.CTkLabel(master=tabview.tab('Interface'), text="Change Hostname:", text_color='#262626')
label_name.grid(row=4, column=0, padx=15, pady=5)
entry_name = customtkinter.CTkEntry(master=tabview.tab('Interface'))
entry_name.grid(row=4, column=1, padx=10, pady=5)

# Configure Interface Button
configure_button = customtkinter.CTkButton(master=tabview.tab('Interface'), text="Configure Interface", fg_color='#A66851', text_color='#262626', hover_color='#A0A603', command=configure_interface)
configure_button.grid(row=1, pady=15, column=2)

# Change Hostname Button
hostname_button = customtkinter.CTkButton(master=tabview.tab('Interface'), text="Change Hostname", fg_color='#A66851', text_color='#262626', hover_color='#A0A603', command=change_hostname)
hostname_button.grid(row=4, pady=15, column=2, padx=20)

# Change Vlan Button
hostname_button = customtkinter.CTkButton(master=tabview.tab('Interface'), text="Add Vlan ID", fg_color='#A66851', text_color='#262626', hover_color='#A0A603', command=vlan)
hostname_button.grid(row=3, pady=15, column=2, padx=20)


def configure_acl():
    if connection is None:
        messagebox.showerror("Error", "No connection established. Please connect first.")
        return

    aclid = entry_acl_id.get()
    aclip = entry_acl_ip.get()
    aclwm = entry_acl_wildcard.get()
    modeacl = mode_var_status.get()

    commands = []
    if modeacl == "Permit":
        commands = [
            f"access-list {aclid} {modeacl} {aclip} {aclwm}"
        ]
    elif modeacl == "Deny":
        commands = [
            f"access-list {aclid} {modeacl} {aclip} {aclwm}"
        ]

    try:
        connection.send_config_set(commands)  # Send config commands
        messagebox.showinfo("Success", "Interface configuration applied successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to configure interface: {e}")


label_configure_acl =  customtkinter.CTkLabel(master=tabview.tab('Access List'), text='Configure Access Lists', font=("Arial Rounded MT Bold", 15), text_color='#262626')
label_configure_acl.grid(row=0, padx=19, columnspan=3, pady=10)

label_acl_id = customtkinter.CTkLabel(master=tabview.tab('Access List'), text="Access List ID:", text_color='#262626')
label_acl_id.grid(row=1, column=0, padx=15, pady=5)
entry_acl_id = customtkinter.CTkEntry(master=tabview.tab('Access List'))
entry_acl_id.grid(row=1, column=1, padx=10, pady=5)

label_mode_status = customtkinter.CTkLabel(master=tabview.tab('Access List'), text="Status:", text_color='#262626')
label_mode_status.grid(row=2, column=0, padx=15, pady=5)
mode_var_status = tk.StringVar(value="Permit")
radio_permit = customtkinter.CTkRadioButton(master=tabview.tab('Access List'), text="Permit", variable=mode_var_status, value="Permit", text_color='#262626')
radio_permit.grid(row=2, column=1, padx=10, pady=5, sticky='e')
radio_deny = customtkinter.CTkRadioButton(master=tabview.tab('Access List'), text="Deny", variable=mode_var_status, value="Deny", text_color='#262626')
radio_deny.grid(row=2, column=2, padx=10, pady=5, sticky='w')

label_acl_ip = customtkinter.CTkLabel(master=tabview.tab('Access List'), text="IP Address:", text_color='#262626')
label_acl_ip.grid(row=3, column=0, padx=15, pady=5)
entry_acl_ip = customtkinter.CTkEntry(master=tabview.tab('Access List'))
entry_acl_ip.grid(row=3, column=1, padx=10, pady=5)

label_acl_wildcard = customtkinter.CTkLabel(master=tabview.tab('Access List'), text="Wild Card Mask:", text_color='#262626')
label_acl_wildcard.grid(row=4, column=0, padx=15, pady=5)
entry_acl_wildcard = customtkinter.CTkEntry(master=tabview.tab('Access List'))
entry_acl_wildcard.grid(row=4, column=1, padx=10, pady=5)

acl_button = customtkinter.CTkButton(master=tabview.tab('Access List'), text="Configure Access List", fg_color='#A66851', text_color='#262626', hover_color='#A0A603', command=configure_acl)
acl_button.grid(row=5, pady=15, columnspan=3, padx=20)

def save_running_config_to_file():
    if connection is None:
        messagebox.showerror("Error", "No connection established. Please connect first.")
        return

    try:
        # Retrieve the running configuration
        running_config = connection.send_command("show running-config")
        
        # Define the file path
        file_path = "running_config.txt"
        
        if os.path.exists(file_path):
            # Prompt user to overwrite or save as a new file
            overwrite = messagebox.askyesno("File exists", "The file running_config.txt already exists. Do you want to overwrite it?")
            if not overwrite:
                file_path = simpledialog.askstring("Save As", "Enter the new file name:", initialvalue="profile.txt")
                if not file_path:
                    return  # User cancelled the save as dialog

        # Write the running configuration to the file
        with open(file_path, 'w') as file:
            file.write(running_config)
        
        messagebox.showinfo("Success", f"Running configuration saved to {file_path}!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save running configuration: {e}")


def load_config_from_file():
    if connection is None:
        messagebox.showerror("Error", "No connection established. Please connect first.")
        return

    try:
        # Open file dialog to select a configuration file
        file_path = filedialog.askopenfilename(title="Select Configuration File", filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        
        if not file_path:
            return  # User cancelled the file dialog

        # Read the configuration commands from the file
        with open(file_path, 'r') as file:
            config_lines = file.readlines()
        
        # Prepare the configuration commands
        commands = []
        for line in config_lines:
            line = line.strip()
            if line and not line.startswith('!') and not line.startswith('Building configuration'):
                commands.append(line)

        if not commands:
            messagebox.showinfo("Error", "No valid configuration commands found in the file.")
            return

        # Send the configuration commands to the switch in chunks
        chunk_size = 10
        for i in range(0, len(commands), chunk_size):
            chunk = commands[i:i + chunk_size]
            output = connection.send_config_set(chunk, read_timeout=30)
            print(output)
            
        messagebox.showinfo("Success", f"Configuration loaded from {file_path}!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load configuration: {e}")

profile_label = customtkinter.CTkLabel(master=tabview.tab('Profile'), text='Profile', font=("Arial Rounded MT Bold", 15), text_color='#262626')
profile_label.grid(row=0, padx=24, columnspan=2, pady=10)



load_running_config_button = customtkinter.CTkButton(master=tabview.tab('Profile'), text="Load Running Configuration", fg_color='#A66851', text_color='#262626', hover_color='#A0A603', command=load_config_from_file)
load_running_config_button.grid(row=1, pady=5, column=0)

# Save Running Config to File Button
save_running_config_button = customtkinter.CTkButton(master=tabview.tab('Profile'), text="Save Running Configuration", fg_color='#A66851', text_color='#262626', hover_color='#A0A603', command=save_running_config_to_file)
save_running_config_button.grid(row=1, pady=5, column=1, padx=15)


# Run the main loop
window.mainloop()
