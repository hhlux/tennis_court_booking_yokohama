from pages.login_page import LoginPage
from pages.park_selection_page import ParkSelectionPage
from pages.vacancy_by_court_page import VacancyByCourtPage
from pages.vacancy_by_time_slot_page import VacancyByTimeSlotPage
from utils.mail_util import MailUtil

if __name__ == '__main__':

    parks = [('入船公園', 4), ('潮田公園', 3)]

    results = {}

    for park in parks:
        LoginPage().login()
        print(park[0])

        ParkSelectionPage().go_to_park(park[0])

        vacancy_by_court_page = VacancyByCourtPage()

        # days_count = vacancy_by_court_page.select_one_month()
        days_count = 7

        result = []

        # 按天数遍历，每一天为一列，也即遍历列（日期是从第3列开始）
        for i in range(3, 3 + days_count):
            vacancy_by_court_page = VacancyByCourtPage()

            vacancy_by_court_page.clear_selected()

            date = vacancy_by_court_page.get_date(i)

            is_any_court_vacant = vacancy_by_court_page.click_next_if_any_court_is_vacant_by_date(i, park[1])


            if is_any_court_vacant:

                vacancy_by_time_slot_page = VacancyByTimeSlotPage()

                if vacancy_by_time_slot_page.is_last_time_slot_vacant_for_any_count():
                    result.append(date)

                vacancy_by_time_slot_page.return_page()

        print(result)

        if result:
            results[park[0]] = result

    print(results)

    if results:
        MailUtil.send('鹤见球场 19:00-21:00 空缺', str(results))
        print('通知邮件已发送')
