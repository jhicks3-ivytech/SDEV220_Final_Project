import tkinter as tk

# Define a class for creating windows
class AppWindow:
    def __init__(self, title, size):
        self.window = tk.Toplevel()  # Create a new window
        self.window.title(title)    # Set the window title
        self.window.geometry(size)  # Set the window size
        
        # Add a label to the window
        label = tk.Label(self.window, text=f"This is {title}", font=("Arial", 14))
        label.pack(pady=20)

        # Add a close button
        close_button = tk.Button(self.window, text="Close", command=self.window.destroy)
        close_button.pack(pady=10)

# Main application window
def main():
    root = tk.Tk()
    root.title("Main Window")
    root.geometry("400x300")

    # Function to open a new window using the class
    def open_window():
        new_window = AppWindow(title="New Window", size="300x200")

    # Button to create new windows
    button = tk.Button(root, text="Create New Window", command=open_window)
    button.pack(pady=20)

    root.mainloop()

if __name__ == "__main__":
    main()
