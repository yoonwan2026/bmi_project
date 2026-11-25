
import customtkinter as ctk
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from modules.health_logic import HealthManager
from modules.health_db import HealthManager as DBManager, HealthRecord


# =====================================================
# 기본 설정
# =====================================================

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class HealthManagerGUI:

    def __init__(self, root):

        self.root = root
        self.root.title("HEALTHCARE | BMI Management System")
        self.root.geometry("1250x800")
        self.root.minsize(1050, 700)

        self.manager = HealthManager()
        self.db = DBManager()

        self.colors = {
            "bg": "#F4F6FA",
            "sidebar": "#17243A",
            "sidebar_hover": "#263954",
            "primary": "#3978F6",
            "primary_hover": "#2863D8",
            "white": "#FFFFFF",
            "text": "#1E293B",
            "subtext": "#8491A5",
            "border": "#E8EDF4",
            "green": "#16A783",
            "orange": "#F0A43A",
            "red": "#E45B69",
            "purple": "#8871D9"
        }

        self.current_page = "dashboard"
        self.search_text = ""

        self.setup_style()
        self.create_main_layout()
        self.show_records()

    # =================================================
    # 스타일 설정
    # =================================================

    def setup_style(self):

        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Health.Treeview",
            background="#FFFFFF",
            foreground="#334155",
            rowheight=43,
            fieldbackground="#FFFFFF",
            font=("맑은 고딕", 10),
            borderwidth=0
        )

        style.configure(
            "Health.Treeview.Heading",
            background="#F1F5F9",
            foreground="#475569",
            font=("맑은 고딕", 10, "bold"),
            relief="flat",
            padding=12
        )

        style.map(
            "Health.Treeview",
            background=[("selected", "#DBEAFE")],
            foreground=[("selected", "#1D4ED8")]
        )

    # =================================================
    # 메인 레이아웃
    # =================================================

    def create_main_layout(self):

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # 왼쪽 사이드바
        self.sidebar = ctk.CTkFrame(
            self.root,
            width=235,
            corner_radius=0,
            fg_color=self.colors["sidebar"]
        )

        self.sidebar.grid(
            row=0, column=0, sticky="nsew"
        )

        self.sidebar.grid_propagate(False)

        # 로고
        ctk.CTkLabel(
            self.sidebar,
            text="✚ HEALTHCARE",
            font=("Arial", 21, "bold"),
            text_color="#FFFFFF"
        ).pack(anchor="w", padx=24, pady=(35, 3))

        ctk.CTkLabel(
            self.sidebar,
            text="BMI MANAGEMENT SYSTEM",
            font=("Arial", 9),
            text_color="#8EA0BA"
        ).pack(anchor="w", padx=26, pady=(0, 40))

        self.add_sidebar_title("WORKSPACE")

        self.dashboard_btn = self.add_sidebar_button(
            "▦    대시보드",
            self.show_dashboard
        )

        self.records_btn = self.add_sidebar_button(
            "▤    건강정보 관리",
            self.show_records
        )

        self.add_sidebar_title("MANAGEMENT")

        self.add_sidebar_button(
            "＋    회원 정보 추가",
            self.add_record
        )

        self.add_sidebar_button(
            "◈    건강정보 통계",
            self.show_statistics
        )

        self.add_sidebar_title("DATA MANAGEMENT")

        self.add_sidebar_button(
            "↓    데이터 불러오기",
            self.load_data
        )

        self.add_sidebar_button(
            "↑    데이터 저장하기",
            self.save_data
        )

        # 사이드바 하단
        ctk.CTkFrame(
            self.sidebar,
            height=1,
            fg_color="#34445C"
        ).pack(fill="x", padx=20, pady=(30, 15))

        ctk.CTkLabel(
            self.sidebar,
            text="BMI HEALTH SYSTEM\nVersion 2.0",
            font=("Arial", 10),
            text_color="#8192AA",
            justify="left"
        ).pack(anchor="w", padx=25, side="bottom", pady=25)

        # 오른쪽 콘텐츠 영역
        self.content = ctk.CTkFrame(
            self.root,
            corner_radius=0,
            fg_color=self.colors["bg"]
        )

        self.content.grid(
            row=0, column=1, sticky="nsew"
        )

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        # 상단 헤더
        self.header = ctk.CTkFrame(
            self.content,
            height=75,
            corner_radius=0,
            fg_color="#FFFFFF"
        )

        self.header.grid(
            row=0, column=0, sticky="ew"
        )

        self.header.grid_columnconfigure(0, weight=1)

        self.page_title = ctk.CTkLabel(
            self.header,
            text="Overview",
            font=("Arial", 20, "bold"),
            text_color=self.colors["text"]
        )

        self.page_title.grid(
            row=0, column=0, sticky="w", padx=30, pady=20
        )

        self.header_right = ctk.CTkLabel(
            self.header,
            text="● SYSTEM ONLINE",
            font=("Arial", 10, "bold"),
            text_color=self.colors["green"]
        )

        self.header_right.grid(
            row=0, column=1, padx=30
        )

        # 페이지 영역
        self.page = ctk.CTkFrame(
            self.content,
            corner_radius=0,
            fg_color=self.colors["bg"]
        )

        self.page.grid(
            row=1, column=0, sticky="nsew"
        )

        self.show_dashboard()

    # =================================================
    # 사이드바
    # =================================================

    def add_sidebar_title(self, title):

        ctk.CTkLabel(
            self.sidebar,
            text=title,
            font=("Arial", 9, "bold"),
            text_color="#71839E"
        ).pack(anchor="w", padx=25, pady=(12, 10))

    def add_sidebar_button(self, text, command):

        button = ctk.CTkButton(
            self.sidebar,
            text=text,
            height=43,
            corner_radius=8,
            anchor="w",
            fg_color="transparent",
            hover_color=self.colors["sidebar_hover"],
            text_color="#D6DFEC",
            font=("맑은 고딕", 12),
            command=command
        )

        button.pack(fill="x", padx=12, pady=3)

        return button

    # =================================================
    # 페이지 초기화
    # =================================================

    def clear_page(self):

        for widget in self.page.winfo_children():
            widget.destroy()

    def show_page_title(self, title):

        self.page_title.configure(text=title)

    # =================================================
    # 대시보드
    # =================================================

    def show_dashboard(self):

        self.current_page = "dashboard"
        self.show_page_title("Overview")
        self.clear_page()

        records = self.manager.get_all_records()

        # 환영 문구
        ctk.CTkLabel(
            self.page,
            text="건강관리 대시보드",
            font=("맑은 고딕", 25, "bold"),
            text_color=self.colors["text"]
        ).pack(anchor="w", padx=30, pady=(25, 3))

        ctk.CTkLabel(
            self.page,
            text="회원들의 건강정보와 BMI 현황을 확인할 수 있습니다.",
            font=("맑은 고딕", 12),
            text_color=self.colors["subtext"]
        ).pack(anchor="w", padx=30, pady=(0, 20))

        total = len(records)

        if total > 0:

            avg_bmi = sum(
                float(r.bmi) for r in records
            ) / total

            normal = sum(
                1 for r in records
                if "정상" in str(r.status)
            )

            abnormal = total - normal

        else:
            avg_bmi = 0
            normal = 0
            abnormal = 0

        # 통계 카드
        cards = ctk.CTkFrame(
            self.page,
            fg_color="transparent"
        )

        cards.pack(fill="x", padx=22)

        cards.grid_columnconfigure(
            (0, 1, 2), weight=1
        )

        self.create_stat_card(
            cards, 0, "TOTAL MEMBERS",
            f"{total}명", "전체 등록 회원",
            self.colors["primary"]
        )

        self.create_stat_card(
            cards, 1, "AVERAGE BMI",
            f"{avg_bmi:.1f}", "전체 평균 BMI",
            self.colors["green"]
        )

        self.create_stat_card(
            cards, 2, "NORMAL WEIGHT",
            f"{normal}명", "정상 체중 회원",
            self.colors["orange"]
        )

        # 그래프와 최근 데이터
        bottom = ctk.CTkFrame(
            self.page,
            fg_color="transparent"
        )

        bottom.pack(
            fill="both",
            expand=True,
            padx=22,
            pady=20
        )

        bottom.grid_columnconfigure(
            0, weight=1
        )

        bottom.grid_columnconfigure(
            1, weight=1
        )

        bottom.grid_rowconfigure(
            0, weight=1
        )

        # BMI 분포 카드
        chart_card = ctk.CTkFrame(
            bottom,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color=self.colors["border"]
        )

        chart_card.grid(
            row=0, column=0,
            sticky="nsew",
            padx=7
        )

        ctk.CTkLabel(
            chart_card,
            text="BMI HEALTH DISTRIBUTION",
            font=("Arial", 12, "bold"),
            text_color=self.colors["text"]
        ).pack(anchor="w", padx=20, pady=(20, 5))

        ctk.CTkLabel(
            chart_card,
            text="회원 건강상태 분포",
            font=("맑은 고딕", 10),
            text_color=self.colors["subtext"]
        ).pack(anchor="w", padx=20)

        chart_area = tk.Frame(
            chart_card,
            bg="white"
        )

        chart_area.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.draw_chart(
            chart_area, normal, abnormal
        )

        # 최근 회원 카드
        recent_card = ctk.CTkFrame(
            bottom,
            fg_color="#FFFFFF",
            corner_radius=15,
            border_width=1,
            border_color=self.colors["border"]
        )

        recent_card.grid(
            row=0, column=1,
            sticky="nsew",
            padx=7
        )

        ctk.CTkLabel(
            recent_card,
            text="MEMBER OVERVIEW",
            font=("Arial", 12, "bold"),
            text_color=self.colors["text"]
        ).pack(anchor="w", padx=20, pady=(20, 5))

        ctk.CTkLabel(
            recent_card,
            text="등록된 건강정보",
            font=("맑은 고딕", 10),
            text_color=self.colors["subtext"]
        ).pack(anchor="w", padx=20)

        if not records:

            ctk.CTkLabel(
                recent_card,
                text="등록된 회원이 없습니다.",
                text_color=self.colors["subtext"]
            ).pack(expand=True)

        else:

            for record in records[-6:][::-1]:

                row = ctk.CTkFrame(
                    recent_card,
                    fg_color="#F7F9FC",
                    corner_radius=9
                )

                row.pack(
                    fill="x",
                    padx=15,
                    pady=5
                )

                ctk.CTkLabel(
                    row,
                    text=record.name,
                    font=("맑은 고딕", 12, "bold"),
                    text_color=self.colors["text"]
                ).pack(
                    side="left",
                    padx=12,
                    pady=12
                )

                ctk.CTkLabel(
                    row,
                    text=f"BMI {record.bmi}",
                    font=("Arial", 11, "bold"),
                    text_color=self.colors["primary"]
                ).pack(
                    side="right",
                    padx=12
                )

    # =================================================
    # 통계 카드
    # =================================================

    def create_stat_card(
        self, parent, column,
        title, value, description, color
    ):

        card = ctk.CTkFrame(
            parent,
            fg_color="#FFFFFF",
            corner_radius=14,
            border_width=1,
            border_color=self.colors["border"]
        )

        card.grid(
            row=0, column=column,
            sticky="ew",
            padx=7,
            pady=5
        )

        ctk.CTkFrame(
            card,
            width=5,
            fg_color=color,
            corner_radius=5
        ).pack(
            side="left",
            fill="y",
            padx=(0, 15),
            pady=15
        )

        inner = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        inner.pack(
            side="left",
            fill="both",
            expand=True,
            pady=15
        )

        ctk.CTkLabel(
            inner,
            text=title,
            font=("Arial", 10, "bold"),
            text_color=self.colors["subtext"]
        ).pack(anchor="w")

        ctk.CTkLabel(
            inner,
            text=value,
            font=("Arial", 27, "bold"),
            text_color=color
        ).pack(anchor="w", pady=2)

        ctk.CTkLabel(
            inner,
            text=description,
            font=("맑은 고딕", 10),
            text_color=self.colors["subtext"]
        ).pack(anchor="w")

    # =================================================
    # 도넛 그래프
    # =================================================

    def draw_chart(self, parent, normal, abnormal):

        figure = Figure(
            figsize=(4, 3),
            dpi=100,
            facecolor="white"
        )

        ax = figure.add_subplot(111)

        if normal + abnormal == 0:

            ax.text(
                0.5, 0.5,
                "No Data",
                ha="center",
                va="center",
                fontsize=15,
                color="#94A3B8"
            )

            ax.axis("off")

        else:

            ax.pie(
                [normal, abnormal],
                colors=["#3978F6", "#E7EDF5"],
                startangle=90,
                counterclock=False,
                wedgeprops={
                    "width": 0.30,
                    "edgecolor": "white"
                }
            )

            ax.text(
                0, 0,
                f"{normal + abnormal}",
                ha="center",
                va="center",
                fontsize=23,
                fontweight="bold",
                color="#1E293B"
            )

            ax.text(
                0, -0.18,
                "MEMBERS",
                ha="center",
                fontsize=8,
                color="#8491A5"
            )

            ax.legend(
                ["정상 체중", "기타"],
                loc="lower center",
                bbox_to_anchor=(0.5, -0.12),
                ncol=2,
                frameon=False,
                fontsize=9
            )

        figure.tight_layout()

        canvas = FigureCanvasTkAgg(
            figure,
            master=parent
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )

    # =================================================
    # 건강정보 관리 페이지
    # =================================================

    def show_records(self):

        self.current_page = "records"
        self.show_page_title("Member Management")
        self.clear_page()

        ctk.CTkLabel(
            self.page,
            text="건강정보 관리",
            font=("맑은 고딕", 24, "bold"),
            text_color=self.colors["text"]
        ).pack(anchor="w", padx=30, pady=(25, 3))

        ctk.CTkLabel(
            self.page,
            text="회원의 건강정보를 검색하고 관리할 수 있습니다.",
            font=("맑은 고딕", 11),
            text_color=self.colors["subtext"]
        ).pack(anchor="w", padx=30, pady=(0, 20))

        # 검색 및 버튼 영역
        toolbar = ctk.CTkFrame(
            self.page,
            fg_color="transparent"
        )

        toolbar.pack(fill="x", padx=25, pady=5)

        self.search_entry = ctk.CTkEntry(
            toolbar,
            width=270,
            height=40,
            placeholder_text="회원 이름 검색...",
            corner_radius=8,
            border_color=self.colors["border"]
        )

        self.search_entry.pack(
            side="left", padx=5
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_records
        )

        ctk.CTkButton(
            toolbar,
            text="+ 회원 추가",
            width=120,
            height=40,
            corner_radius=8,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            command=self.add_record
        ).pack(side="right", padx=5)

        ctk.CTkButton(
            toolbar,
            text="↻ 새로고침",
            width=110,
            height=40,
            corner_radius=8,
            fg_color="#E8EEF8",
            hover_color="#DCE5F3",
            text_color="#344563",
            command=self.show_records
        ).pack(side="right", padx=5)

        # 테이블 카드
        table_card = ctk.CTkFrame(
            self.page,
            fg_color="#FFFFFF",
            corner_radius=13,
            border_width=1,
            border_color=self.colors["border"]
        )

        table_card.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=15
        )

        columns = (
            "id", "name", "birth_year",
            "gender", "height", "weight",
            "bmi", "status"
        )

        self.tree = ttk.Treeview(
            table_card,
            columns=columns,
            show="headings",
            style="Health.Treeview",
            selectmode="browse"
        )

        headings = {
            "id": "ID",
            "name": "이름",
            "birth_year": "출생연도",
            "gender": "성별",
            "height": "키(cm)",
            "weight": "몸무게(kg)",
            "bmi": "BMI",
            "status": "건강상태"
        }

        widths = {
            "id": 55,
            "name": 100,
            "birth_year": 95,
            "gender": 65,
            "height": 90,
            "weight": 100,
            "bmi": 85,
            "status": 110
        }

        for col in columns:

            self.tree.heading(
                col,
                text=headings[col]
            )

            self.tree.column(
                col,
                width=widths[col],
                anchor="center",
                minwidth=50
            )

        self.tree.tag_configure(
            "normal",
            foreground="#16876C"
        )

        self.tree.tag_configure(
            "other",
            foreground="#D18A28"
        )

        scrollbar = ttk.Scrollbar(
            table_card,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(
            yscrollcommand=scrollbar.set
        )

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        scrollbar.pack(
            side="right",
            fill="y",
            pady=10,
            padx=(0, 5)
        )

        self.tree.bind(
            "<Double-1>",
            lambda event: self.show_detail()
        )

        # 하단 버튼
        bottom = ctk.CTkFrame(
            self.page,
            fg_color="transparent"
        )

        bottom.pack(
            fill="x",
            padx=30,
            pady=(0, 20)
        )

        ctk.CTkButton(
            bottom,
            text="상세 조회",
            width=110,
            command=self.show_detail,
            fg_color="#E8EEF8",
            hover_color="#DCE5F3",
            text_color="#344563"
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            bottom,
            text="정보 수정",
            width=110,
            command=self.update_record,
            fg_color="#E8EEF8",
            hover_color="#DCE5F3",
            text_color="#344563"
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            bottom,
            text="정보 삭제",
            width=110,
            command=self.delete_record,
            fg_color="#FDEBED",
            hover_color="#FBDADD",
            text_color=self.colors["red"]
        ).pack(side="left", padx=4)

        self.populate_table()

    # =================================================
    # 테이블 데이터 출력
    # =================================================

    def populate_table(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.manager.get_all_records()

        keyword = self.search_entry.get().strip().lower()

        for record in records:

            if keyword and keyword not in record.name.lower():
                continue

            tag = (
                "normal"
                if "정상" in str(record.status)
                else "other"
            )

            self.tree.insert(
                "",
                "end",
                values=(
                    record.id,
                    record.name,
                    record.birth_year,
                    record.gender,
                    record.height,
                    record.weight,
                    record.bmi,
                    record.status
                ),
                tags=(tag,)
            )

    def search_records(self, event=None):

        self.populate_table()

    # =================================================
    # 선택한 회원 정보
    # =================================================

    def get_selected_record(self):

        selected = self.tree.selection()

        if not selected:

            messagebox.showwarning(
                "알림",
                "회원을 먼저 선택해주세요."
            )

            return None

        record_id = self.tree.item(
            selected[0], "values"
        )[0]

        for record in self.manager.get_all_records():

            if str(record.id) == str(record_id):
                return record

        return None

    # =================================================
    # 공통 입력창
    # =================================================

    def create_form(self, title, fields, initial=None):

        window = ctk.CTkToplevel(self.root)

        window.title(title)
        window.geometry("420x550")
        window.resizable(False, False)

        window.configure(
            fg_color="#F4F6FA"
        )

        window.transient(self.root)
        window.grab_set()

        ctk.CTkLabel(
            window,
            text=title,
            font=("맑은 고딕", 22, "bold"),
            text_color=self.colors["text"]
        ).pack(anchor="w", padx=30, pady=(25, 5))

        ctk.CTkLabel(
            window,
            text="건강정보를 정확하게 입력해주세요.",
            font=("맑은 고딕", 10),
            text_color=self.colors["subtext"]
        ).pack(anchor="w", padx=30, pady=(0, 20))

        entries = {}

        for field in fields:

            ctk.CTkLabel(
                window,
                text=field,
                font=("맑은 고딕", 11, "bold"),
                text_color=self.colors["text"]
            ).pack(anchor="w", padx=30, pady=(8, 4))

            entry = ctk.CTkEntry(
                window,
                width=355,
                height=40,
                corner_radius=8,
                border_color=self.colors["border"],
                placeholder_text=f"{field} 입력"
            )

            entry.pack(padx=30)

            if initial and field in initial:
                entry.insert(0, str(initial[field]))

            entries[field] = entry

        return window, entries

    # =================================================
    # 회원 추가
    # =================================================

    def add_record(self):

        fields = [
            "이름",
            "출생연도",
            "성별",
            "키(cm)",
            "몸무게(kg)"
        ]

        window, entries = self.create_form(
            "회원 정보 추가",
            fields
        )

        def submit():

            try:

                name = entries["이름"].get().strip()

                birth_year = int(
                    entries["출생연도"].get()
                )

                gender = entries["성별"].get().strip()

                height = float(
                    entries["키(cm)"].get()
                )

                weight = float(
                    entries["몸무게(kg)"].get()
                )

                if not name or not gender:
                    raise ValueError("이름과 성별을 입력해주세요.")

                if birth_year < 1900 or birth_year > 2026:
                    raise ValueError("출생연도를 확인해주세요.")

                if not 50 <= height <= 250:
                    raise ValueError("키는 50~250cm 사이로 입력해주세요.")

                if not 10 <= weight <= 300:
                    raise ValueError("몸무게는 10~300kg 사이로 입력해주세요.")

                self.manager.add_record(
                    name,
                    birth_year,
                    gender,
                    height,
                    weight
                )

                window.destroy()

                self.refresh_current_page()

                messagebox.showinfo(
                    "등록 완료",
                    "회원 정보가 성공적으로 추가되었습니다."
                )

            except ValueError as e:

                messagebox.showwarning(
                    "입력 오류", str(e)
                )

            except Exception as e:

                messagebox.showerror(
                    "오류", str(e)
                )

        ctk.CTkButton(
            window,
            text="회원 정보 등록",
            width=355,
            height=43,
            corner_radius=9,
            fg_color=self.colors["primary"],
            hover_color=self.colors["primary_hover"],
            command=submit
        ).pack(pady=25)

    # =================================================
    # 상세 조회
    # =================================================

    def show_detail(self):

        record = self.get_selected_record()

        if record is None:
            return

        window = ctk.CTkToplevel(self.root)

        window.title("회원 상세 정보")
        window.geometry("430x570")
        window.resizable(False, False)

        window.configure(
            fg_color="#F4F6FA"
        )

        window.transient(self.root)
        window.grab_set()

        ctk.CTkLabel(
            window,
            text="MEMBER PROFILE",
            font=("Arial", 10, "bold"),
            text_color=self.colors["primary"]
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            window,
            text=record.name,
            font=("맑은 고딕", 25, "bold"),
            text_color=self.colors["text"]
        ).pack(pady=5)

        ctk.CTkLabel(
            window,
            text=f"회원 번호  #{record.id}",
            font=("Arial", 11),
            text_color=self.colors["subtext"]
        ).pack(pady=(0, 20))

        info = [
            ("출생연도", record.birth_year),
            ("성별", record.gender),
            ("키", f"{record.height} cm"),
            ("몸무게", f"{record.weight} kg"),
            ("BMI", record.bmi),
            ("건강상태", record.status)
        ]

        for label, value in info:

            row = ctk.CTkFrame(
                window,
                fg_color="#FFFFFF",
                corner_radius=8
            )

            row.pack(
                fill="x",
                padx=30,
                pady=4
            )

            ctk.CTkLabel(
                row,
                text=label,
                text_color=self.colors["subtext"],
                font=("맑은 고딕", 11)
            ).pack(side="left", padx=15, pady=12)

            ctk.CTkLabel(
                row,
                text=str(value),
                text_color=self.colors["text"],
                font=("맑은 고딕", 11, "bold")
            ).pack(side="right", padx=15)

        ctk.CTkButton(
            window,
            text="닫기",
            width=350,
            height=40,
            command=window.destroy
        ).pack(pady=25)

    # =================================================
    # 회원 수정
    # =================================================

    def update_record(self):

        record = self.get_selected_record()

        if record is None:
            return

        fields = ["키(cm)", "몸무게(kg)"]

        initial = {
            "키(cm)": record.height,
            "몸무게(kg)": record.weight
        }

        window, entries = self.create_form(
            "건강정보 수정",
            fields,
            initial
        )

        def submit():

            try:

                height = float(
                    entries["키(cm)"].get()
                )

                weight = float(
                    entries["몸무게(kg)"].get()
                )

                if not 50 <= height <= 250:
                    raise ValueError("키는 50~250cm 사이로 입력해주세요.")

                if not 10 <= weight <= 300:
                    raise ValueError("몸무게는 10~300kg 사이로 입력해주세요.")

                self.manager.update_record(
                    record.id,
                    height,
                    weight
                )

                window.destroy()

                self.refresh_current_page()

                messagebox.showinfo(
                    "수정 완료",
                    "건강정보가 수정되었습니다."
                )

            except ValueError as e:

                messagebox.showwarning(
                    "입력 오류", str(e)
                )

            except Exception as e:

                messagebox.showerror(
                    "오류", str(e)
                )

        ctk.CTkButton(
            window,
            text="수정 내용 저장",
            width=355,
            height=43,
            command=submit
        ).pack(pady=25)

    # =================================================
    # 회원 삭제
    # =================================================

    def delete_record(self):

        record = self.get_selected_record()

        if record is None:
            return

        answer = messagebox.askyesno(
            "회원 삭제",
            f"{record.name}님의 건강정보를 삭제하시겠습니까?"
        )

        if answer:

            try:

                self.manager.delete_record(record.id)

                self.refresh_current_page()

                messagebox.showinfo(
                    "삭제 완료",
                    "회원 정보가 삭제되었습니다."
                )

            except Exception as e:

                messagebox.showerror(
                    "오류", str(e)
                )

    # =================================================
    # 통계
    # =================================================

    def show_statistics(self):

        try:

            stats = self.manager.get_statistics()

            result = "HEALTH STATISTICS\n\n"

            for key, value in stats.items():
                result += f"{key}: {value}\n"

            messagebox.showinfo(
                "건강정보 통계", result
            )

        except Exception as e:

            messagebox.showerror(
                "오류", str(e)
            )

    # =================================================
    # 파일 불러오기
    # =================================================

    def load_data(self):

        file_type = simpledialog.askstring(
            "파일 불러오기",
            "파일 형식을 입력하세요.\n(json / csv / txt / pkl)",
            parent=self.root
        )

        if not file_type:
            return

        file_type = file_type.lower().strip()

        if file_type not in ["json", "csv", "txt", "pkl"]:

            messagebox.showwarning(
                "파일 형식 오류",
                "지원하지 않는 파일 형식입니다."
            )

            return

        try:

            self.db.load_data(file_type)

            new_records = []

            for record in self.db.records:

                if isinstance(record, dict):

                    new_records.append(
                        HealthRecord(
                            record["id"],
                            record["name"],
                            int(record["birth_year"]),
                            record["gender"],
                            float(record["height"]),
                            float(record["weight"]),
                            float(record["bmi"]),
                            record["status"]
                        )
                    )

                elif isinstance(record, HealthRecord):

                    new_records.append(record)

            self.manager.records = new_records

            self.refresh_current_page()

            messagebox.showinfo(
                "불러오기 완료",
                "건강정보를 성공적으로 불러왔습니다."
            )

        except Exception as e:

            messagebox.showerror(
                "불러오기 오류", str(e)
            )

    # =================================================
    # 파일 저장
    # =================================================

    def save_data(self):

        file_type = simpledialog.askstring(
            "파일 저장",
            "저장할 파일 형식을 입력하세요.\n(json / csv / txt / pkl)",
            parent=self.root
        )

        if not file_type:
            return

        file_type = file_type.lower().strip()

        if file_type not in ["json", "csv", "txt", "pkl"]:

            messagebox.showwarning(
                "파일 형식 오류",
                "지원하지 않는 파일 형식입니다."
            )

            return

        try:

            self.db.records = [
                record.to_dict()
                if isinstance(record, HealthRecord)
                else record
                for record in self.manager.records
            ]

            self.db.save_data(file_type)

            messagebox.showinfo(
                "저장 완료",
                "건강정보를 성공적으로 저장했습니다."
            )

        except Exception as e:

            messagebox.showerror(
                "저장 오류", str(e)
            )

    # =================================================
    # 현재 화면 갱신
    # =================================================

    def refresh_current_page(self):

        if self.current_page == "records":
            self.show_records()

        else:
            self.show_dashboard()


# =====================================================
# 프로그램 실행
# =====================================================

if __name__ == "__main__":

    root = ctk.CTk()

    app = HealthManagerGUI(root)

    root.mainloop()
