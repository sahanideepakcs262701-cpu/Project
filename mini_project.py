import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os

CSV_FILE = r"C:\Deepak\Data Science\mini_project.csv"

BG = "#F3F7F9"
WHITE = "#FFFFFF"
NAVY = "#102F3D"
NAVY2 = "#19495A"
PRIMARY = "#07838E"
PRIMARY_DARK = "#05636D"
TEAL = "#18A6A7"
LIGHT_TEAL = "#E6F7F8"
GREEN = "#239B62"
RED = "#D9535F"
ORANGE = "#E58A32"
PURPLE = "#7357A6"
TEXT = "#17313B"
MUTED = "#6F818A"
BORDER = "#D9E6EA"
SOFT_RED = "#FFF0F2"
SOFT_GREEN = "#ECF9F2"
SOFT_ORANGE = "#FFF5E9"

sns.set_theme(style="whitegrid")

if not os.path.exists(CSV_FILE):
    alternative = r"C:\Deepak\Data Science\mini_project.csv.csv"

    if os.path.exists(alternative):
        CSV_FILE = alternative
    else:
        temp_root = tk.Tk()
        temp_root.withdraw()
        messagebox.showerror(
            "Dataset Not Found",
            "CSV file was not found.\n\n"
            "Please keep your file here:\n\n"
            r"C:\Deepak\Data Science\mini_project.csv"
        )
        temp_root.destroy()
        raise SystemExit

df = pd.read_csv(CSV_FILE)

df.columns = df.columns.astype(str).str.strip()

original_df = df.copy()

df = df.drop_duplicates()

for column in df.columns:
    if df[column].dtype == "object":
        df[column] = df[column].astype(str).str.strip()

for column in df.select_dtypes(include=np.number).columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

for column in df.select_dtypes(include=np.number).columns:
    if df[column].isnull().sum() > 0:
        df[column] = df[column].fillna(df[column].median())


def find_column(names):
    normalized = {}

    for column in df.columns:
        key = str(column).lower().replace("_", "").replace(" ", "")
        normalized[key] = column

    for name in names:
        key = name.lower().replace("_", "").replace(" ", "")

        if key in normalized:
            return normalized[key]

    for column in df.columns:
        key = str(column).lower().replace("_", "").replace(" ", "")

        for name in names:
            search = name.lower().replace("_", "").replace(" ", "")

            if search in key:
                return column

    return None


AGE_COL = find_column(["Age"])

SEX_COL = find_column(["Sex", "Gender"])

CHOLESTEROL_COL = find_column([
    "Cholesterol",
    "Chol"
])

TARGET_COL = find_column([
    "HeartDisease",
    "Heart Disease",
    "Target",
    "Outcome",
    "Heart_Disease"
])

MAXHR_COL = find_column([
    "MaxHR",
    "MaximumHeartRate",
    "Maximum Heart Rate"
])

CHEST_COL = find_column([
    "ChestPainType",
    "ChestPain",
    "Chest Pain Type"
])

EXERCISE_COL = find_column([
    "ExerciseAngina",
    "Exercise Angina"
])

ST_COL = find_column([
    "ST_Slope",
    "ST Slope"
])


def positive_target(value):
    text = str(value).lower().strip()

    return text in [
        "1",
        "yes",
        "true",
        "heart disease",
        "disease",
        "positive"
    ]


def get_positive_count(data=None):
    if data is None:
        data = df

    if TARGET_COL is None:
        return 0

    return int(
        data[TARGET_COL].apply(positive_target).sum()
    )


def get_negative_count(data=None):
    if data is None:
        data = df

    if TARGET_COL is None:
        return 0

    return int(
        (~data[TARGET_COL].apply(positive_target)).sum()
    )


