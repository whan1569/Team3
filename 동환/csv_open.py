import pandas as pd
import tkinter as tk
from tkinter import ttk

# 경로 지정
file_path = r"C:\Users\USER\Desktop\새 폴더\(2기) DX데이터스쿨_VOD\2월\상세보기_2월.csv"

try:
    # CSV 파일 읽기
    df = pd.read_csv(file_path)

    # 새로운 창 생성
    root = tk.Tk()
    root.title("VOD 시청 데이터")

    # Treeview 위젯 생성
    tree = ttk.Treeview(root)
    tree["columns"] = list(df.columns)
    tree["show"] = "headings"  # 첫 번째 빈 컬럼 제거

    # 컬럼 설정
    for col in df.columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)  # 컬럼 너비 조정 가능

    # 데이터 추가
    for _, row in df.iterrows():
        tree.insert("", "end", values=list(row))

    # 스크롤바 추가
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    tree.pack(expand=True, fill="both")
    root.mainloop()

except FileNotFoundError:
    print("지정된 경로에 파일이 존재하지 않습니다. 경로를 확인해주세요.")
except Exception as e:
    print(f"오류가 발생했습니다: {e}")
