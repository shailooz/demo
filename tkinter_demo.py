import tkinter as tk
import requests

#url = 'https://35bc219e-6dbf-473e-9990-f25f5282ae46-00-3xyzp1pzf1w4.sisko.replit.dev:3000/'
url = 'http://127.0.0.1:5000/'


def increment_number():
    current_number = int(number_label["text"])
    number_label.config(text=str(current_number + 1))
    data = {"number": current_number + 1}
    try:
        response = requests.post(url+"upsert", json=data)
        
        if response.status_code == 201:
            print("Number created successfully!")
        elif response.status_code == 200:
            print("Number updated successfully!")
        else:
            print("Failed to upsert number")
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")


root = tk.Tk()
root.title("IOT DEVICE")
root.geometry("400x200")

number_label = tk.Label(root, text="0", font=("Arial", 24), bg="white",height=2,width=4)
number_label.pack(pady=10)

increment_button = tk.Button(root, text="Increment", command=increment_number, font=("Arial", 16,"bold"), bg="lightblue", fg="black", width=8, height=2)
increment_button.pack(pady=10)

root.mainloop()
