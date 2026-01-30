"""
Pydantic-модели для извлечения данных из официальных обращений.
"""

from typing import List, Optional

from pydantic import BaseModel, Field


class Fizik(BaseModel):
    fullName: Optional[str] = Field(default=None, description="ФИО физического лица")
    identificationNumber: Optional[str] = Field(
        default=None,
        description="Идентификационный номер паспорта",
    )
    seriesNumber: Optional[str] = Field(default=None, description="Серия и номер паспорта")
    government: Optional[str] = Field(
        default=None,
        description="Орган, выдавший документ",
    )
    dateIssue: Optional[str] = Field(default=None, description="Дата выдачи документа")
    registrationAddress: Optional[str] = Field(
        default=None,
        description="Адрес регистрации клиента",
    )
    dateBirth: Optional[str] = Field(default=None, description="Дата рождения")
    mobileNumber: Optional[str] = Field(default=None, description="Мобильный номер телефона")


class Urik(BaseModel):
    nameOrganization: Optional[str] = Field(
        default=None,
        description="Наименование юридического лица или ИП",
    )
    unp: Optional[str] = Field(default=None, description="УНП")


class Bills(BaseModel):
    infoBills: Optional[str] = Field(
        default=None,
        description="Информация об открытии/закрытии/состоянии счетов, выписки и т.д.",
    )
    accountNumber: Optional[str] = Field(
        default=None,
        description="Номер счета без разделителей",
    )
    currency: Optional[str] = Field(default=None, description="Валюта счета: числовой код")
    accountType: Optional[str] = Field(default=None, description="Тип счета: текущий, депозитный, валютный и т.д.")
    close: Optional[str] = Field(default=None, description="Формулировки по закрытию счетов")
    openingDate: Optional[str] = Field(default=None, description="Дата открытия счета")
    closingDate: Optional[str] = Field(default=None, description="Дата закрытия счета")
    answerBills: Optional[str] = Field(default=None, description="Формулировки о подготовке/направлении ответа")


class Transactions(BaseModel):
    vypiska: Optional[str] = Field(default=None, description="Запрос выписок по счетам/картам, движение средств")
    pp: Optional[str] = Field(
        default=None,
        description="Платежные поручения, приходные/расходные ордера и др.",
    )
    transactionAmount: Optional[str] = Field(default=None, description="Сумма транзакции")
    dateOperation: Optional[str] = Field(default=None, description="Дата операции")
    timeOperation: Optional[str] = Field(default=None, description="Время операции")
    zp_spisok: Optional[str] = Field(default=None, description="Списки к платежным поручениям, в т.ч. на зарплату")
    docs: Optional[str] = Field(
        default=None,
        description="Иные документы: заявления, справки, списки выплат и т.д.",
    )


class Cards(BaseModel):
    cardNumber: Optional[str] = Field(default=None, description="Полный номер карты")
    maskCards: Optional[str] = Field(default=None, description="Первые 6 и последние 4 цифры карты")
    getDate: Optional[str] = Field(default=None, description="Дата выдачи карты")
    expDate: Optional[str] = Field(default=None, description="Срок действия карты")
    paymentSystem: Optional[str] = Field(default=None, description="Платежная система (Visa, Mastercard и т.д.)")
    blockDate: Optional[str] = Field(default=None, description="Дата блокировки карты")
    blockTime: Optional[str] = Field(default=None, description="Время блокировки карты")
    unblockDate: Optional[str] = Field(default=None, description="Дата разблокировки карты")
    unblockTime: Optional[str] = Field(default=None, description="Время разблокировки карты")
    pravoBPK: Optional[str] = Field(
        default=None,
        description="Лица, уполномоченные на получение/снятие средств с карты",
    )
    infoCard: Optional[str] = Field(default=None, description="Общие данные о картах (БПК)")


