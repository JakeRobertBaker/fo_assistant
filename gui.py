import tkinter as tk
from tkinter import ttk
from tkinter import messagebox  # Import messagebox
from solver import TerminalAttempt


def reset_fields():
    """Resets all input fields and the layout to the initial state."""
    global input_fields, input_frames, row_counter, input_frame

    # Destroy all dynamically created frames
    for frame in input_frames:
        frame.destroy()

    # Clear lists and reset counter
    input_fields = []
    input_frames = []
    row_counter = 0

    # Recreate the input frame
    input_frame.destroy()
    input_frame = ttk.Frame(root, padding=10)
    input_frame.grid(row=0, column=0, sticky="nsew")

    # Add the initial 5 rows
    for _ in range(5):
        add_row()

    # Reset the result label
    result_label.config(text="Result: ")


def calculate_candidates():
    # ensure no words are empty
    word_sim_pairs = {
        word_entry.get().upper().strip(): (int(sim_entry.get()) if sim_entry.get() else None)
        for word_entry, sim_entry in input_fields
        if sim_entry.get() or word_entry.get()
    }
    print("Calculating with:", word_sim_pairs)
    # Your calculation logic here
    attempt = TerminalAttempt(list(word_sim_pairs.keys()))
    viable_candidates = attempt.get_viable_candidates(word_sim_pairs)
    print(viable_candidates)

    result_label.config(text=f"Result: {viable_candidates}")


def add_row():
    """Adds a new row of input fields."""
    global row_counter
    row_counter += 1

    frame = ttk.Frame(input_frame, padding=(5, 5, 5, 0))
    frame.grid(row=row_counter - 1, column=0, sticky="ew")
    input_frame.columnconfigure(0, weight=1)

    word_label = ttk.Label(frame, text=f"Word {row_counter}:")
    word_label.grid(row=0, column=0, padx=5, pady=2, sticky=tk.W)

    word_entry = ttk.Entry(frame)
    word_entry.grid(row=0, column=1, padx=5, pady=2, sticky=tk.EW)
    frame.columnconfigure(1, weight=1)

    sim_label = ttk.Label(frame, text=f"Similarity {row_counter}:")
    sim_label.grid(row=0, column=2, padx=5, pady=2, sticky=tk.W)

    sim_entry = ttk.Entry(frame)
    sim_entry.grid(row=0, column=3, padx=5, pady=2, sticky=tk.EW)
    frame.columnconfigure(3, weight=1)

    input_fields.append((word_entry, sim_entry))
    input_frames.append(frame)


def remove_row():
    global row_counter
    if row_counter > 1:
        frame_to_remove = input_frames.pop()
        frame_to_remove.destroy()
        input_fields.pop()
        row_counter -= 1


root = tk.Tk()
root.title("Word Similarity Input")

input_fields = []
input_frames = []
row_counter = 0

# Main frames using grid
input_frame = ttk.Frame(root, padding=10)
input_frame.grid(row=0, column=0, sticky="nsew")

button_frame = ttk.Frame(root, padding=10)
button_frame.grid(row=1, column=0, sticky="ew")

result_frame = ttk.Frame(root, padding=10)  # Frame for the result
result_frame.grid(row=2, column=0, sticky="ew")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(2, weight=1)  # configure row for result

# Initial rows
for _ in range(5):
    add_row()

# Buttons
reset_button = ttk.Button(button_frame, text="Reset", command=reset_fields)
reset_button.grid(row=0, column=0, padx=5)

calculate_button = ttk.Button(
    button_frame, text="Calculate Candidates", command=calculate_candidates
)
calculate_button.grid(row=0, column=1, padx=5)

add_row_button = ttk.Button(button_frame, text="Add Row", command=add_row)
add_row_button.grid(row=0, column=2, padx=5)

remove_row_button = ttk.Button(button_frame, text="Remove Row", command=remove_row)
remove_row_button.grid(row=0, column=3, padx=5)

# Result Label
result_label = ttk.Label(result_frame, text="Result: ")
result_label.pack(pady=5)  # pack used for single element in frame

root.mainloop()
