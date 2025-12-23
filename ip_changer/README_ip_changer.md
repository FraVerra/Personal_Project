# **IP Changer Tool**

**Author:** **Francesco Verra**  
**Language:** **Python 3**  
**Supported Operating System:** **Linux**  
**Main Dependencies:** **iproute2**, **NetworkManager**, **nmap**

---

## **Overview**

**IP Changer Tool** is a **Python-based utility** designed to **automatically change the local IP address** of a **Linux machine** by assigning a **random, valid IP** within the **current network range**.

The program **analyzes the existing network configuration**, **identifies available addresses**, **avoids conflicts with active hosts**, and **applies the new configuration at system level**.  
All operations are performed **automatically** and require **no manual interaction** during execution.

---

## **Features**

- **Automatic detection** of:
  - **Default gateway**
  - **Active network interface**
  - **Current IP address**, **subnet mask**, and **broadcast address**
- **Binary and decimal IP address conversion**
- **Network range calculation**
- **Active host discovery** using **Nmap**
- **Random IP generation** with **conflict avoidance**
- **Full network reconfiguration**:
  - Temporary **NetworkManager disable**
  - **Interface reset**
  - **IP reassignment**
  - **Gateway reconfiguration**

---

## **System Requirements**

### **Operating System**

- **Linux distribution**
  - **Debian / Ubuntu**
  - **Kali / Parrot OS**
  - **Arch-based distributions** (with **NetworkManager**)

This tool is **not compatible** with **Windows** or **macOS**, as it relies on **Linux-specific system commands**.

---

### **Required Software**

Ensure the following components are installed:

#### **Python 3**
```bash
python3 --version
```

#### **Nmap**
Used to **scan the local network** and **detect active hosts**.
```bash
sudo apt install nmap
```

#### **NetworkManager**
Required to **manage network interfaces**.
```bash
nmcli --version
```

#### **iproute2**
Provides the **`ip` command** for **low-level network configuration** (usually preinstalled).

---

## **Required Privileges**

The program must be executed with **root privileges**, since it performs operations such as:

- **Assigning and removing IP addresses**
- **Enabling and disabling network interfaces**
- **Modifying routing tables** and **default gateways**

Typical execution example:
```bash
sudo python3 ip_changer.py
```

---

## **How It Works**

### **1. Network Information Collection**

The program retrieves:
- **Default gateway address**
- **Active network interface name**
- **Current IP configuration**

IP addresses are also converted into **binary format** to allow **precise subnet calculations**.

---

### **2. Network and Broadcast Calculation**

Using **subnet mask information**, the tool calculates:
- **Network address**
- **Broadcast address**
- **Valid IP address range**

---

### **3. Network Scanning**

The local network is scanned using:
```bash
nmap -sn <network>/<subnet>
```

This allows the program to:
- **Detect active hosts**
- **Exclude already-used IP addresses**
- **Avoid gateway and broadcast conflicts**

---

### **4. Random IP Selection**

A **random IP address** is generated within the **valid range** and validated to ensure it is **not currently in use** on the network.

---

### **5. Network Reconfiguration**

The program then:
1. **Disables NetworkManager** on the active interface  
2. **Brings the interface down**  
3. **Flushes existing IP addresses**  
4. **Assigns the new IP address**  
5. **Brings the interface back up**  
6. **Re-enables NetworkManager**  
7. **Configures the default gateway**  
8. **Removes residual secondary IP addresses**

After completion, the **updated network configuration** is displayed.

---

## **Usage**

All **usage instructions**, **command-line options**, and **accepted parameter values** are available directly from the command line.

To display the **help menu**:
```bash
python3 ip_changer.py --help
```

or:
```bash
python3 ip_changer.py -h
```

The help output always reflects the **current version** of the program.

---

## **Warnings and Notes**

- Use this tool **only on networks you are authorized to manage**
- **Frequent IP changes** may result in:
  - **Temporary network disconnections**
  - **Unexpected router or DHCP behavior**
- Avoid usage in **production environments** without **proper testing**

The author assumes **no responsibility** for **misuse** or **unintended consequences**.

---

## **Project Purpose**

This project was developed as:
- An **advanced networking exercise**
- A **learning tool** for **Linux network management**
- A **demonstration** of **Python system-level automation**

It combines:
- **Python scripting**
- **Linux networking concepts**
- **Process and subprocess management**
- **Integration with external system tools**