class Credits(BaseModel):
    dogovorCr: Optional[str] = Field(default=None, description="Наличие договора кредита")
    dogovorLiz: Optional[str] = Field(default=None, description="Наличие договора лизинга")
    dogovorSsuda: Optional[str] = Field(default=None, description="Наличие договора ссуды")
    dogovorVek: Optional[str] = Field(default=None, description="Договорные обязательства по векселям/чекам")
    nomerDogCr: Optional[str] = Field(default=None, description="Номер кредитного договора")
    dateDogCr: Optional[str] = Field(default=None, description="Дата кредитного договора")
    currencyCr: Optional[str] = Field(default=None, description="Валюта кредитного договора")
    dogovorSumma: Optional[str] = Field(default=None, description="Сумма или лимит кредитной линии")
    zalog: Optional[str] = Field(default=None, description="Информация о залоговом имуществе")
    infoCr: Optional[str] = Field(default=None, description="Условия кредитных линий")
    typeCr: Optional[str] = Field(default=None, description="Вид кредита")
    percent: Optional[str] = Field(default=None, description="Процентная ставка")
    graficCr: Optional[str] = Field(default=None, description="График возврата кредита")
    periodCr: Optional[str] = Field(default=None, description="Срок погашения кредита или запрашиваемый период")
    anketaClient: Optional[str] = Field(
        default=None,
        description="Документы при получении кредита (анкеты, балансы и др.)",
    )
    accountCr: Optional[str] = Field(default=None, description="Счета, открытые по кредиту")
    ostatokCr: Optional[str] = Field(default=None, description="Остаток задолженности на дату")
    oborotCr: Optional[str] = Field(default=None, description="Обороты по счетам за период")
    oplataCr: Optional[str] = Field(default=None, description="Полученные суммы по основному долгу и процентам")
    vyborkaCr: Optional[str] = Field(default=None, description="Суммы по основному долгу")
    prosrCr: Optional[str] = Field(default=None, description="Сумма просроченной задолженности")
    poruchitelCr: Optional[str] = Field(default=None, description="Информация о поручительствах и гарантиях")
    covenantyCr: Optional[str] = Field(default=None, description="Невыполнение финансовых ковенантов")
    inoeCr: Optional[str] = Field(default=None, description="Прочие кредитные обязательства")


class Garantii(BaseModel):
    itogSummGar: Optional[str] = Field(default=None, description="Сумма по гарантиям и аккредитивам")
    benGar: Optional[str] = Field(default=None, description="Бенефициар по гарантиям")
    sumPokrGar: Optional[str] = Field(default=None, description="Сумма покрытия")
    dateBank: Optional[str] = Field(default=None, description="Даты оплат банком")
    summBank: Optional[str] = Field(default=None, description="Суммы, оплаченные банком")
    dateGasitGar: Optional[str] = Field(default=None, description="Даты платежей по погашению")
    summGasitGar: Optional[str] = Field(default=None, description="Суммы платежей по погашению")
    uslREPO: Optional[str] = Field(default=None, description="Условия сделок РЕПО")


class Deposit(BaseModel):
    depDogovor: Optional[str] = Field(default=None, description="Наличие депозитов")
    dogNumberDep: Optional[str] = Field(default=None, description="Номер депозитного договора")
    dogDateDep: Optional[str] = Field(default=None, description="Дата депозитного договора")
    currencyDep: Optional[str] = Field(default=None, description="Валюта депозита")
    percentDep: Optional[str] = Field(default=None, description="Процентная ставка по депозиту")
    srokDep: Optional[str] = Field(default=None, description="Срок размещения депозита")
    summDep: Optional[str] = Field(default=None, description="Сумма депозита")
    summPercentNachisl: Optional[str] = Field(default=None, description="Сумма начисленных процентов")
    summPercentPoluch: Optional[str] = Field(default=None, description="Сумма выплаченных процентов")
    typeDep: Optional[str] = Field(
        default=None,
        description="Вид депозита: отзывный, безотзывный, до востребования и т.д.",
    )


class AIS(BaseModel):
    infoAIS: Optional[str] = Field(default=None, description="Сведения о наличии картотеки, к внебалансовым счетам")
    summAIS: Optional[str] = Field(default=None, description="Сумма обязательств в АИС ИДО")
    ammountAIS: Optional[str] = Field(default=None, description="Количество обязательств в АИС ИДО")
    ppDateAIS: Optional[str] = Field(default=None, description="Дата платежной инструкции")
    ppTimeAIS: Optional[str] = Field(default=None, description="Время платежной инструкции")
    ppNumberAIS: Optional[str] = Field(default=None, description="Номер платежной инструкции")
    ptDateAIS: Optional[str] = Field(default=None, description="Дата платежного требования")
    ptSummAIS: Optional[str] = Field(default=None, description="Сумма платежного требования")
    datevAIS: Optional[str] = Field(default=None, description="Дата направления в АИС ИДО")
    timevAIS: Optional[str] = Field(default=None, description="Время направления в АИС ИДО")


class Arest(BaseModel):
    infoOgranich: Optional[str] = Field(default=None, description="Информация о текущих обременениях")
    organArest: Optional[str] = Field(default=None, description="Органы, наложившие арест/ограничение")
    periodArest: Optional[str] = Field(default=None, description="Период блокировки счетов")
    reasonArest: Optional[str] = Field(default=None, description="Причины блокировки")
    infoArest: Optional[str] = Field(default=None, description="Сведения об арестах по счетам")
    infoStop: Optional[str] = Field(default=None, description="Сведения о приостановлениях операций")


class SDBO(BaseModel):
    registrationSDBO: Optional[str] = Field(default=None, description="Регистрация в СДБО (Интернет-/М-Банкинг)")
    ip: Optional[str] = Field(default=None, description="IP-адреса для входа/регистрации")
    polzovateliSDBO: Optional[str] = Field(default=None, description="Пользователи СДБО и их права подписи")
    vhodSDBO: Optional[str] = Field(default=None, description="История входов в СДБО")
    infoSDBO: Optional[str] = Field(default=None, description="Прочая информация по СДБО")


