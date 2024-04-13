import application.salary as salary
import application.db.people as people
from datetime import datetime

if __name__ == '__main__':
    print(salary.calculate_salary())
    print(people.get_employees())
    print(datetime.today())
