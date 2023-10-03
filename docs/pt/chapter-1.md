---
title: "Chapter 1 - O básico"
weight: 2
date: 2023-04-28 18:00:00
description: "Chapter 1 - Isto vai lhe ensinar quase tudo sobre o Zig. Esta parte do tutorial deverá demorar menos de uma hora para completar."
---

## Atribuição de variáveis

A atribuição de variáveis tem a seguinte sintaxe: `(const|var) identificador[: tipo] = valor`.

* `const` indica que o `identificador` é uma **constante** que possui um valor imutável.
* `var` indica que o `identificador` é uma **variável** que possui um valor mutável.
* `: tipo` é a anotação do tipo para o `identificador` e pode ser omitido se o tipo dos dados do `valor` for inferido.

<!--no_test-->
```zig
{{ assignments }}
```

Constantes e variáveis *devem* ter um valor. Se nenhum valor possa ser atribuido, o valor [`undefined`](https://ziglang.org/documentation/master/#undefined), que coage a qualquer tipo, pode ser usado desde que a anotação do tipo seja fornecido.

<!--no_test-->
```zig
{{ variables }}
```

Quando possível, valores `const` são preferidos ao invés de valores `var`.

## Arrays [N]T

Arrays são denotados por `[N]T`, onde `N` é o número de elementos no array e `T` é o tipo dos seus elementos (ou seja, o tipo dos itens no array).

Para a literal do array `N` pode ser substituido por `_` para inferir o tamanho do array.

<!--no_test-->
```zig
{{ array_literal }}
```

Para obter o tamanho do array, simplesmente acesse o campo `len` do array.

<!--no_test-->
```zig
{{ array_len }}
```

## If

A declaração If do Zig é simples porque somente aceita valores `bool` (de valores `true` ou `false`). Não há um conceito de valores verdadeiros ou falsos.

Aqui nós vamos introduzir testes. Guarde o código abaixo e compile + execute com `zig test file-name.zig`. Nós vamos usar a função [`expect`](https://ziglang.org/documentation/master/std/#std;testing.expect) da biblioteca padrão, que vai fazer o teste falhar se receber um valor `false`. Quando o teste falha, o erro e o stack trace vão aparecer.

```zig
{{ if_statement }}
```

Declarações If também funcionam como expressões.

```zig
{{ if_expression }}
```

## While

O loop while do Zig tem 3 partes - uma condição, um bloco e uma expressão continue.

Sem a expressão continue.
```zig
{{ while_expression }}
```

Com a expressão continue.
```zig
{{ while_continue }}
```

Com `continue`.

```zig
{{ while_continue_2 }}
```

Com `break`.

```zig
{{ while_break }}
```

## For
Loops For são usados para iterar arrays (e outros tipos discutidos mais tarde). Para loops siga a seguinte sintaxe. Como o while, os loops for usam `break` e `continue`. Aqui tivemos que atribuir valores ao `_`, porque o Zig não permite valores não usados.

```zig
{{ for_loop }}
```

## Funções

__Todos os argumentos das funções são imutáveis__ - Se quiser uma cópia, o utilizador terá que fazer uma explicitamente. Ao contrário das variáveis que são snake_case, funções são camelCase. Aqui estão alguns exemplos de como declarar e chamar uma função simples.

```zig
fn addFive(x: u32) u32 {
    return x + 5;
}

test "function" {
    const y = addFive(0);
    try expect(@TypeOf(y) == u32);
    try expect(y == 5);
}
```

A recursão é permitida:

```zig
fn fibonacci(n: u16) u16 {
    if (n == 0 or n == 1) return n;
    return fibonacci(n - 1) + fibonacci(n - 2);
}

test "function recursion" {
    const x = fibonacci(10);
    try expect(x == 55);
}
```

Quando uma recursão acontece, o compilador já não vai poder saber qual o tamanho máximo da stack. Isso poderá resultar em comportamentos inseguro - um stack overflow. Detalhes em como fazer recursões seguras serão abordadas no futuro.

Valores podem ser ignorados usando o `_` no lugar de uma declaração de uma variável ou constante. Mas isto não funciona no scope global (ou seja, só funciona em funções e em blocos) e é útil para ignorar valores retornados de funções se elas não forem necessárias.

<!--no_test-->
```zig
_ = 10;
```

## Defer

Defer é usado para executar uma declaração ao sair do bloco atual.

```zig
test "defer" {
    var x: i16 = 5;
    {
        defer x += 2;
        try expect(x == 5);
    }
    try expect(x == 7);
}
```

Quando existem multiplos defers num único bloco, eles são executados na ordem reversa.

```zig
test "multi defer" {
    var x: f32 = 5;
    {
        defer x += 2;
        defer x /= 2;
    }
    try expect(x == 4.5);
}
```

## Erros

Um conjunto de erros é como um enum (detalhes nos enums do Zig mais tarde), em que cada erro no conjunto é um valor. Não existem exceções no Zig; os erros são valores. Vamos criar um conjunto de erros.

```zig
const FileOpenError = error{
    AccessDenied,
    OutOfMemory,
    FileNotFound,
};
```
O conjunto de erros coage ao seu super-conjunto.

```zig
const AllocationError = error{OutOfMemory};

test "coerce error from a subset to a superset" {
    const err: FileOpenError = AllocationError.OutOfMemory;
    try expect(err == FileOpenError.OutOfMemory);
}
```

Um conjunto de erros e um tipo normal podem ser combinados com o operador `!` para formar uma união entre o erro e o tipo. Os valores destes tipos podem ser tanto um erro quanto um valor de um tipo normal.

Vamos criar um valor com uma união com o erro. Aqui usamos o [`catch`](https://ziglang.org/documentation/master/#catch), que é seguido por uma expressão que é avaliada quando o valor antes dela é um erro. O catch é usado aqui para fornecer um valor de fallback, mas ele pode ser também um [`noreturn`](https://ziglang.org/documentation/master/#noreturn) - o tipo do `return`, `while (true)`, etc.

```zig
test "error union" {
    const maybe_error: AllocationError!u16 = 10;
    const no_error = maybe_error catch 0;

    try expect(@TypeOf(no_error) == u16);
    try expect(no_error == 10);
}
```

Muitas vezes as funções retornam uma união com um conjunto de erros. Aqui temos um usando o catch, onde a sintaxe `|err|` recebe o valor de um erro. Isto é chamado de __captura do payload__ e é usado de uma forma parecida em muitos lugares. Nós vamos falar mais sobre isso em detalhe mais tarde neste capítulo. Obs: Algumas linguagens usam uma sintaxe parecida para lambdas - mas esse não é o caso no Zig.

```zig
fn failingFunction() error{Oops}!void {
    return error.Oops;
}

test "returning an error" {
    failingFunction() catch |err| {
        try expect(err == error.Oops);
        return;
    };
}
```

`try x` é um atalho para `x catch |err| return err` e é comummente usado em lugares onde o tratamento dos erros não é apropriado. O [`try`](https://ziglang.org/documentation/master/#try) e o [`catch`](https://ziglang.org/documentation/master/#catch) do Zig não estão relacionados ao try-catch encontrado em outras linguagens.

```zig
fn failFn() error{Oops}!i32 {
    try failingFunction();
    return 12;
}

test "try" {
    var v = failFn() catch |err| {
        try expect(err == error.Oops);
        return;
    };
    try expect(v == 12); // is never reached
}
```

[`errdefer`](https://ziglang.org/documentation/master/#errdefer) funciona como o [`defer`](https://ziglang.org/documentation/master/#defer), mas só é executado quando a função é retornada com um erro dentro do bloco em que o [`errdefer`](https://ziglang.org/documentation/master/#errdefer) está contido.


```zig
var problems: u32 = 98;

fn failFnCounter() error{Oops}!void {
    errdefer problems += 1;
    try failingFunction();
}

test "errdefer" {
    failFnCounter() catch |err| {
        try expect(err == error.Oops);
        try expect(problems == 99);
        return;
    };
}
```

As uniões de erros retornados de uma função podem ter os seus conjuntos de erros inferidos desde que não haja um conjunto de erros explicito. Este conjunto de erros inferido contém todos os erros possíveis retornados pela função.

```zig
fn createFile() !void {
    return error.AccessDenied;
}

test "inferred error set" {
    //type coercion successfully takes place
    const x: error{AccessDenied}!void = createFile();

    //Zig does not let us ignore error unions via _ = x;
    //we must unwrap it with "try", "catch", or "if" by any means
    _ = x catch {};
}
```

Conjuntos de erros podem ser unidos.

```zig
const A = error{ NotDir, PathNotFound };
const B = error{ OutOfMemory, PathNotFound };
const C = A || B;
```

O `anyerror` é um conjunto de erros global que por ser um super-conjunto de todos os conjuntos, pode ter um erro de qualquer conjunto. O seu uso geralmente deve ser evitado.

## Switch

O `switch` do Zig funciona como uma declaração e como uma expressão. O tipo de todos os ramos devem coagir ao tipo a que se está a fazer o switch. Todos os valores possíveis devem ser associados ao ramo - os valores não podem ser ignorados. Os cases não podem fazer fallthrough a outros ramos.

Um exemplo de uma declaração de switch. O else é necessário para satisfazer a exaustividade do switch.

```zig
test "switch statement" {
    var x: i8 = 10;
    switch (x) {
        -1...1 => {
            x = -x;
        },
        10, 100 => {
            //special considerations must be made
            //when dividing signed integers
            x = @divExact(x, 10);
        },
        else => {},
    }
    try expect(x == 1);
}
```

Aqui está o código anterior mas como uma expressão.
```zig
test "switch expression" {
    var x: i8 = 10;
    x = switch (x) {
        -1...1 => -x,
        10, 100 => @divExact(x, 10),
        else => x,
    };
    try expect(x == 1);
}
```

## A segurança durante a execução

O Zig fornece alguns níveis de segurança, onde problemas podem ser descobertos durante a execução. A segurança pode ser desativada. O Zig possui muitos casos de __comportamento ilegal detetáveil__. OU seja, comportamentos ilegais serão apanhados (causando um pânico) quando a segurança estiver ativada, mas o mesmo resulta em comportamento não definido quando a segurança estiver desativada. É recomendado que crie e teste o seu software com a segurança ativada, mesmo tendo penalidades na velocidade de execução.

Por exemplo, a segurança durante a execução o protege contra indexações fora do limite.

<!--fail_test-->
```zig
test "out of bounds" {
    const a = [3]u8{ 1, 2, 3 };
    var index: u8 = 5;
    const b = a[index];
    _ = b;
}
```
```
test "out of bounds"...index out of bounds
.\tests.zig:43:14: 0x7ff698cc1b82 in test "out of bounds" (test.obj)
    const b = a[index];
             ^
```

Pode escolher desativar a segurança durante a execução para o bloco atual usando a função built-in [`@setRuntimeSafety`](https://ziglang.org/documentation/master/#setRuntimeSafety).

```zig
test "out of bounds, no safety" {
    @setRuntimeSafety(false);
    const a = [3]u8{ 1, 2, 3 };
    var index: u8 = 5;
    const b = a[index];
    _ = b;
}
```

A segurança é desativada para alguns modos de compilação (isto será discutido mais tarde).

## Unreachable

[`unreachable`](https://ziglang.org/documentation/master/#unreachable) é uma afirmação que diz para o compilador que esta declaração nunca será executada. Isto pode ser usado para dizer ao compilador que um ramo é impossível, o que permite certos tipos de otimizações. Chegar a um [`unreachable`](https://ziglang.org/documentation/master/#unreachable) é considerado um comportado ilegal detetável.

Por ser do tipo [`noreturn`](https://ziglang.org/documentation/master/#noreturn), ele é compatível com todos os outros tipos. Aqui ele coage para o tipo u32.
<!--fail_test-->
```zig
test "unreachable" {
    const x: i32 = 1;
    const y: u32 = if (x == 2) 5 else unreachable;
    _ = y;
}
```
```
test "unreachable"...reached unreachable code
.\tests.zig:211:39: 0x7ff7e29b2049 in test "unreachable" (test.obj)
    const y: u32 = if (x == 2) 5 else unreachable;
                                      ^
```

Aqui temos um unreachable sendo usado numa switch.
```zig
fn asciiToUpper(x: u8) u8 {
    return switch (x) {
        'a'...'z' => x + 'A' - 'a',
        'A'...'Z' => x,
        else => unreachable,
    };
}

test "unreachable switch" {
    try expect(asciiToUpper('a') == 'A');
    try expect(asciiToUpper('A') == 'A');
}
```

## Ponteiros `*T`

Os ponteiros normais no Zig não são permitidos de terem os valores 0 ou null. Eles seguem a seguinte sintaxe `*T`, onde `T`é o tipo base.
Referências são feitas com `&variavel` e dereferências com `variavel.*`.


```zig
fn increment(num: *u8) void {
    num.* += 1;
}

test "pointers" {
    var x: u8 = 1;
    increment(&x);
    try expect(x == 2);
}
```

Tentar atribuir `*T` com um valor 0 é um comportamento ilegal detetável.

<!--fail_test-->
```zig
test "naughty pointer" {
    var x: u16 = 0;
    var y: *u8 = @intToPtr(*u8, x);
    _ = y;
}
```
```
test "naughty pointer"...cast causes pointer to be null
.\tests.zig:241:18: 0x7ff69ebb22bd in test "naughty pointer" (test.obj)
    var y: *u8 = @intToPtr(*u8, x);
                 ^
```

O zig também possui ponteiros const, que não podem ser usados para modificar os dados referenciados. Referenciar uma variável const resulta num ponteiro const.

<!--fail_test-->
```zig
test "const pointers" {
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

Um `*T` coage a um `*const T`.


## Inteiros do tamanho de ponteiros: `usize` e `isize`

`usize` e `isize` são inteiros não assinados e assinados respetivamente, cujo tamanho é do mesmo tamanho de ponteiros. 

```zig
test "usize" {
    try expect(@sizeOf(usize) == @sizeOf(*u8));
    try expect(@sizeOf(isize) == @sizeOf(*u8));
}
```

## Ponteiros de muitos itens `[*]T`

Às vezes podem haver ponteiros com uma quantidade desconhecida de elementos. `[*]T` é a solução para isto, ele funciona como um `*T` mas também suporta a sintaxe para indexação, aritmética de ponteiros e slicing. Ao contrário do `*T`,  ele não pode apontar para um tipo com um tamanho desconhecido. O `*T` coage para `[*]T`.

Todos estes ponteiros podem apontar para qualquer quantidade de elementos, incluindo 0 e 1.

## Slices `[]T`

Os slices podem ser considerados como um par de `[*]T` (um ponteiro para uns dados quaisquer) e um `usize` (o contador do elemento). A sua sintaxe é `[]T`, `T` sendo o seu tipo base. Os slices são frequentemente utilizados no Zig quando quer se fazer operações numa quantidade arbitrária de dados. Os slices também têm os mesmos atributos dos ponteiros, ou seja também existem slices const. Loops For também funcionam com slices. Strings literais também coagem a `[]const u8` no Zig.

Aqui a sintaxe `x[n..m]` é usada para criar um slice a partir de um array. Isto é chamado de __slicing__ e cria um slice coms os seus elementos começando de `x[n]` e acabando em `x[m - 1]`. Este exemplo usa um slice const porque os valores apontados pelo slice não precisam ser modificados.

```zig
fn total(values: []const u8) usize {
    var sum: usize = 0;
    for (values) |v| sum += v;
    return sum;
}
test "slices" {
    const array = [_]u8{ 1, 2, 3, 4, 5 };
    const slice = array[0..3];
    try expect(total(slice) == 6);
}
```

Quando estes valores `n` e `m` são conhecidos durante a compilação, o slice irá produzir ponteiros para um array. Isto não é um problema porque o ponteiro para o array  `*[N]T` coage para `[]T`.

```zig
test "slices 2" {
    const array = [_]u8{ 1, 2, 3, 4, 5 };
    const slice = array[0..3];
    try expect(@TypeOf(slice) == *const [3]u8);
}
```

A sintaxe `x[n..]` pode também ser usada quando quiser um slice até o final.

```zig
test "slices 3" {
    var array = [_]u8{ 1, 2, 3, 4, 5 };
    var slice = array[0..];
    _ = slice;
}
```

Os tipos que podem ser convertidos em slices são: arrays, ponteiros de vários itens e outros slices.

## Enums

Os enums do Zig permitem que defina tipos que têm um conjunto de valores restrito.

Vamos criar um enum.
```zig
const Direction = enum { north, south, east, west };
```

Os enums podem ter o tipo da suas tags especificadas (inteiros). 
```zig
const Value = enum(u2) { zero, one, two };
```

Os valores ordinais dos enums começam do 0. Eles podem ser acessados com a função built-in [`@intFromEnum`](https://ziglang.org/documentation/master/#intFromEnum).
```zig
test "enum ordinal value" {
    try expect(@intFromEnum(Value.zero) == 0);
    try expect(@intFromEnum(Value.one) == 1);
    try expect(@intFromEnum(Value.two) == 2);
}
```

Os seus valores podem ser mudados, a partir do próximo valor eles continuam a partir desse valor.
```zig
const Value2 = enum(u32) {
    hundred = 100,
    thousand = 1000,
    million = 1000000,
    next,
};

test "set enum ordinal value" {
    try expect(@intFromEnum(Value2.hundred) == 100);
    try expect(@intFromEnum(Value2.thousand) == 1000);
    try expect(@intFromEnum(Value2.million) == 1000000);
    try expect(@intFromEnum(Value2.next) == 1000001);
}
```

Os métodos podem receber enums. Estes agem como funções com namespace que podem usar a sintaxe com um ponto. 
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

test "enum method" {
    try expect(Suit.spades.isClubs() == Suit.isClubs(.spades));
}
```

Os enums também podem receber declarações `var`e `const`. Estes agem como globais com namespace e os seus valores não estão relacionados nem anexados às instâncias do tipo enum. 

```zig
const Mode = enum {
    var count: u32 = 0;
    on,
    off,
};

test "hmm" {
    Mode.count += 1;
    try expect(Mode.count == 1);
}
```


## Structs

Os structs são o tipo de dados compósito mais comum no Zig, permitindo que defina tipos que podem guardar um número fixo de campos nomeados. O Zig não oferece nenhuma garantia da ordem dos campos do struct na memória nem do seu tamanho. Tal como arrays, os structs são criados com a sintaxe `T{}`. Aqui está um exemplo declarando e preenchendo uma struct.
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

Todos os campos têm de ter um valor atribuido.

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

Os campos podem ter um valor padrão:
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

Tal como os enums, os structs podem também conter funções e declarações.

Os structs também têm uma propriedade única em que quando recebem um ponteiro para um struct, é feito dereferência automaticamente ao aceder os seus campos. observe como neste exemplo, o self.x e o self.y são acessados na função swap sem precisar de fazer a dereferência do ponteiro self.

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

## Uniões

As uniões do Zig permitem que declare tipos que guarde um valor de vários tipos dependendo do campo; só um campo pode estar ativo de cada vez.

Uniões por sí só não têm um layout de memória garantido. Por causa disso, eles não podem ser utilizados para reinterpretar a memória. Acessar um campo de uma uniao que não está ativo e um comportamento ilegal detetável.


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

Uniões marcadas são uniões que usam um enum para detetar qual campo está ativo. Aqui fazemos outra vez o uso da captura do payload para poder se fazer switch na tag do tipo de uma união enquanto se captura o valor contido nele. Aqui usamos uma `captura do ponteiro`; A captura de valores é imutável, mas com a sintaxe `|*valor|` podemos capturar o ponteiro os valores em vez dos próprios valores. Isto permite-nos usar dereferência para mutar o valor original.

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

O tipo da tag de uma união marcada pode também ser inferida. Isto é equivalente ao tipo marcado em cima.

<!--no_test-->
```zig
const Tagged = union(enum) { a: u8, b: f32, c: bool };
```

Membros tipo `void` podem ter os seus tipos omitidos da sintaxe. Aqui, nenhum deles é do tipo `void`. 

```zig
const Tagged2 = union(enum) { a: u8, b: f32, c: bool, none };
```

## Regras para inteiros

O Zig suporta numeros literais hexadecimais, octais e binários.
```zig
const decimal_int: i32 = 98222;
const hex_int: u8 = 0xff;
const another_hex_int: u8 = 0xFF;
const octal_int: u16 = 0o755;
const binary_int: u8 = 0b11110000;
```

O underscore pode também ser colocado entre os dígitos como um separador visual.
```zig
const one_billion: u64 = 1_000_000_000;
const binary_mask: u64 = 0b1_1111_1111;
const permissions: u64 = 0o7_5_5;
const big_address: u64 = 0xFF80_0000_0000_0000;
```

"Aumento do inteiro" é permitido, ou seja os inteiros de um determinado tipo coagem a outro tipo de inteiro, desde que o novo tipo consiga armazenar todos os valores contidos no tipo anterior.

```zig
test "integer widening" {
    const a: u8 = 250;
    const b: u16 = a;
    const c: u32 = b;
    try expect(c == a);
}
```

Se tiver valor guardado em um inteiro que não possa ser coagido para o tipo que queira, [`@intCast`](https://ziglang.org/documentation/master/#intCast) pode ser usado para converter explicitamente de um tipo para o outro. Se o valor usado estiver fora do intervalo de valores permitidos para o tipo de destino, isso é considerado como um comportamento ilegal detetável.

```zig
test "@intCast" {
    const x: u64 = 200;
    const y = @as(u8, @intCast(x));
    try expect(@TypeOf(y) == u8);
}
```

Os inteiros por padrão não aceitam overflows. Os overflows são comportamentos detetáveis ilegais. Às vezes ser capaz de causar overflows num inteiro é um comportamento bem definido e desejado.
Para isto o Zig fornece operadores capazes de causar overflows. 

| Operador Normal | Operador com Overflow |
|-----------------|-----------------------|
| +               | +%                    |
| -               | -%                    |
| *               | *%                    |
| +=              | +%=                   |
| -=              | -%=                   |
| *=              | *%=                   |

```zig
test "well defined overflow" {
    var a: u8 = 255;
    a +%= 1;
    try expect(a == 0);
}
```

## Floats

Os floats (números com pontos flutuantes) do Zig são estritamente em conformidade com o IEEE, a não ser que [`@setFloatMode(.Optimized)`](https://ziglang.org/documentation/master/#setFloatMode) seja usado, que é equivalente ao `-ffast-math` do GCC. Floats coagem a tipos de floats maiores.

```zig
test "float widening" {
    const a: f16 = 0;
    const b: f32 = a;
    const c: f128 = b;
    try expect(c == @as(f128, a));
}
```

Floats suportam vários tipos de literais.
```zig
const floating_point: f64 = 123.0E+77;
const another_float: f64 = 123.0;
const yet_another: f64 = 123.0e+77;

const hex_floating_point: f64 = 0x103.70p-5;
const another_hex_float: f64 = 0x103.70;
const yet_another_hex_float: f64 = 0x103.70P-5;
```

Underscores podem também ser utilizados entre os digitos.
```zig
const lightspeed: f64 = 299_792_458.000_000;
const nanosecond: f64 = 0.000_000_001;
const more_hex: f64 = 0x1234_5678.9ABC_CDEFp-10;
```

Inteiros e floats podem ser convertidos usando as funções built-in [`@floatFromInt`](https://ziglang.org/documentation/master/#floatFromInt) e [`@intFromFloat`](https://ziglang.org/documentation/master/#intFromFloat). [`@floatFromInt`](https://ziglang.org/documentation/master/#floatFromInt) é sempre seguro, enquanto que [`@intFromFloat`](https://ziglang.org/documentation/master/#intFromFloat) é um comportamento ilegal detetável se o valor do float não cabe no tipo do inteiro de destino.
```zig
test "int-float conversion" {
    const a: i32 = 0;
    const b = @as(f32, @floatFromInt(a));
    const c = @as(i32, @intFromFloat(b));
    try expect(c == a);
}
```

## Blocos rotulados `:blk {}`

Os blocos no Zig são expressões que podem receber rótulos que são utilizados para retornar valores. Aqui nós usamos um rótulo chamado de blk. Os blocos retornam valores, ou seja, eles podem ser usados no lugar dos valores. O valor de um bloco vazio `{}` é o valor do tipo `void`.

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

Isto pode ser considerado como o equivalente do `i++`do C.
<!--no_test-->
```zig
blk: {
    const tmp = i;
    i += 1;
    break :blk tmp;
}
```

## Loops rotulados

Os loops podem receber rótulas, permitindo assim fazer `break`e `continue` para os loops externos.

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

## Loops como expressões

Como o `return`, o `break` aceita um valor. Isto pode ser usado para return um valor do loop. Os loops no Zig tambêm têm um ramo `else` que é executado quando o loop não é parado com um `break`.

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

## Opcionais `?T`

Opcionais usam a sintaxe `?T` e são usados para guardar [`null`](https://ziglang.org/documentation/master/#null), ou um valor com o tipo `T`.

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


Opcionais suportam expressões `orelse` que executam quando a opcional é [`null`](https://ziglang.org/documentation/master/#null). Isto torna o valor optional no seu tipo base.

```zig
test "orelse" {
    var a: ?f32 = null;
    var b = a orelse 0;
    try expect(b == 0);
    try expect(@TypeOf(b) == f32);
}
```

O `.?` é uma abreviação para `orelse unreachable`. Isto é usado quando sabemos que é impossível para um valor opcional ser null, usar isto num valor [`null`](https://ziglang.org/documentation/master/#null) é um comportamento ilegal detetável.

```zig
test "orelse unreachable" {
    const a: ?f32 = 5;
    const b = a orelse unreachable;
    const c = a.?;
    try expect(b == c);
    try expect(@TypeOf(c) == f32);
}
```

A captura de payload funciona em vários lugares para opcionais, ou seja, caso o valor não seja null nós podemos "capturar" esse valor.

Aqui nós usamos uma captura de payload com um opcional num `if`; a e b são equivalentes aqui. `if (b) |valor|`captura o valor de `b` (nos casos onde `b` não é null) e faz com que esse `valor` possa ser usado. Como no exemplo com a união, o valor capturado é imutável, mas aqui nós ainda podemos usar o ponteiro capturado para modificar o valor em `b`.

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

E com `while`:
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

Ponteiros e slices opcionais não ocupam nenhum espaço extra na memória quando comparado com as não opcionais. Isto é porque internamente eles usam o valor 0 do ponteiro para `null`.
Os ponteiros em Zig funcionam assim - eles têm de ser desempacotados para um não opcional antes de serem dereferenciados o que previne a dereferência acidental de ponteiros null.

## Comptime

Blocos de código podem forçar a executação durante a compilação usando o [`comptime`](https://ziglang.org/documentation/master/#comptime). Neste exemplo as variáveis x e y são equivalentes.

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

Inteiros literais são do tipo `comptime_int`. Eles são tipos especiais porque não têm um tamanho especifico (eles não podem ser usados durante a execução) e têm precisão arbitrária. Os valores do tipo `comptime_int` coagem a qualquer tipo de inteiro em que podem caber. Eles também coagem a floats. Caractéres literais são também deste tipo.

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

Também existe `comptime_float`, que internamente é um `f128`. Estes não podem ser coagidos a inteiros mesmo que caibam num valor inteiro.

Os tipos no Zig são valores do tipo `type`. Estes estão disponíveis durante a compilação. Nós os vimos anteriormente ao usar verificar o [`@TypeOf`](https://ziglang.org/documentation/master/#TypeOf) e comparar com outros tipos, mas nós podemos fazer mais do que isso.

```zig
test "branching on types" {
    const a = 5;
    const b: if (a < 10) f32 else i32 = 5;
    _ = b;
}
```

Os parametros das funções em Zig podem ser marcados como sendo [`comptime`](https://ziglang.org/documentation/master/#comptime). Isso significa que o valor passado a essa função tem de ser conhecida durante a compilação. Vamos criar uma função que retorne um tipo. Observe como a função usa PascalCase isto é porque ela retorna um tipo. 

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

Nós podemos refletir tipos usando o built-in [`@typeInfo`](https://ziglang.org/documentation/master/#typeInfo), que toma um `type` e retorna uma união marcada. Este tipo de união marcada pode ser encontrada em [`std.builtin.Type`](https://ziglang.org/documentation/master/std/#std;builtin.Type) (mais informações sobre como importar e usar std serão dadas mais tarde).


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

Podemos usar a função [`@Type`](https://ziglang.org/documentation/master/#Type) para criar um tipo a partir de um [`@typeInfo`](https://ziglang.org/documentation/master/#typeInfo).
Aqui usamos structs anónimas com `.{}`, porque o `T` em `T{}` pode ser inferido. Structs anónimas serão abordadas em detalhe mais tarde. Neste examplo vamos ter um erro de compilação se o rótulo `Int` não estiver definido.

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

Em zig estruturas de dados genéricos são feitos retornando uma struct. O uso de [`@This`](https://ziglang.org/documentation/master/#This) é necessário aqui, ele retorna a struct, union ou enum mais contida. Aqui também usamos [`std.mem.eql`](https://ziglang.org/documentation/master/std/#A;std:mem.eql) para comparar dois slices. 

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

O tipo dos parâmetros das funções podem também ser inferidos usando `anytype` no lugar desse tipo. Então [`@TypeOf`](https://ziglang.org/documentation/master/#TypeOf) pode ser usado nos parâmetros. 

```zig
fn plusOne(x: anytype) @TypeOf(x) {
    return x + 1;
}

test "inferred function parameter" {
    try expect(plusOne(@as(u32, 1)) == 2);
}
```

O comptime introduz também alguns operadores `++` e `**` para concatenar e repetir arrays e slices. Estes operadores não funcionam durante a execução.

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

## Captura de payloads `|n|`

A captura de payloads usa a sintaxe `|valor|` e aparece em vários lugares, nós já vimos alguns deles. Sempre que aparecem são usados para "capturar" o valor de alguma coisa.

Com declarações if e opcionais.
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
Com declarações if e união de erros
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

Com loops while e opcionais. Isto pode ter um bloco else.
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

Com loops while e com união de erros. O else com a captura do erro é necessário aqui.

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

Loops for.
```zig
test "for capture" {
    const x = [_]i8{ 1, 5, 120, -5 };
    for (x) |v| try expect(@TypeOf(v) == i8);
}
```

Switch com uniões marcadas.
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

Como vimos nas secções de Uniões e Opcionais em cima, os valores capturados com a sintaxe `|val|` são imutáveis (como os argumentos das funções), mas podemos usar um ponteiro para modificar o valor original. A captura de valores como ponteiros são também imutáveis, mas porque o valor é um ponteiro, nós podemos modificar o valor original fazendo dereferência nele:

```zig
test "for with pointer capture" {
    var data = [_]u8{ 1, 2, 3 };
    for (&data) |*byte| byte.* += 1;
    try expect(eql(u8, &data, &[_]u8{ 2, 3, 4 }));
}
```

## Loops Inline

Os loops `inline` são desenrolados e permitem algumas coisas que só podem acontecer durante a compilação.
Aqui usamos o [`for`](https://ziglang.org/documentation/master/#inline-for), mas o [`while`](https://ziglang.org/documentation/master/#inline-while) também funciona do mesmo jeito.
```zig
test "inline for" {
    const types = [_]type{ i32, f32, u8, bool };
    var sum: usize = 0;
    inline for (types) |T| sum += @sizeOf(T);
    try expect(sum == 10);
}
```

Usar estes loops para melhorar a performance não é aconselhável a não ser que tenha feito testes e desenrolar os loops foram mais performáticos; o compilador costuma tomar melhores decisões que as que poderia tomar geralmente.

## Opaque

Os tipos [`opaque`](https://ziglang.org/documentation/master/#opaque) no Zig são tipos que não têm um tamanho e um alinhamento conhecidos (mas que não sejam zero). Por isso estes tipos de dados não podem ser armazenados diretamente. Estes são usados para manter o segurança dos tipos com ponteiros para tipos de que não temos nenhuma informação.

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

Tipos opacos (opaque) podem ter declarações nas suas definições (o mesmo que structs, enums, unions).

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

O uso tipico de opaque é para manter a segurança dos tipos quando se está interoperando com programas em C que não expõem completamente a informação dos seus tipos.

## Structs anónimas  `.{}`

O tipo de structs podem ser omitidos de uma struct literal. Estas literais podem coagir para outros tipos de structs.

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

Structs anónimas podem ser completamente anónimas ou seja sem serem coagidas a outro tipo de struct.

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

Podem ser criadas structs anónimas sem campos nomeados, elas são chamadas de __tuplas__. Estes têm muitas das mesmas propriedades que têm os arrays; as tuplas podem ser iteradas, indexadas, usadas com os operadores `++` e `**`, têm um campo len. Internamente, eles têm campos com nomes começando por `"0"`, que podem ser acessados com a sintaxe especial `@"0"`que age como um escape para a sintaxe - coisas dentro do `@""` são sempre considerados como identificadores.

Um loop `inline` deve ser usado para iterar uma tupla aqui, já que o tipo de cada campo da tupla podem ser diferentes.

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

## Sentinela de término: `[N:t]T`, `[:t]T`, and `[*:t]T`


Arrays, slices e ponteiros de vários ítens podem terminar com um valor do seu tipo base. Isto é conhecido como sentinela de término. Eles usam a sintaxe `[N:t]T`, `[:t]T`, e `[*:t]T`, onde `t` é um valor do tipo base `T`.

O exemplo de um array com uma sentinela de término. O built-in [`@bitCast`](https://ziglang.org/documentation/master/#bitCast) é usado para fazer uma conversão insegura de um tipo bit-a-bit. Isto mostra-nos que o último elemento do array é seguido por um byte 0.

```zig
test "sentinel termination" {
    const terminated = [3:0]u8{ 3, 2, 1 };
    try expect(terminated.len == 3);
    try expect(@as(*const [4]u8, @ptrCast(&terminated))[3] == 0);
}
```


Os tipo de strings literais é `*const [N:0]u8`, onde N é o comprimento da string. Isto permite que as strings literais coajam para uma slice com setinela de término e ponteiros de vários ítens com sentinela de término. Obs: As strings literais estão codificadas em UTF-8.

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

Os tipos com sentinelas de términos são coagidas aos seus tipos sem sentinelas.

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

É possível criar slices com sentinelas de término, elas são criadas com a sintaxe `x[n..m:t]`, onde `t` é o valor de término. Fazer isso é afirmar para o programador que a memória é terminada onde é esperado - errar isso é um comportamento detetável ilegal.

```zig
test "sentinel terminated slicing" {
    var x = [_:0]u8{255} ** 3;
    const y = x[0..3 :0];
    _ = y;
}
```

## Vetores

O Zig fornece tipos de vetores para SIMD. Estes não devem ser confundidos com vetores no seu sentido matemático nem com os vetores em C++ como std::vector (para isto, veja "ArrayList" no capitulo 2). Os vetores são criados com a função built-in [@Vector](https://ziglang.org/documentation/master/#Vector).

Um vetor é um grupo de [Inteiros](https://ziglang.org/documentation/master/#Integers), [Floats](#floats), ou [Ponteiros](#pointers-t) que são executados em paralelo, usando instruções SIMD quando possível.

As operações podem ser feitas com vetores que tenham o mesmo comprimento e o mesmo tipo base. As operações são efetuadas em cada valor do vetor. O [`std.meta.eql`](https://ziglang.org/documentation/master/std/#A;std:meta.eql) é usado aqui para verificar a igualdade entre os dois vetores. (é também útil para outros tipos como structs).

```zig
const meta = @import("std").meta;

test "vector add" {
    const x: @Vector(4, f32) = .{ 1, -10, 20, -1 };
    const y: @Vector(4, f32) = .{ 2, 10, 0, 1 };
    const z = x + y;
    try expect(meta.eql(z, @Vector(4, f32){ 3, 0, 20, 0 }));
}
```

Os vetores são indexáveis.
```zig
test "vector indexing" {
    const x: @Vector(4, u8) = .{ 255, 0, 255, 0 };
    try expect(x[0] == 255);
}
```

A função built-in [`@splat`](https://ziglang.org/documentation/master/#splat) pode ser usada para construir um vetor onde todos os seus valores são iguais. Aqui o usamos para multiplicar o vetor por um escalar.

```zig
test "vector * scalar" {
    const x: @Vector(3, f32) = .{ 12.5, 37.5, 2.5 };
    const vec: @Vector(3, f32) = @splat(2);
    const y = x * vec;
    try expect(meta.eql(y, @Vector(3, f32){ 25, 75, 5 }));
}
```

Os vetores não têm um campo `len` como os arrays, mas ainda assim podem ser usados em loops. Aqui, [`std.mem.len`](https://ziglang.org/documentation/master/std/#A;std:mem.len) é usado como um atalho para `@typeInfo(@TypeOf(x)).Vector.len`.

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

Vetores podem coagir aos seus respetivos arrays.

```zig
const arr: [4]f32 = @Vector(4, f32){ 1, 2, 3, 4 };
```

É importante ressaltar que usar vetores explicitamente pode resultar em perdas de performance se não fizer as decisões acertadas - a auto-vetorização do compilador já é inteligente o suficiente.

## Importações

A função built-in [`@import`](https://ziglang.org/documentation/master/#import) recebe um ficheiro e retorna uma struct baseada no ficheiro. Todas as declarações marcadas como `pub` (público) serão incluidas neste novo struct.

`@import("std")` é um caso especial no compilador, ele oferece-nos acesso à biblioteca padrão. Outros [`@import`](https://ziglang.org/documentation/master/#import)s recebem um caminho para um ficheiro ou nome de um pacote (falaremos de pacotes num capitulo mais à frente).

Nós exploraremos mais sobre a biblioteca padrão nos próximos capítulos.

## Fim do Capítulo
No próximo capítulo nós vamos abordar padrões comuns, incluindo muitas áreas úteis da biblioteca padrão.

Feedback e PRs são bem-vindos.
