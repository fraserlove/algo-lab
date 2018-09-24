def generate(_len):
    record_array = [["", "", 0.0, ""] for i in range(_len)]
    return record_array

def insert(record_array):
    for i in range(len(record_array)):
        print(record_array)
        city = input("City: ")
        country = input("Country: ")
        pop = input("Population: ")
        lan = input("Language: ")
        record_array[i] = [city, country, pop, lan]
    return record_array

def out_table(record_array):
    print("\n")
    for record in record_array:
        for element in record:
            print(element,"\t\t", end="")
        print()

def out_record(record_array):
    print("\n")
    n = (int(input("What record do you want to access: "))-1)
    for i in range(len(record_array)):
        if i == n:
            for element in record_array[i]:
                print(element,"\t\t", end="")
                
def query_display(record_array):
    print("\n")
    query = input("Enter a city to diplay info on: ")
    for i in range(len(record_array)):
        if record_array[i][0] == query:
            for element in record_array[i]:
                print(element,"\t\t", end="")
                
def record_search(record_array):
    print("\n")
    query = input("Enter a country to diplay info on: ")
    for i in range(len(record_array)):
        if record_array[i][1] == query:
            print(record_array[i][0])   

def main():
    _len = int(input("How many records will you be entering: "))
    city_array = insert(generate(_len))
    out_record(city_array)
    out_table(city_array)
    query_display(city_array)
    record_search(city_array)

main()
