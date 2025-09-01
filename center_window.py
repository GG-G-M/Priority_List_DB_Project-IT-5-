class center:
    def __init__(self, window, width, height):

        window.update_idletasks()  # window is drawn before we center it
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        # Find the Mid of the Scween
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        # Set the W x H at the x+y Position of the Screen
        window.geometry(f'{width}x{height}+{x}+{y}')