class CustomerInformation(BaseModel):
    infoClient: Optional[str] = Field(default=None, description="Обслуживается ли ФЛ в банке, является ли клиентом")
    adressClient: Optional[str] = Field(default=None, description="Адрес регистрации/проживания клиента")
    nomerClient: Optional[str] = Field(default=None, description="Абонентские номера клиента")
    mailClient: Optional[str] = Field(default=None, description="Электронные почтовые адреса клиента")
    zaimClient: Optional[str] = Field(default=None, description="Информация о займах и выплатах")


class OfficialRequestModel(BaseModel):
    sender: Optional[str] = Field(
        default=None,
        description="Отправитель запроса",
    )
    dateNumber: Optional[str] = Field(
        default=None,
        description="Дата и номер документа (пример: 11.01.2024 №22/14-3345)",
    )
    title: Optional[str] = Field(
        default=None,
        description="Тема запроса — заголовок (пример: О предоставлении информации)",
    )
    deadline: Optional[str] = Field(
        default=None,
        description="Срок ответа (пример: в трехдневный срок со дня получения)",
    )
    auditorName: Optional[str] = Field(
        default=None,
        description="Наименование получателя: аудитор, антикризисный управляющий и т.д.",
    )
    email: Optional[str] = Field(default=None, description="Адрес электронной почты для направления ответа")
    period: Optional[str] = Field(default=None, description="Период, за который запрашивается информация")
    requestType: Optional[str] = Field(default=None, description="Тип запроса — распознанная суть запроса")
    adress: Optional[str] = Field(default=None, description="Адрес (если указан отдельно в теле запроса)")
    adress_sender: Optional[str] = Field(default=None, description="Адрес отправителя (часто в шапке письма)")
    podpisant: Optional[str] = Field(default=None, description="ФИО подписавшего лица")
    law: Optional[str] = Field(
        default=None,
        description="Наличие ссылки на ст. 106 Закона №227-З: 'ссылка на ст.106 есть' / 'ссылки на ст.106 нет'",
    )
    fizik: List[Fizik] = Field(default_factory=list, description="Список физических лиц, упомянутых в запросе")
    urik: List[Urik] = Field(
        default_factory=list,
        description="Список юридических лиц или ИП, упомянутых в запросе",
    )
    bills: Bills = Field(default_factory=Bills, description="Информация о банковских счетах")
    transactions: Transactions = Field(default_factory=Transactions, description="Информация о транзакциях")
    leftovers: Optional[str] = Field(default=None, description="Сведения об остатках денежных средств на дату")
    cards: Cards = Field(default_factory=Cards, description="Информация о банковских картах")
    credit: Credits = Field(default_factory=Credits, description="Информация о кредитах, лизинге, займах")
    garantii: Garantii = Field(default_factory=Garantii, description="Информация о гарантиях и аккредитивах")
    deposit: Deposit = Field(default_factory=Deposit, description="Информация о депозитах")
    informationSecurities: Optional[str] = Field(default=None, description="Наличие ценных бумаг")
    informationMetals: Optional[str] = Field(default=None, description="Наличие драгоценных металлов на хранении")
    informationOwn: Optional[str] = Field(
        default=None,
        description="Иное имущество на хранении, сейфы, доверительное управление",
    )
    informationWallet: Optional[str] = Field(default=None, description="Наличие электронного кошелька")
    inoe: Optional[str] = Field(
        default=None,
        description="Производные финансовые инструменты: фьючерсы, форварды",
    )
    broni: Optional[str] = Field(default=None, description="Сведения о бронировании средств")
    ais: AIS = Field(default_factory=AIS, description="Информация по АИС ИДО")
    arest: Arest = Field(default_factory=Arest, description="Информация об арестах и ограничениях")
    sdbo: SDBO = Field(default_factory=SDBO, description="Информация по СДБО")
    customerInformation: CustomerInformation = Field(default_factory=CustomerInformation, description="Общая информация о клиенте")
    videoInformation: Optional[str] = Field(default=None, description="Информация о видео")
    informationErip: Optional[str] = Field(default=None, description="Информация о чеках ЕРИП")
    other: Optional[str] = Field(default=None, description="Прочая информация, не попавшая в другие категории")
    sud: Optional[str] = Field(
        default=None,
        description="Информация об определении суда: орган, должник, назначение управляющего",
    )
    doverennost: Optional[str] = Field(default=None, description="Информация о доверенности и полномочиях")
    closeForm: Optional[str] = Field(
        default=None,
        description="Наличие заявления на закрытие счета и формулировки по закрытию",
    )
