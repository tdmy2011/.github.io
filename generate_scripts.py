"""
生成10期YouTube系列视频脚本的完整HTML文件
"""
import os

WORKSPACE = r"C:\Users\Administrator\WorkBuddy\2026-05-31-11-24-40"
OUTPUT = os.path.join(WORKSPACE, "YouTube系列脚本_10期完整版.html")

EPISODES = [
    {
        "num": 1,
        "title_zh": "法律合规与组织保障",
        "title_en": "Legal Compliance & Organization",
        "tag": "合规红线", "color": "#e24b4a",
        "duration": "7分钟", "items": "第1-10条",
        "yt_title_zh": "东南亚开厂第一件事不是生产，90%中资企业都做错了！法律合规10条红线",
        "yt_title_en": "First thing NOT to do when opening a factory in SE Asia - 10 legal compliance red lines",
        "keywords_zh": ["东南亚工厂安全", "中资企业合规", "越南劳动法", "ISO 45001法律合规", "东南亚安全法规", "工厂安全注册", "中资出海安全"],
        "keywords_en": ["SE Asia factory safety", "Chinese overseas compliance", "Vietnam labor law", "ISO 45001 legal compliance"],
        "tags": ["东南亚工厂安全合规", "中资企业出海", "越南安全法规", "泰国安全法规", "印尼安全法规", "ISO 45001", "安全合规自查清单", "中资工厂", "海外安全管理", "安全生产", "工厂安全检查", "EHS管理", "职业健康安全"],
        "thumb_idea": "人物表情：惊讶/警告。背景：红色警示条。大字：「开厂先别生产！」。左下角：安全帽+法律天平图标。右侧：10个大红叉标记的问题清单缩略。",
        "hook": "去年帮一家越南工厂做安全评估，走进去第一眼就看出来——他们在当地政府根本没注册安全许可。这家工厂已经生产了两年，月产值200万美金。你知道吗？越南劳动局可以一纸通知让你停工，不管你产量多大。今天我讲的这10条，每一条都可能让你面临罚款、停工、甚至刑事责任。尤其是第1条和第5条，我见过最惨的企业被罚了600万。",
        "outline": "今天我要讲的，是东南亚工厂安全合规的第一维度：法律合规与组织保障。这10条不是建议，是红线。不达标，其他做得再好也没用。",
        "body_sections": [
            ("第1条：工厂必须在当地注册安全许可", "中资企业最大的误区就是以为在国内注册了就行。越南《劳动法》第6条、泰国《工作安全健康管理法》第12条、印尼《劳动法》都明确要求——你必须在当地单独注册工厂实体并获取安全许可。去年我接触的一家越南北宁的电子厂，开了两年没注册，被劳动局查处，罚款+停工整改直接损失800万人民币。正确的做法很简单：建厂之前先找当地律师+安全顾问，走完注册流程，拿到许可再开工。别省这个时间。",
            ("第2条：必须指定专职安全管理人员", "越南要求50人以上工厂设安全员，印尼要求100人以上设安全委员会。很多中资企业让生产经理兼职管安全，这在ISO审核里会被质疑独立性。我见过一个泰国工厂，安全员兼了5个职务，最后外审直接不合格。正确做法：设立独立的安全管理岗位，至少有一人全职负责，并且要有明确的书面授权。",
            ("第5条：中方外派管理层的安全责任必须写入当地文件", "这个是中资出海最容易被忽视的。出事故后法律追责的时候，如果中方管理层的责任没有用当地语言形成书面文件，追责非常困难。我曾经帮一家印尼工厂处理事故善后，就是因为这个漏洞，中方总经理差点被当地警方扣留。正确做法：把所有层级人员的安全职责用当地语言写成正式文件，从总经理到一线工人，四级都要覆盖。"),
            ("第7条：必须和当地政府建立正式沟通渠道", "东南亚部分地区有所谓的'关系文化'，很多中资企业觉得有关系就万事大吉了。错。出了事故，政府第一件事就是查你有没有主动报备过、有没有正式沟通记录。没有？那就是你的全责。正确的做法：明确知道当地安全监管部门是谁、检查频率多少、报告流程是什么，建立正式的书面沟通渠道。"),
            ("第10条：最高管理者必须亲自参与安全", "ISO审核员必查项。不是你签个字拍个照就行了，要有实际参与安全活动的证据——巡检记录、会议纪要、签字的安全改进指令。我见过一个企业，总经理的签字安全方针写得很漂亮，但一年没进过一次车间，外审直接给了不符合项。"),
        ],
        "cta": "以上只是100条安全合规清单中的前10条。如果你想看完整的100条，包括ISO条款编号、法规依据和实操建议，可以点击视频下方链接免费下载。如果你们工厂正在准备ISO 45001认证，或者刚在东南亚建厂不知道安全合规从哪下手，可以看看我的30天体系落地营，15份程序文件模板拿来就能用。关注我，下期讲危险源辨识，这个是出事最多的环节。"
    },
    {
        "num": 2,
        "title_zh": "危险源辨识与风险评估",
        "title_en": "Hazard Identification & Risk Assessment",
        "tag": "高风险", "color": "#ba7517",
        "duration": "8分钟", "items": "第11-20条",
        "yt_title_zh": "越南工厂死了3个人后才明白的事：危险源辨识不是走流程！5个致命误区",
        "yt_title_en": "What a Vietnam factory learned after 3 deaths: Risk assessment is NOT a checkbox exercise",
        "keywords_zh": ["危险源辨识", "风险评估", "JSA", "工作安全分析", "东南亚工厂风险", "ISO 45001风险评估", "工厂安全管理"],
        "keywords_en": ["hazard identification", "risk assessment", "JSA", "ISO 45001 risk", "SE Asia factory safety"],
        "tags": ["危险源辨识", "风险评估方法", "JSA工作安全分析", "东南亚工厂风险", "ISO 45001", "安全检查清单", "中资出海", "工厂安全", "风险矩阵", "变更管理", "安全评估", "海外安全"],
        "thumb_idea": "人物表情：严肃/悲痛。背景：工厂车间场景。大字：「3条人命的教训」。红色数字'3'放在醒目位置。左侧：风险矩阵图表缩略。右下角：警笛图标。",
        "hook": "2024年9月，越南北江省一家中资电池工厂发生化学品泄漏事故，3名工人死亡。调查发现，这家工厂一年前做过风险评估，但只覆盖了主生产车间，完全遗漏了化学品仓储区。这个疏忽直接导致了3条人命。今天我要讲的危险源辨识和风险评估，是ISO 45001里最容易做形式主义、但一旦出事最致命的环节。我见过太多企业拿个模板填一填就算完成了，这是在拿员工命开玩笑。",
        "outline": "危险源辨识和风险评估，是ISO 45001条款6.1.2的要求，也是整个安全体系的基石。这10条讲的是怎么把风险评估做对、做全、做到位。",
        "body_sections": [
            ("第11条：风险评估必须覆盖全厂所有区域", "最常见的错误就是只做了主要车间。我见过一家越南工厂，风险评估覆盖了3个生产车间，但漏了仓库、食堂、宿舍、停车场、污水处理站。结果去年停车场出了货车碾压事故。正确做法：画一张完整的厂区平面图，逐个区域辨识危险源，一个都不能漏。",
            ("第13条：东南亚特有风险——登革热、高温、暴雨", "这是国内风险评估模板几乎不包含的内容。东南亚/非洲特有的风险：登革热和疟疾传播、极端高温导致中暑、暴雨洪涝淹没厂区、地震（印尼在环太平洋火山带上）。一家在印尼苏拉威西建厂的镍矿加工企业，建厂半年就因为没做暴雨风险评估，车间被洪水淹了，损失2000万。正确做法：在当地气象数据基础上，把热带疾病、极端天气纳入风险评估。",
            ("第16条：风险信息要传递到一线员工", "你做了厚厚一本风险评估报告，但一线工人根本看不懂——等于白做。东南亚工厂文化程度参差不齐，纯文字标识效果很差。正确做法：用多语言（中文+英文+当地语），图片+颜色编码。绿色=安全、黄色=注意、红色=危险，直接贴在工位旁边，一目了然。",
            ("第18条：厂区外风险也必须覆盖", "东南亚交通事故率极高。越南和印尼的工人大量骑摩托车通勤，通勤事故算不算工伤？在很多国家是算的。我建议企业提供安全头盔和安全驾驶培训作为员工福利，既能减少工伤争议，又能让员工感受到企业关心。"),
        ],
        "cta": "危险源辨识是安全体系的地基，地基不牢，上面建再多也没用。完整的100条自查清单里有更详细的风险评估步骤和方法，点击下方链接免费下载。如果你觉得自己的风险评估做得不够全面，我的30天落地营里有手把手教你做JSA的实操课，用的是越南电子厂的真实案例。关注我，下期讲电气安全——这个是东南亚工厂事故率最高的领域。"
    },
    {
        "num": 3,
        "title_zh": "电气与机械设备安全",
        "title_en": "Electrical & Mechanical Safety",
        "tag": "合规红线+高风险", "color": "#e24b4a",
        "duration": "7分钟", "items": "第21-30条",
        "yt_title_zh": "东南亚工厂最危险的不是化学品，是电！触电事故7大防坑指南",
        "yt_title_en": "The #1 killer in SE Asia factories is NOT chemicals — it's electricity! 7 life-saving tips",
        "keywords_zh": ["工厂电气安全", "触电事故", "机械设备安全", "东南亚工厂安全", "电气安全检查", "ISO电气安全", "工厂安全"],
        "keywords_en": ["factory electrical safety", "electrocution prevention", "machinery safety", "SE Asia factory"],
        "tags": ["电气安全", "触电事故", "机械设备安全", "东南亚工厂安全", "安全防护装置", "ISO 45001", "工厂安全检查", "电气安全检查", "安全合规", "中资工厂", "PPE个人防护"],
        "thumb_idea": "人物手持绝缘手套/安全帽。背景：闪电/电流符号。大字：「不是化学品，是电！」黄色/红色警示配色。右下角：电压符号⚡",
        "hook": "东南亚工厂最大的安全杀手是什么？你可能以为是化学品泄漏，或者是高处坠落。都不对。是世界卫生组织的数据：东南亚制造业事故死亡率最高的类型是触电。泰国2023年工厂事故统计里，触电占了32%。为什么？因为东南亚很多厂房的电气布线标准和中国不一样，很多中资企业直接搬了国内的电工标准过去，根本不适用。今天这期，我一条一条告诉你电气和机械安全的坑在哪。",
        "outline": "第21-30条，电气与机械设备安全。这是合规红线加高风险双重标记的区域，也是东南亚工厂事故率最高的领域。",
        "body_sections": [
            ("第21条：电气布线必须符合当地标准", "中国用的是GB标准，但越南用TCVN标准、泰国用TIS标准、印尼用SNI标准。电压等级、线径要求、接地方式都有差异。直接搬国内标准过去，在东南亚的高温高湿环境下，绝缘老化速度比国内快3-5倍。正确做法：建厂时就请当地持证电工按当地标准布线，这是不能省的钱。",
            ("第24条：电气设备必须有漏电保护", "这条在国内是常识，但很多东南亚工厂用的二手设备根本没有漏电保护器。印尼有一家中资服装厂，用从国内带过来的旧缝纫机，没有漏电保护，结果一名女工触电身亡。正确做法：所有电气设备都安装RCD（漏电保护器），每月测试一次，记录在案。",
            ("第27条：机械设备必须有防护装置", "冲床、切割机、搅拌机——这些设备的防护罩、急停按钮、光幕传感器不能省。我在越南见过一台冲床没有光幕，工人的手直接伸进去送料。问他为什么不装？说老板说影响效率。我跟他说，一台光幕3000块，断一根手指赔偿至少30万，你自己算。"),
        ],
        "cta": "电气安全是东南亚工厂的生命线，不能有任何侥幸心理。完整的100条清单里，第21-30条详细列出了每一项电气和机械安全的检查标准。下方链接免费下载。我的30天落地营里专门有一期讲电气安全整改的实操案例，从检查到整改到验收，全流程给你演示。关注我，下期讲化学品——东南亚的化学品管理有很多国内不存在的坑。"
    },
    {
        "num": 4,
        "title_zh": "化学品与职业健康",
        "title_en": "Chemicals & Occupational Health",
        "tag": "高风险", "color": "#ba7517",
        "duration": "7分钟", "items": "第31-40条",
        "yt_title_zh": "东南亚工厂化学品管理：你用的胶水可能正在毒害员工！职业健康10条",
        "yt_title_en": "Chemical management in SE Asia: The glue you use may be poisoning your workers!",
        "keywords_zh": ["化学品管理", "MSDS", "职业健康", "工厂化学品安全", "东南亚化学品法规", "PPE个人防护", "职业暴露"],
        "keywords_en": ["chemical management", "MSDS", "occupational health", "PPE", "SE Asia chemical safety"],
        "tags": ["化学品管理", "MSDS安全数据表", "职业健康", "PPE个人防护", "工厂安全", "东南亚法规", "有害物质", "化学品储存", "空气检测", "职业暴露", "ISO 45001"],
        "thumb_idea": "人物戴防毒面具/防护手套。背景：化学瓶/MSDS表格。大字：「你的胶水有毒！」。绿色化学瓶+骷髅头图标。配色：黄+绿警示。",
        "hook": "你可能不知道，东南亚很多服装厂用的胶水，甲醛含量是欧盟标准的5倍。工人每天接触8小时，没有防护，几年后呼吸道疾病发病率是正常人的7倍。更可怕的是，很多中资企业甚至不知道自己用的化学品需要做MSDS。今天我要讲的就是化学品与职业健康这个维度——第31-40条，每一条都可能影响你员工的生命质量。",
        "outline": "化学品管理和职业健康，ISO 45001条款8.1的要求。这10条关注的是工厂里看不见但最致命的风险。",
        "body_sections": [
            ("第31条：所有化学品必须有MSDS安全数据表", "东南亚很多国家强制要求。没有MSDS的化学品，一旦出了事故，企业的赔偿责任是正常情况的3-5倍。正确做法：建厂时就建立化学品清单，每种化学品都必须有当地语言版本的MSDS。",
            ("第34条：化学品储存必须分区分类", "氧化剂和还原剂不能放一起。易燃品要有专用储存柜。东南亚的高温环境下，化学品挥发速度更快，储存不当的风险被放大了。一家泰国工厂就是因为稀释剂和油漆放在同一个柜子里，自燃引发火灾。",
            ("第37条：职业健康体检不能省", "接触化学品、噪音、粉尘的岗位，必须定期做职业健康体检。这不是福利，是法律要求。体检结果要建档保存，至少保存10年。我见过最离谱的是一家印尼工厂，500名员工，从来没做过职业健康体检，结果有一批工人集体出现了呼吸道疾病，被当地工会告了。"),
        ],
        "cta": "职业健康是长期风险，不会今天出事明天就爆炸，但一旦爆发就是群体性的、毁灭性的。完整的100条清单里有化学品管理的详细检查项，下方链接免费下载。关注我，下期讲消防安全——东南亚工厂消防和国内完全不一样，90%的中资企业消防方案是错的。"
    },
    {
        "num": 5,
        "title_zh": "消防安全",
        "title_en": "Fire Safety",
        "tag": "合规红线", "color": "#e24b4a",
        "duration": "7分钟", "items": "第41-50条",
        "yt_title_zh": "90%中资东南亚工厂的消防方案是错的！一文讲透消防10条生死线",
        "yt_title_en": "90% of Chinese factories in SE Asia have WRONG fire safety plans! 10 life-or-death rules",
        "keywords_zh": ["工厂消防安全", "东南亚消防法规", "消防验收", "灭火器配置", "消防逃生", "火灾预防", "工厂消防"],
        "keywords_en": ["factory fire safety", "SE Asia fire code", "fire evacuation", "fire extinguisher", "fire prevention"],
        "tags": ["工厂消防安全", "东南亚消防法规", "消防逃生通道", "灭火器配置", "消防演练", "火灾报警", "安全出口", "消防验收", "ISO 45001消防", "工厂安全", "消防喷淋"],
        "thumb_idea": "人物表情：紧张/严肃。背景：火焰元素。大字：「90%都是错的！」。红色+橙色配色。右下角：消防龙头图标。数据标注：「第41-50条」",
        "hook": "2023年柬埔寨一家中资鞋厂发生火灾，23人死亡。调查发现：消防通道被货物堵死、灭火器过期2年没有更换、工人从未做过消防演练。这三个问题，我敢说90%在东南亚的中资工厂都不同程度地存在。消防安全不是贴几张疏散图就完了的，这是今天我要讲的第41-50条。",
        "outline": "消防安全是合规红线项中的红线。不达标不仅仅是罚款的问题，是停工、刑事责任、甚至人命。这10条我每一条都会讲具体怎么检查、怎么整改。",
        "body_sections": [
            ("第41条：消防系统必须符合当地标准并通过验收", "东南亚各国的消防标准差异极大。越南有QCVN 06标准，泰国有NFPA adopted标准，印尼有SNI标准。最关键的是：消防系统在工厂投产前必须通过当地消防部门验收，拿到验收证书。没有这个证书，保险也不赔。",
            ("第44条：消防通道必须时刻保持畅通", "听起来很简单对吧？但我去过几十家东南亚工厂，至少一半的消防通道都被货物堵着。车间主管的解释永远是'临时放一下'。但火灾不会等你放完再烧。正确做法：消防通道两侧画黄色禁停线，每日巡检记录，违规一次警告，二次罚款。",
            ("第47条：消防演练至少每季度一次", "不是走形式！东南亚工厂很多工人从没经历过火灾，真起火的时候会慌乱。我建议每季度做一次全员疏散演练，用烟雾弹模拟真实场景，计时疏散时间。目标：全员疏散不超过3分钟。",
        ],
        "cta": "消防安全是工厂安全的最后一道防线，这道防线不能有任何一个漏洞。100条完整清单里有消防安全的所有检查项，每一条都有具体的检查标准。下方链接免费下载。关注我，下期讲培训——很多企业做了培训但效果为零，问题出在哪？我下期告诉你。"
    },
    {
        "num": 6,
        "title_zh": "培训与能力建设",
        "title_en": "Training & Capability Building",
        "tag": "一般管理", "color": "#1d9e75",
        "duration": "6分钟", "items": "第51-60条",
        "yt_title_zh": "安全培训做了等于没做？3个致命错误让你的培训变形式主义",
        "yt_title_en": "Safety training that works ZERO - 3 fatal mistakes that make your training useless",
        "keywords_zh": ["安全培训", "安全能力建设", "工厂安全培训", "东南亚安全培训", "特种作业证", "安全教育培训"],
        "keywords_en": ["safety training", "competence building", "factory safety training", "SE Asia safety"],
        "tags": ["安全培训", "特种作业证", "安全能力建设", "东南亚安全培训", "培训效果评估", "ISO 45001培训", "工厂安全", "安全考试", "员工培训", "安全教育"],
        "thumb_idea": "人物表情：无奈/困惑。背景：培训教室/投影仪。大字：「培训了=安全了？」。绿色勾号打红叉。配色：绿色为主，点缀红色警示。",
        "hook": "我见过一家越南工厂，安全培训记录做得漂亮极了——每个员工都有培训签到表、培训课件、培训照片。但ISO审核的时候，外审员随便叫了3个工人问了几个问题，一个都答不上来。培训记录满分，实际效果零分。这种形式主义的安全培训，在东南亚中资工厂里至少占了70%。今天讲的就是怎么让安全培训真正有效。",
        "outline": "培训与能力建设，ISO 45001条款7.2和7.3的要求。不是做了培训就完事，是要确保员工真的掌握了安全知识和技能。",
        "body_sections": [
            ("第51条：三级安全教育必须覆盖所有新员工", "厂级、车间级、班组级三级安全教育，这是国内的标准，但在东南亚很多国家也有类似要求。关键是要用当地语言培训，不能只讲中文。我见过一家印尼工厂，培训全用中文PPT，印尼工人一个字看不懂，签了个名就算培训过了。",
            ("第55条：特种作业人员必须持当地有效证书", "这是很多人踩的坑。中国的电工证、焊工证在东南亚不被自动承认。越南要通过MOLISA认证机构认证，泰国要通过DSD认证，印尼要通过K3认证。如果不做这个对接，出了事故保险公司不赔，企业还要承担全部责任。",
            ("第59条：培训效果必须评估", "怎么评估？不是考试。考试只能测知识不能测能力。正确做法：培训后做现场实操考核——比如讲完灭火器使用，直接让每个员工实操一次。讲完急救，让员工在假人上实际操作CPR。能看到动作的，才说明真的学会了。"),
        ],
        "cta": "安全培训的目的是让员工具备保护自己和同事的能力，不是为了应付审核的几张签到表。100条清单里第51-60条详细列出了培训体系的检查标准。下方链接免费下载。关注我，下期讲承包商管理——这是很多中资企业完全没注意到的大坑。"
    },
    {
        "num": 7,
        "title_zh": "承包商与外包管理",
        "title_en": "Contractor & Outsourcing Management",
        "tag": "东南亚特有", "color": "#534ab7",
        "duration": "7分钟", "items": "第61-70条",
        "yt_title_zh": "泰国工厂外墙坍塌的真相：承包商安全管理=给安全埋了定时炸弹",
        "yt_title_en": "Why a Thai factory wall collapsed: Poor contractor management = ticking time bomb",
        "keywords_zh": ["承包商安全管理", "外包安全", "东南亚承包商", "工厂外包管理", "供应商安全", "ISO承包商"],
        "keywords_en": ["contractor safety management", "outsourcing safety", "SE Asia contractor", "ISO contractor"],
        "tags": ["承包商安全管理", "外包安全", "东南亚承包商", "供应商安全评估", "工厂外包", "ISO 45001承包商", "安全准入", "安全协议", "工地安全", "中资出海"],
        "thumb_idea": "人物表情：严肃/警告。背景：施工现场/脚手架。大字：「承包商=定时炸弹？」。紫色警示配色。右侧：合同/安全协议图标。左下角：脚手架缩略。",
        "hook": "2024年泰国罗勇府，一家中资工厂的外墙在施工中坍塌，5名外包工人受伤。调查发现：这家工厂的承包商连安全资质都没有审查，更别说签安全协议了。很多中资企业觉得承包商是别人的工人，出了事是承包商的责任。错。在大多数东南亚国家，工厂对所有在厂区内作业的人员——不管是不是你的员工——都有安全责任。今天讲的就是承包商管理这个很多人完全忽略的领域。",
        "outline": "承包商与外包管理，ISO 45001条款8.1.4的要求。如果你的工厂有任何外包作业——施工、维修、清洁、装卸、物流——这10条你必须逐条对照。",
        "body_sections": [
            ("第61条：承包商安全资质必须审查", "不能只看价格，必须查安全资质、安全管理人员、安全记录、保险。我建议做一张承包商安全准入评分表，达不到分数的直接排除。查什么？查他们在当地的安全事故记录、有没有安全许可证、安全管理人员持什么证。",
            ("第64条：必须与承包商签订安全协议", "这份安全协议要明确：安全责任划分、安全要求、违规处罚、事故报告流程。而且要用当地语言。不能只有中文版，当地法院不认。",
            ("第67条：承包商作业必须现场监督", "不能签了安全协议就不管了。必须有你的安全人员现场监督承包商的作业。我见过一个案例，承包商在高处作业没有系安全绳，工厂的安全员看到了但觉得不是自己的工人没管。结果出了事故，工厂被判承担连带责任。"),
        ],
        "cta": "承包商管理是中资出海最容易踩的坑之一，因为很多人压根没意识到这是自己的责任。100条清单里第61-70条详细列出了承包商管理的全流程检查标准。下方链接免费下载。关注我，下期讲应急管理——预案做得再漂亮，演练不到位就是废纸一张。"
    },
    {
        "num": 8,
        "title_zh": "应急管理",
        "title_en": "Emergency Management",
        "tag": "高风险", "color": "#ba7517",
        "duration": "7分钟", "items": "第71-80条",
        "yt_title_zh": "应急预案别只放抽屉里！东南亚工厂应急管理的5个实操步骤",
        "yt_title_en": "Don't leave your emergency plan in the drawer! 5 practical steps for factory emergency management",
        "keywords_zh": ["应急管理", "应急预案", "消防演练", "工厂应急响应", "东南亚应急", "急救培训", "应急物资"],
        "keywords_en": ["emergency management", "emergency plan", "fire drill", "first aid", "SE Asia emergency"],
        "tags": ["应急预案", "消防演练", "工厂应急响应", "急救培训", "应急物资", "东南亚应急", "ISO 45001应急", "应急联络", "事故报告", "安全演练"],
        "thumb_idea": "人物戴安全帽/背心。背景：消防演练场景/烟雾。大字：「预案≠废纸」。橙色+红色配色。右下角：急救箱图标。",
        "hook": "我做过一个统计，在东南亚的100多家中资工厂里，有应急预案的超过80%。但真正做过全员演练的，不到15%。更讽刺的是，很多应急预案都是拿国内模板改了个公司名字，连当地的报警电话都没改。一旦出事，员工按照应急预案拨了110——结果110在中国是报警电话，在越南要拨113，泰国要拨191。这就是为什么我反复强调：应急预案必须本土化。今天讲应急管理的第71-80条。",
        "outline": "应急管理，ISO 45001条款8.2。预案是基础，演练是关键，物资是保障。这三样缺一个都不行。",
        "body_sections": [
            ("第71条：应急预案必须本土化", "不能直接套国内模板！要针对当地的风险特点——东南亚的暴雨洪涝、热带疾病、地震（印尼）——制定针对性的预案。更重要的是：当地的报警电话、最近的医院地址和路线、当地消防站的位置，这些都必须更新成当地的。",
            ("第75条：应急物资要定期检查和更换", "灭火器过期、急救箱药品过期、应急照明电池没电——这些小问题在关键时刻就是生和死的区别。正确做法：每月检查一次应急物资，建立检查台账，过期的立即更换。急救箱里的药品清单也要根据当地常见疾病来配置。",
            ("第78条：每年至少2次全员应急演练", "而且要用烟雾弹等道具模拟真实场景。我帮一家越南工厂做过一次演练，用烟雾弹模拟火灾，结果发现疏散时间从他们预想的5分钟变成了8分钟——因为没有做过真实演练，疏散路线上的门有一扇被锁住了。"),
        ],
        "cta": "应急管理是最后一道防线，这道防线必须时刻处于可用状态。100条清单第71-80条列出了应急管理全流程的检查标准。下方链接免费下载。关注我，下期讲事故调查——出事不可怕，可怕的是同样的错误重复发生。"
    },
    {
        "num": 9,
        "title_zh": "事故调查与持续改进",
        "title_en": "Incident Investigation & Continuous Improvement",
        "tag": "ISO必审", "color": "#378add",
        "duration": "6分钟", "items": "第81-90条",
        "yt_title_zh": "事故调查5步法：为什么同样的错误在90%的工厂里反复发生？",
        "yt_title_en": "5-step incident investigation: Why 90% of factories keep making the same mistakes",
        "keywords_zh": ["事故调查", "持续改进", "CAPA", "事故分析", "ISO 45001改进", "根本原因分析", "纠正措施"],
        "keywords_en": ["incident investigation", "CAPA", "root cause analysis", "ISO 45001 improvement", "corrective action"],
        "tags": ["事故调查", "根本原因分析", "CAPA纠正预防", "持续改进", "事故报告", "ISO 45001", "安全隐患", "事故统计", "安全改进", "PDCA循环"],
        "thumb_idea": "人物戴护目镜/安全帽，表情专注。背景：调查现场/分析图表。大字：「为什么又犯了！」。蓝色+黄色配色。右下角：放大镜图标。",
        "hook": "我来问你一个问题：你们工厂如果出了一起小事故——比如工人手指被机器夹了——你的第一反应是什么？90%的管理者会说：赔钱、安抚、恢复生产。但这不是事故调查，这是息事宁人。真正的事故调查要回答三个问题：为什么发生了？为什么会发生？怎么确保不再次发生？前两个问题90%的人能回答，第三个问题——怎么确保不再次发生——90%的人做不到。这就是为什么同样的错误在工厂里反复发生。",
        "outline": "事故调查与持续改进，ISO 45001条款10.2。这不是出事之后的亡羊补牢，而是系统性的学习能力建设。",
        "body_sections": [
            ("第81条：事故必须24小时内报告和调查启动", "不能等！越早调查，证据越完整。我建议所有工厂都建立'4小时报告制'——任何安全事件，4小时内必须上报安全部门并启动调查。小事件也要调查，因为今天的小事故不调查，明天可能就是大事故。",
            ("第84条：使用5WHY法找到根本原因", "不是找'工人操作不当'这种表面原因。要连续问5个'为什么'。比如：工人手指被夹了。为什么？没有防护装置。为什么没有？采购时没买。为什么没买？预算审批没通过。为什么没通过？管理层认为防护装置不重要。根本原因出来了——管理层安全意识不足，不是工人操作不当。",
            ("第88条：整改措施必须跟踪验证", "开了整改通知不是完了。要跟踪：谁负责整改、什么时候完成、完成后的验收人是谁。整改不了的要升级处理。我见过一个整改通知开了半年都没关，最后外审直接开了不符合项。"),
        ],
        "cta": "事故调查的核心目的是防止重犯，不是为了追责。100条清单第81-90条详细列出了事故调查和持续改进的检查标准。下方链接免费下载。最后一期，下期讲文件与记录管理——ISO审核员最关注的东西。关注我。"
    },
    {
        "num": 10,
        "title_zh": "文件与记录管理",
        "title_en": "Documentation & Record Management",
        "tag": "一般管理", "color": "#1d9e75",
        "duration": "6分钟", "items": "第91-100条",
        "yt_title_zh": "ISO审核员来了最想看什么？不是你的PPT，是这100份记录文件！",
        "yt_title_en": "What ISO auditors REALLY want to see? Not your PPT, but THESE 100 record documents!",
        "keywords_zh": ["ISO文件管理", "安全记录", "ISO审核", "文件控制", "安全体系文件", "ISO 45001审核准备", "安全管理记录"],
        "keywords_en": ["ISO documentation", "safety records", "ISO audit preparation", "document control", "ISO 45001 audit"],
        "tags": ["ISO文件管理", "安全记录", "ISO审核准备", "文件控制", "安全管理", "ISO 45001", "审核文件", "程序文件", "记录管理", "安全台账"],
        "thumb_idea": "人物表情：自信/微笑，手持文件。背景：文件柜/文件夹。大字：「审核员最想看这个」。绿色/蓝色配色。右下角：ISO证书图标。",
        "hook": "做了10期视频，前面讲了90条。这最后10条，很多人觉得最无聊——文件与记录管理。但我要告诉你一个真相：ISO审核员到了你工厂，第一件事不是下车间看设备，而是先坐下来翻你的文件。你的体系做得再好，如果文件和记录一团糟，审核员会直接判定你的体系'没有证据支撑'，全部白做。所以这第91-100条，虽然看起来最不刺激，但它是让你的所有努力'可证明'的关键。",
        "outline": "文件与记录管理，ISO 45001条款7.5。这是整个体系的'证据链'——让所有你做的事情都有据可查。",
        "body_sections": [
            ("第91条：安全管理体系文件必须受控", "受控是什么意思？文件要有版本号、审批人、生效日期，修改要有记录。不能出现随便一个人改了程序文件就生效了的情况。建议用文档管理系统，最简单的方案：共享文件夹+版本命名规范+v1.0/v1.1/v2.0版本号。",
            ("第94条：记录必须完整、真实、可追溯", "培训签到表、巡检记录、隐患整改记录、事故调查报告——这些都是你的证据。不能造假。外审员有办法识别造假记录的。一个简单的检验方法：看记录的时间分布，如果所有巡检记录都是整点填写，几乎没有周末的记录，这就有造假嫌疑。",
            ("第98条：文件必须用当地语言", "程序文件必须有当地语言版本。ISO审核员如果不会中文，你给他一本全中文的程序文件，他没法审核。而且当地员工也看不懂。正确做法：至少准备中文+英文+当地语言三个版本。我知道这很费事，但这不是可选项，是必须项。如果你不想自己翻译，我的30天落地营里提供的15份程序文件模板有中英双语版本。"),
        ],
        "cta": "10期视频到这里就结束了。这100条自查清单覆盖了ISO 45001的全部核心条款和东南亚工厂的高频风险点。如果你还没有下载完整的100条清单，现在就点下方链接免费下载。如果你想系统学习ISO 45001体系搭建的全部实操步骤，包括15份拿来就能用的程序文件模板，可以了解我的30天体系落地营。关注我，这个频道专门讲中资出海企业的安全合规。我们下个系列见。"
    },
]

def build_html():
    parts = []
    for ep in EPISODES:
        n = ep["num"]
        # Episode card
        parts.append(f'''
<div class="ep-card" id="ep{n}">
  <div class="ep-header" onclick="toggleEp(this.parentElement)">
    <div class="ep-num" style="background:{ep['color']}">{n:02d}</div>
    <div class="ep-info">
      <div class="ep-title">第{n}期：{ep['title_zh']}</div>
      <div class="ep-meta">
        <span>⏱️ {ep['duration']}</span>
        <span>📋 {ep['items']}</span>
        <span class="ep-badge" style="background:{ep['color']}30;color:{ep['color']}">{ep['tag']}</span>
      </div>
    </div>
  </div>
  <div class="ep-body">
    <div class="tabs">
      <div class="tab active" onclick="switchTab(event,'script{n}')">📋 完整脚本</div>
      <div class="tab" onclick="switchTab(event,'seo{n}')">🎯 SEO关键词</div>
      <div class="tab" onclick="switchTab(event,'thumb{n}')">🖼️ 缩略图创意</div>
    </div>
    <div class="tab-content active" id="script{n}">
      <div style="margin-bottom:20px">
        <strong style="color:#38bdf8">YouTube标题：</strong>
        <span style="color:#f1f5f9">{ep['yt_title_zh']}</span><br>
        <span style="color:#64748b;font-size:13px">{ep['yt_title_en']}</span>
      </div>
      <div class="script-section">
        <div class="script-label">🎯 开场钩子 (10秒)</div>
        <div class="script-text">{ep['hook']}</div>
      </div>
      <div class="script-section">
        <div class="script-label">👤 自我介绍 (5秒)</div>
        <div class="script-text">我是安全生产专家，30年实战经验，专注中资出海企业安全合规。</div>
      </div>
      <div class="script-section">
        <div class="script-label">📢 本期概述 (15秒)</div>
        <div class="script-text">{ep['outline']}</div>
      </div>''')

        for title, content in ep["body_sections"]:
            parts.append(f'''
      <div class="script-section">
        <div class="script-label">📝 正文</div>
        <div class="script-text"><strong style="color:#f59e0b">【{title}】</strong>

{content}</div>
      </div>''')

        parts.append(f'''
      <div class="script-section">
        <div class="script-label">🔔 结尾CTA (30秒)</div>
        <div class="script-text"><span class="cta">{ep['cta']}</span></div>
      </div>
    </div>
    <div class="tab-content" id="seo{n}">
      <div class="seo-grid">
        <div class="seo-box">
          <h4>🔑 中文关键词</h4>
          <div class="tag-list">
            <div class="tag-item">{',</div><div class="tag-item">'.join(ep['keywords_zh'])}</div>
          </div>
        </div>
        <div class="seo-box">
          <h4>🔑 英文关键词</h4>
          <div class="tag-list">
            <div class="tag-item">{',</div><div class="tag-item">'.join(ep['keywords_en'])}</div>
          </div>
        </div>
      </div>
      <div class="seo-box" style="margin-top:16px">
        <h4>🏷️ YouTube标签</h4>
        <div class="tag-list">
          <div class="tag-item">{',</div><div class="tag-item">'.join(ep['tags'])}</div>
        </div>
      </div>
    </div>
    <div class="tab-content" id="thumb{n}">
      <div class="thumb-idea">
        <h4>🖼️ 缩略图创意</h4>
        <p>{ep['thumb_idea']}</p>
      </div>
    </div>
  </div>
</div>''')

    # Closing HTML
    parts.append('''
</div>
</div>
<script>
function toggleEp(card){card.classList.toggle('open')}
function switchTab(e,id){
  const tabs=e.target.parentElement.querySelectorAll('.tab');
  const contents=e.target.parentElement.parentElement.querySelectorAll('.tab-content');
  tabs.forEach(t=>t.classList.remove('active'));
  contents.forEach(c=>c.classList.remove('active'));
  e.target.classList.add('active');
  document.getElementById(id).classList.add('active');
}
function scrollToEp(n){
  document.querySelectorAll('.ep-card').forEach(c=>c.classList.remove('open'));
  document.getElementById('ep'+n).classList.add('open');
  document.getElementById('ep'+n).scrollIntoView({behavior:'smooth',block:'start'});
  document.querySelectorAll('.sidebar-item').forEach(s=>s.classList.remove('active'));
  document.getElementById('side'+n).classList.add('active');
}
</script>
</body></html>''')

    return ''.join(parts)

# Read existing base file and append episodes
base_path = OUTPUT
with open(base_path, 'r', encoding='utf-8') as f:
    base = f.read()

episodes_html = build_html()

# Insert episodes before the closing </div></div>
full_html = base.replace('</div>\n</div>\n</body></html>', episodes_html)

with open(base_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Generated {len(EPISODES)} episode scripts")
print(f"Output: {base_path}")
print(f"File size: {os.path.getsize(base_path)/1024:.1f} KB")
