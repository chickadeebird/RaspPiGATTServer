import multiprocessing
import tkinter as tk
import time
import dbus
from server.ble_process import BLEProcess


dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

def gui(queue):
    """GUI process that retrieves data from the queue and displays it."""
    # window = tk.Tk()
    # window.title("Multiprocess Data Sharing")
    # label = tk.Label(window, text="Blue Chick")
    # label.pack(padx=20, pady=20)
    
    root = tk.Tk()
    root.attributes('-fullscreen', True)
    # root.config(cursor="none")
    frame = tk.Frame(root, width=200, height=200, background="red")
    frame.pack(fill=tk.BOTH, expand=True)
    
    output_queue = multiprocessing.Queue()

    ble_process = BLEProcess(output_queue)
    ble_process.start()

    def update_label():
        try:
            curr_value = output_queue.get(timeout=1)
            uuid = curr_value['uuid']
            sent_value = curr_value['value']
            # string_value = sent_value.split('\\x')[-1]
            string_value = sent_value[-1:]
            int_value = ord(string_value)
            # string_value = sent_value[-2]
            # int_value2 = ord(string_value)
            int_value = int_value
            
            int_hexstring = "{0:x}".format(int_value)
            if len(int_hexstring) < 2:
                int_hexstring = '0' + int_hexstring

            colour_string = '#' + int_hexstring + int_hexstring + int_hexstring
            
            # print(f"Value written to Characteristic with UUID {uuid}: {int_value2}: {int_value}: {colour_string}")
            print(f"Full object {curr_value}")
            
            # data = queue.get_nowait()
            # label.config(text=data)
            frame.config(bg=colour_string)
        except multiprocessing.queues.Empty:
            pass
        root.after(100, update_label)  # Schedule the update every 100 ms

    update_label()
    root.mainloop()

if __name__ == "__main__":
    queue = multiprocessing.Queue()
    # process_worker = multiprocessing.Process(target=worker, args=(queue,))
    process_gui = multiprocessing.Process(target=gui, args=(queue,))

    # process_worker.start()
    process_gui.start()

    # process_worker.join()
    process_gui.join()
