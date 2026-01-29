from typing import List, Optional

from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field


class BalanceHeadTable(BaseModel):
    organization: Optional[str] = Field(None, alias="Организация", description="Название организации")
    taxpayer_id: Optional[int] = Field(None, alias="Учетный номер плательщика", description="Учетный номер плательщика")
    economic_activity: Optional[str] = Field(
        None,
        alias="Вид экономической деятельности",
        description="Вид экономической деятельности",
    )
    legal_form: Optional[str] = Field(
        None,
        alias="Организационно-правовая форма",
        description="Организационно-правовая форма",
    )
    governing_body: Optional[str] = Field(None, alias="Орган управления", description="Орган управления")
    unit: Optional[str] = Field(None, alias="Единица измерения", description="Единица измерения")
    address: Optional[str] = Field(None, alias="Адрес", description="Адрес")


class BalanceDatesTable(BaseModel):
    approval_date: Optional[str] = Field(
        None,
        alias="Дата утверждения",
        description="Дата утверждения в формате ДД.ММ.ГГГГ",
    )
    submission_date: Optional[str] = Field(None, alias="Дата отправки", description="Дата отправки в формате ДД.ММ.ГГГГ")
    acceptance_date: Optional[str] = Field(None, alias="Дата принятия", description="Дата принятия в формате ДД.ММ.ГГГГ")


