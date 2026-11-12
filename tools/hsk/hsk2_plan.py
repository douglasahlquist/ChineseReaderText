# HSK 2 (2021 standard): every new word in exactly one lesson, in teaching order.
# (number, Chinese title, English title, setting, words)
# Words already taught in the HSK 1 course (分钟 万 千 亿 刻 喂) are not repeated.
PLAN = [
 (1, "欢迎你", "Welcome!", "church", "欢迎 晚安 不好意思 好久 感谢 快乐 开心 加油 干杯 平安 一路平安 一路顺风 怎么样 挺 挺好"),
 (2, "我们的教室", "Our classroom", "town", "教室 黑板 椅子 座位 课堂 作业 练习 复习 生词 句子 词语 词 字典 词典 题"),
 (3, "说普通话", "Speaking Mandarin", "town", "语言 英语 英文 普通话 读音 音节 意思 有意思 懂 懂得 讲 讲话 对话 听讲 流利"),
 (4, "我的一天", "My day", "home", "早晨 早餐 午餐 晚餐 午睡 洗澡 出门 做饭 平时 平常 经常 老是 半夜 夜里 夜"),
 (5, "春夏秋冬", "The four seasons", "town", "春天 夏天 秋天 冬天 晴 晴天 阴 阴天 多云 云 雪 下雪 气温 温度 零下 凉 凉快"),
 (6, "上周和下周", "Last week and next week", "home", "周 周末 上周 下周 月份 前年 今后 以前 以后 后来 当时 那时 那时候 这时 这时候 那会儿"),
 (7, "我的家庭", "My family", "home", "家庭 家长 爱人 太太 大人 小时候 从小 长大 出生 姓 姓名 名 年轻 少年 青年"),
 (8, "身体", "The body", "home", "头 头发 眼 眼睛 脸 嘴 脚 腿 个子 全身 身边 健康 舒服 疼 药"),
 (9, "去看医生", "Seeing a doctor", "town", "中医 西医 住院 出院 药店 药片 药水 难受 检查 小心 急 怕 可怕 感觉 感到"),
 (10, "中餐和西餐", "Chinese and Western food", "home", "中餐 西餐 快餐 饺子 方便面 蛋 鸡 鱼 酒 筷子 碗 菜单 饱 味道 饭馆"),
 (11, "去超市", "At the supermarket", "town", "超市 便宜 卖 卡 信用卡 银行 银行卡 收 收到 一共 斤 公斤 千克 克 份"),
 (12, "颜色", "Colors", "home", "颜色 红 红色 黄 黄色 蓝 蓝色 绿 绿色 黑 黑色 白色 漂亮 难看 可爱"),
 (13, "我的东西", "My things", "home", "大衣 鞋 球鞋 手表 笔 纸 笔记 笔记本 表 信 封 照片 相机 照相 礼物"),
 (14, "坐地铁", "Taking the subway", "town", "交通 地铁 地铁站 公交车 公共汽车 出租车 出租 司机 停车 停车场 骑 骑车 自行车 车辆 道路"),
 (15, "问路", "Asking the way", "town", "问路 往 向 离 近 对面 边 路边 公路 公里 米 街 广场 出口 入口"),
 (16, "去旅行", "Going on a trip", "town", "旅行 旅游 旅客 游客 护照 出国 回国 外地 酒店 起飞 送到 留学生 机会 计划 打算"),
 (17, "我们的城市", "Our city", "town", "市 市长 公园 花园 动物园 体育馆 体育场 中心 院 院子 大门 墙 层 住房 院长"),
 (18, "大自然", "Nature", "town", "大自然 太阳 月亮 星星 地球 空气 海 大海 海边 河 湖 草 草地 灯 亮"),
 (19, "小动物", "Animals", "home", "动物 猫 狗 鸟 它 它们 养 照顾 关心 爬 爬山 叫作 名称 食物"),
 (20, "打篮球", "Playing basketball", "town", "运动 体育 篮球 排球 网球 球队 球场 队 队长 练 举 举手 场 级 水平"),
 (21, "音乐和电影", "Music and movies", "town", "音乐 音乐会 画 画儿 画家 小说 作家 故事 影片 节目 晚会 新闻 广告 明星 流行"),
 (22, "上网", "Online", "home", "报纸 日报 晚报 信息 网 网站 打印 短信 信号 开机 关机 图片 计算机 数字 数"),
 (23, "在公司", "At the office", "town", "公司 办公室 经理 同事 单位 打工 收入 顾客 商人 服务 主人 客人 请客 实习 中年"),
 (24, "学校生活", "School life", "town", "校长 校园 学期 开学 年级 班长 组 组长 小组 考生 成绩 分数 高中 中小学 教学"),
 (25, "过节", "Festivals", "church", "节日 春节 过年 周年 假期 休假 举行 参加 活动 热情 好事 一生 教育 教师 全家"),
 (26, "交朋友", "Making friends", "church", "交朋友 老朋友 好人 坏人 友好 相信 信心 答应 帮助 愿意 请求 要求 接受 不错"),
 (27, "你怎么看", "What do you think?", "church", "认为 以为 看法 想法 观点 意见 态度 角度 说明 讨论 商量 提出 提到 道理"),
 (28, "心情", "Feelings", "home", "心情 心里 心中 感动 难过 哭 笑话 笑话儿 满意 不满 放心 爱情 难听 气"),
 (29, "比一比", "Comparing", "home", "相同 不同 同样 差不多 不如 更 越 越来越 特别 十分 多么 大大 一点点 有点儿 有一点儿"),
 (30, "因为所以", "Because and so", "church", "但 但是 可是 不过 虽然 而且 不但 因为 所以 为 为什么 原因 结果"),
 (31, "如果", "If", "home", "如果 的话 只要 或 或者 必须 应该 该 可以 可能 也许 一定 不一定 能够 只能"),
 (32, "已经和刚才", "Already and just now", "home", "已经 刚 刚刚 刚才 才 就要 快要 早就 又 一直 永远 忽然 同时 随时 不久"),
 (33, "所有的人", "Everyone", "church", "全 全部 全体 所有 部分 大部分 一部分 多数 大多数 少数 不少 许多 好多 大量 人数"),
 (34, "一辆车", "Measure words", "town", "位 条 件 辆 座 套 瓶 瓶子 篇 段 片 节 遍 道 句"),
 (35, "大家", "All of us", "church", "自己 大家 咱 咱们 人们 有人 其他 其中 老年 青少年 人口 全国 全年 不一会儿"),
 (36, "拿来拿去", "Taking and giving", "home", "拿到 拿出 放下 留 留下 带 带来 送给 交给 交 取 借 换 租"),
 (37, "推和拉", "Push and pull", "home", "推 拉 碰 碰到 碰见 掉 倒 吹 装 弄 占 背 闻 响 干活儿"),
 (38, "变化", "Changes", "town", "变 变成 改 改变 成 成为 组成 重新 实现 完成 做到 进行 提高 取得"),
 (39, "发现", "Finding out", "town", "发现 见到 见过 想到 想起 找出 听说 接到 得出 走过 走进 走开 站住 出现"),
 (40, "大声说", "Speaking up", "church", "喊 大声 小声 通知 提 称 声音 安静 名单 报名 故意 随便 重复 作文"),
 (41, "东西南北", "Directions and places", "town", "方向 东方 西方 南方 北方 东北 西北 东南 西南 面前 以上 以下 以外 到处 里头"),
 (42, "好处和坏处", "Pros and cons", "town", "好处 坏处 正常 普通 一般 正确 准确 清楚 方便 安全 合适 公平 平等 重点 主要"),
 (43, "生活", "Life", "home", "生活 日子 习惯 经过 过去 过来 生 自由 理想 目的 条件 常见 常用 重视 好像"),
 (44, "怎么办", "What to do", "home", "办法 方法 做法 怎样 怎么办 这样 那样 这么 那么 什么样 样子 例如 比如 比如说 例子"),
 (45, "问题", "Problems", "town", "问题 难题 事情 影响 作用 方面 特点 原来 实际 实在 真正 完全 当 大小 正是"),
 (46, "满了", "Full, light and dirty", "home", "满 够 不够 低 轻 平 熟 脏 长 短 假 高级 中级 角"),
 (47, "科学", "Science", "town", "科学 科学家 科 国际 等于 加 度 发 只 像 正好 直接"),
 (48, "排队", "Waiting in line", "town", "停 靠 排 排队 选 查 求 通 通过 进入 离开 超过 来自 受到 让"),
 (49, "完成了", "All done", "home", "完 办 算 接 接着 接下来 然后 使用 顺利 努力 得 行动 行为"),
 (50, "周末去哪儿", "Where to this weekend?", "town", "有空儿 多久 出发 参观 船 等到 分开 快点儿 天上 点头 行人"),
 (51, "最近怎么样", "How have you been?", "home", "最近 啊 不要 不行 不太 外卖 洗衣机 油 店 面 省 流"),
]

