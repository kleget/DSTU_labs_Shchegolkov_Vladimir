#include <iostream>
#include <map>
#include <string>
#include <vector>

#ifdef _WIN32
#include <windows.h>
#endif

class Student {
private:
    std::string surname;
    bool needsDormitory;
    int experience;
    bool workedAsTeacher;
    std::string education;
    std::string language;

public:
    Student() : Student("", false, 0, false, "", "") {}

    Student(const std::string& surname, bool needsDormitory, int experience,
            bool workedAsTeacher, const std::string& education, const std::string& language)
        : surname(surname), needsDormitory(needsDormitory), experience(experience),
          workedAsTeacher(workedAsTeacher), education(education), language(language) {}

    Student(const Student& other) = default;

    const std::string& getSurname() const { return surname; }
    bool getNeedsDormitory() const { return needsDormitory; }
    int getExperience() const { return experience; }
    bool getWorkedAsTeacher() const { return workedAsTeacher; }
    const std::string& getEducation() const { return education; }
    const std::string& getLanguage() const { return language; }

    void setSurname(const std::string& value) { surname = value; }
    void setNeedsDormitory(bool value) { needsDormitory = value; }
    void setExperience(int value) { experience = value; }
    void setWorkedAsTeacher(bool value) { workedAsTeacher = value; }
    void setEducation(const std::string& value) { education = value; }
    void setLanguage(const std::string& value) { language = value; }

    void print() const {
        std::cout << surname << " | общежитие: " << (needsDormitory ? "да" : "нет")
                  << " | стаж учителем: " << experience
                  << " | работал учителем: " << (workedAsTeacher ? "да" : "нет")
                  << " | окончил: " << education << " | язык: " << language << '\n';
    }
};

bool readStudents(std::vector<Student>& students) {
    int count;
    std::cout << "Количество студентов: ";
    if (!(std::cin >> count) || count < 0) {
        return false;
    }

    for (int i = 0; i < count; ++i) {
        std::string surname, education, language;
        int needsDormitory, workedAsTeacher;
        int experience = 0;

        std::cout << "\nСтудент " << i + 1 << "\nФамилия: ";
        if (!std::getline(std::cin >> std::ws, surname)) {
            return false;
        }

        std::cout << "Нуждается в общежитии (1 — да, 0 — нет): ";
        if (!(std::cin >> needsDormitory) || (needsDormitory != 0 && needsDormitory != 1)) {
            return false;
        }

        std::cout << "Работал учителем (1 — да, 0 — нет): ";
        if (!(std::cin >> workedAsTeacher) || (workedAsTeacher != 0 && workedAsTeacher != 1)) {
            return false;
        }
        if (workedAsTeacher == 1) {
            std::cout << "Стаж работы учителем (полных лет): ";
            if (!(std::cin >> experience) || experience < 0) {
                return false;
            }
        }

        std::cout << "Что окончил (для педучилища введи «педучилище»): ";
        if (!std::getline(std::cin >> std::ws, education)) {
            return false;
        }
        std::cout << "Какой язык изучал: ";
        if (!std::getline(std::cin >> std::ws, language)) {
            return false;
        }

        const Student student(surname, needsDormitory == 1, experience,
                              workedAsTeacher == 1, education, language);
        students.push_back(student);
    }
    return true;
}

void printStudents(const std::vector<Student>& students) {
    std::cout << "\nВсе студенты:\n";
    if (students.empty()) {
        std::cout << "Список пуст.\n";
    }
    for (const Student& student : students) {
        student.print();
    }
}

int countDormitoryApplicants(const std::vector<Student>& students) {
    int count = 0;
    for (const Student& student : students) {
        if (student.getNeedsDormitory()) {
            ++count;
        }
    }
    return count;
}

void printTeachers(const std::vector<Student>& students) {
    std::cout << "\nРаботали учителем 2 года и более:\n";
    bool found = false;
    for (const Student& student : students) {
        if (student.getWorkedAsTeacher() && student.getExperience() >= 2) {
            std::cout << "  " << student.getSurname() << '\n';
            found = true;
        }
    }
    if (!found) {
        std::cout << "  Нет таких студентов.\n";
    }
}

void printTeachingSchoolGraduates(const std::vector<Student>& students) {
    std::cout << "\nОкончили педучилище:\n";
    bool found = false;
    for (const Student& student : students) {
        if (student.getEducation() == "педучилище") {
            std::cout << "  " << student.getSurname() << '\n';
            found = true;
        }
    }
    if (!found) {
        std::cout << "  Нет таких студентов.\n";
    }
}

void printLanguageGroups(const std::vector<Student>& students) {
    std::map<std::string, std::vector<std::string>> groups;
    for (const Student& student : students) {
        groups[student.getLanguage()].push_back(student.getSurname());
    }

    std::cout << "\nЯзыковые группы:\n";
    if (groups.empty()) {
        std::cout << "  Нет групп.\n";
    }
    for (const auto& group : groups) {
        std::cout << group.first << ":\n";
        for (const std::string& surname : group.second) {
            std::cout << "  " << surname << '\n';
        }
    }
}

int main() {
#ifdef _WIN32
    SetConsoleCP(CP_UTF8);
    SetConsoleOutputCP(CP_UTF8);
#endif

    std::vector<Student> students;
    if (!readStudents(students)) {
        std::cerr << "Ошибка ввода.\n";
        return 1;
    }

    printStudents(students);
    std::cout << "\nНуждаются в общежитии: " << countDormitoryApplicants(students) << '\n';
    printTeachers(students);
    printTeachingSchoolGraduates(students);
    printLanguageGroups(students);
}
