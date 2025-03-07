class SortingAlgorithm:
    def __init__(self, delay_ms=50):
        self.comparisons = 0
        self.array_accesses = 0
        self.delay = delay_ms / 1000

    def sort(self, arr):
        raise NotImplementedError('Sort method must be implemented')
        
    def reset_stats(self):
        self.comparisons = 0
        self.array_accesses = 0
        
    def compare(self, a, b):
        self.comparisons += 1
        return a > b
    
    def access(self, arr, index):
        self.array_accesses += 1
        return arr[index]
    
    def write(self, arr, index, value):
        self.array_accesses += 1
        arr[index] = value
    
    def print_stats(self):
        print(f'{self.__class__.__name__} - {self.comparisons} comparisons, {self.array_accesses} array accesses\n')

    def delay(self):
        return self.delay


class Bubble(SortingAlgorithm):
    def sort(self, arr):
        n = len(arr)
        for i in range(n - 1):
            for j in range(n - i - 1):
                if self.compare(self.access(arr, j), self.access(arr, j + 1)):
                    temp = self.access(arr, j)
                    self.write(arr, j, self.access(arr, j + 1))
                    self.write(arr, j + 1, temp)
                    yield arr, [j, j + 1]
        self.print_stats()


class Insertion(SortingAlgorithm):
    def sort(self, arr):
        for i in range(1, len(arr)):
            key = self.access(arr, i)
            j = i - 1
            while j >= 0 and self.compare(self.access(arr, j), key):
                self.write(arr, j + 1, self.access(arr, j))
                j -= 1
                yield arr, [j + 1, i]
            self.write(arr, j + 1, key)
            yield arr, [j + 1, i]
        self.print_stats()


class Selection(SortingAlgorithm):
    def sort(self, arr):
        n = len(arr)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.compare(self.access(arr, min_idx), self.access(arr, j)):
                    min_idx = j
            if min_idx != i:
                temp = self.access(arr, i)
                self.write(arr, i, self.access(arr, min_idx))
                self.write(arr, min_idx, temp)
            yield arr, [i, min_idx]
        self.print_stats()


class Merge(SortingAlgorithm):
    def sort(self, arr):
        if len(arr) <= 1:
            return arr
        
        def merge(left, right):
            result = []
            i = j = 0
            while i < len(left) and j < len(right):
                if self.compare(right[j], left[i]):  # left[i] <= right[j]
                    result.append(left[i])
                    i += 1
                else:
                    result.append(right[j])
                    j += 1
            result.extend(left[i:])
            result.extend(right[j:])
            return result
        
        def merge_sort_yield(arr, start, end):
            if end - start > 1:
                mid = (start + end) // 2
                yield from merge_sort_yield(arr, start, mid)
                yield from merge_sort_yield(arr, mid, end)
                
                left = arr[start:mid]
                right = arr[mid:end]
                merged = merge(left, right)
                
                for i in range(start, end):
                    self.write(arr, i, merged[i - start])
                    yield arr, [i]  # Return index of modified element
        
        yield from merge_sort_yield(arr, 0, len(arr))
        self.print_stats()


class Quick(SortingAlgorithm):
    def sort(self, arr):
        def partition(arr, low, high):
            pivot = self.access(arr, high)
            i = low - 1
            
            for j in range(low, high):
                if not self.compare(self.access(arr, j), pivot):  # arr[j] <= pivot
                    i += 1
                    temp = self.access(arr, i)
                    self.write(arr, i, self.access(arr, j))
                    self.write(arr, j, temp)
                    yield arr, [i, j]  # Return indices of swapped elements
            
            temp = self.access(arr, i + 1)
            self.write(arr, i + 1, self.access(arr, high))
            self.write(arr, high, temp)
            yield arr, [i + 1, high]  # Return indices of swapped elements
            return i + 1
        
        def quick_sort_yield(arr, low, high):
            if low < high:
                pi_generator = partition(arr, low, high)
                pi = None
                
                for step in pi_generator:
                    if isinstance(step, tuple):
                        arr_state, indices = step
                        pi = indices[0]  # Use the first index as the partition index
                        yield arr, indices
                    else:
                        pi = step
                
                yield from quick_sort_yield(arr, low, pi - 1)
                yield from quick_sort_yield(arr, pi + 1, high)
        
        if len(arr) <= 1:
            yield arr, []
        else:
            yield from quick_sort_yield(arr, 0, len(arr) - 1)
        self.print_stats()