NOT_OK = set()

# What each lesson sets out to teach (shown at the top of the lesson).
GOALS = {
 1: "Welcome people, wish them well — good night, have fun, safe travels, cheers — apologize politely, and ask “how is it?”",
 2: "Talk about the classroom: desks and seats, homework, practice and review, new words, sentences and dictionaries.",
 3: "Talk about languages: Mandarin and English, pronunciation, meaning, understanding, and speaking fluently.",
 4: "Describe your day from breakfast to bedtime, and say how often you do things.",
 5: "Talk about the four seasons, sun, cloud and snow, and how warm or cold it is.",
 6: "Talk about weeks and months, before and after, and “at that time” versus “now”.",
 7: "Talk about your family, your name, where you were born, and growing up.",
 8: "Name the parts of the body and say how you feel: healthy, comfortable, or in pain.",
 9: "See a doctor, Chinese or Western medicine; go into and out of hospital; and say you're worried or afraid.",
 10: "Talk about Chinese and Western food, order from a menu, and say how something tastes and that you're full.",
}

GOALS.update({
 11: "Shop at the supermarket and the market: prices per jin and kilo, “altogether”, and paying by card.",
 12: "Name the colors, and say whether something is beautiful, cute or ugly.",
 13: "Talk about your things: coat and shoes, watch, pen and paper, notebooks, letters, photos and presents.",
 14: "Get around town by subway, bus, taxi and bicycle, and find somewhere to park.",
 15: "Ask the way and give directions: toward, opposite, how far, kilometers and meters, exits and entrances.",
})

