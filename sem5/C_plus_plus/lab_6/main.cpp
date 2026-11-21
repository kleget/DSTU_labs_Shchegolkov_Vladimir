#include <cstring>
#include <iostream>

#ifdef _WIN32
#include <windows.h>
#endif

class Patient {
private:
    char* diagnose;
    int age;
    static int objectCount;

    explicit Patient(int age) : diagnose(nullptr), age(age) {
        ++objectCount;
    }

    Patient(const Patient&) = delete;
    Patient& operator=(const Patient&) = delete;

    ~Patient() {
        clearDiagnosis();
        --objectCount;
    }

    void clearDiagnosis() {
        delete[] diagnose;
        diagnose = nullptr;
    }

public:
    void Diagnose(const char* text) {
        char* newDiagnosis = new char[std::strlen(text) + 1];
        std::strcpy(newDiagnosis, text);
        clearDiagnosis();
        diagnose = newDiagnosis;
    }

    void checkOut() {
        clearDiagnosis();
    }

    static int getObjectCount() {
        return objectCount;
    }

    static Patient* create(int age) {
        return new Patient(age);
    }

    static void destroy(Patient* patient) {
        delete patient;
    }

    static void demonstrateObjectCount();

    friend Patient* createPatient(int age);
    friend void destroyPatient(Patient* patient);
    friend void printPatient(const Patient& patient);
};

int Patient::objectCount = 0;

void printPatient(const Patient& patient) {
    std::cout << "Возраст: " << patient.age << ", диагноз: "
              << (patient.diagnose ? patient.diagnose : "нет") << '\n';
}

Patient* createPatient(int age) {
    return new Patient(age);
}

void destroyPatient(Patient* patient) {
    delete patient;
}

void Patient::demonstrateObjectCount() {
    Patient patients[] = {Patient(20), Patient(35)};
    std::cout << "После создания массива: " << getObjectCount() << '\n';
    printPatient(patients[0]);
    printPatient(patients[1]);

    Patient* patient = create(42);
    std::cout << "После создания объекта через статический метод: " << getObjectCount() << '\n';
    destroy(patient);
    std::cout << "После удаления объекта через статический метод: " << getObjectCount() << '\n';
}

int main() {
#ifdef _WIN32
    SetConsoleOutputCP(CP_UTF8);
#endif

    std::cout << "При входе в main: " << Patient::getObjectCount() << '\n';
    Patient::demonstrateObjectCount();
    std::cout << "После выхода из функции с массивом: " << Patient::getObjectCount() << '\n';

    Patient* patient = createPatient(30);
    std::cout << "\nПосле создания через дружественную функцию: "
              << Patient::getObjectCount() << '\n';
    patient->Diagnose("Грипп");
    printPatient(*patient);
    patient->Diagnose("Бронхит");
    printPatient(*patient);
    patient->checkOut();
    printPatient(*patient);

    destroyPatient(patient);
    std::cout << "После удаления через дружественную функцию: "
              << Patient::getObjectCount() << '\n';
}
