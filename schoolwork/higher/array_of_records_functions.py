def generate(_len):
    record_array = [["", "", 0.0, ""] for i in range(_len)]
    return record_array

# Insert values into each record
def insert(record_array):
    for record in range(len(record_array)):
        print(record_array)
        field_0 = input("field_0: ")
        field_1 = input("field_1: ")
        field_2 = input("field_2: ")
        field_3 = input("field_3: ")
        record_array[record] = [field_0, field_1, field_2, field_3]
    return record_array

# Displays array of records as a table
def out_table(record_array):
    print("\n")
    for record in record_array:
        for element in record:
            print(element,"\t\t", end="")
        print()

# Displays record of specified index
def out_record(record_array):
    print("\n")
    record_index = (int(input("What record do you want to access: "))-1)
    for record in range(len(record_array)):
        if record == record_index:
            for element in record_array[record]:
                print(element,"\t\t", end="")
            break
    else:
        print("Error: No Matched Fields...")

# Searches fields in all records for a value and for matched records displays all field values                
def info_query_search(record_array):
    print("\n")
    query = input("Enter a [field_0] value to diplay info on: ")
    for record in range(len(record_array)):
        #array[record][value] - value is the field value being looked for
        if record_array[record][0] == query:
            for element in record_array[record]:
                print(element,"\t\t", end="")
            break
    else:
        print("Error: No Matched Fields...")

# Searches fields in all records for a value and for matched records displays another field value        
def record_search(record_array):
    print("\n")
    query = input("Enter a [field_1] value to diplay [field_0] value: ")
    for record in range(len(record_array)):
        #array[record][value] - value is the field value being looked for
        if record_array[record][1] == query:
            print(record_array[record][0])
            break
    else:
        print("Error: No Matched Fields...")

# Finds the maximum and minimum values for a specified field
def field_max_min(record_array):
    print("\n")
    _max = record_array[0][2]
    _min = record_array[0][2]
    _max_name = record_array[0][0]
    _min_name = record_array[0][0]
    #array[record][value] - value is the field specified
    for record in range(len(record_array)):
        if int(record_array[record][2]) > int(_max):
            _max = record_array[record][2]
            _max_name = record_array[record][0]
        elif int(record_array[record][2]) < int(_min):
            _min = record_array[record][2]
            _min_name = record_array[record][0]
    print("Maximum: {}, Pop - {}".format(_max_name, _max))
    print("Minimum: {}, Pop - {}".format(_min_name, _min))

# Totals the values in a field
def field_total(record_array):
    total = 0
    for record in range(len(record_array)):
        total += int(record_array[record][2])
    print("[field_2] Total: {}".format(total))

def main():
    _len = int(input("How many records will you be entering: "))
    city_array = insert(generate(_len))
    out_table(city_array)
    out_record(city_array)
    info_query_search(city_array)
    record_search(city_array)
    field_max_min(city_array)
    field_total(city_array)

main()
