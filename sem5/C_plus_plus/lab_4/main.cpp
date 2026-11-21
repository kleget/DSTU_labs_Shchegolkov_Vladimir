#include <climits>
#include <cstring>
#include <filesystem>
#include <fstream>
#include <iostream>
#include <sstream>
#include <stdexcept>
#include <string>

#ifdef _WIN32
#include <windows.h>
#endif

using namespace std;

string readLine(string prompt) {
    string line;
    cout << prompt;
    if (!getline(cin, line)) {
        throw runtime_error("Ввод завершён.");
    }
    return line;
}

int readInt(string prompt, int minimum, int maximum) {
    while (true) {
        stringstream input(readLine(prompt));
        int value;
        char extra;
        if (input >> value && !(input >> extra) && value >= minimum && value <= maximum) {
            return value;
        }
        cout << "Введите целое число от " << minimum << " до " << maximum << ".\n";
    }
}

void readField(string prompt, char field[], int size) {
    while (true) {
        string line = readLine(prompt);
        if (!line.empty() && line.size() < static_cast<size_t>(size)) {
            strcpy(field, line.c_str());
            return;
        }
        cout << "Строка должна быть непустой и занимать менее " << size << " байт.\n";
    }
}

class TextFile {
    string filename;

    void checkOutput(string name) const {
        if (filesystem::exists(name) && filesystem::equivalent(filename, name)) {
            throw runtime_error("Исходный файл и файл результата должны различаться.");
        }
    }

public:
    TextFile(string name) : filename(name) {}

    void copyLastLines(int k) {
        ifstream input(filename);
        if (!input.is_open()) {
            throw runtime_error("Исходный файл не существует или недоступен: " + filename);
        }
        checkOutput("last_lines.txt");

        string line;
        int count = 0;
        while (getline(input, line)) {
            count++;
        }
        if (!input.eof()) {
            throw runtime_error("Ошибка чтения исходного файла.");
        }

        input.clear();
        input.seekg(0);
        ofstream output("last_lines.txt");
        if (!input || !output.is_open()) {
            throw runtime_error("Не удалось подготовить файлы для копирования.");
        }
        for (int i = 0; getline(input, line); i++) {
            if (i >= count - k) {
                output << line << '\n';
            }
        }
        if (!input.eof()) {
            throw runtime_error("Ошибка чтения исходного файла.");
        }
        output.close();
        if (!output) {
            throw runtime_error("Ошибка записи last_lines.txt.");
        }
        if (count == 0) {
            cout << "Исходный файл не содержит строк.\n";
        }
        cout << "Результат: last_lines.txt\n";
    }

    void uniqueCharacters() {
        ifstream input(filename);
        if (!input.is_open()) {
            throw runtime_error("Исходный файл не существует или недоступен: " + filename);
        }
        checkOutput("unique_chars.txt");
        ofstream output("unique_chars.txt");
        if (!output.is_open()) {
            throw runtime_error("Не удалось создать unique_chars.txt.");
        }

        string seen;
        char ch;
        while (input.get(ch)) {
            string symbol(1, ch);
            // В UTF-8 один символ может занимать несколько байтов.
            while (input.peek() >= 128 && input.peek() <= 191) {
                input.get(ch);
                symbol += ch;
            }
            if (seen.find(symbol) == string::npos) {
                seen += symbol;
                output << symbol;
            }
        }
        if (!input.eof()) {
            throw runtime_error("Ошибка чтения исходного файла.");
        }
        output.close();
        if (!output) {
            throw runtime_error("Ошибка записи unique_chars.txt.");
        }
        cout << "Результат: unique_chars.txt\n";
    }
};

struct Voucher {
    char fullName[100];
    char department[100];
    int number;
    char period[100];
    char sanatorium[100];
    char note[200];
};

void printVoucher(const Voucher& voucher) {
    cout << "Ф.И.О.: " << voucher.fullName
         << "\nКафедра (группа, отдел): " << voucher.department
         << "\nНомер путёвки: " << voucher.number
         << "\nПериод: " << voucher.period
         << "\nСанаторий: " << voucher.sanatorium
         << "\nПримечание: " << voucher.note << "\n\n";
}

class VoucherList {
    Voucher* data;
    int count;

public:
    VoucherList() : data(nullptr), count(0) {}

    ~VoucherList() {
        delete[] data;
    }

    int getCount() const {
        return count;
    }

    void add(const Voucher& voucher) {
        Voucher* next = new Voucher[count + 1];
        for (int i = 0; i < count; i++) {
            next[i] = data[i];
        }
        next[count] = voucher;
        delete[] data;
        data = next;
        count++;
    }

    void remove(int number) {
        for (int i = number - 1; i < count - 1; i++) {
            data[i] = data[i + 1];
        }
        count--;
    }

    void printAll() const {
        if (count == 0) {
            cout << "Список пуст.\n";
        }
        for (int i = 0; i < count; i++) {
            cout << "Запись " << i + 1 << ":\n";
            printVoucher(data[i]);
        }
    }

