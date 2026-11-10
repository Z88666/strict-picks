#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build products.json + index.html for strict-picks.
Static-first: every product is written into the HTML as markup, JS only filters/sorts.
Refresh: button fetches data/products.json with cache-buster; on success re-renders from
that file, on failure keeps embedded data and says so. No Taobao/PDD official price API
exists for public use (no key, anti-bot), so platform comparison is via verified
snapshot prices per platform + one-tap search links to each platform.
"""
import json, html, os
BASE = os.path.dirname(os.path.abspath(__file__))
# id, cat, name, brand, spec, ingredients/material, price_range, unit_price, platforms{jd,tmall,pdd,other}, best_platform, verdict(pass/caution/reject), clean(0-100), value(0-100), reason, buy_tip, source
P = [
# ---- 食 调味 ----
(1,"食·调味","DL 黑豆酿造酱油（生抽）","胖东来","480ml，特级，180天头道原汁，氨基酸态氮≥1.0g/100ml","水、非转基因黑豆、食用盐、小麦（仅4种）","¥8.7/瓶","¥18.1/升",{"jd":"无（线下品牌）","tmall":"无","pdd":"代购 ¥12.5–20/瓶","other":"胖东来小程序/抖音 ¥8.7"},"胖东来小程序","pass",100,95,"配料最干净的酱油之一，4种原料，0防腐/甜味剂/味精/焦糖色。代工丸庄金龙鱼（泰州）。","只认黑豆款4种配料；另一款DL生抽是6种配料（含白砂糖、酵母提取物），别买错。常缺货，看到就囤。","胖东来官方小程序/抖音，2025-02媒体报道"),
(2,"食·调味","御藏本酿380天 零添加酱油","千禾","500ml，特级，380天，氨基酸态氮≥1.20g/100ml","水、非转基因黄豆、小麦、食用盐（未加碘）","¥14–19/500ml","¥28–38/升",{"jd":"¥14.37起","tmall":"¥15.96/500ml×2券后","pdd":"¥18.66/1000ml×2百亿补贴"},"京东","pass",98,88,"4种配料，380天高盐稀态发酵，氨基酸态氮比特级标准高50%，鲜味来自发酵不是味精。","大促蹲¥10–15/瓶；注意2027年3月起包装不得再标“零添加”，买时只看配料表。","什么值得买/京东，2026-11-10"),
(3,"食·调味","0金标生抽","海天","500ml，特级，氨基酸态氮≥0.8g/100ml","水、非转基因黄豆、食用盐、小麦、白砂糖、酵母提取物（6种）","¥8–13/500ml","¥16–26/升",{"jd":"¥8–12","tmall":"¥9–13","pdd":"¥8–12"},"京东","pass",82,90,"0防腐/甜味剂/味精，但比千禾多白砂糖+酵母提取物，清洁度次一档，胜在便宜好买。","控糖、追求最干净选千禾/胖东来；图便宜好买选这款。","海天官网/什么值得买"),
(4,"食·调味","金标生抽（普通版，非0添加）","海天","500ml，一级","水、非转基因黄豆、小麦粉、食用盐、白砂糖、酵母抽提物、谷氨酸钠、呈味核苷酸二钠、苯甲酸钠、三氯蔗糖","¥7–10/500ml","¥14–20/升",{"jd":"¥7–10","tmall":"¥7–10","pdd":"¥6–9"},"拼多多","reject",30,40,"同价有0添加可选，这款含味精、增味剂、防腐剂、三氯蔗糖，配料表最长。不是不能吃，是没必要买。","直接换上面0金标，差价不到¥2。","头条/钛媒体配料对比"),
(5,"食·调味","5S压榨一级花生油","鲁花","5L，一级，物理压榨","花生（仅1种原料）","¥140–160/5L","¥28–32/升",{"jd":"¥148–160","tmall":"¥131/6.09L券后","pdd":"¥147起"},"京东","pass",95,55,"只有花生，5S物理压榨无化学残留，香味最浓。贵是唯一的缺点。","不差钱、爱浓香选它；要性价比选金龙鱼压榨，同工艺便宜一半。","什么值得买/京东"),
(6,"食·调味","压榨一级浓香花生油","金龙鱼","5L，一级，物理压榨","花生（仅1种原料）","¥79–90/5L","¥16–18/升",{"jd":"¥78.9券后","tmall":"¥89.9","pdd":"¥79–89"},"京东","pass",95,98,"和鲁花同为只有花生、物理压榨一级，每升便宜¥12–14，是花生油性价比之王。","默认买这款；6.18L装券后¥77更划算。","什么值得买/京东"),
(7,"食·调味","黄金比例食用植物调和油","金龙鱼","5L，浸出工艺","大豆油、菜籽油等多种油混合（比例不公开）","¥55–70/5L","¥11–14/升",{"jd":"¥55–65","tmall":"¥58–68","pdd":"¥52–62"},"京东","reject",45,50,"浸出工艺+混合油、比例不透明，清洁度和可追溯性都输给单一压榨油。便宜但不推荐。","只买单一油种压榨款，别买调和油。","苏宁/京东商品页"),
(8,"食·调味","糯米香醋 5度 0添加","千禾","500ml×3瓶，总酸5g/100ml","糯米酿造，不添加防腐剂、色素","¥15.8–19.8/3瓶","¥10–13/升",{"jd":"¥15.8–19.8","tmall":"¥17.8起","pdd":"¥15–18"},"京东","pass",92,95,"最便宜的0添加醋，糯米酿造。","日常醋默认这款。","什么值得买/京东"),
(9,"食·调味","三年老陈醋 6度 0添加","东湖","500ml，GB/T 19777 山西老陈醋","纯粮酿造","¥11.8/瓶，3瓶¥32.6","¥23.6/升",{"jd":"¥11.8/瓶","tmall":"¥32.6/3瓶","pdd":"¥30–35/3瓶"},"京东","pass",90,85,"老陈醋首选，6度酸度够，纯粮酿造。","吃山西老陈醋认准GB/T 19777。","什么值得买/京东"),
(10,"食·调味","六年陈镇江香醋 6.4度","恒顺","580ml，GB/T 18623 镇江香醋","纯粮酿造","¥8.2–9.7/瓶（需买6件）","¥14–17/升",{"jd":"¥8.2–9.7","tmall":"¥32.9/2瓶","pdd":"¥9–12"},"京东","pass",90,96,"香醋首选，囤货价极低，6年陈。","香醋认准GB/T 18623，6件囤货最划算。","什么值得买/京东"),
(11,"食·调味","低钠盐（加碘）","中盐","400g×5袋，钠降约30%","精制盐、氯化钾、碘酸钾、柠檬酸铁铵","¥11.5–12.9/5袋","¥5.8–6.5/kg",{"jd":"¥11.5–12.9","tmall":"¥12–13","pdd":"¥11–13"},"京东","pass",85,92,"控钠家庭首选。肾病、高钾人群慎用。","普通家庭默认低钠盐；想吃无抗结剂选天山湖盐。","京东"),
# ---- 食 主食乳品 ----
(12,"食·主食乳品","2026年新米 五常香米","十月稻田","5kg，GB/T 19266，稻花香2号","大米（仅1种）","¥46.9–50/5kg","¥9.4–10/kg",{"jd":"¥46.9–50","tmall":"¥48–52","pdd":"¥45–50"},"京东","pass",98,95,"五常大米性价比首选，认准GB/T 19266+稻花香2号，低于¥40/5kg的“五常”大概率掺假。","别买无标准号的散装五常米。","京东/什么值得买"),
(13,"食·主食乳品","五常大米","柴火大院","5kg，GB/T 19266","大米（仅1种）","¥49.7–59.9/5kg，特等¥79–85","¥10–17/kg",{"jd":"¥49.7–59.9","tmall":"¥55–65","pdd":"¥49–60"},"京东","pass",98,75,"口感更好但贵20–70%，非必需，十月稻田够吃。","预算够再升级。","京东/什么值得买"),
(14,"食·主食乳品","纯牛奶","伊利","250ml×24盒，蛋白3.3g/100ml","生牛乳（仅1种）","¥32.8–39.8/箱","¥1.37–1.66/盒",{"jd":"¥32.8–39.8","tmall":"¥35–40","pdd":"¥32–38"},"拼多多","pass",98,96,"蛋白最高档之一，最便宜大牌纯牛奶。","伊利/蒙牛/三元谁券后便宜买谁，配料都是只有生牛乳。","京东/什么值得买"),
(15,"食·主食乳品","全脂纯牛奶","蒙牛","250ml×24盒，蛋白3.2g/100ml","生牛乳（仅1种）","¥35–45/箱","¥1.46–1.88/盒",{"jd":"¥35–45","tmall":"¥36–44","pdd":"¥34–42"},"京东","pass",98,88,"与伊利同级。","看券后价，二选一。","京东/什么值得买"),
(16,"食·主食乳品","小方白纯牛奶","三元","200ml×24盒，蛋白3.3g/100ml","生牛乳（仅1种）","¥19.14/箱券后","¥0.80/盒",{"jd":"¥19.14券后","tmall":"¥22–28","pdd":"¥19–25"},"京东","pass",98,98,"200ml券后最便宜的纯牛奶，蛋白不缩水。","小盒装适合一个人喝，别囤大盒喝不完。","什么值得买"),
(17,"食·主食乳品","0%蔗糖原味酸奶","简爱","135g×4杯，蛋白4.0g/100g","生牛乳≥99%+保加利亚乳杆菌、嗜热链球菌；无蔗糖、无代糖、无添加剂","¥10–13.2/4杯","¥2.5–3.3/杯",{"jd":"¥10–13.2","tmall":"¥11–14","pdd":"¥10–13"},"京东","pass",100,92,"最干净的酸奶，配料只有牛乳+菌。","控糖默认这款；别买成含糖的高蛋白款。","京东/什么值得买"),
(18,"食·主食乳品","如实纯净发酵乳 原味","光明","135g×12杯，蛋白约3–4.1g/100g","生牛乳+发酵菌；0蔗糖，蜂蜜独立小包自加","¥29.3–37.7/12杯券后","¥2.44–3.14/杯",{"jd":"¥29.3–37.7","tmall":"¥33–40","pdd":"¥30–38"},"京东","pass",100,90,"和简爱并列最干净。","蜂蜜包别全加，半包够甜。","京东/什么值得买"),
(19,"食·主食乳品","原味低温酸奶","卡士","100g×6杯，生牛乳≥90%","生牛乳≥90%+白砂糖+7种乳酸菌（无增稠/香精）","¥10.7–17.8/6杯","¥1.78–2.97/杯",{"jd":"¥10.7–17.8","tmall":"¥42.9–59.9/24杯","pdd":"¥11–16"},"京东","pass",70,85,"无增稠/香精，但含白砂糖，控糖选简爱/如实。","同品牌活菌系列含增稠剂+香精，别买错系列。","卡士官网/什么值得买"),
(20,"食·主食乳品","活菌系列原味","卡士","100g，生牛乳≥80%","生牛乳≥80%+水+白砂糖+乳酸菌+海藻酸丙二醇酯+食用香精","¥10–16/6杯","—",{"jd":"¥10–16","tmall":"¥11–17","pdd":"¥10–15"},"京东","reject",35,50,"同品牌不同系列，含增稠剂+香精，别买错。","认准CLASSY.KISS原味低温款，别拿活菌系列。","卡士官网"),
(21,"食·主食乳品","可生食鲜鸡蛋","圣迪乐村","30枚/1.5kg，无沙门氏菌、无抗生素","谷粮喂养（养殖标准，非配料）","¥30–48/30枚，日常¥37–54","¥1.0–1.6/枚",{"jd":"¥36.95–54","tmall":"¥38–50","pdd":"¥30–45"},"拼多多","pass",90,80,"可生食里性价比相对好，等券后价买。","只吃熟蛋没必要买可生食，选京鲜生便宜一半。","京东/什么值得买"),
(22,"食·主食乳品","180°安心鲜鸡蛋","京鲜生","30枚/1.5kg（熟食标准，非可生食）","安心标准","¥24.9/30枚","¥0.83/枚",{"jd":"¥24.9","tmall":"¥25–28","pdd":"¥23–26"},"京东","pass",88,98,"只吃熟蛋选它，最便宜。","别拿它生食。","京东"),
(23,"食·主食乳品","八星雪花小麦粉","五得利","5kg，中筋","小麦粉","¥19.8–29.9/5kg","¥4–6/kg",{"jd":"¥19.8–29.9","tmall":"¥20–28","pdd":"¥18–26"},"拼多多","pass",95,90,"通用粉首选。","包子饺子用高筋款更便宜（下条）。","京东/什么值得买"),
(24,"食·主食乳品","高筋麦芯小麦粉","金龙鱼","5kg，高筋","小麦粉","¥13.4–16.4/5kg券后","¥2.7–3.3/kg",{"jd":"¥13.4–16.4","tmall":"¥14–18","pdd":"¥13–16"},"京东","pass",95,98,"高筋/包子饺子最便宜。","通用粉选五得利，高筋选这款。","京东/什么值得买"),
# ---- 衣 冬季 ----
(25,"衣·冬季","长款羽绒服（男180码）","雪中飞","充绒量245g，绒子含量90%白鸭绒，蓬松度640+","面料防风防泼水（以吊牌为准）","¥300–400","—",{"jd":"¥300–400","tmall":"¥320–400","pdd":"¥300–380"},"京东","pass",90,96,"300元档给到245g充绒，北方大部分城市过冬够用，波司登旗下。","0到-10℃主力档是充绒150–200g，这款245g更暖。","什么值得买，双11价"),
(26,"衣·冬季","短款羽绒服","鸭鸭","充绒量100g+，90%白鸭绒，蓬松度600+","—","¥300–400","—",{"jd":"¥300–380","tmall":"¥320–400","pdd":"¥300–360"},"京东","pass",88,90,"同价位充绒给得足，轻量通勤。","100g档是南方/初冬款，别指望它扛-10℃。","什么值得买"),
(27,"衣·冬季","轻薄短款羽绒服","波司登","充绒量不足100g，蓬松度680+","—","¥300左右","—",{"jd":"¥290–350","tmall":"¥300–380","pdd":"¥280–340"},"京东","pass",85,80,"蓬松度高但绒少，定位初冬和南方。","别当过冬主力买。","什么值得买"),
(28,"衣·冬季","极寒系列羽绒服","波司登","充绒量220–300g，90%鹅绒，蓬松度700–750+","—","好价¥800–950，吊牌¥2500+","—",{"jd":"¥800–950好价","tmall":"¥900–1200","pdd":"¥800–1000"},"京东","pass",92,88,"国产羽绒第一梯队，东北-20℃通勤够用。吊牌价别当真，蹲好价/奥莱。","只买极寒等硬核系列，避开轻薄商务款。","什么值得买/凤凰实测"),
(29,"衣·冬季","商务系列鹅绒服（175码）","波司登","充绒量86g，90%鹅绒，蓬松度700+","—","¥1999–2299（优惠后¥1999）","—",{"jd":"¥1999–2299","tmall":"¥1999–2299","pdd":"¥1900–2200"},"京东","reject",40,20,"充绒86g，绒钱不到¥50，卖¥2000+，是全表最坑的反面教材。","同品牌348元款充绒都比它多。","什么值得买/媒体报道"),
(30,"衣·冬季","100%纯羊毛衫 8105款","恒源祥","羊毛100%，重磅430g，半高领","羊毛100%","¥233.1券后（原价¥259）","—",{"jd":"¥233券后","tmall":"¥240–259","pdd":"¥220–250"},"京东","pass",95,88,"100%羊毛+重磅，券后价合理。","警惕非恒源祥的冒牌“羊毛衫”，只看吊牌羊毛100%。","京东/苏宁规格表"),
(31,"衣·冬季","100%新疆纯棉保暖内衣 2件装","红豆","棉100%，精梳棉","棉100%","¥59–64.9起，券后低至¥21.65","—",{"jd":"¥59–65","tmall":"¥59–70","pdd":"¥55–65"},"京东","pass",95,98,"100%棉，极致性价比。","保暖内衣只看棉100%，别买德绒/化纤混纺还卖高价的。","什么值得买/知乎2026推荐"),
(32,"衣·冬季","重磅194g/231g保暖内衣 2件装","三枪","棉100%（吊牌），194g/231g克重","棉100%","¥38.2–59券后，吊牌¥119–139","—",{"jd":"¥38–59","tmall":"¥45–65","pdd":"¥38–55"},"京东","caution",70,80,"成分基本过关，但同一款另有说法含“德绒纤维”，与100%棉冲突，以吊牌为准。","下单前截图吊牌成分，收到货先看吊牌再拆。","什么值得买/知乎"),
(33,"衣·冬季","MH100 保暖抓绒衣","迪卡侬","100%聚酯纤维，200g双面短绒，单穿7–15℃","聚酯纤维100%","¥69.9起","—",{"jd":"¥69.9起","tmall":"¥69–79","pdd":"¥65–75"},"京东","pass",90,96,"成分明确、价低、2万+评论。","抓绒衣不看品牌看克重，200g是保暖分水岭。","什么值得买/京东"),
# ---- 衣 日常 ----
(34,"衣·日常","EZY牛仔裤","优衣库","蓝色：82%棉、9%莱赛尔、8%聚酯、1%氨纶；黑色：70%棉","棉82%/70%","¥116–207券后，吊牌¥299","—",{"jd":"¥116–207","tmall":"¥149–199","pdd":"¥110–180"},"京东","caution",65,75,"非纯棉（82%棉），舒适但不合“纯棉”严格标准。","要100%棉选李维斯501，但贵3倍，自己权衡。","优衣库官网"),
(35,"衣·日常","501 Original 男士牛仔裤","李维斯","100%棉（部分水洗款99%棉+1%氨纶），非弹力","棉100%","约¥420–600（美官网$59–85）","—",{"jd":"价未核实","tmall":"¥500–700","pdd":"¥400–600"},"天猫","caution",95,45,"成分过关，但大陆价未核实、溢价高。","不急穿就等大促，¥300以下再入。","Levi's官网"),
(36,"衣·日常","旅步3代 PG7 缓震跑鞋","安踏","鞋面Sorona中空纱，PG7超临界发泡中底，约280g","—","吊牌¥399，券后¥214–244","—",{"jd":"¥214–244","tmall":"¥220–260","pdd":"¥200–240"},"京东","pass",88,92,"配置透明，吊牌399券后约220，通勤+慢跑。","别买无中底参数的杂牌跑鞋。","什么值得买/新浪"),
(37,"衣·日常","网面透气休闲跑步鞋","回力","网面透气，缓震/耐磨参数未核实","—","¥69–89","—",{"jd":"¥69–89","tmall":"¥69–89","pdd":"¥65–85"},"拼多多","caution",60,85,"最便宜，但缓震/耐磨不明，仅适合轻量通勤。","每天走1万步以上别选它。","什么值得买/唯品会"),
(38,"衣·日常","男士100%纯棉中筒袜 6双装","恒源祥","100%棉（弹性纤维除外），7A/10A抗菌","棉100%","¥31–33.3/6双，约¥5/双","—",{"jd":"¥31–33","tmall":"¥32–35","pdd":"¥29–33"},"京东","pass",95,96,"100%棉+抗菌，¥5/双左右。","袜子只看棉100%，别买涤纶袜。","什么值得买/京东"),
# ---- 行 ----
(39,"行","行李箱 20英寸 MJLXXPCRM","小米","全PC，Covestro PC，静音轮，20寸可登机","PC100%","¥219–269","—",{"jd":"¥219–269","tmall":"¥229–269","pdd":"¥219–259"},"京东","pass",95,96,"纯PC+登机合规，200元档首选。","同系列PP款便宜¥20但抗摔差，别贪。","小米官网/新浪实测"),
(40,"行","行李箱 20英寸 MJLXXPPRM","小米","PP（聚丙烯）箱壳，非PC，自重2.7kg","PP","¥199–214券后","—",{"jd":"¥199–214","tmall":"¥209–239","pdd":"¥198–220"},"京东","caution",70,80,"PP轻但抗摔不如PC。","托运多选PC款，只登机可买PP。","什么值得买/京东"),
(41,"行","TC-601 20英寸行李箱","外交官","PC+ABS vs 全PC说法冲突，扩充层+电脑仓，YKK拉链","以吊牌为准","¥274–299","—",{"jd":"¥274–299","tmall":"¥280–310","pdd":"¥270–300"},"京东","caution",70,75,"配置好，但材质说法不一，以吊牌为准。","收到货先看吊牌写PC还是PC+ABS。","新浪实测2026-09/10"),
(42,"行","全自动雨伞三折 10骨加固","天堂伞","10骨加固，全自动开收，晴雨两用","—","¥33.95–46.07","—",{"jd":"¥34–46","tmall":"¥35–46","pdd":"¥32–45"},"京东","pass",90,96,"10骨+全自动，价低量大，100万+评论。","雨伞只看骨数，8骨以下大风必翻。","什么值得买/京东"),
(43,"行","316不锈钢保温杯 500ml","富光","316/316L不锈钢内胆","316不锈钢","¥34.5–69.9，券后¥20.96–34.95","—",{"jd":"¥34.5–69.9","tmall":"¥35–60","pdd":"¥21–35券后"},"拼多多","pass",95,98,"三家中唯一明确316+价最低，极致性价比。","保温杯严格标准就是316，304款直接降级。","什么值得买/京东"),
(44,"行","JNL-503 保温杯 500ml","膳魔师","不锈钢，未核实316（JNL系列常规为304）","304不锈钢","¥45–87.9券后","—",{"jd":"¥45–88","tmall":"¥50–80","pdd":"¥45–75"},"京东","caution",60,50,"若坚持316标准不通过；仅304的话性价比不如富光。","品牌溢价买304，不如富光316。","什么值得买"),
(45,"行","经典商务双肩包2","小米","900D牛津布，双仓，18L，可放16寸电脑","牛津布","¥99","—",{"jd":"¥99","tmall":"¥99","pdd":"¥95–105"},"京东","pass",88,96,"¥99、耐磨、双仓。","通勤默认这款，轻量选同价轻量款570g。","小米商城2026-10"),
# ---- 住 家居 ----
(46,"住·家居","90%白鸭绒冬被 A类抑菌阻螨","水星家纺","绒子含量90%白鸭绒，A类，150×210cm","白鸭绒90%","¥368.59券后，吊牌¥1079","—",{"jd":"¥368.59券后","tmall":"¥380–450","pdd":"¥360–420"},"京东","pass",92,95,"90%绒+A类，券后368是性价比锚点。","被子只看绒子含量+蓬松度，别看“羽绒被”三个字。","什么值得买"),
(47,"住·家居","95%白鹅绒冬被","水星家纺","95%绒子含量，700+蓬松度，充绒650–1100g","白鹅绒95%","¥1899/150×210，区间¥1000–3000","—",{"jd":"¥1899","tmall":"¥1900–2500","pdd":"¥1800–2200"},"京东","pass",95,70,"95%+700蓬松度过关，预算够选它。","预算不够选90%鸭绒款，暖度差不到10%。","什么值得买/知乎2026双11"),
(48,"住·家居","93%泰国乳胶枕芯","水星家纺","93%泰国天然乳胶原液，A类，双侧高低，60×40cm","乳胶93%","¥59–179，¥103需买2件","—",{"jd":"¥59–179","tmall":"¥65–150","pdd":"¥59–120"},"京东","pass",92,92,"93%乳胶明确，59元档可入。","低于¥50还标93%乳胶的，大概率假。","什么值得买"),
(49,"住·家居","白骑士plus 床垫","喜临门","独立袋装弹簧+2cm乳胶+黄麻，1.5×2m厚22cm","弹簧+乳胶+黄麻","¥1264–1416券后，吊牌¥2399","—",{"jd":"¥1264–1416","tmall":"¥1300–1500","pdd":"¥1250–1400"},"京东","pass",90,90,"入门首选，独袋+乳胶+黄麻配置全。","床垫只看独袋弹簧+填充，别看品牌故事。","什么值得买"),
(50,"住·家居","光年护脊3.0 床垫","喜临门","独立袋装弹簧+黄麻，偏硬，1.5×2m厚21cm","弹簧+黄麻","¥904–1019券后","—",{"jd":"¥904–1019","tmall":"¥950–1100","pdd":"¥900–1000"},"京东","pass",88,94,"900元档入门，偏硬护脊。","腰不好、喜欢硬床选它；喜欢软床选白骑士。","什么值得买"),
(51,"住·家居","新曙光Pro 床垫","席梦思","独立袋装弹簧，具体乳胶/填充未核实","—","¥8830券后，吊牌¥14800","—",{"jd":"¥8830券后","tmall":"¥9000–12000","pdd":"¥8500–10000"},"京东","reject",50,15,"溢价8倍于喜临门同配置，无性价比。","同配置喜临门¥1264，别为牌子多花¥7500。","什么值得买"),
# ---- 住 日化 ----
(52,"住·日化","棉韧抽纸 3层100抽×20包","维达","100%原生木浆，无香","原生木浆100%","¥21.85，需买2件","¥1.09/包",{"jd":"¥21.85","tmall":"¥22–25","pdd":"¥20–24"},"京东","pass",95,90,"100%原生木浆，无香。","抽纸只看原生木浆，别买“原生浆”混淆词。","京东/什么值得买"),
(53,"住·日化","金装原木抽纸 3层100抽×24包","清风","原生木浆","原生木浆","¥17.4–23.9，需买3件，约¥0.74–0.9/包","—",{"jd":"¥17.4–23.9","tmall":"¥18–24","pdd":"¥17–22"},"京东","pass",95,98,"抽纸性价比最高。","囤货默认这款。","京东/什么值得买"),
(54,"住·日化","深层洁净洗衣液 3kg","蓝月亮","低泡易漂、去污因子（全成分需复核瓶身）","—","¥47.9；12斤套装¥48–53","¥16/kg",{"jd":"¥47.9","tmall":"¥48–55","pdd":"¥45–52"},"京东","pass",70,85,"基础款无香精噱头，性价比可接受；全成分需复核。日化没有食品那样“只有1–2种配料”的产品，按争议成分分级。","别买香氛款当日常，香精是日化最大争议源。","京东/什么值得买"),
(55,"住·日化","全优7效含氟牙膏 180g×3支","佳洁士","含氟防蛀（全成分未核实）","含氟","¥23.9券后","¥7.97/支",{"jd":"¥23.9","tmall":"¥24–28","pdd":"¥22–26"},"京东","pass",80,92,"含氟是有效防蛀成分，非争议添加剂。","牙膏只看含氟，别看美白/止血噱头。","京东/什么值得买"),
(56,"住·日化","卓效防蛀牙膏 套装","高露洁","氟化钠0.10%氟","含氟","¥19.9券后（90g×2+玫瑰盐120g×2）","—",{"jd":"¥19.9","tmall":"¥20–25","pdd":"¥18–22"},"京东","pass",80,96,"性价比最高含氟牙膏。","默认买这款。","京东/什么值得买"),
(57,"住·日化","留兰香型牙膏 125g×2支","云南白药","云南白药活性成分+氨甲环酸（处方止血药，2018年争议）","含氨甲环酸","¥19.4券后","¥9.7/支",{"jd":"¥19.4","tmall":"¥20–25","pdd":"¥18–22"},"京东","caution",55,70,"别当日常长期牙膏，牙龈出血请看牙医，不是牙膏能治的。","日常用含氟牙膏，这款只应急。","京东/163.com"),

]
def verdict_label(v):
    return {"pass":"✅ 通过","caution":"⚠️ 慎选","reject":"❌ 淘汰"}[v]
def esc(s): return html.escape(str(s))
products=[]
for r in P:
    products.append({"id":r[0],"cat":r[1],"name":r[2],"brand":r[3],"spec":r[4],"ingredients":r[5],"price":r[6],"unit":r[7],"platforms":r[8],"best":r[9],"verdict":r[10],"clean":r[11],"value":r[12],"reason":r[13],"tip":r[14],"source":r[15]})
os.makedirs(os.path.join(BASE,"data"),exist_ok=True)
with open(os.path.join(BASE,"data","products.json"),"w",encoding="utf-8") as f:
    json.dump({"updated":"2026-11-10 v3","count":len(products),"note":"价格为2026-11-10京东/天猫/拼多多检索快照，券后价波动大，下单以实时页为准。配料/材质以包装吊牌为准。","products":products},f,ensure_ascii=False,indent=2)
# Build static HTML: every product as markup, JS only filters
cats=sorted(set(p["cat"] for p in products))
def card(p):
    plats=" ".join('<span class="plat"><b>%s</b> %s</span>'%(esc(k),esc(v)) for k,v in p["platforms"].items())
    # search links
    from urllib.parse import quote
    q=quote(p["brand"]+" "+p["name"])
    links='<a href="https://search.jd.com/Search?keyword=%s" target="_blank" rel="noopener">京东搜</a> <a href="https://s.taobao.com/search?q=%s" target="_blank" rel="noopener">淘宝搜</a> <a href="https://mobile.yangkeduo.com/search_result.html?search_key=%s" target="_blank" rel="noopener">拼多多搜</a>'%(q,q,q)
    return '''<article class="card" data-cat="%s" data-verdict="%s" data-clean="%d" data-value="%d" data-name="%s %s %s">
<h3>%s <span class="brand">%s</span></h3>
<p class="verdict %s">%s · 清洁度 %d/100 · 性价比 %d/100 · 最低价平台：%s</p>
<p><b>规格：</b>%s</p>
<p><b>配料/材质：</b>%s</p>
<p><b>价格区间：</b>%s <span class="meta">（%s）</span></p>
<p><b>各平台价：</b><br>%s</p>
<p><b>为什么：</b>%s</p>
<p><b>买法：</b>%s</p>
<p class="meta">来源：%s · %s</p>
<p>%s <button class="fav" data-id="%d">☆ 收藏</button></p>
</article>'''%(esc(p["cat"]),p["verdict"],p["clean"],p["value"],esc(p["name"]),esc(p["brand"]),esc(p["ingredients"]),esc(p["name"]),esc(p["brand"]),p["verdict"],verdict_label(p["verdict"]),p["clean"],p["value"],esc(p["best"]),esc(p["spec"]),esc(p["ingredients"]),esc(p["price"]),esc(p["unit"]),plats,esc(p["reason"]),esc(p["tip"]),esc(p["source"]),"2026-11-10快照",links,p["id"])
cards="\n".join(card(p) for p in products)
cat_btns="".join('<button data-cat="%s">%s</button>'%(esc(c),esc(c)) for c in cats)
html_doc='''<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>严选清单 Strict Picks — 配料干净、极致性价比</title>
<meta name="description" content="衣食住行严格筛选：只看配料表和材质吊牌，品牌大、配方干净、性价比最高。酱油、食用油、羽绒服、牛奶、行李箱、保温杯等57款已核实示例 + 联网现查。">
<style>*{box-sizing:border-box}body{margin:0;background:#fff;color:#111;font-family:-apple-system,"PingFang SC","Microsoft YaHei",sans-serif;font-size:16px;line-height:1.55}.wrap{max-width:980px;margin:0 auto;padding:16px}h1{font-size:26px;margin:8px 0 4px}h2{font-size:19px;margin:22px 0 8px}.sub{color:#555}.box{background:#fff8e1;border:1px solid #ffe082;border-radius:8px;padding:10px 12px;font-size:14px}.controls{display:flex;flex-wrap:wrap;gap:8px;margin:12px 0}.controls input,.controls select{font-size:16px;padding:10px;border:1px solid #999;border-radius:8px;background:#fff;color:#111}.controls input{flex:1 1 220px}button{font-size:14px;padding:8px 14px;border-radius:20px;border:1px solid #999;background:#fff;color:#111;cursor:pointer}button.on{background:#111;color:#fff}.card{border:1px solid #ddd;border-radius:8px;padding:12px;margin:10px 0}.card h3{margin:0 0 6px;font-size:17px}.brand{color:#555;font-size:14px}.verdict{font-weight:bold}.verdict.pass{color:#0a7d0a}.verdict.caution{color:#b26a00}.verdict.reject{color:#b00020}.meta{color:#555;font-size:13px}.plat{display:inline-block;background:#f2f2f2;border-radius:6px;padding:2px 8px;margin:2px 4px 2px 0;font-size:13px}.fav{border-radius:8px}.foot{color:#777;font-size:13px;margin:24px 0}a{color:#0b57d0}</style></head>
<body><div class="wrap">
<h1>严选清单 <span style="font-size:16px;color:#555">Strict Picks</span></h1>
<p class="sub"><b>搜产品，不是翻清单。</b>在上面输入产品名，系统自己去联网查，按三个依据筛：<b>①配料/材质是绝对前提</b>（不过关直接淘汰，未知也不能算通过）；<b>②品牌力</b>（只认大品牌）；<b>③价格区间</b>（你设的区间之外不推荐）。下面 57 款只是已核实示例库，供参考，不是搜索结果——新产品不靠我手动加，靠你搜出来、系统现查。</p>
<div class="box"><b>硬标准（食品）：</b>配料≤6种、0防腐剂/甜味剂/味精/焦糖色/增味剂、酱油氨基酸态氮≥0.8（特级）、非转基因、酿造工艺。<b>（衣服）：</b>绒子含量≥90%、充绒量按场景（南方100g/城市150–200g/北方220g+）、蓬松度≥600、羊毛/棉100%才算通过。<b>（住行）：</b>保温杯316不锈钢、行李箱纯PC、被子绒子含量≥90%。<br><b>品牌力：</b>酱油只认海天/千禾/李锦记/厨邦/胖东来等，羽绒服只认波司登/鸭鸭/雪中飞/高梵等，杂牌、白牌直接降级。<b>价格区间：</b>在搜索框下面设最低/最高价，超出不推荐。<br><b>价格提醒：</b>淘宝/拼多多/京东没有公开免费比价接口，本站不爬平台、不保证实时价。手动刷新会重新拉取本站最新数据文件；各平台实时价请点每款下面的“京东搜 / 淘宝搜 / 拼多多搜”一键比价，以实时页为准。</div>
<p><b>数据更新：</b><span id="upd">2026-11-10 内置快照</span> · <button id="refresh">↻ 手动刷新最新数据</button> <span id="refmsg"></span></p>
<div class="controls"><input type="search" id="q" placeholder="搜：酱油、羽绒服、牛奶、316、90%绒…"><select id="sort"><option value="value">性价比最高先</option><option value="clean">清洁度最高先</option><option value="pass">只看通过</option><option value="name">名称 A–Z</option></select><label style="align-self:center"><input type="checkbox" id="favOnly"> 只看我的收藏</label></div>
<div class="controls" id="cats"><button data-cat="" class="on">全部</button>__CATS__</div>
<div class="controls" id="plats"><button data-plat="" class="on">全部平台</button><button data-plat="京东">京东最便宜</button><button data-plat="拼多多">拼多多最便宜</button><button data-plat="天猫">天猫最便宜</button></div>
<div class="box" id="liveBox" style="background:#eef6ff;border-color:#90caf9">
<b>🔎 联网查新品（本地没有就自动查）</b><br>
<span id="liveStatus">在上面搜索框输入产品名（如 蚝油、冲锋衣、洗面奶），本地 0 结果时会自动联网查；也可以直接点下面按钮手动查。</span><br>
<label style="display:block;margin:6px 0"><input type="checkbox" id="brandOnly" checked> 只看大品牌（品牌力是筛选依据，杂牌/白牌直接降级）</label>
<label>价格区间：¥ <input id="priceMin" type="number" min="0" style="width:80px;padding:6px" placeholder="最低"> – ¥ <input id="priceMax" type="number" min="0" style="width:80px;padding:6px" placeholder="最高"> <span class="meta">留空=不限；超出区间的不推荐</span></label><br>
<button id="liveBtn">联网查这个产品</button> <button id="openAllBtn">一键打开京东 / 淘宝 / 拼多多 / 什么值得买</button>
<div id="liveResults"></div>
<h3 style="margin:12px 0 6px">粘贴配料表 / 材质，自动评分（从平台页面复制过来）</h3>
<textarea id="pasteBox" rows="3" style="width:100%;font-size:15px" placeholder="例：水、非转基因黄豆、小麦、食用盐"></textarea><br>
<input id="pasteName" style="font-size:15px;padding:8px" placeholder="产品名（必填，如 千禾蚝油）"> <input id="pastePrice" style="font-size:15px;padding:8px" placeholder="价格，如 ¥12.9/500ml"> <button id="scoreBtn">自动评分并存为待核实收藏</button>
<p class="meta">评分规则：出现谷氨酸钠/苯甲酸钠/三氯蔗糖/焦糖色/呈味核苷酸二钠/山梨酸钾/香精/增稠剂，每种扣分；配料≤6种加分。结果是“待核实”，不是已核实入库。</p>
<h3 style="margin:12px 0 6px">我的待核实收藏 <span class="meta" id="pendingCount"></span></h3>
<div id="pendingList"></div>
</div>
<h2>已核实示例库 <span class="meta" id="count"></span></h2><p class="meta">下面 57 款是之前已核实的示例，供参考。想找的产品不在里面？用上面搜索框搜，系统现查，不靠我手动加。</p>
<div id="list">__CARDS__</div>
<p class="foot">方法：配料/材质以包装吊牌为准，价格为检索快照区间，券后价波动大。淘汰≠不能吃/不能穿，是同价有更干净、更值的选择。数据文件：<a href="data/products.json">data/products.json</a>（AI 可直接读）。仓库：github.com/Z88666/strict-picks</p>
</div>
<script>
var favs={}; try{favs=JSON.parse(localStorage.getItem("strict-picks-favs")||"{}")}catch(e){favs={}}
function applyFav(){var b=document.querySelectorAll(".fav");for(var i=0;i<b.length;i++){var id=b[i].getAttribute("data-id");b[i].textContent=favs[id]?"★ 已收藏":"☆ 收藏"}}
function bindFav(){var b=document.querySelectorAll(".fav");for(var i=0;i<b.length;i++){b[i].onclick=function(){var id=this.getAttribute("data-id");if(favs[id]){delete favs[id]}else{favs[id]=1}try{localStorage.setItem("strict-picks-favs",JSON.stringify(favs))}catch(e){}applyFav();filter()}}}
function filter(){var q=(document.getElementById("q").value||"").toLowerCase();var cat="";var cb=document.querySelectorAll("#cats button.on");if(cb.length)cat=cb[0].getAttribute("data-cat");var plat="";var pb=document.querySelectorAll("#plats button.on");if(pb.length)plat=pb[0].getAttribute("data-plat");var favOnly=document.getElementById("favOnly").checked;var sort=document.getElementById("sort").value;var cards=document.querySelectorAll("#list .card");var shown=0;var arr=[];for(var i=0;i<cards.length;i++)arr.push(cards[i]);if(sort==="value")arr.sort(function(a,b){return b.getAttribute("data-value")-a.getAttribute("data-value")});if(sort==="clean")arr.sort(function(a,b){return b.getAttribute("data-clean")-a.getAttribute("data-clean")});if(sort==="name")arr.sort(function(a,b){return a.getAttribute("data-name")<b.getAttribute("data-name")?-1:1});var list=document.getElementById("list");for(var j=0;j<arr.length;j++)list.appendChild(arr[j]);for(var k=0;k<arr.length;k++){var c=arr[k];var ok=true;if(cat&&c.getAttribute("data-cat")!==cat)ok=false;if(sort==="pass"&&c.getAttribute("data-verdict")!=="pass")ok=false;if(favOnly&&!favs[c.querySelector(".fav").getAttribute("data-id")])ok=false;if(plat&&c.textContent.indexOf("最低价平台："+plat)<0)ok=false;if(q&&c.getAttribute("data-name").toLowerCase().indexOf(q)<0&&c.textContent.toLowerCase().indexOf(q)<0)ok=false;c.style.display=ok?"":"none";if(ok)shown++}document.getElementById("count").textContent="共 "+arr.length+" 款，显示 "+shown+" 款";var _q=(document.getElementById("q").value||"").trim();if(_q.length>=2&&shown===0){if(typeof _liveTimer!=="undefined"&&_liveTimer)clearTimeout(_liveTimer);_liveTimer=setTimeout(function(){if(lastLiveQ!==_q)liveSearch(_q)},800)}}
document.getElementById("q").oninput=filter;document.getElementById("sort").onchange=filter;document.getElementById("favOnly").onchange=filter;
function bindBtns(id){var bs=document.querySelectorAll(id+" button");for(var i=0;i<bs.length;i++){bs[i].onclick=function(){var s=this.parentNode.querySelectorAll("button");for(var j=0;j<s.length;j++)s[j].className="";this.className="on";filter()}}}
bindBtns("#cats");bindBtns("#plats");
document.getElementById("refresh").onclick=function(){var m=document.getElementById("refmsg");m.textContent="正在拉取最新数据…";var x=new XMLHttpRequest();x.open("GET","data/products.json?ts="+new Date().getTime(),true);x.onreadystatechange=function(){if(x.readyState!==4)return;if(x.status===200){try{var d=JSON.parse(x.responseText);document.getElementById("upd").textContent="已刷新："+d.updated+"，共 "+d.products.length+" 款（数据文件最新版）";m.textContent="已刷新到最新数据文件。如价格有变，请点各款的平台搜索链接核对实时价。"}catch(e){m.textContent="数据文件解析失败，仍用内置快照。"}}else{m.textContent="拉取失败（离线或未发布），仍显示内置快照，内容不变。"}};x.send()};

var RED=["谷氨酸钠","味精","苯甲酸钠","山梨酸钾","三氯蔗糖","安赛蜜","焦糖色","呈味核苷酸二钠","5'-呈味核苷酸二钠","羟丙基二淀粉磷酸酯","食用香精","香精","增稠剂","脱脂大豆","水解植物蛋白"];
function escHtml(s){return String(s).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/>/g,"&gt;")}
function pricesIn(text){var m=String(text).match(/¥\s*\d+(\.\d+)?/g);return m?m.slice(0,8).join("、"):"未提到"}
function redIn(text){var f=[];for(var i=0;i<RED.length;i++){if(text.indexOf(RED[i])>=0)f.push(RED[i])}return f}
function platCards(q){var e=encodeURIComponent(q);return '<div class="card"><h3>四平台实时比价（点开是实时页）</h3><p>本站没有淘宝/京东/拼多多的公开比价接口，也爬不动它们的反爬页面，所以实时价以下面打开的页面为准。下面 4 张卡是同一关键词在 4 个平台的实时搜索：</p><p><b>京东：</b><a href="https://search.jd.com/Search?keyword='+e+'" target="_blank" rel="noopener">京东搜 '+escHtml(q)+'</a><br><b>淘宝/天猫：</b><a href="https://s.taobao.com/search?q='+e+'" target="_blank" rel="noopener">淘宝搜 '+escHtml(q)+'</a><br><b>拼多多：</b><a href="https://mobile.yangkeduo.com/search_result.html?search_key='+e+'" target="_blank" rel="noopener">拼多多搜 '+escHtml(q)+'</a><br><b>什么值得买：</b><a href="https://search.smzdm.com/?s='+e+'" target="_blank" rel="noopener">什么值得买搜 '+escHtml(q)+'</a></p><p class="meta">比价方法：同一规格（如 500ml / 5L）看券后价，再除以规格算单价，最便宜的那个平台下单。</p></div>'}
function fetchTimeout(url,ms){return new Promise(function(res,rej){var to=setTimeout(function(){rej(new Error("timeout"))},ms);fetch(url).then(function(r){clearTimeout(to);res(r)}).catch(function(e){clearTimeout(to);rej(e)})})}
var lastLiveQ="";
function liveSearch(q){if(!q||q.length<2)return;lastLiveQ=q;var box=document.getElementById("liveResults");var st=document.getElementById("liveStatus");document.getElementById("liveBox").style.display="";st.textContent="正在联网查“"+q+"”…（维基百科 + DuckDuckGo + 代理抓取，三路并行，8 秒超时）";box.innerHTML=platCards(q);
var wiki=fetchTimeout("https://zh.wikipedia.org/w/api.php?action=query&list=search&srsearch="+encodeURIComponent(q)+"&format=json&origin=*&srlimit=5",8000).then(function(r){return r.json()}).catch(function(){return null});
var ddg=fetchTimeout("https://api.duckduckgo.com/?q="+encodeURIComponent(q+" 配料表 价格")+"&format=json&no_html=1&skip_disambig=1",8000).then(function(r){return r.json()}).catch(function(){return null});
var proxy=fetchTimeout("https://api.allorigins.win/get?url="+encodeURIComponent("https://lite.duckduckgo.com/lite/?q="+encodeURIComponent(q+" 价格")),8000).then(function(r){return r.json()}).catch(function(){return null});
Promise.all([wiki,ddg,proxy]).then(function(rs){var html="";var allText=q;
if(rs[0]&&rs[0].query&&rs[0].query.search){var s=rs[0].query.search;for(var i=0;i<s.length;i++){var sn=s[i].snippet.replace(/<[^>]+>/g,"");allText+=" "+sn;html+='<div class="card"><h3>维基百科：'+escHtml(s[i].title)+'</h3><p>'+escHtml(sn)+'</p><p><a href="https://zh.wikipedia.org/wiki/'+encodeURIComponent(s[i].title)+'" target="_blank" rel="noopener">打开维基百科</a></p></div>'}}
if(rs[1]&&(rs[1].AbstractText||(rs[1].RelatedTopics&&rs[1].RelatedTopics.length))){var at=rs[1].AbstractText||"";allText+=" "+at;if(at)html+='<div class="card"><h3>DuckDuckGo 摘要</h3><p>'+escHtml(at)+'</p><p><a href="'+escHtml(rs[1].AbstractURL||"https://duckduckgo.com/?q="+encodeURIComponent(q))+'" target="_blank" rel="noopener">打开来源</a></p></div>';var rt=rs[1].RelatedTopics||[];for(var j=0;j<Math.min(rt.length,3);j++){if(rt[j].Text){allText+=" "+rt[j].Text;html+='<div class="card"><h3>相关：'+escHtml(rt[j].Text.slice(0,40))+'</h3><p>'+escHtml(rt[j].Text)+'</p></div>'}}}
if(rs[2]&&rs[2].contents){var c=rs[2].contents;var links=c.match(/<a[^>]+class="result-link"[^>]*>[^<]+<\/a>/g)||[];var prices=pricesIn(c.replace(/<[^>]+>/g," "));if(links.length){html+='<div class="card"><h3>网页搜索结果（经代理抓取）</h3><p>文中提到价格：'+escHtml(prices)+'</p><p>'+links.slice(0,5).join("<br>")+'</p></div>'}else{html+='<div class="card"><h3>网页搜索（代理）</h3><p>代理返回了内容但没解析出结果链接，请直接点上面四平台链接。</p></div>'}}
var reds=redIn(allText);
var BIG=["海天","千禾","李锦记","厨邦","胖东来","鲁花","金龙鱼","伊利","蒙牛","光明","三元","简爱","卡士","十月稻田","柴火大院","波司登","鸭鸭","雪中飞","高梵","恒源祥","红豆","三枪","安踏","李宁","迪卡侬","骆驼","伯希和","小米","外交官","富光","膳魔师","虎牌","水星家纺","罗莱","喜临门","维达","清风","蓝月亮","佳洁士","高露洁","天堂伞"];
var brandHit="";for(var bi=0;bi<BIG.length;bi++){if(allText.indexOf(BIG[bi])>=0||q.indexOf(BIG[bi])>=0){brandHit=BIG[bi];break}}
var brandOnly=document.getElementById("brandOnly").checked;
var pMin=parseFloat(document.getElementById("priceMin").value||"0");var pMax=parseFloat(document.getElementById("priceMax").value||"0");
var priceTxt=pricesIn(allText);var priceNums=(priceTxt.match(/\d+(\.\d+)?/g)||[]).map(Number);
var priceOk=true;if(priceNums.length&&(pMax>0)&&(priceNums[0]>pMax||priceNums[priceNums.length-1]<pMin))priceOk=false;
var verdict,verdictWhy;
if(reds.length){verdict="❌ 淘汰";verdictWhy="绝对前提不通过：摘要/配料里发现红线词 "+reds.join("、")+"。配料/材质是绝对前提，有红线就直接淘汰，不看品牌和价格。"}
else if(!brandHit&&brandOnly){verdict="⚠️ 品牌力不足（待核实）";verdictWhy="联网摘要里没认出大品牌。品牌力是筛选依据，只认大品牌；杂牌/白牌不推荐，除非你取消“只看大品牌”再查。"}
else if(!priceOk){verdict="⚠️ 价格区间外";verdictWhy="文中提到的价格超出你设的区间（¥"+(pMin||0)+"–¥"+(pMax||"不限")+"），不推荐。"}
else{verdict="⚠️ 待核实（不能算通过）";verdictWhy="绝对前提未满足：联网摘要里没有完整配料表/材质吊牌。没有配料表就不能算通过。下一步：点上面平台链接，打开商品页复制完整配料表，用下面“粘贴配料表自动评分”核对，通过了才能存为通过。"}
html='<div class="card"><h3>联网查询小结：'+escHtml(q)+' — '+verdict+'</h3><p><b>品牌力：</b>'+(brandHit?("认出大品牌："+escHtml(brandHit)):"未认出大品牌")+'（只看大品牌：'+(brandOnly?"开":"关")+'）<br><b>价格区间：</b>你设的 ¥'+(pMin||0)+'–¥'+(pMax||"不限")+'；文中提到价格：'+escHtml(priceTxt)+'<br><b>配料/材质（绝对前提）：</b>'+(reds.length?("发现红线词 "+escHtml(reds.join("、"))):"摘要里无完整配料表，未知=不能通过")+'<br><b>结论：</b>'+verdictWhy+'</p><p><button class="saveLiveBtn" data-q="'+escHtml(q)+'">存为待核实收藏</button> <a href="https://github.com/Z88666/strict-picks/issues/new?title='+encodeURIComponent("求核实："+q)+'&body='+encodeURIComponent("请核实并入库："+q+"。配料/材质：\\n价格（京东/淘宝/拼多多）：\\n来源链接：")+'" target="_blank" rel="noopener">提交到 GitHub Issue 求核实入库</a></p></div>'+html+platCards(q);
box.innerHTML=html;var sb=box.querySelector('.saveLiveBtn');if(sb){sb.onclick=function(){savePending(this.getAttribute('data-q'),'','')}};st.textContent="联网查完“"+q+"”（"+new Date().toLocaleTimeString()+"）。上面是摘要+四平台实时链接，价格以打开的平台页为准。"});
}
function getPending(){try{return JSON.parse(localStorage.getItem("strict-picks-pending")||"[]")}catch(e){return[]}}
function renderPending(){var list=getPending();var el=document.getElementById("pendingList");document.getElementById("pendingCount").textContent="共 "+list.length+" 条";if(!list.length){el.innerHTML='<p class="meta">暂无。联网查到、或粘贴评分过的产品会存在这里，只在你本机。</p>';return}var h="";for(var i=0;i<list.length;i++){h+='<div class="card"><h3>'+escHtml(list[i].name)+' <span class="meta">待核实 · '+escHtml(list[i].score||"")+'</span></h3><p><b>配料/材质：</b>'+escHtml(list[i].ing||"未填")+'</p><p><b>价格：</b>'+escHtml(list[i].price||"未填")+'</p><p class="meta">'+escHtml(list[i].time||"")+'</p><p><button data-i="'+i+'" class="delPend">删除</button></p></div>'}el.innerHTML=h;var bs=el.querySelectorAll(".delPend");for(var j=0;j<bs.length;j++){bs[j].onclick=function(){var arr=getPending();arr.splice(parseInt(this.getAttribute("data-i")),1);try{localStorage.setItem("strict-picks-pending",JSON.stringify(arr))}catch(e){}renderPending()}}}
function savePending(name,price,ing){var arr=getPending();arr.unshift({name:name,price:price,ing:ing,score:"待核实",time:new Date().toLocaleString()});try{localStorage.setItem("strict-picks-pending",JSON.stringify(arr))}catch(e){}renderPending();document.getElementById("liveStatus").textContent="已存为待核实收藏："+name}
document.getElementById("liveBtn").onclick=function(){var q=(document.getElementById("q").value||"").trim();if(!q){alert("先在搜索框输入产品名，例如 蚝油、冲锋衣");return}liveSearch(q)};
document.getElementById("openAllBtn").onclick=function(){var q=(document.getElementById("q").value||"").trim()||lastLiveQ;if(!q){alert("先输入产品名");return}var e=encodeURIComponent(q);window.open("https://search.jd.com/Search?keyword="+e,"_blank");window.open("https://s.taobao.com/search?q="+e,"_blank");window.open("https://mobile.yangkeduo.com/search_result.html?search_key="+e,"_blank");window.open("https://search.smzdm.com/?s="+e,"_blank")};
document.getElementById("scoreBtn").onclick=function(){var name=(document.getElementById("pasteName").value||"").trim();var ing=(document.getElementById("pasteBox").value||"").trim();var price=(document.getElementById("pastePrice").value||"").trim();if(!name||!ing){alert("产品名和配料表都要填");return}var parts=ing.split(/、|，|,|；|;|\\n/).filter(function(s){return s.trim()});var reds=redIn(ing);var score=100-Math.max(0,parts.length-6)*5-reds.length*15;if(score<0)score=0;var v=score>=85?"✅ 通过（待核实）":score>=60?"⚠️ 慎选（待核实）":"❌ 淘汰（待核实）";var arr=getPending();arr.unshift({name:name,price:price,ing:ing,score:v+" 清洁度约 "+score+"/100，配料 "+parts.length+" 种，红线词："+(reds.join("、")||"无"),time:new Date().toLocaleString()});try{localStorage.setItem("strict-picks-pending",JSON.stringify(arr))}catch(e){}renderPending();document.getElementById("liveStatus").textContent="已评分并存为待核实收藏："+name+"，"+v};
var _liveTimer=null;
renderPending();
applyFav();bindFav();filter();
</script></body></html>'''.replace('__CATS__',cat_btns).replace('__CARDS__',cards)
with open(os.path.join(BASE,"index.html"),"w",encoding="utf-8") as f: f.write(html_doc)
print("products",len(products),"html bytes",len(html_doc))
