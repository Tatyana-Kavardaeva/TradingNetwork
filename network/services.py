def get_company_level(supplier):
    """ Получает уровень компании в торговой сети. """

    if supplier is None:
        return 0
    elif supplier.company_level == 0:
        return 1
    return 2
