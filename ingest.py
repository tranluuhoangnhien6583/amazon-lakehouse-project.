import os
import duckdb
import pandas as pd
from datasets import load_dataset

def main():
    md_token = os.environ.get("MOTHERDUCK_TOKEN")
    hf_token = os.environ.get("HF_TOKEN")

    if not md_token:
        raise ValueError("Không tìm thấy MOTHERDUCK_TOKEN!")
    print("Đang kết nối tới MotherDuck...")
    con = duckdb.connect(f'md:amazon_lakehouse?motherduck_token={md_token}')

    print("Đang tải dữ liệu AMAZON-Products-2023 từ Hugging Face...")
    dataset = load_dataset("milistu/AMAZON-Products-2023", split="train", token=hf_token)

    df = dataset.to_pandas()
    print(f"Tải thành công {len(df)} dòng dữ liệu.")

    print("Đang nạp dữ liệu thô vào Lakehouse (Bảng: amazon_raw)...")
    # Lệnh này tạo bảng mới và ghi đè nếu bảng đã tồn tại, rất hợp cho việc cập nhật hàng ngày
    con.execute("CREATE OR REPLACE TABLE amazon_raw AS SELECT * FROM df")

    print("Hoàn tất nạp dữ liệu!")
    con.close()

if __name__ == "__main__":
    main()
