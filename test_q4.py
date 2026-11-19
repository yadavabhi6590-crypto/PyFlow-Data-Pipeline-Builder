from pyflow.utils import read_csv_in_chunk

if __name__ =="__main__":
    print("__Question 4: Large CSV Generator Test __")

    file_path = "D:\\tutedude\\Python_Project_t\\PyFlow_Assignment_2\\data\\gdp.csv"

    chunk_count=0
    for chunk in read_csv_in_chunk(file_path,chunk_size= 100):
        chunk_count +=1
        print(f"Chunk {chunk_count} is load, from this {len(chunk)}rows ")

        if chunk_count ==3:
            break
    print("[Success] CSV Generator Successfully is working")



    #QUestion 5  List Comprehension and Dictionary


    