# 🚀 CTF Buddy 🕵️

CTF Buddy is your companion for Capture The Flag (CTF) competitions! It provides a simplified interface for enumerating a target and is specifically designed to aid in penetration testing scenarios in CTF environments. 

CTF Buddy performs an Nmap scan, provides output in a simple or detailed format based on user preference, and offers suggestions on the next steps like running a Hydra command when an SSH service is detected.

---

## 💡 Features

- Simple and interactive command line interface
- Performs an aggressive Nmap scan
- Provides a simplified table view of scan results
- Also offers option for a detailed Nmap output
- Auto-suggests next steps based on scan results

---

## 🏃‍♂️ Quick Start

You can install and run CTF Buddy with a single command:

```
curl -s -o ctfbuddy.sh https://raw.githubusercontent.com/neutronsec/ctfbuddy/main/ctfbuddy.sh && bash ./ctfbuddy.sh && rm ./ctfbuddy.sh
```

This will download a script from the CTF Buddy repository, run it to install CTF Buddy, and then remove the script. After this, you can start CTF Buddy using:

```
sudo ctfbuddy
```

Note: `sudo` is necessary for CTF Buddy to perform Nmap scans. Follow the on-screen prompts to start enumerating your target 🎯!

---

## ⚠️ Disclaimer

CTF Buddy is intended for use in legal and consensual scenarios, such as Capture The Flag competitions or pen testing environments. The developers are not responsible for any misuse or damage caused by this program.

---

## 📄 License

This project is licensed under the terms of the [MIT License](LICENSE).

---

## ✉️ Contact

Feel free to reach out for any queries or suggestions.