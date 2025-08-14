# config.py
questions = [
    {"id": "name", "text": "姓名"},
    {"id": "gender", "text": "性别(1男 2女)"},
    {"id": "birth_year", "text": "出生年份"},
    {"id": "id_card", "text": "身份证号"},
    {"id": "insurance_card", "text": "医保卡号(选填)"},
    {"id": "family_doctor", "text": "家庭医生"},
    {"id": "investigator", "text": "问卷调查人(楼栋负责人)"},
    {"id": "height", "text": "身高(cm)"},
    {"id": "weight", "text": "体重(kg)"},
    {"id": "occupation", "text": "职业"},
    {"id": "education", "text": "文化程度(1小学 2初中 3中专 4高中 5大专 6大学 7硕士 8博士 9博士后)"},
    {"id": "address", "text": "家庭地址"},
    {"id": "phone1", "text": "联系电话1(住宅)"},
    {"id": "phone2", "text": "联系电话2(手机)"},
    {"id": "phone3", "text": "联系电话3(家属)"},

    # 吸烟相关
    {"id": "smoking", "text": "吸烟史(1是 2否)"},
    {"id": "smoking_freq", "text": "吸烟频率(支/天)", "condition": lambda a: a.get("smoking") == "1"},
    {"id": "smoking_years", "text": "累计吸烟年数", "condition": lambda a: a.get("smoking") == "1"},
    {"id": "quit_smoking", "text": "目前是否戒烟(1是 2否)", "condition": lambda a: a.get("smoking") == "1"},
    {"id": "quit_years", "text": "戒烟年数",
     "condition": lambda a: a.get("smoking") == "1" and a.get("quit_smoking") == "1"},

    # 被动吸烟
    {"id": "passive_smoking", "text": "被动吸烟(1否 2是)"},
    {"id": "passive_freq", "text": "被动吸烟频率(1≤1小时/天 2 1-2小时/天 3>2小时/天)",
     "condition": lambda a: a.get("passive_smoking") == "2"},
    {"id": "passive_years", "text": "累计被动吸烟年数", "condition": lambda a: a.get("passive_smoking") == "2"},

    # 厨房油烟接触
    {"id": "kitchen_smoke", "text": "长期厨房油烟接触(1每周<1次 2每周1-3次 3每周>3次 4每天)"},
    {"id": "kitchen_years", "text": "累计厨房油烟接触年数", "condition": lambda a: a.get("kitchen_smoke") != "1"},

    # 职业致癌物
    {"id": "occup_carcinogen", "text": "职业致癌物质接触(1有 2无)"},
    {"id": "carcinogen_detail", "text": "致癌物类型及累计接触年数(如有)",
     "condition": lambda a: a.get("occup_carcinogen") == "1"},

    # 既往个人肿瘤史
    {"id": "personal_tumor", "text": "既往个人肿瘤史(1有 2无)"},
    {"id": "tumor_detail", "text": "肿瘤类型及确诊年份(如有)", "condition": lambda a: a.get("personal_tumor") == "1"},

    # 家族肺癌史
    {"id": "family_lung_cancer", "text": "三代以内直系亲属肺癌家族史(1有 2无)"},
    {"id": "family_lung_detail", "text": "肿瘤类型及关系(如有)",
     "condition": lambda a: a.get("family_lung_cancer") == "1"},

    # 近一年胸部CT检查
    {"id": "ct_check", "text": "一年内胸部CT检查(1是 2否)"},

    # 慢性疾病
    {"id": "chronic_bronchitis", "text": "慢性支气管炎(1是 2否)"},
    {"id": "bronchitis_years", "text": "患病年数", "condition": lambda a: a.get("chronic_bronchitis") == "1"},

    {"id": "emphysema", "text": "肺气肿(1是 2否)"},
    {"id": "emphysema_years", "text": "患病年数", "condition": lambda a: a.get("emphysema") == "1"},

    {"id": "tuberculosis", "text": "肺结核(1是 2否)"},
    {"id": "tuberculosis_years", "text": "患病年数", "condition": lambda a: a.get("tuberculosis") == "1"},

    {"id": "copd", "text": "慢性阻塞性肺病(1是 2否)"},
    {"id": "copd_years", "text": "患病年数", "condition": lambda a: a.get("copd") == "1"},

    {"id": "interstitial_fibrosis", "text": "肺间质纤维化(1是 2否)"},
    {"id": "fibrosis_years", "text": "患病年数", "condition": lambda a: a.get("interstitial_fibrosis") == "1"},

    # 最近半年症状
    {"id": "recent_weight_loss", "text": "近半年不明原因消瘦(1有 2无)"},
    {"id": "weight_loss", "text": "体重下降kg(如有)", "condition": lambda a: a.get("recent_weight_loss") == "1"},

    {"id": "recent_symptoms", "text": "最近是否有持续性干咳、痰中带血、声音嘶哑、反复同部位肺炎(1有 2无)"},
    {"id": "symptom_detail", "text": "具体症状(如有)", "condition": lambda a: a.get("recent_symptoms") == "1"},

    {"id": "self_feeling", "text": "最近自我感觉(1好 2一般 3不好)"}
]

