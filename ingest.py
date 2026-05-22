import os
import duckdb
import pandas as pd
from datasets import load_dataset

def main():
    # Thêm .strip() để tự động dọn dẹp khoảng trắng/xuống dòng thừa khi copy
    md_token = os.environ.get("MOTHERDUCK_TOKEN", "").strip()
    hf_token = os.environ.get("HF_TOKEN", "").strip()

    if not md_token:
        raise ValueError("Không tìm thấy MOTHERDUCK_TOKEN!")

    # Kết nối tới database amazon_lakehouse trên MotherDuck
    print("Đang kết nối tới MotherDuck...")
    con = duckdb.connect(f'md:amazon_lakehouse?motherduck_token={md_token}')

    # Tải bộ dữ liệu từ Hugging Face
    print("Đang tải dữ liệu AMAZON-Products-2023 từ Hugging Face...")
    dataset = load_dataset("milistu/AMAZON-Products-2023", split="train", token=hf_token)
    
    df = dataset.to_pandas()
    print(f"Tải thành công {len(df)} dòng dữ liệu.")

    # Nạp dữ liệu vào MotherDuck (Tầng Bronze)
    print("Đang nạp dữ liệu thô vào Lakehouse (Bảng: amazon_raw)...")
    con.execute("CREATE OR REPLACE TABLE amazon_raw AS SELECT * FROM df")

    print("Hoàn tất nạp dữ liệu!")
    con.close()

if __name__ == "__main__":
    main()