GOALS.update({
 16: "Plan a trip: travel and tourism, passports, going abroad and coming home, hotels, flights and opportunities.",
 17: "Describe your city: parks, gardens and the zoo, sports grounds, the city center, courtyards, gates, walls and floors.",
 18: "Talk about nature: sun, moon and stars, the Earth and the air, sea, rivers and lakes, grass and light.",
 19: "Talk about animals and pets: cats, dogs and birds, “it” and “they”, looking after them, and what things are called.",
 20: "Talk about sport: basketball, volleyball and tennis, teams and captains, practice, games, levels and standards.",
})

GOALS.update({
 21: "Talk about music, art, books and films: concerts, paintings, novels, stories, shows, news, ads and stars.",
 22: "Read the news and get online: newspapers, information, websites, printing, texts, signal and numbers.",
 23: "Talk about work: companies and offices, managers and colleagues, part-time jobs, customers, hosts, guests and treating.",
 24: "Talk about school life: principals and campuses, terms and grades, groups and leaders, results and scores.",
 25: "Celebrate festivals and holidays: the Spring Festival, anniversaries, events and taking part, and the whole family.",
 26: "Make friends: old friends, good and bad people, believing and trusting, helping, promising and accepting.",
 27: "Give and ask for opinions: “I think” and “I thought”, ideas, views, discussing, talking things over, and making sense.",
 28: "Talk about feelings: mood, being moved or sad, crying and joking, satisfied or not, don't worry, and anger.",
 29: "Compare things: same and different, about the same, not as good as, even more, more and more, especially, and a bit.",
 30: "Join ideas with but, although, not only… but also, because… so, and ask why.",
})
