import project as p


def test_get_year_path():
    assert p.get_year_path(2022) == "data/2022"
    

def test_get_month_path():
    assert p.get_month_path("data/2022", 11) == "data/2022/11.csv"


def test_get_month_data():
    assert p.get_month_data("data/2022/11.csv")[0] == ["id", "Day", "Description", "Amount"]
    assert isinstance(p.get_month_data("data/2022/11.csv")[1], list) == True
    assert isinstance(p.get_month_data("data/2022/11.csv")[2], float) == True


def test_validate_menu_input():
    assert p.validate_menu_input("abc") == None
    assert p.validate_menu_input(7) == None
    assert p.validate_menu_input(0) == None
    assert p.validate_menu_input(1) == p.MENU[0]["value"]
    assert p.validate_menu_input(2) == p.MENU[1]["value"]
    assert p.validate_menu_input(3) == p.MENU[2]["value"]
    assert p.validate_menu_input(4) == p.MENU[3]["value"]


def test_next_month():
    assert p.next_month(2022, 11) == (2022, 12)
    assert p.next_month(2022, 12) == (2023, 1)


def test_prev_month():
    assert p.prev_month(2022, 1) == (2021, 12)
    assert p.prev_month(2022, 11) == (2022, 10)


def test_get_transaction_type():
    assert p.get_transaction_type(test_input="out")[0] == "out"
    assert p.get_transaction_type(test_input="in")[0] == "in"
    assert p.get_transaction_type(test_input="cancel")[0] == "cancel"


def test_get_day():
    assert p.get_day(2022, 11, "green", test_input="30") == "30"
    assert p.get_day(2022, 11, "green", test_input="32") == None
    assert p.get_day(2022, 11, "green", test_input="cancel") == "cancel"


def test_is_day_valid():
    assert p.is_day_valid(2022, 11, "30") == True
    assert p.is_day_valid(2022, 11, "32") == False
    assert p.is_day_valid(2022, 11, "abc") == False


def test_get_amount():
    assert p.get_amount("in", "green", test_input="20,00") == None
    assert p.get_amount("in", "green", test_input="abc") == None
    assert p.get_amount("in", "green", test_input="20") == "20.00"
    assert p.get_amount("out", "green", test_input="20") == "-20.00"
    assert p.get_amount("in", "green", test_input="cancel") == "cancel"


def test_delete_transaction():
    assert p.delete_transaction("abc", "data/2022/11.csv") == False
    assert p.delete_transaction(0, "nopath") == False