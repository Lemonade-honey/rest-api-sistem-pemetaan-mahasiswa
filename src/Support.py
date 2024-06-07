class ArraySupport:
    # mencari key dari nilai value
    def find_key_by_value(self, lists: dict, target_value) -> str | int:
        # Loop melalui pasangan kunci-nilai dalam lists
        for key, value in lists.items():
            # Jika nilai (value) sesuai dengan nilai yang dicari, tambahkan kunci ke dalam list (value adalah array)
            # atau jika nilai sesuai dengan nilai yang dicari (value adalah single value)
            if isinstance(value, list) and target_value in value or value == target_value:
                return key
            
    # mencari nilai value dari key
    def find_value(self, lists: dict, target_key) -> str | int:
        for key, value in lists.items():
            if key == target_key :
                return value
            
    
    # combined array
    def combined_same_key(self, lists: dict)-> dict:
        combined_values = {}

        for item in lists :
            for key, value in item.items() :
                # Jika kunci sudah ada, tambahkan nilai ke dalam array yang sudah ada
                if key in combined_values:
                    combined_values[key].append(value)
                else:
                    # Jika kunci belum ada, buat array baru
                    combined_values[key] = [value]

        result = {}
        for key, values in combined_values.items():
            result[key] = values


        return result
    
    # sum value by key
    def sum_values_by_keys(self, dictionary: dict)-> dict:

        for key, values in dictionary.items():
            # defaukt value
            nilai = 0
            for value in values:
                nilai += value

            dictionary[key] = nilai

        return dictionary