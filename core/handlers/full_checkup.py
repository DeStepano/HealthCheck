from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import json
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from core.keyboards import keyboards
from core.sql_utils import insert_array, get_array, get_data_by_id, insert_data
from core.config import config
from core.rcp_client import rpcClient
from core.states import States


class Form3(StatesGroup):
    q1 = State()
    q2 = State()


class Form4(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()


class Form5(StatesGroup):
    q1 = State()
    q2 = State()
    q3 = State()
    q4 = State()
    q5 = State()
    q6 = State()
    q7 = State()


router = Router()


ans_women = f'''11.Кормили ли вы грудью более 9 месяцев?
723.Была ли у вас первая менструация до 12 лет?
727.У вас очень обильные или очень длительные менструации?
910.Были ли у вас какие-нибудь выделения из влагалища в последнее время?
914.Вы допускаете, что можете быть беременной сейчас?
'''


ans_medicines=f'''439.Принимаете ли вы в настоящее время внутривенные препараты?
10.Принимали ли вы недавно противовоспалительные препараты (НПВП)?
15.Принимали ли вы какие-либо антипсихотические препараты в течение последних 7 дней?
1.Лечились ли вы недавно пероральным антибиотиком от ушной инфекции?
440.Вы регулярно принимаете стимуляторы?
476.Вы сейчас принимаете гормоны?
728.Принимаете ли вы какие-либо новые пероральные антикоагулянты (НОАК)?
43.Вы принимаете кортикостероиды?
731.Принимаете ли вы блокаторы кальциевых каналов?
972.Принимали ли вы недавно противозастойные средства или другие вещества, которые могут оказывать стимулирующее действие?
'''


ans_heart=f'''984.Есть ли у вас близкие родственники, у которых были проблемы с сердечно-сосудистой системой в возрасте до 50 лет?
3.Был ли у вас когда-нибудь перикардит?
721.Есть ли у вас порок сердца?
22.Есть ли у вас проблемы в работе сердечного клапана?
481.Был ли у вас когда-нибудь сердечный приступ или стенокардия (боль в груди)?
482.У вас сердечная недостаточность?
442.У вас появляется отдышка из-за минимальных физических усилий?
445.У вас бывают приступы удушья или одышки, которые будят вас ночью?"
14.Бывает ли у вас боль в груди даже в состоянии покоя?
902.Чувствуете ли вы, что ваше сердце бьется быстро (учащенно), нерегулярно (пропускает удары)?
911.Чувствуете ли вы, что ваше сердце бьется очень нерегулярно или беспорядочно?
483.Был ли у вас когда-нибудь инсульт?
484.У вас есть проблемы с кровообращением?
480.Есть ли у вас высокое кровяное давление или вы принимаете лекарства для лечения высокого кровяного давления?
478.Вы проходите лечение высокого кровяного давления?
931.Принимаете ли вы лекарства, расширяющие кровеносные сосуды?
485.Был ли у вас когда-либо тромбоз глубоких вен (ТГВ)?
'''


ans_lungs=f'''23.Случается ли у вас апноэ (задержки в выполнении дыхательных движений)?
933.Ставили ли вам когда-нибудь диагноз обструктивного апноэ во сне?
26.Есть ли у вас члены семьи, у которых диагностирована анемия?
24.Вам когда-нибудь ставили диагноз анемия?
25.Были ли у кого-либо из членов вашей семьи диагностированы кластерные головные боли?
28.Есть ли среди членов вашей семьи диагноз миастения?
29.Есть ли у кого-либо из ваших ближайших родственников психические заболевания?
18.У вас есть муковисцидоз?
19.У вас есть диагноз гипертиреоз?
20.У вас есть ревматоидный артрит?
2.Вы инфицированы вирусом иммунодефицита человека (ВИЧ)?
34.Вы болеете раком (активная стадия)?
36.Есть ли у вас метастазы?
457.Вам когда-нибудь ставили диагноз «депрессия»?
494.Вам поставили диагноз хронический синусит?
495.У вас есть полипы в носу?
496.У вас искривлена носовая перегородка?
499.Вам ставили диагноз гастроэзофагеальный рефлюкс?
500.У вас есть цирроз печени?
905.Были ли у вас диагностированы эндокринные заболевания или гормональная дисфункция?
982.Есть ли среди членов вашей семьи диагноз «рак поджелудочной железы»?
6.У вас есть хронический панкреатит?
46.Страдаете ли вы болезнью крона или язвенным колитом?
42.Были ли у вас эпизоды эпилепсии?
446.У вас есть диабет?
471.У вас есть болезнь Паркинсона?
474.У вас есть хиатальная грыжа?
475.Была ли у вас когда-нибудь мигрень или известно, что кто-то из членов вашей семьи страдает мигренью?
489.У вас есть хроническая почечная недостаточность?
944.Есть ли у вас проблемы с почками, приводящая к неспособности удерживать белки в организме (гипопротеинемия)?
458.Страдаете ли вы от хронической тревоги?
900.Вы лечитесь от остеопороза?
'''


general_symptoms='''
50. Была ли у вас диарея или учащение стула в последнее время?
722. Был ли у вас недавно стул черного цвета (как уголь)?
935. У вас бледный стул и темная моча?
926. Вы заметили в своем стуле светло-красную кровь или сгустки крови?
452. Чувствовали ли вы, что задыхаетесь?
453. Вы чувствуете легкое головокружение?
459. Вы чувствуете головокружение или, что вот-вот упадете в обморок?
460. Замечали ли вы слабость мышц лица и/или глаз?
461. Чувствуете ли вы слабость в обеих руках и/или обеих ногах?
939. Чувствуете ли вы, что мышечные спазмы или болезненность в шее мешают вам повернуть голову в сторону?
940. У вас наблюдаются раздражающие мышечные спазмы на лице, шее или в любой другой части тела?
465. Вы постоянно чувствуете усталость или спите беспокойно?
490. В последнее время вы стали более раздражительными или ваше настроение очень нестабильное?
464. Вы чувствуете себя настолько уставшим, что не можете заниматься своими обычными делами, или целый день проводите в постели?
922. Заметили ли вы какую-либо новую усталость, общий и неопределенный дискомфорт, диффузные (распространенные) мышечные боли или изменения в вашем общем самочувствии?
726. Есть ли у вас диффузная (распространенная) мышечная боль?
720. Страдаете ли вы фибромиалгией?
467. Есть ли у вас жар (ощущаемый или измеряемый термометром)?
468. Краснеют ли щеки?
469. Есть ли у вас онемение, потеря чувствительности или покалывание в ногах?
470. Был ли у вас озноб или дрожь?
472. Вы недавно набрали вес?
473. У вас болит горло?
479. Вы потеряли обоняние?
486. Были ли вы не в состоянии двигаться или вставать более 3 дней подряд в течение последних 4 недель?
487. Чувствуете ли вы, что умираете, или боялись, что вот-вот умрете?
51. Есть ли у вас ощущение, что вы видите два изображения одного объекта, накладывающихся друг на друга или примыкающих друг к другу (двоение в глазах)?
30. Чувствуете ли вы, что ваш живот раздут или распух (опухает из-за давления изнутри)?
32. Снижен ли ваш аппетит?
37. Есть ли у вас боль в челюсти?
38. Чувствовали ли вы в последнее время растерянность или дезориентацию?
'''


types_of_pain='''
55.преследующая
56.ноющая
57.чувствительная
58.режущая
60.жжение
61.судорога
62.тяжелая
63.пульсирующая
64.жесткая
65.острая
66.тошная
67.страшная
68.изматывающая'''


place_of_pain1='''
70. нигде
71. подвздошное крыло (тазовая область)
73. пах
75. подмышка
77. миндалина
79. анус
80. задняя сторона лодыжки
82. затылок
83. задняя часть шеи
84. предплечье
86. нижняя часть грудь
87. бицепс
89. рот
90. щитовидный хрящ
91. лодыжка
93. клитор
94. копчик
95. шейный отдел позвоночника
96. грудной отдел позвоночника
97. поясничный отдел позвоночника
98. спайка
100. внешняя сторона стопы
102. локоть
104. подколенная ямка
108. бедро
110. правая сторона шеи
111. левая сторона шеи
112. сторона груди
114. нижние зубы
116. верхние зубы
118. над языком
119. макушка головы
120. палец руки
128. спинная сторона стопа
129. тыльная сторона стопы
131. тыльная сторона запястья
132. тыльная сторона руки
134. ладонная сторона предплечья
140. бок
144. лоб
145. нижняя десна
146. верхняя десна
147. колено
149. головка
150. большие половые губы
156. верхняя часть груди
162. щека
166. почечная ямка
168. язычок
169. нижняя губа
171. подбородок
172. икра
174. челюсть
175. нос
176. затылок
177. глаз
179. лопатка (п)
180. лопатка (л)
181. ухо
190. стенка влагалища
193. ладонь
197. малые половые губы
199. глотка
200. подошва
204. лобок
205. пенис
206. мошонка
207. грудь (п)
208. грудь (л)
209. под языком
210. под челюстью
211. пятка
213. висок
215. яичко
217. задняя грудная стенка
219. большеберцовая кость
221. трахея
222. трапециевидная мышца
224. трицепс
226. уретра
227. влагалище
228. живот
231. у влагалища
232. плечо'''


place_of_pain2 = '''
248. никуда
249. подвздошное крыло (тазовая область)
251. пах
253. подмышка
255. миндалина
257. анус
258. задняя сторона лодыжки
260. затылок
261. задняя часть шеи
262. предплечье
264. нижняя часть грудь
265. бицепс
267. рот
268. щитовидный хрящ
269. лодыжка
271. клитор
272. копчик
273. шейный отдел позвоночника
274. грудной отдел позвоночника
275. поясничный отдел позвоночника
276. спайка
278. внешняя сторона стопы
280. локоть
282. подколенная ямка
286. бедро
288. правая сторона шеи
289. левая сторона шеи
290. сторона груди
292. нижние зубы
294. верхние зубы
296. над языком
297. макушка головы
298. палец руки
306. спинная сторона стопа
307. тыльная сторона стопы
309. тыльная сторона запястья
310. тыльная сторона руки
312. ладонная сторона предплечья
318. бок
322. лоб
323. нижняя десна
324. верхняя десна
325. колено
327. головка
328. большие половые губы
334. верхняя часть груди
340. щека
344. почечная ямка
346. язычок
347. нижняя губа
349. подбородок
350. икра
352. челюсть
353. нос
354. затылок
355. глаз
357. лопатка (п)
358. лопатка (л)
359. ухо
368. стенка влагалища
371. ладонь
375. малые половые губы
377. глотка
378. подошва
382. лобок
383. пенис
384. мошонка
385. грудь (п)
386. грудь (л)
387. под языком
388. под челюстью
389. пятка
391. висок
393. яичко
395. задняя грудная стенка
397. большеберцовая кость
399. трахея
400. трапециевидная мышца
402. трицепс
404. уретра
405. влагалище
406. живот
409. рядом с влагалищем
410. плечо
'''


color_of_rash='''504. не указать
505. черного
506. желтого
507. бледного
508. розового
509. красного'''


where_damaged_skin_located='''526. нигде
527. подвздошное крыло (тазовая область)
529. пах
531. подмышка
533. миндалина
535. анус
536. задняя сторона лодыжки
538. затылок
539. задняя часть шеи
540. предплечье
542. нижняя часть грудь
543. бицепс
545. рот
546. щитовидный хрящ
547. лодыжка
549. клитор
550. копчик
551. шейный отдел позвоночника
552. грудной отдел позвоночника
553. поясничный отдел позвоночника
554. спайка
556. внешняя сторона стопы
558. локоть
560. подколенная ямка
564. бедро
566. правая сторона шеи
567. левая сторона шеи
568. сторона груди
570. нижние зубы
572. верхние зубы
574. над языком
575. макушка головы
576. палец руки
584. спинная сторона стопа
585. тыльная сторона стопы
587. тыльная сторона запястья
588. тыльная сторона руки
590. ладонная сторона предплечья
596. бок
600. лоб
601. нижняя десна
602. верхняя десна
603. колено
605. головка
606. большие половые губы
612. верхняя часть груди
618. щека
622. почечная ямка
624. язычок
625. нижняя губа
627. подбородок
628. икра
630. челюсть
631. нос
632. затылок
633. глаз
635. лопатка (п)
636. лопатка (л)
637. ухо
646. стенка влагалища
649. ладонь
653. малые половые губы
655. глотка
656. подошва
660. лобок
661. пенис
662. мошонка
663. грудь (п)
664. грудь (л)
665. под языком
666. под челюстью
667. пятка
669. висок
671. яичко
673. задняя грудная стенка
675. большеберцовая кость
677. трахея
678. трапециевидная мышца
680. трицепс
682. уретра
683. влагалище
684. живот
687. рядом с влагалищем
688. плечо
'''


dictionary_of_topics={1:ans_lungs, 2: ans_heart,4:general_symptoms, 5:ans_medicines, 6:ans_women}


@router.message(Command("Полная_проверка"), StateFilter(States.check_diseases_command))
async def first_anwer1(message: Message, state: FSMContext):
    await message.answer("Выберете:", reply_markup=keyboards.fullcheck_kb)


@router.message(Command("Перепройти"), StateFilter(States.check_diseases_command))
async def first_anwer2(message: Message, state: FSMContext):
    array = [0]*989
    data = await get_data_by_id("SELECT sex, age FROM users WHERE key = $1 and additional_key = $2", message.from_user.id)
    dictionary = {"Парень": 1, "Девушка":0}
    array[-2] = data[1]/110
    array[-1] = dictionary[data[0]]
    await state.update_data(ans=array)
    await state.set_state(Form3.q1)
    await message.answer(f'''Выберете номер заболевания(отправте номера через запятую): 
1)Проблемы с легкими
2)Проблемы с сердечно-сосудистой системой
3)Ваши диагнозы или диагнозы ваших родственников
4)Общие симптомы
5)Лекарства, которые вы принимаете
6)Вопросы для женщин
7)Условия жизни и работы
8)Общие вопросы
9)Есть ли у вас болевой синдром
10)Повреждения кожи  
''')


@router.message(Command("Допройти"), StateFilter(States.check_diseases_command))
async def first_anwer3(message: Message, state: FSMContext):
    ans = await get_array(message.from_user.id)
    await state.update_data(ans=ans)
    await state.set_state(Form3.q1)
    await message.answer(f'''Выберете номер заболевания(отправте номера через запятую): 
1)Проблемы с легкими
2)Проблемы с сердечно-сосудистой системой
3)Ваши диагнозы или диагнозы ваших родственников
4)Общие симптомы
5)Лекарства, которые вы принимаете
6)Вопросы для женщин
7)Условия жизни и работы
8)Общие вопросы
9)Есть ли у вас болевой синдром
10)Повреждения кожи                         
''')


@router.message(Form3.q1)
async def second_answer(message: Message, state: FSMContext):
    text = message.text
    if not text.strip().isdigit() or int(text) < 1 or int(text) > 10:
        await message.answer("Неверный формат ввода, повторите попытку")
    else:
        if int(text) == 9:
            await state.set_state(Form4.q1)
            await message.answer("Введите номера типов боли, которые у вас наблюдаются")
            await message.answer(types_of_pain)
            data = await state.get_data()
            ans = data.get("ans")
            ans[52] = 1
            ans[53+16] = 1
            ans[70+165] = 1
            ans[236+11] = 1
            ans[248+165] = 1
            ans[414+11] = 1
            ans[426+11] = 1
            await state.update_data(ans=ans)
        elif int(text)==10:
            await state.set_state(Form5.q1)
            data = await state.get_data()
            ans = data.get("ans")
            ans[504] = 1
            ans[504+6] = 1
            ans[511+2] = 1
            ans[514+11] = 1
            ans[526+165] = 1
            ans[692+11] = 1
            ans[704+2] = 1
            ans[707+11] = 1
            await message.answer("Какого цвета сыпь")
            await message.answer(color_of_rash)
        else:
            await state.set_state(Form3.q2)
            await message.answer("Пришлите номера симптомов, которые у вас есть, через запятую")
            await message.answer(dictionary_of_topics[int(text)])


@router.message(Form5.q1)
async def color_of_rash1(message: Message, state: FSMContext):
    text = message.text
    correct_input = True
    numbers =[i.strip() for i in text.split(',')]
    for i in numbers:
        if ((not i.isdigit()) or int(i)<1 or int(i)>986):
            correct_input=False
    if correct_input:
        index = [int(i) for i in numbers]
        data = await state.get_data()
        ans = data.get("ans")
        for i in index:
            ans[i]=1
        await state.update_data(ans=ans)
        await state.set_state(Form5.q2)
        await message.answer("Ваши повреждения шелушатся?")
        await message.answer('''1.Нет
2.Да
''')
        
@router.message(Form5.q2)
async def peeling(message: Message, state: FSMContext):
    text = message.text
    if (not text.isdigit())  or (  int(text)!=1 and int(text)!=2):
        await message.answer("Введите заново")
    else:
        data = await state.get_data()
        ans = data.get("ans")
        ans[511-1 - int(text)] = 1
        await state.set_state(Form5.q3)
        await state.update_data(ans=ans)
        await message.answer("Сыпь опухла? Оцените от 0 до 10")
        


@router.message(Form5.q3)
async def rash_is_swollen(message: Message, state: FSMContext):
    text = message.text.strip()
    if text.isdigit() and int(text)>=0 and int(text) <=10:
        data = await state.get_data()
        ans = data.get("ans")
        ans[int(text) + 514] = 1
        await state.update_data(ans=ans)
        await state.set_state(Form5.q4)
        await message.answer("Где находится пострадавшая кожа?")
        await message.answer(where_damaged_skin_located)
    else:
        await message.answer("Введите заново")


@router.message(Form5.q4)
async def third_answer(message: Message, state: FSMContext):
    text = message.text
    correct_input = True
    numbers =[i.strip() for i in text.split(',')]
    
    for i in numbers:
        if ((not i.isdigit()) or int(i)<1 or int(i)>986):
            correct_input=False

    if correct_input:
        data = await state.get_data()
        ans = data.get("ans")
        index = [int(i) for i in numbers]
        for i in index:
            ans[i] = 1
        await state.update_data(ans=ans)
        await state.set_state(Form5.q5)
        await message.answer("Насколько сильна боль, вызванная сыпью? Оцените от 0 до 10")
    else:
        await message.answer("Неправильный формат ввода, повторите попытку")


@router.message(Form5.q5)
async def pain_caused_rash(message: Message, state: FSMContext):
    text = message.text.strip()
    if text.isdigit() and int(text)>=0 and int(text) <=10:
        data = await state.get_data()
        ans = data.get("ans")
        ans[int(text) + 692] = 1
        await state.update_data(ans=ans)
        await state.set_state(Form5.q6)
        await message.answer("Размер поражения кожи сыпью превышает 1 см?")
        await message.answer('''1.Нет
2.Да''')
    else:
        await message.answer("Введите заново")


@router.message(Form5.q6)
async def peeling(message: Message, state: FSMContext):
    text = message.text
    if (not text.isdigit())  or (  int(text)!=1 and int(text)!=2):
        await message.answer("Введите заново")
    else:
        data = await state.get_data()
        ans = data.get("ans")
        ans[704-1 - int(text)] = 1
        await state.set_state(Form5.q7)
        await state.update_data(ans=ans)
        await message.answer("Насколько сильный зуд? Оцените от 0 до 10")


@router.message(Form5.q7)
async def pain_caused_rash(message: Message, state: FSMContext):
    text = message.text.strip()
    if text.isdigit() and int(text)>=0 and int(text) <=10:
        data = await state.get_data()
        ans = data.get("ans")
        ans[int(text) + 707] = 1
        await state.update_data(ans=ans)
        await insert_array(ans, message.from_user.id)
        await state.set_state(States.check_diseases_command)
        await message.answer("Начат анализ")
        data = json.dumps(ans)
        response = json.loads(rpcClient.call(data, config.fullcheck_queue))
        await message.answer(f"Ваш результат: {response}", reply_markup=keyboards.diagnostic_kb)
        await insert_data("UPDATE users SET fullcheck_result = $3 WHERE key = $1 AND additional_key = $2", (response,), message.from_user.id)
    else:
        await message.answer("Введите заново")


@router.message(Form3.q2)
async def third_answer(message: Message, state: FSMContext):
    text = message.text
    correct_input = True
    numbers =[i.strip() for i in text.split(',')]
    
    for i in numbers:
        if ((not i.isdigit()) or int(i)<1 or int(i)>989):
            correct_input=False

    if correct_input:
        data = await state.get_data()
        ans = data.get("ans")
        index = [int(i) for i in numbers]
        for i in index:
            ans[i] = 1
        await insert_array(ans, message.from_user.id)
        await state.set_state(States.check_diseases_command)
        await message.answer("Начат анализ")
        data = json.dumps(ans)
        response = json.loads(rpcClient.call(data, config.fullcheck_queue))
        await message.answer(f"Ваш результат: {response}", reply_markup=keyboards.diagnostic_kb)
        await insert_data("UPDATE users SET fullcheck_result = $3 WHERE key = $1 AND additional_key = $2", (response,), message.from_user.id)
    else:
        await message.answer("Неправильный формат ввода, повторите попытку")
        

@router.message(Form4.q1)
async def fourth_answer(message: Message, state: FSMContext):
    text = message.text
    correct_input = True
    numbers =[i.strip() for i in text.split(',')]
    for i in numbers:
        if ((not i.isdigit()) or int(i)<1 or int(i)>986):
            correct_input=False
    if correct_input:
        index = [int(i) for i in numbers]
        data = await state.get_data()
        ans = data.get("ans")
        for i in index:
            ans[i]=1
        await state.update_data(ans=ans)
        await state.set_state(Form4.q2)
        await message.answer("Выберете места, где чувствуете боль")
        await message.answer(place_of_pain1)


@router.message(Form4.q2)
async def fifth_answer(message: Message, state: FSMContext):
    text = message.text
    correct_input = True
    numbers =[i.strip() for i in text.split(',')]
    for i in numbers:
        if ((not i.isdigit()) or int(i)<1 or int(i)>986):
            correct_input=False
    if correct_input:
        index = [int(i) for i in numbers]
        data = await state.get_data()
        ans = data.get("ans")
        for i in index:
            ans[i]=1
        await state.update_data(ans=ans)
        await state.set_state(Form4.q3)
        await message.answer("Оцените силу боли от 0 до 10")


@router.message(Form4.q3)
async def sixth_answer(message: Message, state: FSMContext):
    text = message.text.strip()
    if text.isdigit() and int(text)>=0 and int(text) <=10:
        data = await state.get_data()
        ans = data.get("ans")
        ans[int(text)+236] = 1
        await state.update_data(ans=ans)
        await message.answer("Введите номера мест, куда отдает боль")
        await message.answer(place_of_pain2)
        await state.set_state(Form4.q4)
    else:
        await message.answer("Неправильный формат ввода, повторите попытку")

    
@router.message(Form4.q4)
async def seventh_answer(message: Message, state: FSMContext):
    text = message.text
    correct_input = True
    numbers =[i.strip() for i in text.split(',')]
    for i in numbers:
        if ((not i.isdigit()) or int(i)<1 or int(i)>986):
            correct_input=False
    if correct_input:
        index = [int(i) for i in numbers]
        data = await state.get_data()
        ans = data.get("ans")
        for i in index:
            ans[i]=1
        await state.update_data(ans=ans)
        await state.set_state(Form4.q5)
        await message.answer("Насколько четкие границы локализуется боль? Оценте от 0 до 10")
    else:
        await message.answer("Неправильный формат ввода, повторите попытку")


@router.message(Form4.q5)
async def sixth_answer(message: Message, state: FSMContext):
    text = message.text.strip()
    if text.isdigit() and int(text)>=0 and int(text) <=10:
        data = await state.get_data()
        ans = data.get("ans")
        ans[int(text)+414]
        await state.update_data(ans=ans)
        await message.answer("Как быстро появилась боль? Оцените от 0 до 10")
        await state.set_state(Form4.q6)
    else:
        await message.answer("Неправильный формат ввода, повторите попытку")

@router.message(Form4.q6)
async def sixth_answer(message: Message, state: FSMContext):
    text = message.text.strip()
    if text.isdigit() and int(text)>=0 and int(text) <=10:
        data = await state.get_data()
        ans = data.get("ans")
        ans[int(text)+426]
        await state.set_state(States.check_diseases_command)
        await insert_array(ans, message.from_user.id)
        await message.answer("Начат анализ")
        data = json.dumps(ans)
        response = json.loads(rpcClient.call(data, config.fullcheck_queue))
        await message.answer(f"Ваш результат: {response}", reply_markup=keyboards.diagnostic_kb)
        await insert_data("UPDATE users SET fullcheck_result = $3 WHERE key = $1 and additional_key = $2", (response,), message.from_user.id)

    else:
        await message.answer("Неправильный формат ввода, повторите попытку")