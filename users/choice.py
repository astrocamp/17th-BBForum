from django.db import models


class Gender(models.TextChoices):
    Female = "F", "Female"
    Men = "M", "Men"
    None_gender = "N", "None_gender"


class Education_level(models.TextChoices):
    MIDDLE_SCHOOL_OR_BELOW = "MS", "中學以下"
    HIGH_SCHOOL = "HS", "高中、高職"
    JUNIOR_COLLEGE = "JC", "專科"
    UNIVERSITY = "U", "大學"
    POST_GRADUATE = "PG", "研究所以上"


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
