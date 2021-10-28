import re
import textwrap

import news.crawlers.db.schema
import news.crawlers.util.normalize
import news.crawlers.util.request_url
import news.parse.db.schema
import news.parse.epochtimes


def test_parsing_result() -> None:
    r"""Ensure parsing result consistency."""
    company_id = news.crawlers.util.normalize.get_company_id(company='大紀元')
    url = r'https://www.epochtimes.com/b5/20/10/10/n12466941.htm'
    response = news.crawlers.util.request_url.get(url=url)

    raw_news = news.crawlers.db.schema.RawNews(
        company_id=company_id,
        raw_xml=news.crawlers.util.normalize.compress_raw_xml(
            raw_xml=response.text,
        ),
        url_pattern=news.crawlers.util.normalize.compress_url(
            company_id=company_id,
            url=url,
        )
    )

    parsed_news = news.parse.epochtimes.parser(raw_news=raw_news)

    assert parsed_news.article == re.sub(
        r'\n',
        '',
        textwrap.dedent(
            '''\
            據明慧網不完全統計,截至2019年2月1日,僅大連地區,至少有185人遭遇厄運,他們都曾
            迫害過法輪功學員。 他們中有病亡、自殺、罹患癌症的,有的被判死刑、無期徒刑、被
            逮捕、審查、禍及家人等等。 自中共1999年開始迫害法輪功以來,遼寧省大連市成為迫害
            最嚴重的地區之一。截至2018年4月25日,大連地區被迫害致死的法輪功學員
            至少有一百四十多名。 接上文:大連近兩百人遭厄運 都曾迫害法輪功(5)
             94. 亮甲店前任派出所所長叢長嶺出車禍撞斷兩腿 叢長嶺在任職期間賣力迫害當地
             法輪功學員,抄家,毒打他們。在零下十幾度寒冷的冬天,他將去北京為法輪功上訪而被綁架
             回來的兩位女學員的鞋子脫掉,讓她們光著腳站在水泥地上,以致腳被凍腫
             ;還將一個女學員送到馬三家非法勞教。 2000年,中共召開「人大會議」期間,叢長嶺又把
             當地14名法輪功學員送到金州區北三里非法拘留15天。當地法輪功學員曲蘋就是被他們
             迫害離世的。 叢長嶺被調到大連登沙河派出所,在一次車禍中,他的兩條腿當場被撞斷
             。 95. 瓦房店公安局政經保大隊警察高士雲患上多種疾病 高士雲曾是瓦房店公安局
             政經保大隊警察、「610」(專門迫害法輪功的非法組織)的主要成員。 2000年10月份
             ,法輪功學員崔德軍、高卓夫妻被綁架,高士雲先是解下崔德軍的軍用皮帶,抽打他,僅兩下
             就把皮帶抽折了;又找來一根一米來長、拇指粗的實心塑料棍,猛抽崔德軍的頭部,抽了
             2個多小時。同年11月份,法輪功學員柳忠堯被綁架,高士雲等將其頭、臉打變了形
             。 高士雲患有心臟病、腎病、腿浮腫、皮膚病等多種疾病。 96. 金州區公安局長
             馬仕俊患腦血栓 馬仕俊,原大連金州區公安局長,曾任瓦房店市公安局局長,在任職期間
             積極參與迫害法輪功。在馬仕俊指使下,金州區警察採取監視、跟蹤、電話騷擾、綁架
             、非法拘留等手段迫害法輪功學員。 截止2000年12月份,金州區有幾百名法輪功學員
             被非法拘留、判刑、勞教。馬仕俊是金州區迫害法輪功的元凶。 終究馬仕俊得了腦血栓
             ,不能行走。 97. 西崗分局政經保科副科長李體健獲刑 李體健在任職期間非常賣力地
             抓捕法輪功學員,曾揚言:如他說了算,就要把法輪功學員都扔到虎籠子裡去。法輪功學員
             曲淑梅進京為法輪功說句公道話,被大連市西崗區公安分局非法拘留一個月,扣押現金
             3.6萬,並失去工作。當時非法抓捕她的主謀就是李體健。 李體健被判7年徒刑
             ,並得了癌症。 98. 金州區公安局亮甲店派出所警察李廣敏撞斷了腿 李廣敏,三十八歲
             左右,積極參與迫害法輪功。2000年5月中旬,綁架王姓女法輪功學員到亮甲店派出所
             ,殘忍地用電棍電她。不到一個星期,李廣敏騎摩托車出了車禍,把腿撞斷
             。 99. 東電二公司公安處處長韓國權患病長瘤 韓國權任職期間曾非法開除陳萬
             、王賓華、鄭豔榮、丁德福、任雅芝等五名法輪功學員,其中三名法輪功學員從
             1999年7月20日迫害開始到被非法開除,工資分文沒給。 韓國權後因經濟貪污而撤職
             ,發現肝上已長瘤,年僅五十多歲。 100. 舉報三位法輪功學員遭厄運 張偉,女,29歲
             ,於2001年10月12日舉報莊河市長勝村三位法輪功學員,使三人非法拘留,每人被勒索
             5,000元。結果第二天張偉的嘴就歪了。她丈夫開車為給她治病,把人給撞壞了,賠了
             4,000元,給她治病花了三四千元,共花了七千多元錢。 101. 大連市金州區村治保
             劉迎春得怪病 劉迎春任職期間多次撕毀法輪功真相黏貼、塗抹真相標語。法輪功學員
             勸他,他也不聽。後來劉迎春得了一種病,小便不能正常排泄,到醫院做了手術,必須通過
             導管往外排泄。 102. 金州區八里村民摔成粉碎性骨折 大連市金州區八里村有一村民
             ,聽信中共對法輪功的造謠謊言,對法輪功學員講的真相一直不接受。一天她和鄰居閒談時
             ,鄰居在看撿到的法輪功真相資料,她一把抓過來,給扔到了廁所裡。倆人分手後,鄰居
             就聽到一聲「哎呀」,原來她剛走出不遠就摔倒在地,到醫院診斷為粉碎性骨折,住了
             四十多天的醫院,花了大約1萬多元錢。 103. 遼寧省地質勘查院書記王節剛患胃癌
              王節剛是位於大連市金州區的遼寧省地質勘查院書記,多方面刁難單位的法輪功學員
              ,曾經非法扣掉法輪功學員的3年退休金。法輪功學員去要,他只給最低的生活費
              。有的法輪功學員竟被開除。 104. 金州區市民宮振花胳膊摔斷 宮振花,六十多歲
              ,每月獲得200多元錢去幹昧著良心的事,惡意舉報法輪功學員貼真相
              。 105. 大連馬欄街道居民委書記陳蓮香患兩種癌症 陳蓮香挨家挨戶逼迫法輪功學員
              放棄修煉,查抄法輪功書籍。有法輪功學員被抓到派出所,她整夜看守迫害,後來得了
              乳腺癌、淋巴癌,一個月做兩次手術。 106. 沙河口區富國街派出所副所長李傳東患瘤
               李傳東不遺餘力地迫害法輪功,到法輪功學員家中抄家,連電腦鍵盤、滑鼠、信紙
               都不放過,並且製造假現場,栽贓陷害法輪功學員,結果他自己腦袋上長個瘤子
               。 107. 大連市金石灘梨樹房屯村民姚作本患胃癌晚期 馬菊花及其丈夫姚作本參與
               迫害法輪功學員,對他們進行蹲坑、跟蹤、窺探等,還晚上出來監視。姚作本患胃癌晚期
               。 108. 原遼寧大連市教委主任賈聚林患直腸癌 賈聚林(音)剋扣各校的十幾名
               法輪功學員被非法勞教期間的工資,至今沒退還。後身患直腸癌,飽受痛苦
               。 109. 大連市普蘭店墨盤鄉一村長王某遭厄運 王某積極配合中共監視迫害法輪功
               學員,見到法輪功學員貼的真相條幅就撕,影響極壞。2007年2月17日晚
               (即大年三十晚),他在放爆竹時,爆竹直奔其右眼飛去,導致眼出血
               。 天網恢恢 疏而不漏 天網恢恢,疏而不漏。《太上感應篇》有云:「禍福無門
               ,惟人自召;善惡之報,如影隨形。」 明慧網評論員唐恩表示,「因果報應的鮮明實例
               ,值得人們深思。那些仍在參與迫害法輪功學員的各級人員,唯有趕快懸崖勒馬
               ,停止迫害,才能彌補罪愆、贖罪自救。」
            '''
        ),
    )
    assert parsed_news.category is None
    assert parsed_news.company_id == company_id
    assert parsed_news.timestamp == 1602259200
    assert parsed_news.reporter is None
    assert parsed_news.title == '大連近兩百人遭厄運 都曾迫害法輪功'
    assert parsed_news.url_pattern == '20-10-10-12466941'
