---
title: "Глава 1 — Основы"
weight: 2
date: 2023-04-28 18:00:00
description: "Глава 1 — Здесь мы пройдёмся по основам языка программирования Zig. Приблизительное время чтения — менее 1 часа"
---

## Переменные

Так мы присваиваем значение константе или переменной: `(const|var) название[: тип] = значение`.

* Модификатор `const` указывает, что `название` является **константой**, которая не меняет своё значение.
* Модификатор `var` указывает, что `название` является **переменной**, которая может изменить своё значение.
* Аннотация `: тип` указывает тип для `название`, он может быть пропущен, если можно автоматически вывести тип.

<!--no_test-->
```zig
{{ assignments }}
```

Константы и переменные *должны* иметь значение. Если значение ещё неизвестно, вы можете присвоить значение [`undefined`](https://ziglang.org/documentation/master/#undefined), которое может приводиться к любому типу, при условии, что вы явно аннотировали тип.

<!--no_test-->
```zig
{{ variables }}
```

В большинстве случаев желательно использовать `const` вместо `var`.

## Массивы [N]T

Массивы обозначаются синтаксисом `[N]T`, где `N` — количество элементов в массиве, а `T` — тип этих элементов (т.е. дочерний тип массива).

В литералах массива (безымянных массивах), `N` можно заменить на `_`, тогда размер массива будет выведен автоматически.

<!--no_test-->
```zig
{{ array_literal }}
```

Чтобы получить размер массива, обратитесь к полю массива `len`.

<!--no_test-->
```zig
{{ array_len }}
```

## If

Обычная версия оператора `if` в Zig принимает только значения типа `bool` (т.е. `true` — истина или `false` — ложь). В этом случае не существует истинноподобных (truthy) или ложноподобных (falsy) значений.

Здесь мы начинаем использовать тесты. Сохраните код ниже, а затем соберите и запустите его командой `zig test название-файла.zig`. Здесь мы используем функцию [`expect`](https://ziglang.org/documentation/master/std/#A;std:testing.expect) из стандартной библиотеки, которая выдаст ошибку, если выражение ложно. Если тест завершается с ошибкой, появится трассировка ошибки и стека.

```zig
{{ if_statement }}
```

Оператор if также можно использовать в выражениях.

```zig
{{ if_expression }}
```

## While

Цикл `while` может содержать три части — условие, выполняемый код (в блоке) и выражение, которое исполняется после каждой итерации (continue expression).

Пример без «continue expression».
```zig
{{ while_expression }}
```

Пример с «continue expression».
```zig
{{ while_continue }}
```

С оператором пропуска итерации `continue`.

```zig
{{ while_continue_2 }}
```

С оператором досрочного выхода из цикла `break`.

```zig
{{ while_break }}
```

## For
Цикл `for` используется для прохода по массивам (и другим типам, о них расскажем позже). Цикл `for` следует нижеуказанному синтаксису. Как и в цикле `while`, в цикле `for` иогут использоваться операторы `break` и `continue`. Мы присваиваем значения к `_`, т.к. Zig не разрешает **молча** игнорировать значения (подробнее в подразделе Функции).

```zig
{{ for_loop }}
```

## Функции

__Все аргументы функции являются неизменяемыми__ — если вам нужна копия, необходимо явно создать её. Переменные принято оформлять в змеином_регистре (snake_case), а функции в нижнеВерблюжемРегистре (lowerCamelCase). Ниже мы объявляем и вызываем простую фукнцию.

```zig
fn addFive(x: u32) u32 {
    return x + 5;
}

test "Вызов функции addFive" {
    const y = addFive(0);
    try expect(@TypeOf(y) == u32);
    try expect(y == 5);
}
```

Вы также можете использовать рекурсию (вызывать функцию внутри себя):

```zig
fn fibonacci(n: u16) u16 {
    if (n == 0 or n == 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

test "Вызов рекурсивной функции fibonacci" {
    const x = fibonacci(10);
    try expect(x == 55);
}
```

Когда случается рекурсия, компилятор уже не может предварительно рассчитать максимальный размер стека. Это может привести к небезопасному поведению — стек может переполниться. О том, как добиться безопасной рекурсии, будет написано в будущем.

Значения можно игнорировать, используя `_` вместо объявления переменной или константы. Это не работает и не нужно в глобальной области видимости (т.е. работает только внутри функций и блоков) и полезно для игнорирования значений, если они вам не нужны.

<!--no_test-->
```zig
_ = 10;
```

## Defer

Оператор defer используется для выполнения выражения во время выхода из текущей области видимости.

```zig
test "Оператор defer" {
    var x: i16 = 5;
    {
        defer x += 2;
        try expect(x == 5);
    }
    try expect(x == 7);
}
```

Если в одном блоке находятся несколько операторов defer, они выполняются в обратном порядке (снизу вверх).

```zig
test "Множество операторов defer" {
    var x: f32 = 5;
    {
        defer x += 2;
        defer x /= 2;
    }
    try expect(x == 4.5);
}
```

## Ошибки

Множество ошибок (error set) похоже на перечисления (подробнее о перечислениях в Zig позже), но в качестве элементов используются коды ошибок. В Zig не существует исключений — ошибки обрабатываются как обычные значения. Давайте создадим множество ошибок.

```zig
const FileOpenError = error{
    AccessDenied,
    OutOfMemory,
    FileNotFound,
};
```

Множество ошибок можно привести к его надмножеству.

```zig
const AllocationError = error{OutOfMemory};

test "Приведение ошибки из подмножества к надмножеству" {
    const err: FileOpenError = AllocationError.OutOfMemory;
    try expect(err == FileOpenError.OutOfMemory);
}
```

Тип «множество ошибок» и тип обычных значений можно соединить с помощью оператора `!` для формирования типа «объединение с ошибкой» (error union type). Этот тип содержит или ошибку, или обычное значение.

Давайте создадим значение с этим типом. Здесь используется оператор [`catch`](https://ziglang.org/documentation/master/#catch), за которым должно следовать выражение, которое выполняется, если значение является ошибкой. Здесь мы используем этот оператор для выставления резервного значения на случай ошибки, но вместо него может идти тип [`noreturn`](https://ziglang.org/documentation/master/#noreturn) — тип выражений `return`, `while (true)` и т.д, означающий, что здесь находится точка невозврата.

```zig
test "Объединение с ошибкой" {
    const maybe_error: AllocationError!u16 = 10;
    const no_error = maybe_error catch 0;

    try expect(@TypeOf(no_error) == u16);
    try expect(no_error == 10);
}
```

Функции часто возвращают объединение с ошибкой. Вот пример использования оператора catch, где в `|err|` передаётся код ошибки. Этот синтаксис называется __захватом значения__ (payload capturing) и используется аналогичным образом во многих местах. Далее в главе мы поговорим об этом подробнее. Примечание: некоторые языки используют подобный синтаксис для лямбда-выражений — это не относится к Zig.

```zig
fn failingFunction() error{Oops}!void {
    return error.Oops;
}

test "Возврат ошибки и её захват с помощью catch" {
    failingFunction() catch |err| {
        try expect(err == error.Oops);
        return;
    };
}
```

`try x` является краткой записью выражения `x catch |err| return err` и обычно используется в местах, где обработка ошибки неуместна. Операторы [`try`](https://ziglang.org/documentation/master/#try) и [`catch`](https://ziglang.org/documentation/master/#catch) в Zig не связаны с конструкцией try-catch в других языках.

```zig
fn failFn() error{Oops}!i32 {
    try failingFunction();
    return 12;
}

test "Оператор try" {
    var v = failFn() catch |err| {
        try expect(err == error.Oops);
        return;
    };
    try expect(v == 12); // тест не доходит до этой строки
}
```

Оператор [`errdefer`](https://ziglang.org/documentation/master/#errdefer) схож с [`defer`](https://ziglang.org/documentation/master/#defer), но выполняет выражение только в том случае, если в блоке функции с [`errdefer`](https://ziglang.org/documentation/master/#errdefer) была возвращена ошибка.

```zig
var problems: u32 = 98;

fn failFnCounter() error{Oops}!void {
    errdefer problems += 1;
    try failingFunction();
}

test "Оператор errdefer" {
    failFnCounter() catch |err| {
        try expect(err == error.Oops);
        try expect(problems == 99);
        return;
    };
}
```

Если функция возвращает объединение с ошибкой и множество ошибок не указано явно, оно будет выведено. Это выведенное множество содержит все возможные ошибки, которые может вернуть эта функция.

```zig
fn createFile() !void {
    return error.AccessDenied;
}

test "Выведенное множество ошибок" {
    // Здесь происходит приведение типа
    const x: error{AccessDenied}!void = createFile();

    // Zig не позволяет нам игнорировать объединение с ошибкой
    // синтаксисом _ = x;
    // Мы обязаны «распаковать» (unwrap) возможную ошибку с помощью `try`, `catch` или версией `if` для ошибок
    _ = x catch {};
}
```

Множества ошибок можно объединять вместе.

```zig
const A = error{ NotDir, PathNotFound };
const B = error{ OutOfMemory, PathNotFound };
const C = A || B;
```

`anyerror` — это глобальное множество ошибок. Оно является надмножеством для всех множеств ошибок и содержит все возможные коды ошибок. В большинстве случаев его следует избегать.

## Switch

Конструкция `switch` в Zig работает как оператор, так выражение. Результат во всех ветвях должен приводиться к типу результата. Все возможные значения должны быть явно сопоставлены с какой-то ветвью. Из одних ветвей нельзя попасть в другие.

Ниже показан пример использования `switch` в качестве оператора. Ветвь `else` используется для всех оставшихся (не покрытых) случаев `x`.

```zig
test "Оператор многозначного выбора switch" {
    var x: i8 = 10;
    switch (x) {
        -1...1 => {
            x = -x;
        },
        10, 100 => {
            // Следует уделять особое внимание
            // при делении знаковых чисел
            x = @divExact(x, 10);
        },
        else => {},
    }
    try expect(x == 1);
}
```

Тот же пример, но с `switch` в качестве выражения.

```zig
test "Выражение с switch" {
    var x: i8 = 10;
    x = switch (x) {
        -1...1 => -x,
        10, 100 => @divExact(x, 10),
        else => x,
    };
    try expect(x == 1);
}
```

## Безопасность во время выполнения

Zig предоставляет уровень безопасности «во время выполнения» (runtime safety), при котором проблемы могут быть найдены во время выполнения. Эти проверки можно включить или отключить. В Zig существует концепция __обнаруживаемого недопустимого поведения__ (detectable illegal behaviour) — такое поведение при включенных проверках будет обнаружено (вызывая панику), а при отключенных становится неопределенным поведением (undefined behaviour). Пользователям строго рекомендуется разрабатывать и тестировать разрабатываемое ПО с включенными проверками, несмотря на ухудшение производительности.

Одним из примеров обнаруживаемого недопустимого поведения является «выход за диапазон допустимых индексов».

<!--fail_test-->
```zig
test "Выход за границы массива во время выполнения" {
    const a = [3]u8{ 1, 2, 3 };
    var index: u8 = 5;
    const b = a[index];
    _ = b;
}
```
```
Test [1/1] test.Выход за границы массива во время выполнени... thread 8964 panic: index out of bounds: index 5, len 3
./tests.zig:4:16: 0x2246e1 in test.Выход за границы массива во время выполнения (test)
    const b = a[index];
               ^
```

По умолчанию проверки включены для режимов сборки `Debug` и `ReleaseSafe` и отключены для `ReleaseFast` и `ReleaseSmall` (подробнее о режимах сборки в следующих главах).
Пользователь может принудительно (для любого режима сборки) включить или отключить эти проверки, используя в нужном блоке встроенную функцию [`@setRuntimeSafety`](https://ziglang.org/documentation/master/#setRuntimeSafety).

```zig
test "Выход за пределы массива во время выполнения, без проверки" {
    @setRuntimeSafety(false);
    const a = [3]u8{ 1, 2, 3 };
    var index: u8 = 5;
    const b = a[index];
    _ = b;
}
```

## Unreachable

Оператор [`unreachable`](https://ziglang.org/documentation/master/#unreachable) утверждает, что эта инструкция недостижима. С помощью него вы обещаете компилятору, что данная ветвь никогда не выполнится, благодаря чему он может производить более умные оптимизации. Достижение [`unreachable`](https://ziglang.org/documentation/master/#unreachable) считается нарушением обещания/контракта и обнаруживаемым недопустимым поведением.

Так как этот оператор имеет тип [`noreturn`](https://ziglang.org/documentation/master/#noreturn) (точки невозврата), он совместим со всеми другими типами. Здесь он совместим с типом u32 и приводится к нему.
<!--fail_test-->
```zig
test "Достижение unreachable" {
    const x: i32 = 1;
    const y: u32 = if (x == 2) 5 else unreachable;
    _ = y;
}
```
```
Test [1/1] test.Достижение unreachable... thread 14125 panic: reached unreachable code
./tests.zig:3:39: 0x2246f0 in test.Достижение unreachable (test)
    const y: u32 = if (x == 2) 5 else unreachable;
                                      ^
```

В примере ниже unreachable используется для утверждения «ветвь else никогда не выполнится».
```zig
fn asciiToUpper(x: u8) u8 {
    return switch (x) {
        'a'...'z' => x + 'A' - 'a',
        'A'...'Z' => x,
        else => unreachable,
    };
}

test "Оператор unreachable в ветви switch" {
    try expect(asciiToUpper('a') == 'A');
    try expect(asciiToUpper('A') == 'A');
}
```

## Указатель на один элемент (`*T`)

Обычные указатели в Zig не могут иметь значение 0 или null. Они следуют синтаксису `*T`, что означает «указатель на одно значение типа T».

Указатель создаётся при помощи синтаксиса `&variable`, а разыменовывается при помощи `pointer.*`.

```zig
fn increment(num: *u8) void {
    num.* += 1;
}

test "Указатель на переменную" {
    var x: u8 = 1;
    increment(&x);
    try expect(x == 2);
}
```

Попытка установить значение 0 для указателя `*T` считается обнаруживаемым недопустимым поведением.

<!--fail_test-->
```zig
test "Непослушный указатель" {
    var x: u16 = 0;
    var y: *u8 = @ptrFromInt(x);
    _ = y;
}
```
```
Test [1/1] test.Непослушный указатель... thread 15237 panic: cast causes pointer to be null
/home/bratishkaerik/github.com/zighelp/tests.zig:3:18: 0x224711 in test.Непослушный указатель (test)
    var y: *u8 = @ptrFromInt(x);
                 ^
```

Zig также содержит указатели на константы (const pointers) в виде `*const T`, которые нельзя использовать для изменения указываемого значения.

<!--fail_test-->
```zig
test "Указатель на константу" {
    const x: u8 = 1;
    var y = &x;
    y.* += 1;
}
```
```
error: cannot assign to constant
    y.* += 1;
    ~~~~^~~~
```

Тип `*T` может быть автоматически приведён к типу `*const T`, но не наоборот.

## Целые числа размером с указатель: `usize` и `isize`

Типы `usize` и `isize` используются для объявления беззнаковых и знаковых целых чисел соотвественно и имеют тот же размер, что и указатели на данной архитектуре.

```zig
test "Размеры usize и isize" {
    try expect(@sizeOf(usize) == @sizeOf(*u8));
    try expect(@sizeOf(isize) == @sizeOf(*u8));
}
```

## Указатель на неизвестное количество элементов (`[*]T`)

Иногда вам может понадобиться указатель на неизвестное количество элементов. В этом случае используется синтаксис `[*]T` (указатель на неизвестное количество элементов с типом T), который схож с указателем `*T`. В отличии от последнего. этот указатель поддерживает доступ по индексу, арифметику указателей и обрезание (slicing). Также он __не__ поддерживает типы с неизвестным размером. Тип `*T` приводится к типу `[*]T`.

Они могут указывать на любое количество элементов, включая 0 и 1.

## Срезы (`[]T`)

Срезы (slices) можно рассматривать как объединение `[*]T` (указатель на данные) и `usize` (кол-во элементов). Синтаксис выглядит подобным образом: `[]T`, где `T` является типом дочернего элемента. Срезы широко используются в яZig, когда необходимо оперировать с данными разной длины. Срезы могут содержать те же атрибуты, что и указатели, напр. константность элемента (`[*]const T` и `[]const T`). Как и массивы, срезы можно использовать в циклах for. Строковые литералы в Zig могут быть приведены к типу `[]const u8`.

Для обрезания части массива используется синтаксис `x[n..m]`. Эта операция называется __обрезанием__ и создаёт срез элементов с `x[n]` и до `x[m - 1]`. В этом примере мы используем неизменяемый срез, т.к. мы не изменяем значения, на которые он указывает.

```zig
fn total(values: []const u8) usize {
    var sum: usize = 0;
    for (values) |v| sum += v;
    return sum;
}
test "Срезы" {
    const array = [_]u8{ 1, 2, 3, 4, 5 };
    const slice = array[0..3];
    try expect(total(slice) == 6);
}
```

Если значения `n` и `m` известны во время компиляции, вместо среза будет создан указатель на подмассив. Так как этот указатель может быть приведён к срезу, это не является проблемой (т.е. `*[N]T` приводим к `[]T`).

```zig
test "Срезы 2" {
    const array = [_]u8{ 1, 2, 3, 4, 5 };
    const slice = array[0..3];
    try expect(@TypeOf(slice) == *const [3]u8);
}
```

Вы можете пропустить второе значение, если вы обрезаете до конца — `x[n..]`.

```zig
test "Срезы 3" {
    var array = [_]u8{ 1, 2, 3, 4, 5 };
    var slice = array[0..];
    _ = slice;
}
```

Кроме массивов, также можно обрезать указатели на неизвестное кол-во элементов и сами срезы.

## Перечисления

Перечисления (enumerations) в Zig являются набором идентификаторов с целочисленными значениями.

Давайте создадим тип для перечисления направления.
```zig
const Direction = enum { north, south, east, west };
```

В перечислениях можно явно указать (численный) тип находящихся внутри элементов.
```zig
const Value = enum(u2) { zero, one, two };
```

По умолчанию, численные значения элементов начинаются с нуля. Элементы можно преобразовать в числа при помощи встроенной функции [`@intFromEnum`](https://ziglang.org/documentation/master/#intFromEnum).
```zig
test "Получение численных значений из элементов" {
    try expect(@intFromEnum(Value.zero) == 0);
    try expect(@intFromEnum(Value.one) == 1);
    try expect(@intFromEnum(Value.two) == 2);
}
```

Значения элементов можно переопределять, при этом значения следующих элементов всё так же продолжают численный ряд.

```zig
const Value2 = enum(u32) {
    hundred = 100,
    thousand = 1000,
    million = 1000000,
    next,
};

test "Переопределение численных значений" {
    try expect(@intFromEnum(Value2.hundred) == 100);
    try expect(@intFromEnum(Value2.thousand) == 1000);
    try expect(@intFromEnum(Value2.million) == 1000000);
    try expect(@intFromEnum(Value2.next) == 1000001);
}
```

В объявлении перечисляемого типа можно добавить функции, при этом они будут ограничены окружающим пространством имён. Их можно вызвать как обычную функцию, либо в стиле методов используя синтаксис `элемент.вызываемаяФункция(a, b)` (dot syntax), при этом элемент перечисления автоматически становится первым параметром функции (т.е. данная запись эквивалента `Перечисление.вызываемаяФункция(элемент, a, b)`).

```zig
const Suit = enum {
    clubs,
    spades,
    diamonds,
    hearts,

    pub fn isClubs(self: Suit) bool {
        return self == Suit.clubs;
    }
};

test "Вызов функции из пространства имён перечисления" {
    const element = Suit.spades; // экземпляр перечисления Suit
    try expect(element.isClubs() == true);
    try expect(Suit.isClubs(element) == true);
}
```

Перечисления также могут иметь объявления значений с помощью `var` и `const`. Они действуют как глобальные переменные (или константы) в этом пространстве имён, и их значения не связаны и не привязаны к экземплярам самого перечисления.

```zig
const Mode = enum {
    var count: u32 = 0;

    on,
    off,
};

test "Изменение глобальной переменной перечисления Mode" {
    Mode.count += 1;
    try expect(Mode.count == 1);
}
```


## Structs

Structs are Zig's most common kind of composite data type, allowing you to define types that can store a fixed set of named fields. Zig gives no guarantees about the in-memory order of fields in a struct, or its size. Like arrays, structs are also neatly constructed with `T{}` syntax. Here is an example of declaring and filling a struct.
```zig
const Vec3 = struct { x: f32, y: f32, z: f32 };

test "struct usage" {
    const my_vector = Vec3{
        .x = 0,
        .y = 100,
        .z = 50,
    };
    _ = my_vector;
}
```

All fields must be given a value.

<!--fail_test-->
```zig
test "missing struct field" {
    const my_vector = Vec3{
        .x = 0,
        .z = 50,
    };
    _ = my_vector;
}
```
```
error: missing field: 'y'
    const my_vector = Vec3{
                        ^
```

Fields may be given defaults:
```zig
const Vec4 = struct { x: f32, y: f32, z: f32 = 0, w: f32 = undefined };

test "struct defaults" {
    const my_vector = Vec4{
        .x = 25,
        .y = -50,
    };
    _ = my_vector;
}
```

Like enums, structs may also contain functions and declarations.

Structs have the unique property that when given a pointer to a struct, one level of dereferencing is done automatically when accessing fields. Notice how in this example, self.x and self.y are accessed in the swap function without needing to dereference the self pointer.

```zig
const Stuff = struct {
    x: i32,
    y: i32,
    fn swap(self: *Stuff) void {
        const tmp = self.x;
        self.x = self.y;
        self.y = tmp;
    }
};

test "automatic dereference" {
    var thing = Stuff{ .x = 10, .y = 20 };
    thing.swap();
    try expect(thing.x == 20);
    try expect(thing.y == 10);
}
```

## Unions

Zig's unions allow you to define types which store one value of many possible typed fields; only one field may be active at one time.

Bare union types do not have a guaranteed memory layout. Because of this, bare unions cannot be used to reinterpret memory. Accessing a field in a union which is not active is detectable illegal behaviour.

<!--fail_test-->
```zig
const Result = union {
    int: i64,
    float: f64,
    bool: bool,
};

test "simple union" {
    var result = Result{ .int = 1234 };
    result.float = 12.34;
}
```
```
Test [1/1] test.simple union... thread 6604310 panic: access of union field 'float' while field 'int' is active
./tests.zig:9:11: 0x10487c807 in test.simple union (test)
    result.float = 12.34;
```

Tagged unions are unions which use an enum to detect which field is active. Here we make use of payload capturing again, to switch on the tag type of a union while also capturing the value it contains. Here we use a *pointer capture*; captured values are immutable, but with the `|*value|` syntax we can capture a pointer to the values instead of the values themselves. This allows us to use dereferencing to mutate the original value.

```zig
const Tag = enum { a, b, c };

const Tagged = union(Tag) { a: u8, b: f32, c: bool };

test "switch on tagged union" {
    var value = Tagged{ .b = 1.5 };
    switch (value) {
        .a => |*byte| byte.* += 1,
        .b => |*float| float.* *= 2,
        .c => |*b| b.* = !b.*,
    }
    try expect(value.b == 3);
}
```

The tag type of a tagged union can also be inferred. This is equivalent to the Tagged type above.

<!--no_test-->
```zig
const Tagged = union(enum) { a: u8, b: f32, c: bool };
```

`void` member types can have their type omitted from the syntax. Here, none is of type `void`.

```zig
const Tagged2 = union(enum) { a: u8, b: f32, c: bool, none };
```

## Integer Rules

Zig supports hex, octal and binary integer literals.
```zig
const decimal_int: i32 = 98222;
const hex_int: u8 = 0xff;
const another_hex_int: u8 = 0xFF;
const octal_int: u16 = 0o755;
const binary_int: u8 = 0b11110000;
```
Underscores may also be placed between digits as a visual separator.
```zig
const one_billion: u64 = 1_000_000_000;
const binary_mask: u64 = 0b1_1111_1111;
const permissions: u64 = 0o7_5_5;
const big_address: u64 = 0xFF80_0000_0000_0000;
```

"Integer Widening" is allowed, which means that integers of a type may coerce to an integer of another type, providing that the new type can fit all of the values that the old type can.

```zig
test "integer widening" {
    const a: u8 = 250;
    const b: u16 = a;
    const c: u32 = b;
    try expect(c == a);
}
```

If you have a value stored in an integer that cannot coerce to the type that you want, [`@intCast`](https://ziglang.org/documentation/master/#intCast) may be used to explicitly convert from one type to the other. If the value given is out of the range of the destination type, this is detectable illegal behaviour.

```zig
test "@intCast" {
    const x: u64 = 200;
    const y = @as(u8, @intCast(x));
    try expect(@TypeOf(y) == u8);
}
```

Integers by default are not allowed to overflow. Overflows are detectable illegal behaviour. Sometimes being able to overflow integers in a well defined manner is wanted behaviour. For this use case, Zig provides overflow operators.

| Normal Operator | Wrapping Operator |
|-----------------|-------------------|
| +               | +%                |
| -               | -%                |
| *               | *%                |
| +=              | +%=               |
| -=              | -%=               |
| *=              | *%=               |

```zig
test "well defined overflow" {
    var a: u8 = 255;
    a +%= 1;
    try expect(a == 0);
}
```

## Floats

Zig's floats are strictly IEEE compliant unless [`@setFloatMode(.Optimized)`](https://ziglang.org/documentation/master/#setFloatMode) is used, which is equivalent to GCC's `-ffast-math`. Floats coerce to larger float types.

```zig
test "float widening" {
    const a: f16 = 0;
    const b: f32 = a;
    const c: f128 = b;
    try expect(c == @as(f128, a));
}
```

Floats support multiple kinds of literal.
```zig
const floating_point: f64 = 123.0E+77;
const another_float: f64 = 123.0;
const yet_another: f64 = 123.0e+77;

const hex_floating_point: f64 = 0x103.70p-5;
const another_hex_float: f64 = 0x103.70;
const yet_another_hex_float: f64 = 0x103.70P-5;
```
Underscores may also be placed between digits.
```zig
const lightspeed: f64 = 299_792_458.000_000;
const nanosecond: f64 = 0.000_000_001;
const more_hex: f64 = 0x1234_5678.9ABC_CDEFp-10;
```

Integers and floats may be converted using the built-in functions [`@floatFromInt`](https://ziglang.org/documentation/master/#floatFromInt) and [`@intFromFloat`](https://ziglang.org/documentation/master/#intFromFloat). [`@floatFromInt`](https://ziglang.org/documentation/master/#floatFromInt) is always safe, whereas [`@intFromFloat`](https://ziglang.org/documentation/master/#intFromFloat) is detectable illegal behaviour if the float value cannot fit in the integer destination type.

```zig
test "int-float conversion" {
    const a: i32 = 0;
    const b = @as(f32, @floatFromInt(a));
    const c = @as(i32, @intFromFloat(b));
    try expect(c == a);
}
```

## Labelled Blocks `:blk {}`

Blocks in Zig are expressions and can be given labels, which are used to yield values. Here, we are using a label called blk. Blocks yield values, meaning that they can be used in place of a value. The value of an empty block `{}` is a value of the type `void`.

```zig
test "labelled blocks" {
    const count = blk: {
        var sum: u32 = 0;
        var i: u32 = 0;
        while (i < 10) : (i += 1) sum += i;
        break :blk sum;
    };
    try expect(count == 45);
    try expect(@TypeOf(count) == u32);
}
```

This can be seen as being equivalent to C's `i++`.
<!--no_test-->
```zig
blk: {
    const tmp = i;
    i += 1;
    break :blk tmp;
}
```

## Labelled Loops

Loops can be given labels, allowing you to `break` and `continue` to outer loops.

```zig
test "nested continue" {
    var count: usize = 0;
    outer: for ([_]i32{ 1, 2, 3, 4, 5, 6, 7, 8 }) |_| {
        for ([_]i32{ 1, 2, 3, 4, 5 }) |_| {
            count += 1;
            continue :outer;
        }
    }
    try expect(count == 8);
}
```

## Loops as expressions

Like `return`, `break` accepts a value. This can be used to yield a value from a loop. Loops in Zig also have an `else` branch on loops, which is evaluated when the loop is not exited from with a `break`.

```zig
fn rangeHasNumber(begin: usize, end: usize, number: usize) bool {
    var i = begin;
    return while (i < end) : (i += 1) {
        if (i == number) {
            break true;
        }
    } else false;
}

test "while loop expression" {
    try expect(rangeHasNumber(0, 10, 3));
}
```

## Optionals `?T`

Optionals use the syntax `?T` and are used to store the data [`null`](https://ziglang.org/documentation/master/#null), or a value of type `T`.

```zig
test "optional" {
    var found_index: ?usize = null;
    const data = [_]i32{ 1, 2, 3, 4, 5, 6, 7, 8, 12 };
    for (data, 0..) |v, i| {
        if (v == 10) found_index = i;
    }
    try expect(found_index == null);
}
```

Optionals support the `orelse` expression, which acts when the optional is [`null`](https://ziglang.org/documentation/master/#null). This unwraps the optional to its child type.

```zig
test "orelse" {
    var a: ?f32 = null;
    var b = a orelse 0;
    try expect(b == 0);
    try expect(@TypeOf(b) == f32);
}
```

`.?` is a shorthand for `orelse unreachable`. This is used for when you know it is impossible for an optional value to be null, and using this to unwrap a [`null`](https://ziglang.org/documentation/master/#null) value is detectable illegal behaviour.

```zig
test "orelse unreachable" {
    const a: ?f32 = 5;
    const b = a orelse unreachable;
    const c = a.?;
    try expect(b == c);
    try expect(@TypeOf(c) == f32);
}
```

Payload capturing works in many places for optionals, meaning that in the event that it is non-null we can "capture" its non-null value.

Here we use an `if` optional payload capture; a and b are equivalent here. `if (b) |value|` captures the value of `b` (in the cases where `b` is not null), and makes it available as `value`. As in the union example, the captured value is immutable, but we can still use a pointer capture to modify the value stored in `b`.

```zig
test "if optional payload capture" {
    const a: ?i32 = 5;
    if (a != null) {
        const value = a.?;
        _ = value;
    }

    var b: ?i32 = 5;
    if (b) |*value| {
        value.* += 1;
    }
    try expect(b.? == 6);
}
```

And with `while`:
```zig
var numbers_left: u32 = 4;
fn eventuallyNullSequence() ?u32 {
    if (numbers_left == 0) return null;
    numbers_left -= 1;
    return numbers_left;
}

test "while null capture" {
    var sum: u32 = 0;
    while (eventuallyNullSequence()) |value| {
        sum += value;
    }
    try expect(sum == 6); // 3 + 2 + 1
}
```

Optional pointer and optional slice types do not take up any extra memory, compared to non-optional ones. This is because internally they use the 0 value of the pointer for `null`.

This is how null pointers in Zig work - they must be unwrapped to a non-optional before dereferencing, which stops null pointer dereferences from happening accidentally.

## Comptime

Blocks of code may be forcibly executed at compile time using the [`comptime`](https://ziglang.org/documentation/master/#comptime) keyword. In this example, the variables x and y are equivalent.

```zig
test "comptime blocks" {
    var x = comptime fibonacci(10);
    _ = x;

    var y = comptime blk: {
        break :blk fibonacci(10);
    };
    _ = y;
}
```

Integer literals are of the type `comptime_int`. These are special in that they have no size (they cannot be used at runtime!), and they have arbitrary precision. `comptime_int` values coerce to any integer type that can hold them. They also coerce to floats. Character literals are of this type.

```zig
test "comptime_int" {
    const a = 12;
    const b = a + 10;

    const c: u4 = a;
    _ = c;
    const d: f32 = b;
    _ = d;
}
```

`comptime_float` is also available, which internally is an `f128`. These cannot be coerced to integers, even if they hold an integer value.

Types in Zig are values of the type `type`. These are available at compile time. We have previously encountered them by checking [`@TypeOf`](https://ziglang.org/documentation/master/#TypeOf) and comparing with other types, but we can do more.

```zig
test "branching on types" {
    const a = 5;
    const b: if (a < 10) f32 else i32 = 5;
    _ = b;
}
```

Function parameters in Zig can be tagged as being [`comptime`](https://ziglang.org/documentation/master/#comptime). This means that the value passed to that function parameter must be known at compile time. Let's make a function that returns a type. Notice how this function is PascalCase, as it returns a type.

```zig
fn Matrix(
    comptime T: type,
    comptime width: comptime_int,
    comptime height: comptime_int,
) type {
    return [height][width]T;
}

test "returning a type" {
    try expect(Matrix(f32, 4, 4) == [4][4]f32);
}
```

We can reflect upon types using the built-in [`@typeInfo`](https://ziglang.org/documentation/master/#typeInfo), which takes in a `type` and returns a tagged union. This tagged union type can be found in [`std.builtin.Type`](https://ziglang.org/documentation/master/std/#std;builtin.Type) (info on how to make use of imports and std later).

```zig
fn addSmallInts(comptime T: type, a: T, b: T) T {
    return switch (@typeInfo(T)) {
        .ComptimeInt => a + b,
        .Int => |info| if (info.bits <= 16)
            a + b
        else
            @compileError("ints too large"),
        else => @compileError("only ints accepted"),
    };
}

test "typeinfo switch" {
    const x = addSmallInts(u16, 20, 30);
    try expect(@TypeOf(x) == u16);
    try expect(x == 50);
}
```

We can use the [`@Type`](https://ziglang.org/documentation/master/#Type) function to create a type from a [`@typeInfo`](https://ziglang.org/documentation/master/#typeInfo).

Here anonymous struct syntax is used with `.{}`, because the `T` in `T{}` can be inferred. Anonymous structs will be covered in detail later. In this example we will get a compile error if the `Int` tag isn't set.

```zig
fn GetBiggerInt(comptime T: type) type {
    return @Type(.{
        .Int = .{
            .bits = @typeInfo(T).Int.bits + 1,
            .signedness = @typeInfo(T).Int.signedness,
        },
    });
}

test "@Type" {
    try expect(GetBiggerInt(u8) == u9);
    try expect(GetBiggerInt(i31) == i32);
}
```

Returning a struct type is how you make generic data structures in Zig. The usage of [`@This`](https://ziglang.org/documentation/master/#This) is required here, which gets the type of the innermost struct, union, or enum. Here [`std.mem.eql`](https://ziglang.org/documentation/master/std/#A;std:mem.eql) is also used which compares two slices.

```zig
fn Vec(
    comptime count: comptime_int,
    comptime T: type,
) type {
    return struct {
        data: [count]T,
        const Self = @This();

        fn abs(self: Self) Self {
            var tmp = Self{ .data = undefined };
            for (self.data, 0..) |elem, i| {
                tmp.data[i] = if (elem < 0)
                    -elem
                else
                    elem;
            }
            return tmp;
        }

        fn init(data: [count]T) Self {
            return Self{ .data = data };
        }
    };
}

const eql = @import("std").mem.eql;

test "generic vector" {
    const x = Vec(3, f32).init([_]f32{ 10, -10, 5 });
    const y = x.abs();
    try expect(eql(f32, &y.data, &[_]f32{ 10, 10, 5 }));
}
```

The types of function parameters can also be inferred by using `anytype` in place of a type. [`@TypeOf`](https://ziglang.org/documentation/master/#TypeOf) can then be used on the parameter.

```zig
fn plusOne(x: anytype) @TypeOf(x) {
    return x + 1;
}

test "inferred function parameter" {
    try expect(plusOne(@as(u32, 1)) == 2);
}
```

Comptime also introduces the operators `++` and `**` for concatenating and repeating arrays and slices. These operators do not work at runtime.

```zig
test "++" {
    const x: [4]u8 = undefined;
    const y = x[0..];

    const a: [6]u8 = undefined;
    const b = a[0..];

    const new = y ++ b;
    try expect(new.len == 10);
}

test "**" {
    const pattern = [_]u8{ 0xCC, 0xAA };
    const memory = pattern ** 3;
    try expect(eql(u8, &memory, &[_]u8{ 0xCC, 0xAA, 0xCC, 0xAA, 0xCC, 0xAA }));
}
```

## Payload Captures `|n|`

Payload captures use the syntax `|value|` and appear in many places, some of which we've seen already. Wherever they appear, they are used to "capture" the value from something.

With if statements and optionals.
```zig
test "optional-if" {
    var maybe_num: ?usize = 10;
    if (maybe_num) |n| {
        try expect(@TypeOf(n) == usize);
        try expect(n == 10);
    } else {
        unreachable;
    }
}
```

With if statements and error unions. The else with the error capture is required here.
```zig
test "error union if" {
    var ent_num: error{UnknownEntity}!u32 = 5;
    if (ent_num) |entity| {
        try expect(@TypeOf(entity) == u32);
        try expect(entity == 5);
    } else |err| {
        _ = err catch {};
        unreachable;
    }
}
```

With while loops and optionals. This may have an else block.
```zig
test "while optional" {
    var i: ?u32 = 10;
    while (i) |num| : (i.? -= 1) {
        try expect(@TypeOf(num) == u32);
        if (num == 1) {
            i = null;
            break;
        }
    }
    try expect(i == null);
}
```

With while loops and error unions. The else with the error capture is required here.

```zig
var numbers_left2: u32 = undefined;

fn eventuallyErrorSequence() !u32 {
    return if (numbers_left2 == 0) error.ReachedZero else blk: {
        numbers_left2 -= 1;
        break :blk numbers_left2;
    };
}

test "while error union capture" {
    var sum: u32 = 0;
    numbers_left2 = 3;
    while (eventuallyErrorSequence()) |value| {
        sum += value;
    } else |err| {
        try expect(err == error.ReachedZero);
    }
}
```

For loops.
```zig
test "for capture" {
    const x = [_]i8{ 1, 5, 120, -5 };
    for (x) |v| try expect(@TypeOf(v) == i8);
}
```

Switch cases on tagged unions.
```zig
const Info = union(enum) {
    a: u32,
    b: []const u8,
    c,
    d: u32,
};

test "switch capture" {
    var b = Info{ .a = 10 };
    const x = switch (b) {
        .b => |str| blk: {
            try expect(@TypeOf(str) == []const u8);
            break :blk 1;
        },
        .c => 2,
        //if these are of the same type, they
        //may be inside the same capture group
        .a, .d => |num| blk: {
            try expect(@TypeOf(num) == u32);
            break :blk num * 2;
        },
    };
    try expect(x == 20);
}
```

As we saw in the Union and Optional sections above, values captured with the `|val|` syntax are immutable (similar to function arguments), but we can use pointer capture to modify the original values. This captures the values as pointers that are themselves still immutable, but because the value is now a pointer, we can modify the original value by dereferencing it:

```zig
test "for with pointer capture" {
    var data = [_]u8{ 1, 2, 3 };
    for (&data) |*byte| byte.* += 1;
    try expect(eql(u8, &data, &[_]u8{ 2, 3, 4 }));
}
```

## Inline Loops

`inline` loops are unrolled, and allow some things to happen which only work at compile time. Here we use a [`for`](https://ziglang.org/documentation/master/#inline-for), but a [`while`](https://ziglang.org/documentation/master/#inline-while) works similarly.
```zig
test "inline for" {
    const types = [_]type{ i32, f32, u8, bool };
    var sum: usize = 0;
    inline for (types) |T| sum += @sizeOf(T);
    try expect(sum == 10);
}
```

Using these for performance reasons is inadvisable unless you've tested that explicitly unrolling is faster; the compiler tends to make better decisions here than you.

## Opaque

[`opaque`](https://ziglang.org/documentation/master/#opaque) types in Zig have an unknown (albeit non-zero) size and alignment. Because of this these data types cannot be stored directly. These are used to maintain type safety with pointers to types that we don't have information about.

<!--fail_test-->
```zig
const Window = opaque {};
const Button = opaque {};

extern fn show_window(*Window) callconv(.C) void;

test "opaque" {
    var main_window: *Window = undefined;
    show_window(main_window);

    var ok_button: *Button = undefined;
    show_window(ok_button);
}
```
```
tests.zig:11:17: error: expected type '*tests.Window', found '*tests.Button'
    show_window(ok_button);
                ^~~~~~~~~
tests.zig:11:17: note: pointer type child 'tests.Button' cannot cast into pointer type child 'tests.Window'
tests.zig:2:16: note: opaque declared here
const Button = opaque {};
               ^~~~~~~~~
tests.zig:1:16: note: opaque declared here
const Window = opaque {};
               ^~~~~~~~~
tests.zig:4:23: note: parameter type declared here
extern fn show_window(*Window) callconv(.C) void;
                      ^~~~~~~
```

Opaque types may have declarations in their definitions (the same as structs, enums and unions).

<!--no_test-->
```zig
const Window = opaque {
    fn show(self: *Window) void {
        show_window(self);
    }
};

extern fn show_window(*Window) callconv(.C) void;

test "opaque with declarations" {
    var main_window: *Window = undefined;
    main_window.show();
}
```

The typical usecase of opaque is to maintain type safety when interoperating with C code that does not expose complete type information.

## Anonymous Structs `.{}`

The struct type may be omitted from a struct literal. These literals may coerce to other struct types.

```zig
test "anonymous struct literal" {
    const Point = struct { x: i32, y: i32 };

    var pt: Point = .{
        .x = 13,
        .y = 67,
    };
    try expect(pt.x == 13);
    try expect(pt.y == 67);
}
```

Anonymous structs may be completely anonymous i.e. without being coerced to another struct type.

```zig
test "fully anonymous struct" {
    try dump(.{
        .int = @as(u32, 1234),
        .float = @as(f64, 12.34),
        .b = true,
        .s = "hi",
    });
}

fn dump(args: anytype) !void {
    try expect(args.int == 1234);
    try expect(args.float == 12.34);
    try expect(args.b);
    try expect(args.s[0] == 'h');
    try expect(args.s[1] == 'i');
}
```
<!-- TODO: mention tuple slicing when it's implemented -->

Anonymous structs without field names may be created, and are referred to as __tuples__. These have many of the properties that arrays do; tuples can be iterated over, indexed, can be used with the `++` and `**` operators, and have a len field. Internally, these have numbered field names starting at `"0"`, which may be accessed with the special syntax `@"0"` which acts as an escape for the syntax - things inside `@""` are always recognised as identifiers.

An `inline` loop must be used to iterate over the tuple here, as the type of each tuple field may differ.

```zig
test "tuple" {
    const values = .{
        @as(u32, 1234),
        @as(f64, 12.34),
        true,
        "hi",
    } ++ .{false} ** 2;
    try expect(values[0] == 1234);
    try expect(values[4] == false);
    inline for (values, 0..) |v, i| {
        if (i != 2) continue;
        try expect(v);
    }
    try expect(values.len == 6);
    try expect(values.@"3"[0] == 'h');
}
```

## Sentinel Termination: `[N:t]T`, `[:t]T`, and `[*:t]T`

Arrays, slices and many pointers may be terminated by a value of their child type. This is known as sentinel termination. These follow the syntax `[N:t]T`, `[:t]T`, and `[*:t]T`, where `t` is a value of the child type `T`.

An example of a sentinel terminated array. The built-in [`@bitCast`](https://ziglang.org/documentation/master/#bitCast) is used to perform an unsafe bitwise type conversion. This shows us that the last element of the array is followed by a 0 byte.

```zig
test "sentinel termination" {
    const terminated = [3:0]u8{ 3, 2, 1 };
    try expect(terminated.len == 3);
    try expect(@as(*const [4]u8, @ptrCast(&terminated))[3] == 0);
}
```

The types of string literals is `*const [N:0]u8`, where N is the length of the string. This allows string literals to coerce to sentinel terminated slices, and sentinel terminated many pointers. Note: string literals are UTF-8 encoded.

```zig
test "string literal" {
    try expect(@TypeOf("hello") == *const [5:0]u8);
}
```

`[*:0]u8` and `[*:0]const u8` perfectly model C's strings.

```zig
test "C string" {
    const c_string: [*:0]const u8 = "hello";
    var array: [5]u8 = undefined;

    var i: usize = 0;
    while (c_string[i] != 0) : (i += 1) {
        array[i] = c_string[i];
    }
}
```

Sentinel terminated types coerce to their non-sentinel-terminated counterparts.

```zig
test "coercion" {
    var a: [*:0]u8 = undefined;
    const b: [*]u8 = a;
    _ = b;

    var c: [5:0]u8 = undefined;
    const d: [5]u8 = c;
    _ = d;

    var e: [:10]f32 = undefined;
    const f = e;
    _ = f;
}
```

Sentinel terminated slicing is provided which can be used to create a sentinel terminated slice with the syntax `x[n..m:t]`, where `t` is the terminator value. Doing this is an assertion from the programmer that the memory is terminated where it should be - getting this wrong is detectable illegal behaviour.

```zig
test "sentinel terminated slicing" {
    var x = [_:0]u8{255} ** 3;
    const y = x[0..3 :0];
    _ = y;
}
```

## Vectors

Zig provides vector types for SIMD. These are not to be conflated with vectors in a mathematical sense, or vectors like C++'s std::vector (for this, see "Arraylist" in chapter 2). Vector types are created with the builtin function [@Vector](https://ziglang.org/documentation/master/#Vector).

A vector is a group of booleans, [Integers](https://ziglang.org/documentation/master/#Integers), [Floats](#floats), or [Pointers](#pointers-t) which are operated on in parallel, using SIMD instructions if possible.

Operations between vectors with the same child type and length can take place. These operations are performed on each of the values in the vector.[`std.meta.eql`](https://ziglang.org/documentation/master/std/#A;std:meta.eql) is used here to check for equality between two vectors (also useful for other types like structs).

```zig
const meta = @import("std").meta;

test "vector add" {
    const x: @Vector(4, f32) = .{ 1, -10, 20, -1 };
    const y: @Vector(4, f32) = .{ 2, 10, 0, 1 };
    const z = x + y;
    try expect(meta.eql(z, @Vector(4, f32){ 3, 0, 20, 0 }));
}
```

Vectors are indexable.
```zig
test "vector indexing" {
    const x: @Vector(4, u8) = .{ 255, 0, 255, 0 };
    try expect(x[0] == 255);
}
юю`

The built-in function [`@splat`](https://ziglang.org/documentation/master/#splat) may be used to construct a vector where all of the values are the same. Here we use it to multiply a vector by a scalar.

```zig
test "vector * scalar" {
    const x: @Vector(3, f32) = .{ 12.5, 37.5, 2.5 };
    const vec: @Vector(3, f32) = @splat(2);
    const y = x * vec;
    try expect(meta.eql(y, @Vector(3, f32){ 25, 75, 5 }));
}
```

Vectors do not have a `len` field like arrays, but may still be looped over. Here, [`std.mem.len`](https://ziglang.org/documentation/master/std/#A;std:mem.len) is used as a shortcut for `@typeInfo(@TypeOf(x)).Vector.len`.

```zig
const len = @import("std").mem.len;

test "vector looping" {
    const x = @Vector(4, u8){ 255, 0, 255, 0 };
    var sum = blk: {
        var tmp: u10 = 0;
        var i: u8 = 0;
        while (i < 4) : (i += 1) tmp += x[i];
        break :blk tmp;
    };
    try expect(sum == 510);
}
```

Vectors coerce to their respective arrays.

```zig
const arr: [4]f32 = @Vector(4, f32){ 1, 2, 3, 4 };
```

It is worth noting that using explicit vectors may result in slower software if you do not make the right decisions - the compiler's auto-vectorisation is fairly smart as-is.

## Imports

The built-in function [`@import`](https://ziglang.org/documentation/master/#import) takes in a file, and gives you a struct type based on that file. All declarations labelled as `pub` (for public) will end up in this struct type, ready for use.

`@import("std")` is a special case in the compiler, and gives you access to the standard library. Other [`@import`](https://ziglang.org/documentation/master/#import)s will take in a file path, or a package name (more on packages in a later chapter).

We will explore more of the standard library in later chapters.

## End Of Chapter 1
In the next chapter we will cover standard patterns, including many useful areas of the standard library.

Feedback and PRs are welcome.
