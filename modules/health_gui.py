
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog

from modules.health_logic import HealthManager
from modules.health_db import HealthManager as DBManager, HealthRecord


class HealthManagerGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("BMI 건강관리 시스템")
        self.root.geometry("1100x750")
        self.root.minsize(950, 650)
        self.root.configure(bg="#F3F6FB")

        # 기존 모듈 연결
        self.manager = HealthManager()
        self.db = DBManager()

        # 색상 설정
        self.colors = {
            "background": "#F3F6FB",
            "sidebar": "#172B4D",
            "primary": "#3478F6",
            "white": "#FFFFFF",
            "text": "#26354A",
            "subtext": "#8492A6",
            "green": "#20B486",
            "orange": "#F5A623",
            "red": "#E85D75",
            "border": "#E6EBF2"
        }

        self.setup_style()
        self.create_layout()
        self.show_records()

    # 테이블 디자인
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background="white",
            foreground="#26354A",
            rowheight=38,
            fieldbackground="white",
            font=("맑은 고딕", 10),
            borderwidth=0
        )

        style.configure(
            "Treeview.Heading",
            background="#EAF0F8",
            foreground="#344563",
            font=("맑은 고딕", 10, "bold"),
            relief="flat",
            padding=10
        )

        style.map(
            "Treeview",
            background=[("selected", "#DCE9FF")],
            foreground=[("selected", "#172B4D")]
        )

    # 전체 화면 구성
    def create_layout(self):

        # 왼쪽 사이드바
        sidebar = tk.Frame(
            self.root,
            bg=self.colors["sidebar"],
            width=210
        )
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="♥ HEALTH CARE",
            font=("맑은 고딕", 17, "bold"),
            fg="white",
            bg=self.colors["sidebar"]
        ).pack(pady=(35, 5))

        tk.Label(
            sidebar,
            text="BMI MANAGEMENT",
            font=("맑은 고딕", 9),
            fg="#AAB9D0",
            bg=self.colors["sidebar"]
        ).pack(pady=(0, 40))

        tk.Label(
            sidebar,
            text="MENU",
            font=("맑은 고딕", 9, "bold"),
            fg="#8295B5",
            bg=self.colors["sidebar"]
        ).pack(anchor="w", padx=22, pady=8)

        self.sidebar_button(sidebar, "건강정보 추가", self.add_record)
        self.sidebar_button(sidebar, "건강정보 조회", self.show_records)
        self.sidebar_button(sidebar, "상세 정보 조회", self.show_detail)
        self.sidebar_button(sidebar, "건강정보 수정", self.update_record)
        self.sidebar_button(sidebar, "건강정보 삭제", self.delete_record)

        tk.Label(
            sidebar,
            text="FILE MANAGEMENT",
            font=("맑은 고딕", 9, "bold"),
            fg="#8295B5",
            bg=self.colors["sidebar"]
        ).pack(anchor="w", padx=22, pady=(35, 8))

        self.sidebar_button(sidebar, "파일 불러오기", self.load_data)
        self.sidebar_button(sidebar, "파일 저장하기", self.save_data)
        self.sidebar_button(sidebar, "건강정보 통계", self.show_statistics)

        tk.Label(
            sidebar,
            text="BMI HEALTH SYSTEM\nVersion 1.0",
            font=("맑은 고딕", 8),
            fg="#8295B5",
            bg=self.colors["sidebar"],
            justify="left"
        ).pack(side="bottom", anchor="w", padx=22, pady=25)

        # 오른쪽 메인 영역
        self.main = tk.Frame(
            self.root,
            bg=self.colors["background"]
        )
        self.main.pack(side="right", fill="both", expand=True)

        # 상단 제목
        header = tk.Frame(
            self.main,
            bg=self.colors["background"]
        )
        header.pack(fill="x", padx=30, pady=(25, 15))

        tk.Label(
            header,
            text="건강관리 대시보드",
            font=("맑은 고딕", 23, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"]
        ).pack(anchor="w")

        tk.Label(
            header,
            text="회원들의 건강정보와 BMI 지수를 한눈에 관리하세요.",
            font=("맑은 고딕", 10),
            fg=self.colors["subtext"],
            bg=self.colors["background"]
        ).pack(anchor="w", pady=5)

        # 통계 카드 영역
        self.card_frame = tk.Frame(
            self.main,
            bg=self.colors["background"]
        )
        self.card_frame.pack(fill="x", padx=25, pady=10)

        self.total_label = self.create_card(
            "전체 회원 수", "0명", "#3478F6", 0
        )

        self.bmi_label = self.create_card(
            "평균 BMI", "0.0", "#20B486", 1
        )

        self.normal_label = self.create_card(
            "정상 체중", "0명", "#F5A623", 2
        )

        # 목록 제목
        list_header = tk.Frame(
            self.main,
            bg=self.colors["background"]
        )
        list_header.pack(fill="x", padx=30, pady=(25, 10))

        tk.Label(
            list_header,
            text="건강정보 목록",
            font=("맑은 고딕", 16, "bold"),
            fg=self.colors["text"],
            bg=self.colors["background"]
        ).pack(side="left")

        self.count_label = tk.Label(
            list_header,
            text="총 0건",
            font=("맑은 고딕", 10),
            fg=self.colors["subtext"],
            bg=self.colors["background"]
        )
        self.count_label.pack(side="right")

        # 테이블 영역
        table_frame = tk.Frame(
            self.main,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )
        table_frame.pack(
            fill="both",
            expand=True,
            padx=30,
            pady=(0, 25)
        )

        columns = (
            "id", "name", "birth_year",
            "gender", "height", "weight", "bmi", "status"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headings = {
            "id": "번호",
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
            "name": 90,
            "birth_year": 90,
            "gender": 65,
            "height": 85,
            "weight": 100,
            "bmi": 85,
            "status": 110
        }

        for col in columns:
            self.tree.heading(col, text=headings[col])
            self.tree.column(
                col,
                width=widths[col],
                anchor="center"
            )

        scrollbar = ttk.Scrollbar(
            table_frame,
            orient="vertical",
            command=self.tree.yview
        )

        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(
            side="left",
            fill="both",
            expand=True,
            padx=8,
            pady=8
        )

        scrollbar.pack(side="right", fill="y", pady=8)

        # 더블클릭 상세 조회
        self.tree.bind(
            "<Double-1>",
            lambda event: self.show_detail()
        )

    # 사이드바 버튼
    def sidebar_button(self, parent, text, command):

        button = tk.Button(
            parent,
            text="   " + text,
            command=command,
            font=("맑은 고딕", 10),
            fg="#DCE6F5",
            bg=self.colors["sidebar"],
            activebackground="#2D4770",
            activeforeground="white",
            relief="flat",
            anchor="w",
            cursor="hand2",
            padx=15,
            pady=11
        )

        button.pack(fill="x", padx=10, pady=2)

    # 통계 카드 생성
    def create_card(self, title, value, color, column):

        card = tk.Frame(
            self.card_frame,
            bg="white",
            highlightbackground=self.colors["border"],
            highlightthickness=1
        )

        card.grid(
            row=0,
            column=column,
            sticky="nsew",
            padx=7,
            pady=5
        )

        self.card_frame.grid_columnconfigure(
            column,
            weight=1
        )

        tk.Frame(
            card,
            bg=color,
            height=4
        ).pack(fill="x")

        tk.Label(
            card,
            text=title,
            font=("맑은 고딕", 10),
            fg=self.colors["subtext"],
            bg="white"
        ).pack(anchor="w", padx=17, pady=(15, 5))

        value_label = tk.Label(
            card,
            text=value,
            font=("맑은 고딕", 21, "bold"),
            fg=color,
            bg="white"
        )

        value_label.pack(anchor="w", padx=17, pady=(0, 15))

        return value_label

    # 통계 카드 업데이트
    def update_dashboard(self):

        records = self.manager.get_all_records()

        total = len(records)

        if total > 0:
            average_bmi = sum(
                float(r.bmi) for r in records
            ) / total

            normal = sum(
                1 for r in records
                if "정상" in str(r.status)
            )
        else:
            average_bmi = 0
            normal = 0

        self.total_label.config(text=f"{total}명")
        self.bmi_label.config(text=f"{average_bmi:.1f}")
        self.normal_label.config(text=f"{normal}명")

        self.count_label.config(text=f"총 {total}건")

    # 건강정보 목록 조회
    def show_records(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        records = self.manager.get_all_records()

        for record in records:

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
                )
            )

        self.update_dashboard()

    # 선택한 데이터 가져오기
    def get_selected_record(self):

        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "알림",
                "건강정보를 선택하세요."
            )
            return None

        record_id = self.tree.item(
            selected[0], "values"
        )[0]

        for record in self.manager.get_all_records():
            if str(record.id) == str(record_id):
                return record

        return None

    # 건강정보 추가
    def add_record(self):

        name = simpledialog.askstring(
            "건강정보 추가", "이름을 입력하세요."
        )
        if not name:
            return

        birth_year = simpledialog.askinteger(
            "건강정보 추가", "출생연도를 입력하세요."
        )
        if birth_year is None:
            return

        gender = simpledialog.askstring(
            "건강정보 추가", "성별을 입력하세요."
        )
        if not gender:
            return

        height = simpledialog.askfloat(
            "건강정보 추가", "키(cm)를 입력하세요."
        )
        if height is None:
            return

        weight = simpledialog.askfloat(
            "건강정보 추가", "몸무게(kg)를 입력하세요."
        )
        if weight is None:
            return

        try:
            self.manager.add_record(
                name, birth_year, gender, height, weight
            )

            self.show_records()

            messagebox.showinfo(
                "완료", "건강정보가 추가되었습니다."
            )

        except Exception as e:
            messagebox.showerror("오류", str(e))

    # 상세 조회
    def show_detail(self):

        record = self.get_selected_record()

        if record is None:
            return

        detail = (
            f"번호: {record.id}\n"
            f"이름: {record.name}\n"
            f"출생연도: {record.birth_year}\n"
            f"성별: {record.gender}\n"
            f"키: {record.height}cm\n"
            f"몸무게: {record.weight}kg\n"
            f"BMI: {record.bmi}\n"
            f"건강상태: {record.status}"
        )

        messagebox.showinfo(
            "건강정보 상세 조회", detail
        )

    # 정보 수정
    def update_record(self):

        record = self.get_selected_record()

        if record is None:
            return

        height = simpledialog.askfloat(
            "정보 수정",
            "새로운 키(cm)를 입력하세요.",
            initialvalue=float(record.height)
        )

        if height is None:
            return

        weight = simpledialog.askfloat(
            "정보 수정",
            "새로운 몸무게(kg)를 입력하세요.",
            initialvalue=float(record.weight)
        )

        if weight is None:
            return

        try:
            self.manager.update_record(
                record.id, height, weight
            )

            self.show_records()

            messagebox.showinfo(
                "완료", "건강정보가 수정되었습니다."
            )

        except Exception as e:
            messagebox.showerror("오류", str(e))

    # 정보 삭제
    def delete_record(self):

        record = self.get_selected_record()

        if record is None:
            return

        answer = messagebox.askyesno(
            "삭제 확인",
            f"{record.name}님의 건강정보를 삭제하시겠습니까?"
        )

        if answer:
            try:
                self.manager.delete_record(record.id)
                self.show_records()

                messagebox.showinfo(
                    "완료", "건강정보가 삭제되었습니다."
                )

            except Exception as e:
                messagebox.showerror("오류", str(e))

    # 건강정보 통계
    def show_statistics(self):

        try:
            stats = self.manager.get_statistics()

            result = "건강정보 통계\n\n"

            for key, value in stats.items():
                result += f"{key}: {value}\n"

            messagebox.showinfo(
                "건강정보 통계", result
            )

        except Exception as e:
            messagebox.showerror("오류", str(e))

    # 파일 불러오기
    def load_data(self):

        file_type = simpledialog.askstring(
            "파일 불러오기",
            "파일 형식을 입력하세요. (json/csv/txt/pkl)"
        )

        if not file_type:
            return

        file_type = file_type.lower().strip()

        if file_type not in ["json", "csv", "txt", "pkl"]:
            messagebox.showwarning(
                "알림", "올바른 파일 형식을 입력하세요."
            )
            return

        try:
            self.db.load_data(file_type)
            self.manager.records = []

            for record in self.db.records:

                if isinstance(record, dict):
                    self.manager.records.append(
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
                    self.manager.records.append(record)

            self.show_records()

            messagebox.showinfo(
                "완료", "파일을 불러왔습니다."
            )

        except Exception as e:
            messagebox.showerror("오류", str(e))

    # 파일 저장하기
    def save_data(self):

        file_type = simpledialog.askstring(
            "파일 저장",
            "저장할 파일 형식을 입력하세요. (json/csv/txt/pkl)"
        )

        if not file_type:
            return

        file_type = file_type.lower().strip()

        if file_type not in ["json", "csv", "txt", "pkl"]:
            messagebox.showwarning(
                "알림", "올바른 파일 형식을 입력하세요."
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
                "완료", "파일을 저장했습니다."
            )

        except Exception as e:
            messagebox.showerror("오류", str(e))


# 프로그램 실행
if __name__ == "__main__":

    root = tk.Tk()

    app = HealthManagerGUI(root)

    root.mainloop()
