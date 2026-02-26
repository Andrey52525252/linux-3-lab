#include <iostream>
#include <chrono>
#include <fstream>
#include <vector>
#include <random>
#include <algorithm>
#include <iterator>




void append_commit(const std::string& filename, const std::vector<int>& numbers) {
    // Открываем файл в режиме добавления
    std::ofstream file(filename, std::ios::app);

    // Записываем числа через пробел в одну строку
    std::copy(numbers.begin(), numbers.end(),
              std::ostream_iterator<int>(file, " "));
    // Завершаем строку переводом
    file << '\n';
}  //функция для добавления в файл нового состояния массива

void bubbleSort(std::vector<int>& arr, std::string file) {
    int n = arr.size();
    
    // Проходим по всем элементам n-1 раз
    for (int i = 0; i < n - 1; i++) {
        // Сравниваем соседние элементы
        for (int j = 0; j < n - i - 1; j++) {
            // Если текущий элемент больше следующего, меняем их местами
            if (arr[j] > arr[j + 1]) {
                std::swap(arr[j], arr[j + 1]);
                append_commit(file, arr);
            }
        }
    }
}

void insertionSort(std::vector<int>& arr, std::string file) {
    int n = arr.size();
    
    for (int i = 1; i < n; i++) {
        int key = arr[i];
        int j = i - 1;
        
        while (j >= 0 && arr[j] > key) {
            arr[j + 1] = arr[j];
            append_commit(file, arr);
            j--;
        }
        arr[j + 1] = key;
    }
}

void selectionSort(std::vector<int>& arr, std::string file) {
    int n = arr.size();
    
    for (int i = 0; i < n - 1; i++) {
        int minIndex = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[minIndex]) {
                minIndex = j;
            }
        }
        if (minIndex != i) {
            std::swap(arr[i], arr[minIndex]);
            append_commit(file, arr);
        }
    }
}

void quickSort(std::vector<int>& arr, std::string file) {
    if (arr.size() <= 1) return;
    
    int pivot = arr[arr.size() / 2];
    int i = 0, j = arr.size() - 1;
    
    while (i <= j) {
        while (arr[i] < pivot) i++;
        while (arr[j] > pivot) j--;
        if (i <= j) {
            std::swap(arr[i], arr[j]);
            append_commit(file, arr);
            i++;
            j--;
        }
    }
    
    if (j > 0) {
        std::vector<int> left(arr.begin(), arr.begin() + j + 1);
        quickSort(left, file);
        std::copy(left.begin(), left.end(), arr.begin());
    }
    
    if (i < arr.size()) {
        std::vector<int> right(arr.begin() + i, arr.end());
        quickSort(right, file);
        std::copy(right.begin(), right.end(), arr.begin() + i);
    }
}

void heapify(std::vector<int>& arr, int size, int root, std::string file) {
    int largest = root;
    int left = 2 * root + 1;
    int right = 2 * root + 2;
    
    if (left < size && arr[left] > arr[largest])
        largest = left;
    
    if (right < size && arr[right] > arr[largest])
        largest = right;
    
    if (largest != root) {
        std::swap(arr[root], arr[largest]);
        append_commit(file, arr);
        heapify(arr, size, largest, file);
    }
}

void heapSort(std::vector<int>& arr, std::string file) {
    int size = arr.size();
    
    // Построение max-heap
    for (int i = size / 2 - 1; i >= 0; i--)
        heapify(arr, size, i, file);
    
    // Извлечение элементов из кучи
    for (int i = size - 1; i > 0; i--) {
        std::swap(arr[0], arr[i]);
        heapify(arr, i, 0, file);
    }
}

int rand_uns(int min, int max) {
    unsigned seed = std::chrono::steady_clock::now().time_since_epoch().count();
    static std::default_random_engine e(seed);
    std::uniform_int_distribution<int> d(min, max);
    return d(e);
}


int min_element = 1;
int max_element = 100; // limits of acceptable values in lists


int main(int argc, char* argv[]) {
    std::ofstream file("1.csv", std::ios::app);
    
    // Проверяем открылся ли файл
    if (!file.is_open()) {
        std::cout << "Error: Cannot open file!" << std::endl;
        return 1;
    }

    int length = 100;
    std::vector<int> list(length);

    for (int i = 0; i < length; i++) {
        list[i] = rand_uns(min_element, max_element);
    }

    std::string bubbleSort_file("result_files/bubbleSort_file.txt");
    bubbleSort(list, bubbleSort_file);

}

