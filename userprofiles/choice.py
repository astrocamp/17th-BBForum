from django.db import models


class Gender(models.TextChoices):
    Female = "F", "女"
    Men = "M", "男"


class Education_level(models.TextChoices):
    MIDDLE_SCHOOL_OR_BELOW = "MS", "中學以下"
    HIGH_SCHOOL = "HS", "高中、高職"
    JUNIOR_COLLEGE = "JC", "專科"
    UNIVERSITY = "U", "大學"
    POST_GRADUATE = "PG", "研究所以上"


Profession= [
        ('investor', '專職投資人'),
        ('finance_insurance', '金融保險'),
        ('electronics_manufacturing', '電子製造'),
        ('traditional_manufacturing', '傳統製造'),
        ('internet_software', '網際網路/資訊軟體'),
        ('food_retail', '餐飲/百貨/零售'),
        ('media_publishing', '媒體/出版'),
        ('real_estate_construction', '不動產/建築/營造'),
        ('healthcare', '醫療'),
        ('education_research', '教育/研究'),
        ('government_employee', '公務人員'),
        ('agriculture_fisheries', '農漁牧'),
        ('homemaker', '家管'),
        ('student', '學生'),
        ('other', '其他'),
    ]


class Inves_attributes(models.TextChoices):
    proactive = "P", "積極(短線交易)"
    stable = "S", "穩健(波段操作)"
    conservative = "C", "保守(長期持有)"


Investment_experience_choices = [
    ("0-1", "0-1年"),
    ("1-3", "1-3年"),
    ("3-5", "3-5年"),
    ("5-10", "5年-10年"),
    ("10-20", "10年-20年"),
    ("20-30", "20年-30年"),
    ("30-50", "30年-50年"),
]

Investment_tools = [
    ("stock", "股票"),
    ("fund", "基金"),
    ("futures", "期貨"),
    ("options", "選擇權"),
    ("forex", "外匯"),
    ("gold", "黃金"),
    ("time_deposit", "定存"),
    ("real_estate", "不動產"),
]

Taiwan_regions = [
    ("TP", "台北市"),
    ("NTPC", "新北市"),
    ("TPE", "台中市"),
    ("TN", "台南市"),
    ("KH", "高雄市"),
    ("KHH", "基隆市"),
    ("TYC", "桃園市"),
    ("HCC", "新竹市"),
    ("HSC", "新竹縣"),
    ("MIA", "苗栗縣"),
    ("CHW", "彰化縣"),
    ("NTO", "南投縣"),
    ("YUN", "雲林縣"),
    ("CYI", "嘉義市"),
    ("CYC", "嘉義縣"),
    ("TNN", "台南縣"),
    ("KHH", "高雄縣"),
    ("PIF", "屏東縣"),
    ("ILA", "宜蘭縣"),
    ("HUN", "花蓮縣"),
    ("TTT", "台東縣"),
    ("PEN", "澎湖縣"),
    ("KMN", "金門縣"),
    ("MZC", "馬祖縣"),
]
