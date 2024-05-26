Цель данной части: написать нейронную сеть, которая будет способна прогнозировать возможные заболевания у человека по подробному описанию его симптомов. 

Изначальные данные были представлены в тяжелом для анализа виде (https://huggingface.co/datasets/aai530-group6/ddxplus-french). Данные можно преобразовать в удобный вид с помощью Parquet (https://parquet.apache.org).
В датасете около 1'300'000 строк данных.
(https://huggingface.co/datasets/aai530-group6/ddxplus). 

Что представляют из себя симптомы? По сути мы имеем два типа симптомов: бинарные и categorical.
Бинарные -- принимают значение true/false, то есть либо наличие данного симптома, либо отсутствие. 
Сategorical -- с таким симптомом идёт дополнительный параметр, уточняющий характер проблемы.

Итого мы имеем 987 различных симптомов (с учётом уточняющих параметров) и 49 различных заболеваний. Данные необходимо преобразовать в нужный для обучения формат. 

P.S. обучение данной нейронной сети затормаживается из-за трудозатратной нормализации.