class HealthIQ:

    def __init__(self, root):

        self.root = root

        self.root.title(
            "HEALTHIQ | Patient Health Analytics"
        )

        self.root.geometry("1500x950")
        self.root.minsize(1100, 700)
        self.root.configure(bg=BG)

        try:
            self.root.state("zoomed")
        except:
            pass

        self.filtered_df = df.copy()
        self.chart_canvases = []

        self.setup_style()
        self.build_interface()
        self.show_page("dashboard")

    def setup_style(self):

        style = ttk.Style()

        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            rowheight=34,
            fieldbackground=WHITE,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background=NAVY,
            foreground=WHITE,
            font=("Segoe UI", 10, "bold"),
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", PRIMARY)],
            foreground=[("selected", WHITE)]
        )

        style.configure(
            "TCombobox",
            padding=8,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Vertical.TScrollbar",
            background="#D7E4E8"
        )

    def build_interface(self):

        self.sidebar = tk.Frame(
            self.root,
            bg=NAVY,
            width=255
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        self.right_area = tk.Frame(
            self.root,
            bg=BG
        )

        self.right_area.pack(
            side="right",
            fill="both",
            expand=True
        )

        self.build_sidebar()
        self.build_topbar()

        self.content = tk.Frame(
            self.right_area,
            bg=BG
        )

        self.content.pack(
            fill="both",
            expand=True,
            padx=28,
            pady=24
        )

    def build_sidebar(self):

        logo_box = tk.Frame(
            self.sidebar,
            bg=NAVY
        )

        logo_box.pack(
            fill="x",
            padx=25,
            pady=(28, 32)
        )

        tk.Label(
            logo_box,
            text="♥",
            bg=NAVY,
            fg="#65D6D4",
            font=("Arial", 30, "bold")
        ).pack(anchor="w")

        tk.Label(
            logo_box,
            text="HEALTHIQ",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 23, "bold")
        ).pack(anchor="w")

        tk.Label(
            logo_box,
            text="PATIENT HEALTH ANALYTICS",
            bg=NAVY,
            fg="#91C9D1",
            font=("Segoe UI", 8, "bold")
        ).pack(
            anchor="w",
            pady=(3, 0)
        )

        self.nav_buttons = {}

        navigation = [
            ("dashboard", "⌂", "Dashboard"),
            ("analysis", "▤", "Data Analysis"),
            ("charts", "◈", "Visual Analytics"),
            ("dataset", "▥", "Dataset Explorer")
        ]

        for key, icon, text in navigation:

            button = tk.Button(
                self.sidebar,
                text=f"  {icon}    {text}",
                command=lambda page=key: self.show_page(page),
                bg=NAVY,
                fg="#D8E7EB",
                activebackground=PRIMARY,
                activeforeground=WHITE,
                relief="flat",
                bd=0,
                anchor="w",
                padx=20,
                font=("Segoe UI", 11),
                cursor="hand2"
            )

            button.pack(
                fill="x",
                padx=12,
                pady=4,
                ipady=12
            )

            self.nav_buttons[key] = button

        bottom = tk.Frame(
            self.sidebar,
            bg=NAVY
        )

        bottom.pack(
            side="bottom",
            fill="x",
            padx=25,
            pady=25
        )

        tk.Label(
            bottom,
            text="DATA SCIENCE PROJECT",
            bg=NAVY,
            fg="#82A9B3",
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        tk.Label(
            bottom,
            text="Python • Pandas • NumPy",
            bg=NAVY,
            fg="#82A9B3",
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            pady=3
        )

        tk.Label(
            bottom,
            text="Matplotlib • Seaborn • BeautifulSoup",
            bg=NAVY,
            fg="#82A9B3",
            font=("Segoe UI", 8)
        ).pack(anchor="w")

    def build_topbar(self):

        self.topbar = tk.Frame(
            self.right_area,
            bg=WHITE,
            height=88,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        self.topbar.pack(fill="x")
        self.topbar.pack_propagate(False)

        left = tk.Frame(
            self.topbar,
            bg=WHITE
        )

        left.pack(
            side="left",
            padx=28,
            pady=12
        )

        self.page_title = tk.Label(
            left,
            text="Dashboard",
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 21, "bold")
        )

        self.page_title.pack(anchor="w")

        self.page_subtitle = tk.Label(
            left,
            text="Patient health data overview",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9)
        )

        self.page_subtitle.pack(
            anchor="w",
            pady=(2, 0)
        )

        right = tk.Frame(
            self.topbar,
            bg=WHITE
        )

        right.pack(
            side="right",
            padx=28
        )

        tk.Label(
            right,
            text="● SYSTEM ONLINE",
            bg=SOFT_GREEN,
            fg=GREEN,
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=7
        ).pack(
            side="left",
            padx=6
        )

        tk.Label(
            right,
            text=f"{len(df):,} RECORDS",
            bg=LIGHT_TEAL,
            fg=PRIMARY_DARK,
            font=("Segoe UI", 9, "bold"),
            padx=14,
            pady=7
        ).pack(
            side="left",
            padx=6
        )

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

        self.chart_canvases = []

    def show_page(self, page):

        self.clear_content()

        for key, button in self.nav_buttons.items():

            if key == page:
                button.configure(
                    bg=PRIMARY,
                    fg=WHITE
                )
            else:
                button.configure(
                    bg=NAVY,
                    fg="#D8E7EB"
                )

        if page == "dashboard":

            self.page_title.config(
                text="Dashboard"
            )

            self.page_subtitle.config(
                text="Patient health data overview"
            )

            self.dashboard_page()

        elif page == "analysis":

            self.page_title.config(
                text="Data Analysis"
            )

            self.page_subtitle.config(
                text="Statistical analysis using Pandas and NumPy"
            )

            self.analysis_page()

        elif page == "charts":

            self.page_title.config(
                text="Visual Analytics"
            )

            self.page_subtitle.config(
                text="Healthcare insights through visualizations"
            )

            self.charts_page()

        elif page == "dataset":

            self.page_title.config(
                text="Dataset Explorer"
            )

            self.page_subtitle.config(
                text="Search, filter and explore patient records"
            )

            self.dataset_page()

    def section_title(
        self,
        parent,
        title,
        subtitle=""
    ):

        frame = tk.Frame(
            parent,
            bg=BG
        )

        frame.pack(
            fill="x",
            pady=(0, 14)
        )

        tk.Label(
            frame,
            text=title,
            bg=BG,
            fg=NAVY,
            font=("Segoe UI", 17, "bold")
        ).pack(anchor="w")

        if subtitle:

            tk.Label(
                frame,
                text=subtitle,
                bg=BG,
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                pady=(3, 0)
            )

    def stat_card(
        self,
        parent,
        title,
        value,
        subtitle,
        color,
        bg_color
    ):

        card = tk.Frame(
            parent,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        top = tk.Frame(
            card,
            bg=WHITE
        )

        top.pack(
            fill="x",
            padx=18,
            pady=(16, 4)
        )

        tk.Label(
            top,
            text="●",
            bg=WHITE,
            fg=color,
            font=("Arial", 9)
        ).pack(side="left")

        tk.Label(
            top,
            text=f"  {title}",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left")

        tk.Label(
            card,
            text=value,
            bg=WHITE,
            fg=color,
            font=("Segoe UI", 25, "bold")
        ).pack(
            anchor="w",
            padx=18
        )

        tk.Label(
            card,
            text=subtitle,
            bg=bg_color,
            fg=color,
            font=("Segoe UI", 8, "bold"),
            padx=8,
            pady=4
        ).pack(
            anchor="w",
            padx=18,
            pady=(3, 16)
        )

        return card

    def dashboard_page(self):

        page = self.create_scroll_page()

        hero = tk.Frame(
            page,
            bg=LIGHT_TEAL,
            highlightbackground="#C6E7E9",
            highlightthickness=1
        )

        hero.pack(
            fill="x",
            pady=(0, 25)
        )

        hero.grid_columnconfigure(
            0,
            weight=3
        )

        hero.grid_columnconfigure(
            1,
            weight=2
        )

        hero.grid_rowconfigure(
            0,
            weight=1
        )

        hero_left = tk.Frame(
            hero,
            bg=LIGHT_TEAL
        )

        hero_left.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(30, 15),
            pady=30
        )

        badge = tk.Label(
            hero_left,
            text="  PATIENT HEALTH ANALYTICS  ",
            bg=PRIMARY,
            fg=WHITE,
            font=("Segoe UI", 9, "bold"),
            padx=10,
            pady=6
        )

        badge.pack(
            anchor="w",
            pady=(0, 13)
        )

        title_frame = tk.Frame(
            hero_left,
            bg=LIGHT_TEAL
        )

        title_frame.pack(
            anchor="w",
            fill="x"
        )

        tk.Label(
            title_frame,
            text="Understand Health.",
            bg=LIGHT_TEAL,
            fg=NAVY,
            font=("Segoe UI", 30, "bold")
        ).pack(anchor="w")

        highlight = tk.Frame(
            title_frame,
            bg=LIGHT_TEAL
        )

        highlight.pack(
            anchor="w",
            pady=(0, 8)
        )

        tk.Label(
            highlight,
            text="Discover Insights.",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 30, "bold"),
            padx=10,
            pady=2
        ).pack(anchor="w")

        tk.Label(
            hero_left,
            text="Explore patient records, identify heart disease patterns",
            bg=LIGHT_TEAL,
            fg=MUTED,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w",
            pady=(2, 0)
        )

        tk.Label(
            hero_left,
            text="and transform healthcare data into meaningful insights.",
            bg=LIGHT_TEAL,
            fg=MUTED,
            font=("Segoe UI", 11)
        ).pack(
            anchor="w"
        )

        tags = tk.Frame(
            hero_left,
            bg=LIGHT_TEAL
        )

        tags.pack(
            anchor="w",
            pady=(17, 0)
        )

        for text, color, bg_color in [
            ("PANDAS", PRIMARY, WHITE),
            ("NUMPY", PURPLE, WHITE),
            ("MATPLOTLIB", ORANGE, WHITE),
            ("SEABORN", GREEN, WHITE)
        ]:

            tk.Label(
                tags,
                text=text,
                bg=bg_color,
                fg=color,
                font=("Segoe UI", 8, "bold"),
                padx=9,
                pady=5
            ).pack(
                side="left",
                padx=(0, 7)
            )

        image_area = tk.Frame(
            hero,
            bg=LIGHT_TEAL
        )

        image_area.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 25),
            pady=25
        )

        self.health_illustration(
            image_area
        )

        self.section_title(
            page,
            "Health Overview",
            "Important statistics from your patient dataset"
        )

        cards = tk.Frame(
            page,
            bg=BG
        )

        cards.pack(
            fill="x",
            pady=(0, 25)
        )

        for i in range(4):
            cards.columnconfigure(
                i,
                weight=1
            )

        avg_age = (
            f"{df[AGE_COL].mean():.1f}"
            if AGE_COL else "N/A"
        )

        max_chol = (
            f"{df[CHOLESTEROL_COL].max():.0f}"
            if CHOLESTEROL_COL else "N/A"
        )

        values = [
            (
                "TOTAL PATIENTS",
                f"{len(df):,}",
                "All records",
                PRIMARY,
                LIGHT_TEAL
            ),
            (
                "HEART DISEASE",
                f"{get_positive_count():,}",
                "Positive cases",
                RED,
                SOFT_RED
            ),
            (
                "AVERAGE AGE",
                avg_age,
                "Years",
                GREEN,
                SOFT_GREEN
            ),
            (
                "MAX CHOLESTEROL",
                max_chol,
                "Highest value",
                ORANGE,
                SOFT_ORANGE
            )
        ]

        for i, data in enumerate(values):

            card = self.stat_card(
                cards,
                *data
            )

            card.grid(
                row=0,
                column=i,
                sticky="ew",
                padx=6
            )

        self.section_title(
            page,
            "Health Insights",
            "Visual summary of important patient characteristics"
        )

        chart_grid = tk.Frame(
            page,
            bg=BG
        )

        chart_grid.pack(
            fill="x",
            pady=(0, 25)
        )

        chart_grid.columnconfigure(
            0,
            weight=1
        )

        chart_grid.columnconfigure(
            1,
            weight=1
        )

        first = self.chart_box(
            chart_grid,
            "Heart Disease by Gender",
            0,
            0
        )

        second = self.chart_box(
            chart_grid,
            "Age Distribution",
            0,
            1
        )

        self.dashboard_gender_chart(first)
        self.dashboard_age_chart(second)

        self.section_title(
            page,
            "Key Findings",
            "Automatically generated observations from the dataset"
        )

        findings = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        findings.pack(
            fill="x",
            pady=(0, 30)
        )

        self.create_findings(findings)

    def health_illustration(self, parent):

        canvas = tk.Canvas(
            parent,
            bg=LIGHT_TEAL,
            highlightthickness=0,
            height=250
        )

        canvas.pack(
            fill="both",
            expand=True
        )

        canvas.create_oval(
            70,
            20,
            280,
            230,
            fill=WHITE,
            outline=""
        )

        canvas.create_oval(
            105,
            55,
            245,
            195,
            fill="#F4FBFB",
            outline="#D3EEEE",
            width=2
        )

        canvas.create_text(
            175,
            108,
            text="♥",
            fill=RED,
            font=("Arial", 68, "bold")
        )

        points = [
            25, 145,
            55, 145,
            72, 145,
            85, 145,
            98, 145,
            112, 145,
            124, 108,
            140, 178,
            157, 126,
            172, 145,
            205, 145,
            230, 145,
            255, 145,
            280, 145,
            315, 145
        ]

        canvas.create_line(
            *points,
            fill=PRIMARY,
            width=4
        )

        canvas.create_oval(
            255,
            25,
            320,
            90,
            fill="#D4F1F2",
            outline=""
        )

        canvas.create_text(
            287,
            57,
            text="+",
            fill=PRIMARY,
            font=("Arial", 27, "bold")
        )

        canvas.create_text(
            175,
            220,
            text="HEALTH  •  HEART  •  WELLNESS",
            fill=PRIMARY_DARK,
            font=("Segoe UI", 9, "bold")
        )

    def chart_box(
        self,
        parent,
        title,
        row,
        column
    ):

        box = tk.Frame(
            parent,
            bg=WHITE,
            height=365,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        box.grid(
            row=row,
            column=column,
            sticky="nsew",
            padx=6,
            pady=6
        )

        box.grid_propagate(False)

        tk.Label(
            box,
            text=title,
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 12, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(15, 0)
        )

        return box

    def create_figure(
        self,
        parent,
        width=6,
        height=3
    ):

        fig = Figure(
            figsize=(width, height),
            dpi=90,
            facecolor=WHITE
        )

        canvas = FigureCanvasTkAgg(
            fig,
            master=parent
        )

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True,
            padx=10,
            pady=5
        )

        self.chart_canvases.append(canvas)

        return fig, canvas

    def dashboard_gender_chart(self, parent):

        if SEX_COL is None or TARGET_COL is None:
            return

        temp = df.copy()

        temp["_Disease"] = temp[
            TARGET_COL
        ].apply(positive_target)

        result = temp.groupby(
            SEX_COL
        )["_Disease"].sum()

        fig, canvas = self.create_figure(
            parent,
            6,
            2.8
        )

        ax = fig.add_subplot(111)

        ax.bar(
            result.index.astype(str),
            result.values
        )

        ax.set_ylabel(
            "Cases",
            fontsize=9
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()

        canvas.draw()

    def dashboard_age_chart(self, parent):

        if AGE_COL is None:
            return

        fig, canvas = self.create_figure(
            parent,
            6,
            2.8
        )

        ax = fig.add_subplot(111)

        sns.histplot(
            df[AGE_COL].dropna(),
            bins=15,
            kde=True,
            ax=ax
        )

        ax.set_xlabel(
            "Age",
            fontsize=9
        )

        ax.set_ylabel(
            "Patients",
            fontsize=9
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()

        canvas.draw()

    def create_findings(self, parent):

        findings = []

        if AGE_COL:

            findings.append(
                (
                    "01",
                    "Age Insight",
                    f"The average patient age is {df[AGE_COL].mean():.1f} years."
                )
            )

        if CHOLESTEROL_COL:

            findings.append(
                (
                    "02",
                    "Cholesterol Insight",
                    f"The highest recorded cholesterol value is {df[CHOLESTEROL_COL].max():.0f}."
                )
            )

        if MAXHR_COL:

            findings.append(
                (
                    "03",
                    "Heart Rate Insight",
                    f"The maximum recorded heart rate is {df[MAXHR_COL].max():.0f}."
                )
            )

        if TARGET_COL:

            percentage = (
                get_positive_count() / len(df) * 100
                if len(df) > 0
                else 0
            )

            findings.append(
                (
                    "04",
                    "Disease Insight",
                    f"{percentage:.1f}% of the records are classified as positive cases."
                )
            )

        if SEX_COL:

            common_gender = (
                df[SEX_COL]
                .value_counts()
                .idxmax()
            )

            findings.append(
                (
                    "05",
                    "Gender Insight",
                    f"{common_gender} is the most frequently recorded gender category."
                )
            )

        for number, title, text in findings:

            row = tk.Frame(
                parent,
                bg=WHITE
            )

            row.pack(
                fill="x",
                padx=20,
                pady=10
            )

            tk.Label(
                row,
                text=number,
                bg=PRIMARY,
                fg=WHITE,
                font=("Segoe UI", 9, "bold"),
                width=4,
                pady=5
            ).pack(
                side="left"
            )

            text_box = tk.Frame(
                row,
                bg=WHITE
            )

            text_box.pack(
                side="left",
                fill="x",
                expand=True,
                padx=15
            )

            tk.Label(
                text_box,
                text=title,
                bg=WHITE,
                fg=NAVY,
                font=("Segoe UI", 10, "bold")
            ).pack(anchor="w")

            tk.Label(
                text_box,
                text=text,
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 9)
            ).pack(
                anchor="w",
                pady=(2, 0)
            )

    def create_scroll_page(self):

        canvas = tk.Canvas(
            self.content,
            bg=BG,
            highlightthickness=0
        )

        scrollbar = ttk.Scrollbar(
            self.content,
            orient="vertical",
            command=canvas.yview
        )

        page = tk.Frame(
            canvas,
            bg=BG
        )

        window = canvas.create_window(
            (0, 0),
            window=page,
            anchor="nw"
        )

        page.bind(
            "<Configure>",
            lambda event: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda event: canvas.itemconfigure(
                window,
                width=event.width
            )
        )

        canvas.configure(
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        return page

    def analysis_page(self):

        page = self.create_scroll_page()

        self.section_title(
            page,
            "Dataset Summary",
            "Pandas-based information about the loaded dataset"
        )

        summary = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        summary.pack(
            fill="x",
            pady=(0, 25)
        )

        items = [
            ("ROWS", len(df)),
            ("COLUMNS", len(df.columns)),
            ("DUPLICATES REMOVED", len(original_df) - len(df)),
            ("NUMERIC COLUMNS", len(df.select_dtypes(include=np.number).columns)),
            ("CATEGORICAL COLUMNS", len(df.select_dtypes(include="object").columns)),
            ("MISSING VALUES", int(df.isnull().sum().sum()))
        ]

        for i, (title, value) in enumerate(items):

            summary.columnconfigure(
                i % 3,
                weight=1
            )

            box = tk.Frame(
                summary,
                bg=WHITE
            )

            box.grid(
                row=i // 3,
                column=i % 3,
                sticky="ew",
                padx=25,
                pady=18
            )

            tk.Label(
                box,
                text=title,
                bg=WHITE,
                fg=MUTED,
                font=("Segoe UI", 8, "bold")
            ).pack(anchor="w")

            tk.Label(
                box,
                text=f"{value:,}",
                bg=WHITE,
                fg=PRIMARY,
                font=("Segoe UI", 20, "bold")
            ).pack(anchor="w")

        self.section_title(
            page,
            "Statistical Analysis",
            "Mean, median, minimum, maximum, standard deviation and groupby operations"
        )

        analysis_box = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        analysis_box.pack(
            fill="x",
            pady=(0, 25)
        )

        text = tk.Text(
            analysis_box,
            bg=WHITE,
            fg=TEXT,
            font=("Consolas", 10),
            relief="flat",
            wrap="word",
            height=27,
            padx=25,
            pady=20
        )

        text.pack(
            fill="both",
            expand=True
        )

        lines = []

        if AGE_COL:

            age = df[AGE_COL].dropna()

            lines.extend([
                "AGE ANALYSIS",
                "────────────────────────────────────────",
                f"Mean Age       : {np.mean(age):.2f}",
                f"Median Age     : {np.median(age):.2f}",
                f"Minimum Age    : {np.min(age):.2f}",
                f"Maximum Age    : {np.max(age):.2f}",
                f"Age Sum        : {np.sum(age):.2f}",
                f"Age Count      : {np.count_nonzero(age):,}",
                f"Standard Dev.  : {np.std(age):.2f}",
                ""
            ])

        if CHOLESTEROL_COL:

            cholesterol = df[
                CHOLESTEROL_COL
            ].dropna()

            lines.extend([
                "CHOLESTEROL ANALYSIS",
                "────────────────────────────────────────",
                f"Average        : {np.mean(cholesterol):.2f}",
                f"Minimum        : {np.min(cholesterol):.2f}",
                f"Maximum        : {np.max(cholesterol):.2f}",
                f"Standard Dev.  : {np.std(cholesterol):.2f}",
                ""
            ])

        if MAXHR_COL:

            maxhr = df[
                MAXHR_COL
            ].dropna()

            lines.extend([
                "MAXIMUM HEART RATE ANALYSIS",
                "────────────────────────────────────────",
                f"Average        : {np.mean(maxhr):.2f}",
                f"Minimum        : {np.min(maxhr):.2f}",
                f"Maximum        : {np.max(maxhr):.2f}",
                ""
            ])

        if SEX_COL:

            lines.extend([
                "GENDER COUNTS",
                "────────────────────────────────────────",
                df[SEX_COL].value_counts().to_string(),
                ""
            ])

        if CHEST_COL:

            lines.extend([
                "CHEST PAIN COUNTS",
                "────────────────────────────────────────",
                df[CHEST_COL].value_counts().to_string(),
                ""
            ])

        if TARGET_COL:

            lines.extend([
                "HEART DISEASE COUNTS",
                "────────────────────────────────────────",
                df[TARGET_COL].value_counts().to_string(),
                ""
            ])

        if SEX_COL and AGE_COL:

            group = (
                df.groupby(SEX_COL)[AGE_COL]
                .mean()
                .sort_values(ascending=False)
            )

            lines.extend([
                "AVERAGE AGE BY GENDER",
                "────────────────────────────────────────",
                group.to_string(),
                ""
            ])

        if CHEST_COL and AGE_COL:

            group = (
                df.groupby(CHEST_COL)[AGE_COL]
                .mean()
                .sort_values(ascending=False)
            )

            lines.extend([
                "AVERAGE AGE BY CHEST PAIN TYPE",
                "────────────────────────────────────────",
                group.to_string(),
                ""
            ])

        text.insert(
            "1.0",
            "\n".join(lines)
        )

        text.configure(
            state="disabled"
        )

        self.section_title(
            page,
            "Column Information",
            "Column names and Pandas data types"
        )

        dtype_box = tk.Frame(
            page,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        dtype_box.pack(
            fill="x",
            pady=(0, 25)
        )

        for column in df.columns:

            row = tk.Frame(
                dtype_box,
                bg=WHITE
            )

            row.pack(
                fill="x",
                padx=25,
                pady=8
            )

            tk.Label(
                row,
                text=str(column),
                bg=WHITE,
                fg=NAVY,
                font=("Segoe UI", 10, "bold"),
                width=32,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                row,
                text=str(df[column].dtype),
                bg=LIGHT_TEAL,
                fg=PRIMARY_DARK,
                font=("Segoe UI", 9, "bold"),
                padx=10,
                pady=4
            ).pack(side="left")

    def charts_page(self):

        page = self.create_scroll_page()

        self.section_title(
            page,
            "Healthcare Visual Analytics",
            "Five meaningful visualizations created using Matplotlib and Seaborn"
        )

        grid = tk.Frame(
            page,
            bg=BG
        )

        grid.pack(
            fill="x"
        )

        grid.columnconfigure(
            0,
            weight=1
        )

        grid.columnconfigure(
            1,
            weight=1
        )

        chart1 = self.visual_card(
            grid,
            "01",
            "Heart Disease by Gender",
            "Comparison of positive heart disease cases",
            0,
            0
        )

        chart2 = self.visual_card(
            grid,
            "02",
            "Age Distribution",
            "Distribution of patient ages",
            0,
            1
        )

        chart3 = self.visual_card(
            grid,
            "03",
            "Chest Pain Types",
            "Frequency of different chest pain categories",
            1,
            0
        )

        chart4 = self.visual_card(
            grid,
            "04",
            "Cholesterol Distribution",
            "Distribution and spread of cholesterol values",
            1,
            1
        )

        chart5 = self.visual_card(
            grid,
            "05",
            "Maximum Heart Rate",
            "Distribution of maximum heart rate",
            2,
            0,
            2
        )

        self.draw_gender_chart(chart1)
        self.draw_age_chart(chart2)
        self.draw_chest_chart(chart3)
        self.draw_cholesterol_chart(chart4)
        self.draw_maxhr_chart(chart5)

    def visual_card(
        self,
        parent,
        number,
        title,
        subtitle,
        row,
        column,
        span=1
    ):

        box = tk.Frame(
            parent,
            bg=WHITE,
            height=390,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        box.grid(
            row=row,
            column=column,
            columnspan=span,
            sticky="nsew",
            padx=7,
            pady=7
        )

        box.grid_propagate(False)

        heading = tk.Frame(
            box,
            bg=WHITE
        )

        heading.pack(
            fill="x",
            padx=18,
            pady=(15, 0)
        )

        tk.Label(
            heading,
            text=number,
            bg=PRIMARY,
            fg=WHITE,
            font=("Segoe UI", 8, "bold"),
            width=4,
            pady=5
        ).pack(side="left")

        title_box = tk.Frame(
            heading,
            bg=WHITE
        )

        title_box.pack(
            side="left",
            padx=12
        )

        tk.Label(
            title_box,
            text=title,
            bg=WHITE,
            fg=NAVY,
            font=("Segoe UI", 12, "bold")
        ).pack(anchor="w")

        tk.Label(
            title_box,
            text=subtitle,
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w")

        return box

    def draw_gender_chart(self, parent):

        if SEX_COL is None or TARGET_COL is None:
            return

        temp = df.copy()

        temp["_Disease"] = temp[
            TARGET_COL
        ].apply(positive_target)

        result = temp.groupby(
            SEX_COL
        )["_Disease"].sum()

        fig, canvas = self.create_figure(
            parent,
            6,
            3.1
        )

        ax = fig.add_subplot(111)

        ax.bar(
            result.index.astype(str),
            result.values
        )

        ax.set_ylabel(
            "Heart Disease Cases"
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()

        canvas.draw()

    def draw_age_chart(self, parent):

        if AGE_COL is None:
            return

        fig, canvas = self.create_figure(
            parent,
            6,
            3.1
        )

        ax = fig.add_subplot(111)

        sns.histplot(
            df[AGE_COL].dropna(),
            bins=15,
            kde=True,
            ax=ax
        )

        ax.set_xlabel("Age")
        ax.set_ylabel("Patients")

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()

        canvas.draw()

    def draw_chest_chart(self, parent):

        if CHEST_COL is None:
            return

        counts = df[
            CHEST_COL
        ].value_counts()

        fig, canvas = self.create_figure(
            parent,
            6,
            3.1
        )

        ax = fig.add_subplot(111)

        ax.bar(
            counts.index.astype(str),
            counts.values
        )

        ax.set_xlabel(
            "Chest Pain Type"
        )

        ax.set_ylabel(
            "Patients"
        )

        ax.tick_params(
            axis="x",
            rotation=20
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()

        canvas.draw()

    def draw_cholesterol_chart(self, parent):

        if CHOLESTEROL_COL is None:
            return

        fig, canvas = self.create_figure(
            parent,
            6,
            3.1
        )

        ax = fig.add_subplot(111)

        sns.boxplot(
            x=df[CHOLESTEROL_COL],
            ax=ax
        )

        ax.set_xlabel(
            "Cholesterol"
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()

        canvas.draw()

    def draw_maxhr_chart(self, parent):

        if MAXHR_COL is None:
            return

        fig, canvas = self.create_figure(
            parent,
            10,
            3.1
        )

        ax = fig.add_subplot(111)

        sns.histplot(
            df[MAXHR_COL].dropna(),
            bins=20,
            kde=True,
            ax=ax
        )

        ax.set_xlabel(
            "Maximum Heart Rate"
        )

        ax.set_ylabel(
            "Patients"
        )

        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)

        fig.tight_layout()

        canvas.draw()

    def dataset_page(self):

        controls = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        controls.pack(
            fill="x",
            pady=(0, 15)
        )

        search_box = tk.Frame(
            controls,
            bg=WHITE
        )

        search_box.pack(
            side="left",
            padx=18,
            pady=14
        )

        tk.Label(
            search_box,
            text="SEARCH PATIENT DATA",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        self.search_var = tk.StringVar()

        self.search_entry = tk.Entry(
            search_box,
            textvariable=self.search_var,
            width=32,
            bg="#F7FAFB",
            fg=TEXT,
            relief="flat",
            font=("Segoe UI", 10)
        )

        self.search_entry.pack(
            pady=(5, 0),
            ipady=8
        )

        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.apply_filters()
        )

        outcome_box = tk.Frame(
            controls,
            bg=WHITE
        )

        outcome_box.pack(
            side="left",
            padx=18,
            pady=14
        )

        tk.Label(
            outcome_box,
            text="HEART DISEASE",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        self.outcome_var = tk.StringVar(
            value="All Records"
        )

        self.outcome_combo = ttk.Combobox(
            outcome_box,
            textvariable=self.outcome_var,
            values=[
                "All Records",
                "Heart Disease",
                "No Disease"
            ],
            state="readonly",
            width=18
        )

        self.outcome_combo.pack(
            pady=(5, 0)
        )

        self.outcome_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        gender_box = tk.Frame(
            controls,
            bg=WHITE
        )

        gender_box.pack(
            side="left",
            padx=18,
            pady=14
        )

        tk.Label(
            gender_box,
            text="GENDER",
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")

        self.gender_var = tk.StringVar(
            value="All"
        )

        genders = ["All"]

        if SEX_COL:

            genders += [
                str(value)
                for value in df[
                    SEX_COL
                ].dropna().unique()
            ]

        self.gender_combo = ttk.Combobox(
            gender_box,
            textvariable=self.gender_var,
            values=genders,
            state="readonly",
            width=15
        )

        self.gender_combo.pack(
            pady=(5, 0)
        )

        self.gender_combo.bind(
            "<<ComboboxSelected>>",
            lambda event: self.apply_filters()
        )

        buttons = tk.Frame(
            controls,
            bg=WHITE
        )

        buttons.pack(
            side="right",
            padx=18
        )

        tk.Button(
            buttons,
            text="RESET",
            command=self.reset_filters,
            bg="#E8EFF2",
            fg=NAVY,
            activebackground="#D7E4E8",
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            padx=4
        )

        tk.Button(
            buttons,
            text="EXPORT CSV",
            command=self.export_csv,
            bg=PRIMARY,
            fg=WHITE,
            activebackground=PRIMARY_DARK,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=8,
            cursor="hand2"
        ).pack(
            side="left",
            padx=4
        )

        info = tk.Frame(
            self.content,
            bg=BG
        )

        info.pack(
            fill="x",
            pady=(0, 8)
        )

        self.result_label = tk.Label(
            info,
            text=f"Showing {len(df):,} patient records",
            bg=BG,
            fg=PRIMARY_DARK,
            font=("Segoe UI", 10, "bold")
        )

        self.result_label.pack(
            anchor="w"
        )

        table_frame = tk.Frame(
            self.content,
            bg=WHITE,
            highlightbackground=BORDER,
            highlightthickness=1
        )

        table_frame.pack(
            fill="both",
            expand=True
        )

        self.create_table(table_frame)

    def create_table(self, parent):

        for widget in parent.winfo_children():
            widget.destroy()

        container = tk.Frame(
            parent,
            bg=WHITE
        )

        container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        columns = list(
            self.filtered_df.columns
        )

        self.tree = ttk.Treeview(
            container,
            columns=columns,
            show="headings"
        )

        vertical = ttk.Scrollbar(
            container,
            orient="vertical",
            command=self.tree.yview
        )

        horizontal = ttk.Scrollbar(
            container,
            orient="horizontal",
            command=self.tree.xview
        )

        self.tree.configure(
            yscrollcommand=vertical.set,
            xscrollcommand=horizontal.set
        )

        self.tree.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        vertical.grid(
            row=0,
            column=1,
            sticky="ns"
        )

        horizontal.grid(
            row=1,
            column=0,
            sticky="ew"
        )

        container.rowconfigure(
            0,
            weight=1
        )

        container.columnconfigure(
            0,
            weight=1
        )

        for column in columns:

            self.tree.heading(
                column,
                text=str(column)
            )

            self.tree.column(
                column,
                width=135,
                minwidth=90,
                anchor="center"
            )

        for _, row in self.filtered_df.iterrows():

            values = []

            for value in row:

                if pd.isna(value):

                    values.append("")

                elif isinstance(value, float):

                    values.append(
                        f"{value:.2f}"
                    )

                else:

                    values.append(
                        str(value)
                    )

            self.tree.insert(
                "",
                "end",
                values=values
            )

    def apply_filters(self):

        result = df.copy()

        search = self.search_var.get().strip().lower()

        if search:

            mask = result.astype(
                str
            ).apply(
                lambda column:
                column.str.lower().str.contains(
                    search,
                    na=False
                )
            ).any(axis=1)

            result = result[mask]

        outcome = self.outcome_var.get()

        if TARGET_COL and outcome != "All Records":

            status = result[
                TARGET_COL
            ].apply(positive_target)

            if outcome == "Heart Disease":
                result = result[status]
            else:
                result = result[~status]

        gender = self.gender_var.get()

        if SEX_COL and gender != "All":

            result = result[
                result[SEX_COL].astype(str) == gender
            ]

        self.filtered_df = result

        self.result_label.config(
            text=f"Showing {len(result):,} patient records"
        )

        table = self.content.winfo_children()[-1]

        self.create_table(table)

    def reset_filters(self):

        self.search_var.set("")
        self.outcome_var.set("All Records")
        self.gender_var.set("All")

        self.filtered_df = df.copy()

        self.result_label.config(
            text=f"Showing {len(df):,} patient records"
        )

        table = self.content.winfo_children()[-1]

        self.create_table(table)

    def export_csv(self):

        if self.filtered_df.empty:

            messagebox.showwarning(
                "No Data",
                "There are no records to export."
            )

            return

        path = filedialog.asksaveasfilename(
            title="Export Patient Dataset",
            defaultextension=".csv",
            filetypes=[
                ("CSV Files", "*.csv")
            ],
            initialfile="healthiq_filtered_data.csv"
        )

        if not path:
            return

        try:

            self.filtered_df.to_csv(
                path,
                index=False
            )

            messagebox.showinfo(
                "Export Complete",
                "Filtered patient data was exported successfully."
            )

        except Exception as error:

            messagebox.showerror(
                "Export Error",
                str(error)
            )


if __name__ == "__main__":

    root = tk.Tk()

    app = HealthIQ(root)

    root.mainloop()