questionnaire_reference = {
    "基本信息": {
        "姓名": "2~4个汉字",
        "性别(1男 2女)": "1 或 2",
        "出生年份": "四位数字，如 1950~2010",
        "身份证号": "18位，最后一位可能是 X",
        "医保卡号(选填)": "10~20位字母或数字，可为空",
        "家庭医生": "2~4个字",
        "问卷调查人(楼栋负责人)": "2~4个字"
    },
    "身体指标": {
        "身高(cm)": "数值，100~250",
        "体重(kg)": "数值，30~200"
    },
    "社会信息": {
        "职业": "自由文本，如“工人”、“教师”",
        "文化程度(1小学 2初中 3中专 4高中 5大专 6大学 7硕士 8博士 9博士后)": "1~9之间整数"
    },
    "联系方式": {
        "家庭地址": "不少于10个字的详细地址",
        "联系电话1(住宅)": "区号+号码，如 010-12345678",
        "联系电话2(手机)": "11位手机号",
        "联系电话3(家属)": "可为固话或手机号"
    },
    "吸烟史": {
        "吸烟史(1是 2否)": "1 或 2",
        "吸烟频率(支/天)": "0~100",
        "累计吸烟年数": "0~80",
        "目前是否戒烟(1是 2否)": "1 或 2",
        "戒烟年数": "0~80（如已戒烟）"
    },
    "被动吸烟": {
        "被动吸烟(1否 2是)": "1 或 2",
        "被动吸烟频率(1≤1小时/天 2 1-2小时/天 3>2小时/天)": "1~3",
        "累计被动吸烟年数": "0~80"
    },
    "厨房油烟": {
        "长期厨房油烟接触(1每周<1次 2每周1-3次 3每周>3次 4每天)": "1~4",
        "累计厨房油烟接触年数": "0~80"
    },
    "职业暴露": {
        "职业致癌物质接触(1有 2无)": "1 或 2",
        "致癌物类型及累计接触年数(如有)": "如“石棉10年”，无可为空或“无”"
    },
    "肿瘤相关史": {
        "既往个人肿瘤史(1有 2无)": "1 或 2",
        "肿瘤类型及确诊年份(如有)": "如“肺癌，2010年”，无可为空",
        "三代以内直系亲属肺癌家族史(1有 2无)": "1 或 2",
        "肿瘤类型及关系(如有)": "如“父亲，肺癌”，无可为空"
    },
    "影像检查": {
        "一年内胸部CT检查(1是 2否)": "1 或 2"
    },
    "呼吸系统疾病史": {
        "慢性支气管炎(1是 2否)": "1 或 2",
        "患病年数": "0~80",
        "肺气肿(1是 2否)": "1 或 2",
        "患病年数": "0~80",
        "肺结核(1是 2否)": "1 或 2",
        "患病年数": "0~80",
        "慢性阻塞性肺病(1是 2否)": "1 或 2",
        "患病年数": "0~80",
        "肺间质纤维化(1是 2否)": "1 或 2",
        "患病年数": "0~80"
    },
    "近期症状": {
        "近半年不明原因消瘦(1有 2无)": "1 或 2",
        "体重下降kg(如有)": "0~30",
        "最近是否有持续性干咳、痰中带血、声音嘶哑、反复同部位肺炎(1有 2无)": "1 或 2",
        "具体症状(如有)": "自由描述，或填“无”"
    },
    "健康自评": {
        "最近自我感觉(1好 2一般 3不好)": "1~3"
    }
}