    void save() const {
        ofstream file("vouchers.txt", ios::binary);
        if (!file.is_open()) {
            throw runtime_error("Не удалось создать vouchers.txt.");
        }
        for (int i = 0; i < count; i++) {
            file.write(reinterpret_cast<const char*>(&data[i]), sizeof(Voucher));
        }
        file.close();
        if (!file) {
            throw runtime_error("Ошибка записи vouchers.txt.");
        }
        cout << "Сохранено записей: " << count << ".\n";
    }

    void load() {
        ifstream file("vouchers.txt", ios::binary | ios::ate);
        if (!file.is_open()) {
            throw runtime_error("Файл vouchers.txt не существует или недоступен.");
        }
        streamoff size = file.tellg();
        streamoff recordSize = sizeof(Voucher);
        if (size < 0 || size % recordSize != 0 || size / recordSize > INT_MAX) {
            throw runtime_error("Некорректный размер файла vouchers.txt.");
        }
        int newCount = static_cast<int>(size / recordSize);
        Voucher* next = new Voucher[newCount];
        file.seekg(0);
        for (int i = 0; i < newCount; i++) {
            file.read(reinterpret_cast<char*>(&next[i]), sizeof(Voucher));
        }
        if (!file) {
            delete[] next;
            throw runtime_error("Ошибка чтения vouchers.txt.");
        }
        delete[] data;
        data = next;
        count = newCount;
        cout << "Загружено записей: " << count << ".\n";
    }

    void readOne(int number) const {
        ifstream file("vouchers.txt", ios::binary);
        if (!file.is_open()) {
            throw runtime_error("Файл vouchers.txt не существует или недоступен.");
        }
        streamoff recordSize = sizeof(Voucher);
        file.seekg((number - 1) * recordSize);
        Voucher voucher;
        if (!file.read(reinterpret_cast<char*>(&voucher), sizeof(Voucher))) {
            throw runtime_error("Не удалось прочитать запись с таким номером.");
        }
        printVoucher(voucher);
    }

    void findSanatorium(string name) const {
        bool found = false;
        for (int i = 0; i < count; i++) {
            if (name == data[i].sanatorium) {
                cout << data[i].fullName << '\n';
                found = true;
            }
        }
        if (!found) {
            cout << "Сотрудники не найдены.\n";
        }
    }

    void findPeriod(string period) const {
        bool found = false;
        for (int i = 0; i < count; i++) {
            if (period == data[i].period) {
                cout << data[i].fullName << '\n';
                found = true;
            }
        }
        if (!found) {
            cout << "Сотрудники не найдены.\n";
        }
    }
};

int main() {
#ifdef _WIN32
    SetConsoleCP(CP_UTF8);
    SetConsoleOutputCP(CP_UTF8);
#endif

    try {
        VoucherList vouchers;
        while (true) {
            cout << "\n1. Последние K строк файла\n"
                 << "2. Символы файла без повторений\n"
                 << "3. Добавить путёвку\n"
                 << "4. Удалить запись из списка\n"
                 << "5. Вывести список\n"
                 << "6. Сохранить список в vouchers.txt\n"
                 << "7. Загрузить список из vouchers.txt\n"
                 << "8. Прочитать одну запись из vouchers.txt\n"
                 << "9. Найти сотрудников по санаторию\n"
                 << "10. Найти сотрудников по периоду\n"
                 << "0. Выход\n";
            int choice = readInt("Выбор: ", 0, 10);
            if (choice == 0) {
                return 0;
            }
            if (choice == 1 || choice == 2) {
                string name = readLine("Bvz файла: ");
                TextFile text(name);
                if (choice == 1) {
                    int k = readInt("K", 1, 9);
                    text.copyLastLines(k);
                } else {
                    text.uniqueCharacters();
                }
            } else if (choice == 3) {
                Voucher voucher{};
                readField("Ф.И.О.: ", voucher.fullName, sizeof(voucher.fullName));
                readField("Кафедра (группа, отдел): ", voucher.department, sizeof(voucher.department));
                voucher.number = readInt("Номер путёвки: ", 1, INT_MAX);
                readField("Период (ДД.ММ.ГГГГ-ДД.ММ.ГГГГ): ", voucher.period, sizeof(voucher.period));
                readField("Название санатория: ", voucher.sanatorium, sizeof(voucher.sanatorium));
                readField("Примечание (или -): ", voucher.note, sizeof(voucher.note));
                vouchers.add(voucher);
            } else if (choice == 4) {
                if (vouchers.getCount() == 0) {
                    cout << "Список пуст.\n";
                } else {
                    int number = readInt("Порядковый номер записи: ", 1, vouchers.getCount());
                    vouchers.remove(number);
                }
            } else if (choice == 5) {
                vouchers.printAll();
            } else if (choice == 6) {
                vouchers.save();
            } else if (choice == 7) {
                vouchers.load();
            } else if (choice == 8) {
                int number = readInt("Порядковый номер записи в файле: ", 1, INT_MAX);
                vouchers.readOne(number);
            } else if (choice == 9) {
                vouchers.findSanatorium(readLine("Название санатория: "));
            } else if (choice == 10) {
                vouchers.findPeriod(readLine("Период (ДД.ММ.ГГГГ-ДД.ММ.ГГГГ): "));
            }
        }
    } catch (const exception& error) {
        cerr << "Ошибка: " << error.what() << '\n';
        return 1;
    }
}
