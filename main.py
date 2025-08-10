import csv
import re

def read_phonebook(path):
    with open(path, encoding="utf-8") as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    return contacts_list

def correct_name(contacts_list: list):
    contacts_list_new = []
    contacts_list_new.append(contacts_list[0])

    for row in contacts_list[1:]:
        try:
            name = ' '.join(row[:3]).split(' ')
            result = [name[0], name[1], name[2], row[3], row[4], row[5], row[6]]
            contacts_list_new.append(result)

        except IndexError:
            print("Индекс вне допустимого диапазона")

    return contacts_list_new

def correct_phone(contacts_list):
    pattern = r"(\+7|8)\s*\(*(\d{3})\)*[\s-]*(\d{3})[\s-]*(\d{2})[\s-]*(\d{2})(\s\(*(\w+.\s*\d+)\)*)*"

    def format_phone(m):
        phone = f"+7({m.group(2)}){m.group(3)}-{m.group(4)}-{m.group(5)}"
        if m.group(7):
            phone += f" {m.group(7)}"
        return phone
    
    for row in contacts_list:
        row[-2] = re.sub(pattern, format_phone, row[-2])

    return contacts_list

def union_duplicate(contacts_list):
    # for contact in contacts_list:
    #     first_name = contact[0]
    #     last_name = contact[1]

    #     for new_contact in contacts_list:
    #         new_first_name = new_contact[0]
    #         new_last_name = new_contact[1]
            
    #         if first_name == new_first_name and last_name == new_last_name:
    #             if contact[2] == "": contact[2] = new_contact[2]
    #             if contact[3] == "": contact[3] = new_contact[3]
    #             if contact[4] == "": contact[4] = new_contact[4]
    #             if contact[5] == "": contact[5] = new_contact[5]
    #             if contact[6] == "": contact[6] = new_contact[6]

    # result_list = []
    # for i in contacts_list:
    #     if i not in result_list:
    #         result_list.append(i)

    # то же, но экономит время

    contact_dict = {}

    for contact in contacts_list[1:]:
        key = (contact[0], contact[1])

        if key not in contact_dict:
            contact_dict[key] = contact

        else:
            existing = contact_dict[key]
            for i in range(2, 7):
                if not existing[i] and contact[i]:
                    existing[i] = contact[i]

    result_list = [contacts_list[0]] + list(contact_dict.values())

    return result_list

def write_phonebook(result_list):
    with open("phonebook.csv", "w", encoding="utf-8") as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(result_list)

if __name__ == '__main__':
    contacts_list = read_phonebook("phonebook_raw.csv")
    contacts_list_new = union_duplicate(correct_phone(correct_name(contacts_list)))
    write_phonebook(contacts_list_new)