class BalanceMainTable(BaseModel):
    code_110: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="110",
        description="Основные средства",
        min_length=2,
        max_length=2,
    )
    code_120: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="120",
        description="Нематериальные активы",
        min_length=2,
        max_length=2,
    )
    code_130: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="130",
        description="Доходные вложения в материальные активы",
        min_length=2,
        max_length=2,
    )
    code_131: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="131",
        description="Инвестиционная недвижимость",
        min_length=2,
        max_length=2,
    )
    code_132: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="132",
        description="Предметы финансовой аренды (лизинга)",
        min_length=2,
        max_length=2,
    )
    code_133: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="133",
        description="Прочие доходные вложения в материальные активы",
        min_length=2,
        max_length=2,
    )
    code_140: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="140",
        description="Вложения в долгосрочные активы",
        min_length=2,
        max_length=2,
    )
    code_150: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="150",
        description="Долгосрочные финансовые вложения",
        min_length=2,
        max_length=2,
    )
    code_160: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="160",
        description="Отложенные налоговые активы",
        min_length=2,
        max_length=2,
    )
    code_170: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="170",
        description="Долгосрочная дебиторская задолженность",
        min_length=2,
        max_length=2,
    )
    code_180: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="180",
        description="Прочие долгосрочные активы",
        min_length=2,
        max_length=2,
    )
    code_190: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="190",
        description="Итого по разделу I",
        min_length=2,
        max_length=2,
    )
    code_210: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="210",
        description="Запасы",
        min_length=2,
        max_length=2,
    )
    code_211: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="211",
        description="Материалы",
        min_length=2,
        max_length=2,
    )
    code_212: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="212",
        description="Животные на выращивании и откорме",
        min_length=2,
        max_length=2,
    )
    code_213: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="213",
        description="Незавершенное производство",
        min_length=2,
        max_length=2,
    )
    code_214: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="214",
        description="Готовая продукция и товары",
        min_length=2,
        max_length=2,
    )
    code_215: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="215",
        description="Товары отгруженные",
        min_length=2,
        max_length=2,
    )
    code_216: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="216",
        description="Прочие запасы",
        min_length=2,
        max_length=2,
    )
    code_220: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="220",
        description="Долгосрочные активы, предназначенные для реализации",
        min_length=2,
        max_length=2,
    )
    code_230: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="230",
        description="Расходы будущих периодов",
        min_length=2,
        max_length=2,
    )
    code_240: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="240",
        description="Налог на добавленную стоимость по приобретенным товарам, работам, услугам",
        min_length=2,
        max_length=2,
    )
    code_250: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="250",
        description="Краткосрочная дебиторская задолженность",
        min_length=2,
        max_length=2,
    )
    code_260: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="260",
        description="Краткосрочные финансовые вложения",
        min_length=2,
        max_length=2,
    )
    code_270: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="270",
        description="Денежные средства и эквиваленты денежных средств",
        min_length=2,
        max_length=2,
    )
    code_280: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="280",
        description="Прочие краткосрочные активы",
        min_length=2,
        max_length=2,
    )
    code_290: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="290",
        description="Итого по разделу II",
        min_length=2,
        max_length=2,
    )
    code_300: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="300",
        description="Баланс",
        min_length=2,
        max_length=2,
    )
    code_410: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="410",
        description="Уставный капитал",
        min_length=2,
        max_length=2,
    )
    code_420: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="420",
        description="Неоплаченная часть уставного капитала",
        min_length=2,
        max_length=2,
    )
    code_430: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="430",
        description="Собственные акции (доли в уставном капитале)",
        min_length=2,
        max_length=2,
    )
    code_440: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="440",
        description="Резервный капитал",
        min_length=2,
        max_length=2,
    )
    code_450: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="450",
        description="Добавочный капитал",
        min_length=2,
        max_length=2,
    )
    code_460: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="460",
        description="Нераспределенная прибыль (непокрытый убыток)",
        min_length=2,
        max_length=2,
    )
    code_470: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="470",
        description="Чистая прибыль (убыток) отчетного периода",
        min_length=2,
        max_length=2,
    )
    code_480: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="480",
        description="Целевое финансирование",
        min_length=2,
        max_length=2,
    )
    code_490: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="490",
        description="Итого по разделу III",
        min_length=2,
        max_length=2,
    )
    code_510: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="510",
        description="Долгосрочные кредиты и займы",
        min_length=2,
        max_length=2,
    )
    code_520: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="520",
        description="Долгосрочные обязательства по лизинговым платежам",
        min_length=2,
        max_length=2,
    )
    code_530: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="530",
        description="Отложенные налоговые обязательства",
        min_length=2,
        max_length=2,
    )
    code_540: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="540",
        description="Доходы будущих периодов",
        min_length=2,
        max_length=2,
    )
    code_550: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="550",
        description="Резервы предстоящих платежей",
        min_length=2,
        max_length=2,
    )
    code_560: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="560",
        description="Прочие долгосрочные обязательства",
        min_length=2,
        max_length=2,
    )
    code_590: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="590",
        description="Итого по разделу IV",
        min_length=2,
        max_length=2,
    )
    code_610: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="610",
        description="Краткосрочные кредиты и займы",
        min_length=2,
        max_length=2,
    )
    code_620: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="620",
        description="Краткосрочная часть долгосрочных обязательств",
        min_length=2,
        max_length=2,
    )
    code_630: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="630",
        description="Краткосрочная кредиторская задолженность",
        min_length=2,
        max_length=2,
    )
    code_631: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="631",
        description="Поставщикам, подрядчикам, исполнителям",
        min_length=2,
        max_length=2,
    )
    code_632: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="632",
        description="По авансам полученным",
        min_length=2,
        max_length=2,
    )
    code_633: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="633",
        description="По налогам и сборам",
        min_length=2,
        max_length=2,
    )
    code_634: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="634",
        description="По социальному страхованию и обеспечению",
        min_length=2,
        max_length=2,
    )
    code_635: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="635",
        description="По оплате труда",
        min_length=2,
        max_length=2,
    )
    code_636: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="636",
        description="По лизинговым платежам",
        min_length=2,
        max_length=2,
    )
    code_637: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="637",
        description="Собственнику имущества (учредителям, участникам)",
        min_length=2,
        max_length=2,
    )
    code_638: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="638",
        description="Прочим кредиторам",
        min_length=2,
        max_length=2,
    )
    code_640: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="640",
        description="Обязательства, предназначенные для реализации",
        min_length=2,
        max_length=2,
    )
    code_650: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="650",
        description="Доходы будущих периодов",
        min_length=2,
        max_length=2,
    )
    code_660: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="660",
        description="Резервы предстоящих платежей",
        min_length=2,
        max_length=2,
    )
    code_670: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="670",
        description="Прочие краткосрочные обязательства",
        min_length=2,
        max_length=2,
    )
    code_690: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="690",
        description="Итого по разделу V",
        min_length=2,
        max_length=2,
    )
    code_700: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="700",
        description="Баланс",
        min_length=2,
        max_length=2,
    )


