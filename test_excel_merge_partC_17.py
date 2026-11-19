from pyflow.utils import merge_excel_sheets

if __name__ =="__main__":
    print("-- Excel sheets Merging Test---")

    # to give the any sample excel sheet path here
    excel_path ="D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\Economic_indicatore.xlsx"

    try:
        master_data =merge_excel_sheets(excel_path)

        print("\n[SUCCESS] Excel Sheets Merged Successfully:")
        print(f" -> Total Consolidated Rows : {len(master_data):,}")
        print(f" -> Columns Available       : {list(master_data.columns)}")
        print("\nFirst 3 rows:")
        print(master_data.head(3))
    except Exception as e:
        print(f"[ERROR]{e}")