from pyflow.extractors import DataExtractor

if __name__ =="__main__":
    extractor=DataExtractor(base_dir="data")

    df=extractor.extract("D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\us-counties-2023.csv")


    print("shape",df.shape)
    print(df.head(3))