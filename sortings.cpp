
    list = generate_array(length);

    std::string insertionSort_file("result_files/insertionSort_file.txt");
    insertionSort(list, insertionSort_file);

    list = generate_array(length);

    std::string selectionSort_file("result_files/selectionSort_file.txt");
    selectionSort(list, selectionSort_file);

    list = generate_array(length);

    std::string quickSort_file("result_files/quickSort_file.txt");
    quickSort(list, 0, 99, quickSort_file);