class ReportMainTable(BaseModel):
    code_010: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="010",
        description="Выручка от реализации продукции, товаров, работ, услуг",
        min_length=2,
        max_length=2,
    )
    code_020: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="020",
        description="Себестоимость реализованной продукции, товаров, работ, услуг",
        min_length=2,
        max_length=2,
    )
    code_030: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="030",
        description="Валовая прибыль",
        min_length=2,
        max_length=2,
    )
    code_040: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="040",
        description="Управленческие расходы",
        min_length=2,
        max_length=2,
    )
    code_050: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="050",
        description="Расходы на реализацию",
        min_length=2,
        max_length=2,
    )
    code_060: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="060",
        description="Прибыль (убыток) от реализации продукции, товаров, работ, услуг",
        min_length=2,
        max_length=2,
    )
    code_070: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="070",
        description="Прочие доходы по текущей деятельности",
        min_length=2,
        max_length=2,
    )
    code_080: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="080",
        description="Прочие расходы по текущей деятельности",
        min_length=2,
        max_length=2,
    )
    code_090: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="090",
        description="Прибыль (убыток) от текущей деятельности",
        min_length=2,
        max_length=2,
    )
    code_100: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="100",
        description="Доходы по инвестиционной деятельности",
        min_length=2,
        max_length=2,
    )
    code_101: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="101",
        description="Доходы от выбытия основных средств, нематериальных активов и других долгосрочных активов",
        min_length=2,
        max_length=2,
    )
    code_102: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="102",
        description="Доходы от участия в уставном капитале других организаций",
        min_length=2,
        max_length=2,
    )
    code_103: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="103",
        description="Проценты к получению",
        min_length=2,
        max_length=2,
    )
    code_104: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="104",
        description="Прочие доходы по инвестиционной деятельности",
        min_length=2,
        max_length=2,
    )
    code_110: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="110",
        description="Расходы по инвестиционной деятельности",
        min_length=2,
        max_length=2,
    )
    code_111: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="111",
        description="Расходы от выбытия основных средств, нематериальных активов и других долгосрочных активов",
        min_length=2,
        max_length=2,
    )
    code_112: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="112",
        description="Прочие расходы по инвестиционной деятельности",
        min_length=2,
        max_length=2,
    )
    code_120: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="120",
        description="Доходы по финансовой деятельности",
        min_length=2,
        max_length=2,
    )
    code_121: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="121",
        description="Курсовые разницы от пересчета активов и обязательств",
        min_length=2,
        max_length=2,
    )
    code_122: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="122",
        description="Прочие доходы по финансовой деятельности",
        min_length=2,
        max_length=2,
    )
    code_130: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="130",
        description="Расходы по финансовой деятельности",
        min_length=2,
        max_length=2,
    )
    code_131: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="131",
        description="Проценты к уплате",
        min_length=2,
        max_length=2,
    )
    code_132: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="132",
        description="Курсовые разницы от пересчета активов и обязательств",
        min_length=2,
        max_length=2,
    )
    code_133: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="133",
        description="Прочие расходы по финансовой деятельности",
        min_length=2,
        max_length=2,
    )
    code_140: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="140",
        description="Прибыль (убыток) от инвестиционной и финансовой деятельности",
        min_length=2,
        max_length=2,
    )
    code_150: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="150",
        description="Прибыль (убыток) до налогообложения",
        min_length=2,
        max_length=2,
    )
    code_160: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="160",
        description="Налог на прибыль",
        min_length=2,
        max_length=2,
    )
    code_170: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="170",
        description="Изменение отложенных налоговых активов",
        min_length=2,
        max_length=2,
    )
    code_180: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="180",
        description="Изменение отложенных налоговых обязательств",
        min_length=2,
        max_length=2,
    )
    code_190: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="190",
        description="Прочие налоги и сборы, исчисляемые из прибыли (дохода)",
        min_length=2,
        max_length=2,
    )
    code_200: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="200",
        description="Прочие платежи, исчисляемые из прибыли (дохода)",
        min_length=2,
        max_length=2,
    )
    code_210: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="210",
        description="Чистая прибыль (убыток)",
        min_length=2,
        max_length=2,
    )
    code_220: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="220",
        description="Результат от переоценки долгосрочных активов, не включаемый в чистую прибыль (убыток)",
        min_length=2,
        max_length=2,
    )
    code_230: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="230",
        description="Результат от прочих операций, не включаемый в чистую прибыль (убыток)",
        min_length=2,
        max_length=2,
    )
    code_240: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="240",
        description="Совокупная прибыль (убыток)",
        min_length=2,
        max_length=2,
    )
    code_250: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="250",
        description="Базовая прибыль (убыток) на акцию",
        min_length=2,
        max_length=2,
    )
    code_260: List[Optional[int]] = Field(
        default_factory=lambda: [None, None],
        alias="260",
        description="Разводненная прибыль (убыток) на акцию",
        min_length=2,
        max_length=2,
    )


class TablesData(BaseModel):
    balance_head_table: BalanceHeadTable
    balance_dates_table: BalanceDatesTable
    balance_main_table_dates: List[Optional[str]] = Field(
        ...,
        description="Даты, соответствующие двум столбцам основной таблицы баланса в формате ДД.ММ.ГГГГ",
    )
    balance_main_table: BalanceMainTable
    report_main_table: ReportMainTable


class ParsedPDF(BaseModel):
    tables_data: TablesData


output_parser = PydanticOutputParser(pydantic_object=ParsedPDF)
format_instructions = output_parser.get_format_instructions()
