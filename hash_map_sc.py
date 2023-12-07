# Name: Courtlen Olmo
# OSU Email: OlmoC@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: Assignment 6 - Hashmap
# Due Date: 12/7/23
# Description: Hashmap implementation with separate chaining


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        Updates the key/value pair in the hash map.
        """
        # Check to see if table needs to be resized
        if self.table_load() >= 1.0:
            self.resize_table(self._capacity * 2)

        index = self._hash_function(key) % self._capacity

        # If the array is empty, put in first element
        if self.get_size() == 0:
            self._buckets.get_at_index(index).insert(key, value)
            self._size += 1
            return

        # Check if node is already in the linkedlist, and replace value if True.
        node = self._buckets.get_at_index(index).contains(key)
        if node:
            node.value = value
            return
        else:
            self._buckets.get_at_index(index).insert(key, value)
        self._size += 1

    def resize_table(self, new_capacity: int) -> None:
        """
        changes the capacity of the internal hash table.
        """
        if new_capacity < 1.0:
            return
        else:
            # Copy nodes into a temporary array
            if self._is_prime(new_capacity) is False:
                new_capacity = self._next_prime(new_capacity)
            old_array = DynamicArray()
            for i in range(self._capacity):
                element = self._buckets.get_at_index(i)
                if element._head is None:
                    continue
                else:
                    old_array.append(element)

            # Reinitialize the DynamicArray for the Hashmap
            self._buckets = DynamicArray()
            self._capacity = new_capacity
            self._size = 0
            for _ in range(self._capacity):
                self._buckets.append(LinkedList())

            # Loop through nodes, readding them to the new array
            for i in range(old_array.length()):
                node = old_array.get_at_index(i)._head
                while node.next is not None:
                    self.put(node.key, node.value)
                    node = node.next
                self.put(node.key, node.value)

    def table_load(self) -> float:
        """
        returns the hash table load factor
        """
        return float(self._size / self._capacity)

    def empty_buckets(self) -> int:
        """
        Returns the number of empty buckets in the hash table
        """
        total = 0
        for i in range(self._capacity):
            element = self._buckets.get_at_index(i)
            if element._head is None:
                total += 1
        return total

    def get(self, key: str):
        """
        Returns the value associated with the given key
        """
        index = self._hash_function(key) % self._capacity
        node = self._buckets.get_at_index(index).contains(key)
        if node:
            return node.value
        else:
            return None

    def contains_key(self, key: str) -> bool:
        """
        Returns True if the given key is in the hash map
        """
        index = self._hash_function(key) % self._capacity
        node = self._buckets.get_at_index(index).contains(key)
        if node:
            return True
        else:
            return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the hash map
        """
        # Find index, run the linkedlist remove function on it. If it's successfully
        # removed, reduce size by 1
        index = self._hash_function(key) % self._capacity
        node = self._buckets.get_at_index(index).remove(key)
        if node == True:
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple of
        a key/value pair stored in the hash map
        """
        array = DynamicArray()
        for i in range(self._capacity):
            node = self._buckets.get_at_index(i)
            if node._head is None:
                continue
            else:
                node = node._head
                while node:
                    key_value = (node.key, node.value)
                    array.append(key_value)
                    node = node.next
        return array

    def clear(self) -> None:
        """
        Clears the contents of the hash map without changing the underlying hash table capacity
        """
        self._buckets = DynamicArray()
        self._size = 0
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())


def find_mode(da: DynamicArray) -> tuple[DynamicArray, int]:
    """
    Receives an unsorted array and returns a tuple containing an array of the mode and
    most occurring value in the hashmap
    """

    map = HashMap()

    # Put values into map, if the key already exists, add 1 to the value
    for i in range(da.length()):
        if map.contains_key(da[i]):
            map.put(da[i], (map.get(da[i]) + 1))
        else:
            map.put(da[i], 1)

    # Initialize values and append the first tuple to the array
    return_array = DynamicArray()
    return_array.append(da[0])
    highest_item = da[0]
    frequency = map.get(da[0])

    # Loop through da, checking to see if the next value is more than the current one
    for i in range(da.length() - 1):
        if map.get(da[i + 1]) > frequency:
            # If a value is found greater than the previous mode, reinitialize the array
            return_array = DynamicArray()
            return_array.append(da[i + 1])
            highest_item, frequency = da[i + 1], map.get(da[i + 1])
        elif map.get(da[i + 1]) == frequency and da[i + 1] != highest_item:
            # If it has the same frequency, check to make sure it isn't already in the return array
            # Set a bool flag to determine the result, then use that to append value
            for n in range(return_array.length()):
                if da[i + 1] != return_array[n]:
                    ok_to_append = True
                else:
                    ok_to_append = False
                    break
            if ok_to_append == True:
                return_array.append(da[i + 1])

    return (return_array, frequency)


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
