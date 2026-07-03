import customtkinter as ctk


class MTNApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        # --------------------
        # WINDOW
        # --------------------

        self.title("MTN Offer Automation")

        self.geometry("1100x750")

        ctk.set_appearance_mode("Dark")

        # --------------------
        # DATA VARIABLES
        # --------------------

        self.total_records = 0

        self.stop_requested = False

        # --------------------
        # TITLE
        # --------------------

        self.title_label = ctk.CTkLabel(
            self,
            text="MTN Offer Automation",
            font=("Segoe UI", 32, "bold")
        )

        self.title_label.pack(
            pady=(20, 10)
        )

        # --------------------
        # WORKBOOK
        # --------------------

        self.workbook_label = ctk.CTkLabel(
            self,
            text="Workbook: Not Loaded",
            font=("Segoe UI", 14)
        )

        self.workbook_label.pack()

        # --------------------
        # STATUS
        # --------------------

        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            font=("Segoe UI", 16)
        )

        self.status_label.pack(
            pady=5
        )

        # --------------------
        # PROGRESS COUNTER
        # --------------------

        self.progress_counter = ctk.CTkLabel(
            self,
            text="0 / 0",
            font=("Segoe UI", 18)
        )

        self.progress_counter.pack()

        # --------------------
        # PROGRESS BAR
        # --------------------

        self.progress_bar = ctk.CTkProgressBar(
            self,
            width=750
        )

        self.progress_bar.pack(
            pady=15
        )

        self.progress_bar.set(0)

        # --------------------
        # METRICS
        # --------------------

        self.metrics_frame = ctk.CTkFrame(
            self
        )

        self.metrics_frame.pack(
            pady=10
        )

        self.speed_label = ctk.CTkLabel(
            self.metrics_frame,
            text="Speed: 0.0/min"
        )

        self.speed_label.grid(
            row=0,
            column=0,
            padx=20,
            pady=10
        )

        self.failures_label = ctk.CTkLabel(
            self.metrics_frame,
            text="Failures: 0"
        )

        self.failures_label.grid(
            row=0,
            column=1,
            padx=20,
            pady=10
        )

        self.checkpoint_label = ctk.CTkLabel(
            self.metrics_frame,
            text="Checkpoint: 0"
        )

        self.checkpoint_label.grid(
            row=0,
            column=2,
            padx=20,
            pady=10
        )

        # --------------------
        # CURRENT NUMBER
        # --------------------

        self.current_label = ctk.CTkLabel(
            self,
            text="Current Number: None",
            font=("Segoe UI", 18)
        )

        self.current_label.pack(
            pady=10
        )

        # --------------------
        # BUTTONS
        # --------------------

        self.button_frame = ctk.CTkFrame(
            self
        )

        self.button_frame.pack(
            pady=10
        )

        self.start_btn = ctk.CTkButton(
            self.button_frame,
            text="Start"
        )

        self.start_btn.grid(
            row=0,
            column=0,
            padx=10
        )

        self.stop_btn = ctk.CTkButton(
            self.button_frame,
            text="Stop",
            fg_color="red",
            command=self.stop
        )

        self.stop_btn.grid(
            row=0,
            column=1,
            padx=10
        )

        self.resume_btn = ctk.CTkButton(
            self.button_frame,
            text="Resume"
        )

        self.resume_btn.grid(
            row=0,
            column=2,
            padx=10
        )

        # --------------------
        # LOG
        # --------------------

        self.log_label = ctk.CTkLabel(
            self,
            text="Live Log"
        )

        self.log_label.pack(
            pady=(20, 5)
        )

        self.log_box = ctk.CTkTextbox(
            self,
            width=1000,
            height=260
        )

        self.log_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.log(
            "Application Ready"
        )

    # ====================================================
    # FUNCTIONS TO BE CALLED FROM YOUR MAIN SCRIPT
    # ====================================================

    def load_workbook(
        self,
        workbook_name,
        total_records
    ):

        self.total_records = total_records

        self.workbook_label.configure(
            text=f"Workbook: {workbook_name}"
        )

        self.progress_counter.configure(
            text=f"0 / {total_records:,}"
        )

        self.status_label.configure(
            text=f"Workbook Loaded ({total_records:,} records)"
        )

    def update_progress(
        self,
        processed,
        speed,
        failures,
        checkpoint,
        current_number
    ):

        # Counter

        self.progress_counter.configure(
            text=f"{processed:,} / {self.total_records:,}"
        )

        # Progress bar

        if self.total_records > 0:

            self.progress_bar.set(
                processed /
                self.total_records
            )

        # Metrics

        self.speed_label.configure(
            text=f"Speed: {speed:.1f}/min"
        )

        self.failures_label.configure(
            text=f"Failures: {failures:,}"
        )

        self.checkpoint_label.configure(
            text=f"Checkpoint: {checkpoint:,}"
        )

        self.current_label.configure(
            text=f"Current Number: {current_number}"
        )

    def set_status(
        self,
        status
    ):

        self.status_label.configure(
            text=status
        )

    def log(
        self,
        message
    ):

        self.log_box.insert(
            "end",
            f"{message}\n"
        )

        self.log_box.see("end")

    def stop(self):

        self.stop_requested = True

        self.log(
            "Stop requested..."
        )

        self.set_status(
            "Stopping..."
        )


if __name__ == "__main__":

    app = MTNApp()

    app.mainloop()