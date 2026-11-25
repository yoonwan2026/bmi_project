
import tkinter as tk
from tkinter import messagebox, simpledialog
from modules.health_logic import HealthManager
from modules.health_db import HealthManager as DBManager, HealthRecord


class HealthManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI 건강관리 프로그램")
        self.root.geometry("750x500")

        # 모듈 2의 HealthManager 객체 생성
        self.manager = HealthManager()

        # 모듈 1의 파일 관리 객체 생성
        self.db = DBManager()

        # 제목
        title = tk.Label(
            root,
            text="BMI 건강관리 프로그램",
            font=("맑은 고딕", 20, "bold")
        )
        title.pack(pady=15)

        # 버튼 영역
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="건강정보 추가",
                  command=self.add_record, width=13).grid(row=0, column=0, padx=5)

        tk.Button(button_frame, text="목록 조회",
                  command=self.show_records, width=13).grid(row=0, column=1, padx=5)

        tk.Button(button_frame, text="상세 조회",
                  command=self.show_detail, width=13).grid(row=0, column=2, padx=5)

        tk.Button(button_frame, text="정보 수정",
                  command=self.update_record, width=13).grid(row=0, column=3, padx=5)

        tk.Button(button_frame, text="정보 삭제",
                  command=self.delete_record, width=13).grid(row=0, column=4, padx=5)

        # 파일 및 통계 버튼
        file_frame = tk.Frame(root)
        file_frame.pack(pady=5)

        tk.Button(file_frame, text="파일 불러오기",
                  command=self.load_data, width=15).grid(row=0, column=0, padx=5)

        tk.Button(file_frame, text="파일 저장하기",
                  command=self.save_data, width=15).grid(row=0, column=1, padx=5)

        tk.Button(file_frame, text="건강정보 통계",
                  command=self.show_statistics, width=15).grid(row=0, column=2, padx=5)

        # 건강정보 목록
        self.listbox = tk.Listbox(root, width=95, height=17)
        self.listbox.pack(pady=15)

        self.show_records()

    # 건강정보 추가
    def add_record(self):
        name = simpledialog.askstring("추가", "이름을 입력하세요.")
        if not name:
            return

        birth_year = simpledialog.askinteger("추가", "출생연도를 입력하세요.")
        if birth_year is None:
            return

        gender = simpledialog.askstring("추가", "성별을 입력하세요.")
        if not gender:
            return

        height = simpledialog.askfloat("추가", "키(cm)를 입력하세요.")
        if height is None:
            return

        weight = simpledialog.askfloat("추가", "몸무게(kg)를 입력하세요.")
        if weight is None:
            return

        try:
            self.manager.add_record(
                name, birth_year, gender, height, weight
            )
            self.show_records()
            messagebox.showinfo("완료", "건강정보가 추가되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", str(e))

    # 건강정보 목록 조회
    def show_records(self):
        self.listbox.delete(0, tk.END)

        records = self.manager.get_all_records()

        for record in records:
            text = (
                f"{record.id} | {record.name} | "
                f"{record.height}cm | {record.weight}kg | "
                f"BMI: {record.bmi} | {record.status}"
            )
            self.listbox.insert(tk.END, text)

    # 선택한 건강정보 가져오기
    def get_selected_record(self):
        selected = self.listbox.curselection()

        if not selected:
            messagebox.showwarning("알림", "건강정보를 선택하세요.")
            return None

        records = self.manager.get_all_records()
        return records[selected[0]]

    # 건강정보 상세 조회
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

        messagebox.showinfo("건강정보 상세 조회", detail)

    # 건강정보 수정
    def update_record(self):
        record = self.get_selected_record()

        if record is None:
            return

        height = simpledialog.askfloat(
            "정보 수정", "새로운 키(cm)를 입력하세요.",
            initialvalue=float(record.height)
        )

        if height is None:
            return

        weight = simpledialog.askfloat(
            "정보 수정", "새로운 몸무게(kg)를 입력하세요.",
            initialvalue=float(record.weight)
        )

        if weight is None:
            return

        try:
            self.manager.update_record(record.id, height, weight)
            self.show_records()
            messagebox.showinfo("완료", "건강정보가 수정되었습니다.")
        except Exception as e:
            messagebox.showerror("오류", str(e))

    # 건강정보 삭제
    def delete_record(self):
        record = self.get_selected_record()

        if record is None:
            return

        answer = messagebox.askyesno(
            "삭제 확인", "선택한 건강정보를 삭제하시겠습니까?"
        )

        if answer:
            self.manager.delete_record(record.id)
            self.show_records()
            messagebox.showinfo("완료", "건강정보가 삭제되었습니다.")

    # 건강정보 통계
    def show_statistics(self):
        try:
            stats = self.manager.get_statistics()

            result = "건강정보 통계\n\n"

            for key, value in stats.items():
                result += f"{key}: {value}\n"

            messagebox.showinfo("건강정보 통계", result)

        except Exception as e:
            messagebox.showerror("오류", str(e))

    # 파일 불러오기
    def load_data(self):
        file_type = simpledialog.askstring(
            "파일 불러오기",
            "파일 형식을 입력하세요. (json/csv/txt/pkl)"
        )

        if file_type not in ["json", "csv", "txt", "pkl"]:
            messagebox.showwarning("알림", "올바른 파일 형식을 입력하세요.")
            return

        try:
            self.db.load_data(file_type)
            self.manager.records = []

            for record in self.db.records:
                if isinstance(record, dict):
                    self.manager.records.append(HealthRecord(
                        record["id"],
                        record["name"],
                        int(record["birth_year"]),
                        record["gender"],
                        float(record["height"]),
                        float(record["weight"]),
                        float(record["bmi"]),
                        record["status"]
                    ))

            self.show_records()
            messagebox.showinfo("완료", "파일을 불러왔습니다.")

        except Exception as e:
            messagebox.showerror("오류", str(e))

    # 파일 저장하기
    def save_data(self):
        file_type = simpledialog.askstring(
            "파일 저장",
            "저장할 파일 형식을 입력하세요. (json/csv/txt/pkl)"
        )

        if file_type not in ["json", "csv", "txt", "pkl"]:
            messagebox.showwarning("알림", "올바른 파일 형식을 입력하세요.")
            return

        try:
            self.db.records = [
                record.to_dict()
                if isinstance(record, HealthRecord)
                else record
                for record in self.manager.records
            ]
            self.db.save_data(file_type)
            messagebox.showinfo("완료", "파일을 저장했습니다.")

        except Exception as e:
            messagebox.showerror("오류", str(e))


# 프로그램 실행
if __name__ == "__main__":
    root = tk.Tk()
    app = HealthManagerGUI(root)
    root.mainloop()
