# СУХД - вторая КР

## Технологии

Транспортный слой: `Apache Pulsar`

Хранилище для данных реального времени: `Clickhouse`

Холодное хранилище: `Apache Hadoop` и `Apache Hive`

BI-инструмент: `Apache Superset`

## Взаимодействие слоев

* Клиент производит события
* События направляются на различные топики, соответствующие типу события, в Apache Pulsar (транспортный слой)
* Брокер сохраняет события в горячий слой (Clickhouse)
* Т.к. в Apache Hadoop запись происходит как batch, имеется сервис Batch Service, который подписывается на топики
  брокера, а далее записывает эти данные пачками в холодный слой (Clickhouse)
* BI-инструмент (сервисный слой) направляет запросы к горячим данным (Clickhouse), а также к холодным (к Apache
  Hadoop) для формирования дашбордов аналитики.

## Используемые события в дашбордах

* Просмотр Страницы Продукта: Когда пользователь просматривает страницу конкретного товара или услуги.
* Фильтрация и Сортировка: Применение фильтров или сортировок в поиске, например, по цене, категории, рейтингу и т.д.
* Добавление в Корзину: Когда пользователь добавляет товар в свою корзину для покупки.
* Удаление из Корзины: Удаление товара из корзины.
* Просмотр Отзывов: Чтение отзывов других пользователей о товаре или услуге.
* Использование Промокодов или Купонов: Применение скидочных кодов при оформлении заказа.
* Просмотр Категорий и Подкатегорий: Переход и просмотр различных категорий и подкатегорий товаров на сайте.

## Дашборды

1. **Анализ популярности фильтров и сортировок**: Дашборд, отображающий информацию о наиболее используемых фильтрах и
   параметрах сортировки.
2. **Анализ взаимодействия с товарами в корзине**: Дашборд, позволяющий анализировать взаимодействие пользователей с
   товарами в корзине, такое как изменение количества, удаление товаров и добавление к сравнению, чтобы оптимизировать
   процесс покупки.
3. **Анализ использования промокодов и купонов**: Дашборд, позволяющий анализировать наиболее популярные промокоды и
   купоны.
4. **Анализ отзывов**: Дашборд, позволяющий анализировать, насколько важны отзывы в принятии решения добавить товар в
   корзину.
5. **Анализ популярных категорий и подкатегорий:** Дашборд, позволяющий анализировать популярность различных категорий и
   подкатегорий товаров, чтобы понять предпочтения пользователей и адаптировать ассортимент.

## События системы

### ProductView

Просмотр Страницы Продукта

**Topic**: product-view

**Table**: product_views

| Поле       | Тип      |
|------------|----------|
| view_time  | datetime |
| user_id    | int      |
| product_id | int      |

### Sorting

Фильтрация и Сортировка

**Topic**: sorting

**Table**: sortings

| Поле       | Тип      |
|------------|----------|
| sort_time  | datetime |
| user_id    | int      |
| price_min  | double?  |
| price_max  | double?  |
| rating_min | double?  |
| rating_max | double?  |

### CartAdd

Добавление в Корзину

**Topic**: cart-add

**Table**: cart_adds

| Поле       | Тип      |
|------------|----------|
| add_time   | datetime |
| user_id    | int      |
| product_id | int      |
| quantity   | int      |

### CartRemove

Удаление из Корзины

**Topic**: cart-remove

**Table**: cart_removes

| Поле        | Тип      |
|-------------|----------|
| remove_time | datetime |
| user_id     | int      |
| product_id  | int      |
| quantity    | int      |

### ReviewView

Просмотр Отзывов

**Topic**: review-view

**Table**: review_views

| Поле          | Тип      |
|---------------|----------|
| view_time     | datetime |
| user_id       | int      |
| review_id     | int      |
| review_rating | int      |

### CouponUse

Использование Промокодов или Купонов

**Topic**: coupon-use

**Table**: coupon_use

| Поле      | Тип      |
|-----------|----------|
| use_time  | datetime |
| user_id   | int      |
| coupon_id | int      |
| order_id  | int      |

### CategoryView

Просмотр Категорий и Подкатегорий

**Topic:** category-view

**Table:** category_views

| Поле               | Тип      |
|--------------------|----------|
| view_time          | datetime |
| user_id            | int      |
| category_id        | int      |
| parent_category_id | int?     |