class Heap(SortingAlgorithm):
    def sort(self, arr):
        def heapify(arr, n, i):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            
            if left < n and self.compare(self.access(arr, left), self.access(arr, largest)):
                largest = left
            
            if right < n and self.compare(self.access(arr, right), self.access(arr, largest)):
                largest = right
            
            if largest != i:
                temp = self.access(arr, i)
                self.write(arr, i, self.access(arr, largest))
                self.write(arr, largest, temp)
                yield arr, [i, largest]  # Return indices of swapped elements
                yield from heapify(arr, n, largest)
        
        n = len(arr)
        
        # Build max heap
        for i in range(n // 2 - 1, -1, -1):
            yield from heapify(arr, n, i)
        
        # Extract elements from heap one by one
        for i in range(n - 1, 0, -1):
            temp = self.access(arr, i)
            self.write(arr, i, self.access(arr, 0))
            self.write(arr, 0, temp)
            yield arr, [0, i]  # Return indices of swapped elements
            yield from heapify(arr, i, 0)
        
        self.print_stats()


class Shell(SortingAlgorithm):
    def sort(self, arr):
        n = len(arr)
        gap = n // 2
        
        while gap > 0:
            for i in range(gap, n):
                temp = self.access(arr, i)
                j = i
                
                while j >= gap and self.compare(self.access(arr, j - gap), temp):
                    self.write(arr, j, self.access(arr, j - gap))
                    j -= gap
                    yield arr, [j, j - gap]  # Return indices of compared elements
                    
                self.write(arr, j, temp)
                yield arr, [j, i]  # Return indices of inserted element and original position
                
            gap //= 2
        
        self.print_stats()


class Cocktail(SortingAlgorithm):
    def sort(self, arr):
        n = len(arr)
        swapped = True
        start = 0
        end = n - 1
        
        while swapped:
            swapped = False
            
            # Forward pass (like bubble sort)
            for i in range(start, end):
                if self.compare(self.access(arr, i), self.access(arr, i + 1)):
                    temp = self.access(arr, i)
                    self.write(arr, i, self.access(arr, i + 1))
                    self.write(arr, i + 1, temp)
                    swapped = True
                    yield arr, [i, i + 1]
            
            if not swapped:
                break
            
            swapped = False
            end -= 1
            
            # Backward pass
            for i in range(end - 1, start - 1, -1):
                if self.compare(self.access(arr, i), self.access(arr, i + 1)):
                    temp = self.access(arr, i)
                    self.write(arr, i, self.access(arr, i + 1))
                    self.write(arr, i + 1, temp)
                    swapped = True
                    yield arr, [i, i + 1]
            
            start += 1
        
        self.print_stats()


class Gnome(SortingAlgorithm):
    def sort(self, arr):
        n = len(arr)
        index = 0
        
        while index < n:
            if index == 0:
                index += 1
            
            if not self.compare(self.access(arr, index - 1), self.access(arr, index)):
                index += 1
            else:
                temp = self.access(arr, index)
                self.write(arr, index, self.access(arr, index - 1))
                self.write(arr, index - 1, temp)
                index -= 1
                yield arr, [index, index + 1]
        
        self.print_stats()


class Radix(SortingAlgorithm):
    def sort(self, arr):
        # Find the maximum number to know number of digits
        max_num = max(arr)
        
        # Do counting sort for every digit
        exp = 1
        while max_num // exp > 0:
            n = len(arr)
            output = [0] * n
            count = [0] * 10
            
            # Store count of occurrences in count[]
            for i in range(n):
                index = self.access(arr, i) // exp % 10
                count[index] += 1
            
            # Change count[i] so that count[i] contains actual
            # position of this digit in output[]
            for i in range(1, 10):
                count[i] += count[i - 1]
            
            # Build the output array
            i = n - 1
            while i >= 0:
                index = self.access(arr, i) // exp % 10
                output[count[index] - 1] = self.access(arr, i)
                count[index] -= 1
                i -= 1
            
            # Copy the output array to arr[]
            for i in range(n):
                self.write(arr, i, output[i])
                yield arr, [i]
            
            exp *= 10
        
        self.print_stats()


class Bitonic(SortingAlgorithm):
    def sort(self, arr):
        def compare_and_swap(arr, i, j, direction):
            if (direction == 1 and self.compare(self.access(arr, i), self.access(arr, j))) or \
               (direction == 0 and not self.compare(self.access(arr, i), self.access(arr, j))):
                temp = self.access(arr, i)
                self.write(arr, i, self.access(arr, j))
                self.write(arr, j, temp)
                yield arr, [i, j]
        
        def bitonic_merge(arr, low, cnt, direction):
            if cnt > 1:
                k = cnt // 2
                for i in range(low, low + k):
                    yield from compare_and_swap(arr, i, i + k, direction)
                yield from bitonic_merge(arr, low, k, direction)
                yield from bitonic_merge(arr, low + k, k, direction)
        
        def bitonic_sort_recursive(arr, low, cnt, direction):
            if cnt > 1:
                k = cnt // 2
                # Sort in ascending order
                yield from bitonic_sort_recursive(arr, low, k, 1)
                # Sort in descending order
                yield from bitonic_sort_recursive(arr, low + k, k, 0)
                # Merge the entire sequence in the required direction
                yield from bitonic_merge(arr, low, cnt, direction)
        
        # Pad the array to a power of 2 length
        n = len(arr)
        # Find the next power of 2
        power_of_2 = 1
        while power_of_2 < n:
            power_of_2 *= 2
        
        # If array length is not a power of 2, we can't use bitonic sort directly
        # For simplicity, we'll only sort the largest power of 2 elements
        yield from bitonic_sort_recursive(arr, 0, min(power_of_2, n), 1)
        self.print_stats()