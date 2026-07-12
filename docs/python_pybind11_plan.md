# Gluecodium Python 生成器计划 (pybind11 方案)

> **状态**: 设计阶段
> **作者**: l2ming
> **日期**: 2026-07-13
> **关联**: 基于 Gluecodium 现有架构（Dart FFI / Swift CBridge 生成器为参考）

---

## 1. 背景与动机

Gluecodium 当前支持 C++ / Java / Kotlin / Swift / Dart 五种目标语言。Python 作为数据科学、机器学习和自动化测试领域的主流语言，在跨平台项目中需求日益增长。

### 1.1 方案选择：pybind11

| 方案 | 优势 | 劣势 |
|------|------|------|
| **ctypes/cffi over C-ABI shim** | 复用 Dart FFI 的 C-ABI 层，零编译依赖 | 需手工实现引用计数、异常封送、GIL 安全回调 |
| **pybind11 生成绑定** ✅ | 自动处理引用计数、异常转换、GIL、STL 容器转换；生成代码量少 | 新增编译时依赖（pybind11 + 编译扩展模块）；架构上偏离 JNI/FFI 模式 |

**选择 pybind11 的理由**：
- Python 的 GIL 和对象模型与 pybind11 天然契合
- 引用计数、异常封送、回调线程安全由 pybind11 框架处理，大幅减少生成代码的复杂度
- CPython 本身就是编译扩展模块，编译依赖对 Python 生态是可接受的
- pybind11 是 CPython 生态中最成熟的 C++ 绑定框架，社区活跃

### 1.2 架构对比

```
现有 Dart 架构:
  LimeIDL → LIME Model → DartGenerator
    ├── Dart 代码 (dart/ffi 调用)
    └── FFI C++ 代码 (C-ABI shim → C++ API)

现有 Swift 架构:
  LimeIDL → LIME Model → SwiftGenerator
    ├── Swift 代码
    └── CBridge C/C++ 代码 (C-ABI shim → C++ API)

新 Python 架构 (pybind11):
  LimeIDL → LIME Model → PythonGenerator
    ├── Python 代码 (.py + .pyi 类型存根)
    └── pybind11 C++ 代码 (直接包装 C++ API，无需 C-ABI 中间层)
```

**关键差异**：pybind11 方案不需要 C-ABI 中间层（ unlike Dart FFI / Swift CBridge），pybind11 的 `.cpp` 绑定文件直接 `#include` C++ 头文件并调用 C++ API。

---

## 2. 实施阶段

### Phase 0 — 前置准备

#### 0.1 确认 pybind11 版本与依赖
- pybind11 >= 2.11.0 (支持 C++17, Python 3.8+)
- 目标平台: Linux (gcc/clang), macOS (clang), Windows (MSVC)
- Python: 3.8+ (与 pybind11 最低支持版本对齐)

#### 0.2 验证 C++ 生成器兼容性
- 确认现有 C++ 生成器产出的头文件可被 pybind11 直接 `#include`
- 确认 `std::optional`, `std::vector`, `std::map`, `std::set` 等类型在 pybind11 中的转换支持
- 确认 `Return<T, Error>` 类型在 pybind11 中的异常映射可行性

---

### Phase 1 — LIME 模型层扩展

#### 1.1 添加 `PYTHON` 属性类型

**文件**: `lime-runtime/src/main/java/com/here/gluecodium/model/lime/LimeAttributeType.kt`

```kotlin
// 在枚举中添加：
PYTHON("Python", LimeAttributeValueType.NAME),
```

这使得 LimeIDL 可以使用 `@Python` 属性：
```lime
@Python(Name = "customName")
class MyClass { ... }

@Python(Skip)
class InternalOnly { ... }

@Python(Internal)
fun internalMethod() { ... }
```

#### 1.2 更新注解解析器

**文件**: `lime-loader/src/main/java/com/here/gluecodium/loader/AntlrLimeConverter.kt`

在 `convertAnnotationType()` 方法中添加：
```kotlin
"Python" -> LimeAttributeType.PYTHON
```

在 `propagateParentAttributes()` 方法中，将 `PYTHON` 加入遍历列表：
```kotlin
listOf(JAVA, SWIFT, DART, KOTLIN, PYTHON).forEach { ... }
```

#### 1.3 添加 Python 名称规则

**新文件**: `gluecodium/src/main/resources/namerules/python.properties`

```properties
field=snake_case
parameter=snake_case
constant=UPPER_SNAKE_CASE
enumerator=UPPER_SNAKE_CASE
method=snake_case
property=snake_case
property.prefix.boolean=is
type=UpperCamelCase
error=UpperCamelCase
error.suffix=Error
join.infix=_
```

#### 1.4 更新 `GeneratorOptions`

**文件**: `gluecodium/src/main/java/com/here/gluecodium/generator/common/GeneratorOptions.kt`

添加 Python 相关选项字段：
```kotlin
var pythonPackages: List<String> = listOf(),
var pythonInternalPackages: List<String> = listOf(),
var pythonNameRules: Configuration = ConfigurationProperties.fromResource(
    Gluecodium::class.java, "/namerules/python.properties"
),
var pythonModule: String = "generated",  // Python 模块名
```

---

### Phase 2 — 生成器骨架

#### 2.1 创建 Python 生成器包

```
gluecodium/src/main/java/com/here/gluecodium/generator/python/
├── PythonGenerator.kt              # 主生成器类，实现 Generator 接口
├── PythonNameResolver.kt           # LIME → Python 名称解析
├── Pybind11NameResolver.kt         # LIME → C++ pybind11 名称解析
├── PythonImportResolver.kt         # Python import 解析
├── PythonImportsCollector.kt       # Python import 收集器
├── Pybind11IncludeResolver.kt      # C++ include 解析
├── PythonGeneratorPredicates.kt    # 模板谓词
├── PythonCommentsProcessor.kt      # 文档注释处理
├── PythonOverloadsValidator.kt     # 重载验证器
├── Pybind11Helpers.kt              # pybind11 辅助工具
└── package-info.java
```

#### 2.2 实现 `PythonGenerator` 类

**文件**: `gluecodium/src/main/java/com/here/gluecodium/generator/python/PythonGenerator.kt`

参照 `DartGenerator` 的结构：

```kotlin
internal class PythonGenerator : Generator {
    override val shortName = "python"

    override fun initialize(options: GeneratorOptions) {
        // 初始化名称规则、命名空间、模块名等
    }

    override fun generate(limeModel: LimeModel): List<GeneratedFile> {
        // 1. 过滤模型 (LimeModelSkipPredicates + PYTHON 属性)
        // 2. 创建名称解析器
        // 3. 运行验证器
        // 4. 为每个顶层元素生成:
        //    a. Python 模块文件 (.py)
        //    b. pybind11 绑定文件 (.cpp)
        // 5. 生成公共文件 (setup.py, __init__.py, 类型转换等)
    }
}
```

生成器产出两类文件：
- **MAIN**: 每个顶层 LIME 元素对应一个 `.py` 文件和一个 `.cpp` pybind11 绑定文件
- **COMMON**: `setup.py`/`pyproject.toml`、类型转换辅助代码、`__init__.py`

#### 2.3 注册生成器

**文件**: `gluecodium/src/main/resources/META-INF/services/com.here.gluecodium.generator.common.Generator`

添加一行：
```
com.here.gluecodium.generator.python.PythonGenerator
```

#### 2.4 CLI 选项支持

**文件**: `gluecodium/src/main/java/com/here/gluecodium/cli/OptionReader.kt`

添加 CLI 选项：
```kotlin
addOption("pythonpackage", true, "Python package name for generated sources")
addOption("pythonintpackage", "python-internal-package", true, 
    "Python sub-package for internal types")
addOption("pythonmodule", true, "Name of the generated Python extension module")
addOption("pythonnamerules", true, "Python name rules property file")
```

在 `read()` 方法中添加对应的选项解析逻辑。

---

### Phase 3 — 模板系统

#### 3.1 创建 Mustache 模板

**目录**: `gluecodium/src/main/resources/templates/python/`

```
templates/python/
├── PythonFile.mustache              # Python 文件框架
├── PythonClass.mustache             # Python 类定义
├── PythonInterface.mustache         # Python 接口/协议
├── PythonStruct.mustache            # Python 结构体 (dataclass)
├── PythonEnumeration.mustache       # Python 枚举
├── PythonException.mustache         # Python 异常类
├── PythonLambda.mustache            # Python 回调类型
├── PythonProperty.mustache          # Python 属性
├── PythonFunction.mustache          # Python 函数声明
├── PythonFunctionBody.mustache      # Python 函数体 (调用 native)
├── PythonField.mustache             # Python 字段
├── PythonDocumentation.mustache     # 文档字符串
├── PythonImport.mustache            # import 语句
├── PythonAttributes.mustache        # 属性装饰器
├── PythonSetupPy.mustache           # setup.py 构建脚本
├── PythonPyproject.mustache         # pyproject.toml
├── PythonInit.mustache              # __init__.py
├── Pybind11Module.mustache          # pybind11 模块入口
├── Pybind11Class.mustache           # pybind11 类绑定
├── Pybind11Struct.mustache          # pybind11 结构体绑定
├── Pybind11Enum.mustache            # pybind11 枚举绑定
├── Pybind11Function.mustache        # pybind11 函数绑定
├── Pybind11Property.mustache        # pybind11 属性绑定
├── Pybind11Exception.mustache       # pybind11 异常映射
├── Pybind11Lambda.mustache          # pybind11 回调包装
└── Pybind11TypeCaster.mustache      # 自定义类型转换器
```

#### 3.2 pybind11 绑定模板示例

**`Pybind11Class.mustache`** (概念示例):
```cpp
// 为 class {{resolveName}} 生成 pybind11 绑定
py::class_<{{resolveName "C++"}}, {{trampolineClassName}}>(module, "{{resolveName}}")
    .def(py::init<>(){{#constructors}}, py::init<{{constructorArgs}}>(){{/constructors}})
    {{#functions}}
    .def("{{resolveName}}", &{{resolveName "C++"}}::{{resolveName "C++"}}, 
         py::arg("{{paramName}}"){{#defaultValue}} = {{.}}{{/defaultValue}})
    {{/functions}}
    {{#properties}}
    .def_property("{{resolveName}}", 
                  &{{resolveName "C++"}}::{{getterName}},
                  &{{resolveName "C++"}}::{{setterName}})
    {{/properties}}
    ;
```

**`Pybind11Module.mustache`** (概念示例):
```cpp
#include <pybind11/pybind11.h>
#include "{{headerInclude}}"

PYBIND11_MODULE({{moduleName}}, m) {
    m.doc() = "{{documentation}}";

    {{#elements}}
    {{> Pybind11Class}}
    {{/elements}}
}
```

#### 3.3 Python 代码模板示例

**`PythonClass.mustache`** (概念示例):
```python
class {{resolveName}}({{parentClass}}):
    """{{documentation}}"""

    {{#properties}}
    @property
    def {{resolveName}}(self) -> {{resolveType typeRef}}:
        return self._native.{{resolveName}}

    {{/properties}}

    {{#functions}}
    def {{resolveName}}(self{{#parameters}}, {{name}}: {{type}}{{/parameters}}) -> {{returnType}}:
        """{{documentation}}"""
        return self._native.{{resolveName}}({{#parameters}}{{name}}{{/parameters}})

    {{/functions}}
```

---

### Phase 4 — 类型映射

#### 4.1 基本类型映射

| LIME 类型 | C++ 类型 | Python 类型 | pybind11 转换 |
|-----------|----------|-------------|---------------|
| `Void` | `void` | `None` | `void` |
| `Boolean` | `bool` | `bool` | 自动 |
| `Byte` | `int8_t` | `int` | 自动 |
| `Short` | `int16_t` | `int` | 自动 |
| `Int` | `int32_t` | `int` | 自动 |
| `Long` | `int64_t` | `int` | 自动 |
| `UByte` | `uint8_t` | `int` | 自动 |
| `UShort` | `uint16_t` | `int` | 自动 |
| `UInt` | `uint32_t` | `int` | 自动 |
| `ULong` | `uint64_t` | `int` | 自动 |
| `Float` | `float` | `float` | 自动 |
| `Double` | `double` | `float` | 自动 |
| `String` | `std::string` | `str` | 自动 |
| `Blob` | `std::vector<uint8_t>` | `bytes` | 自动 |
| `Date` | `std::chrono::system_clock::time_point` | `datetime.datetime` | 自定义 caster |
| `Duration` | `std::chrono::nanoseconds` | `datetime.timedelta` | 自定义 caster |
| `Locale` | 自定义 Locale 类型 | `str` (BCP 47) 或自定义 | 自定义 caster |

#### 4.2 复合类型映射

| LIME 类型 | C++ 类型 | Python 类型 | pybind11 处理 |
|-----------|----------|-------------|---------------|
| `List<T>` | `std::vector<T>` | `list[T]` | 自动 (需 `#include <pybind11/stl.h>`) |
| `Set<T>` | `std::unordered_set<T>` | `set[T]` | 自动 |
| `Map<K,V>` | `std::unordered_map<K,V>` | `dict[K,V]` | 自动 |
| `T?` (nullable) | `std::optional<T>` | `Optional[T]` | 自动 (需 `#include <pybind11/stl.h>`) |

#### 4.3 用户定义类型映射

| LIME 类型 | C++ 类型 | Python 类型 | pybind11 处理 |
|-----------|----------|-------------|---------------|
| `struct` | C++ struct/class | `@dataclass` 或普通类 | pybind11 `py::class_` 绑定 |
| `class` | C++ 抽象类 | Python 类 (包装 C++ 指针) | pybind11 `py::class_` + trampoline |
| `interface` | C++ 纯虚类 | Python ABC/Protocol | pybind11 trampoline + `py::class_` |
| `enum` | C++ enum | `enum.Enum` | pybind11 `py::enum_` |
| `exception` | C++ exception | Python Exception 子类 | pybind11 `py::exception` + 异常翻译 |
| `lambda` | C++ `std::function` | Python callable | pybind11 自动转换 |
| `typealias` | C++ `using`/`typedef` | Python type alias | 在 `.pyi` 中声明 |

#### 4.4 日期/Duration 自定义类型转换器

**`Pybind11TypeCaster.mustache`** (概念示例):
```cpp
#include <pybind11/chrono.h>
#include <chrono>

namespace pybind11::detail {
    // Date: time_point ↔ datetime.datetime
    template<>
    struct type_caster<std::chrono::system_clock::time_point> {
        PYBIND11_TYPE_CASTER(std::chrono::system_clock::time_point, _("datetime.datetime"));
        
        static handle cast(const std::chrono::system_clock::time_point &src, return_value_policy, handle parent) {
            // Convert time_point to datetime.datetime
            ...
        }
        
        static bool load(handle src, bool) {
            // Convert datetime.datetime to time_point
            ...
        }
    };
}
```

---

### Phase 5 — 对象生命周期与回调

#### 5.1 对象生命周期管理

pybind11 自动管理引用计数，但需要注意：

**C++ → Python (返回值)**:
- pybind11 默认使用 `return_value_policy::automatic`
- 对于返回 C++ 对象指针的函数，需要配置合适的策略：
  - `return_value_policy::reference_internal` — 对象生命周期绑定到 Python wrapper
  - `return_value_policy::take_ownership` — Python 接管所有权

**Python → C++ (参数传递)**:
- pybind11 自动处理值传递和引用传递
- 对于接口实现（Python 类继承 C++ 接口），需要 trampoline 类

#### 5.2 引用相等性 (Referential Equality)

Gluecodium 要求跨语言边界保持引用相等性。pybind11 方案需要：

1. **Wrapper Cache**: 维护 `C++ 指针 → Python 对象` 的映射表
2. 当 C++ 返回已有对象的指针时，查找 cache 返回同一 Python 对象
3. 参照 Dart 的 `InstanceCache` 和 Swift 的 `WrapperCache` 实现

**`Pybind11WrapperCache.mustache`** (概念示例):
```cpp
// Wrapper cache: C++ raw pointer → Python object
class WrapperCache {
public:
    static WrapperCache& instance() { ... }
    
    py::object get_or_create(void* cpp_ptr, py::object (*creator)()) {
        auto it = cache.find(cpp_ptr);
        if (it != cache.end()) {
            return it->second;
        }
        auto obj = creator();
        cache[cpp_ptr] = obj;
        return obj;
    }
    
private:
    std::unordered_map<void*, py::object> cache;
};
```

#### 5.3 C++ → Python 回调 (GIL 安全)

当 C++ 线程调用 Python 回调时，必须持有 GIL：

```cpp
// 在 trampoline 类中:
void onCallback(int value) override {
    py::gil_scoped_acquire gil;  // 获取 GIL
    PYBIND11_OVERRIDE(void, BaseClass, onCallback, value);
}
```

**关键点**：
- 所有 trampoline 方法的 `PYBIND11_OVERRIDE` 宏内部需要 `py::gil_scoped_acquire`
- 如果回调可能从非 Python 线程触发，需要确保 Python 解释器已初始化
- 参照 Dart 的 `CallbacksQueue` 和 `IsolateContext` 机制

#### 5.4 异常映射

| C++ 异常 | Python 异常 |
|----------|-------------|
| `std::exception` | `RuntimeError` |
| Gluecodium `Return<T, Error>` 失败 | 生成的 `Error` 子类异常 |
| `std::bad_optional_access` | `ValueError` |
| `std::out_of_range` | `IndexError` |
| `std::invalid_argument` | `ValueError` |

**`Pybind11Exception.mustache`** (概念示例):
```cpp
// 注册自定义异常
static py::exception<MyError> exc(m, "MyError");
py::register_exception_translator([](std::exception_ptr p) {
    try { if (p) std::rethrow_exception(p); }
    catch (const MyError &e) {
        PyErr_SetString(exc.ptr(), e.what());
    }
});
```

#### 5.5 异步支持 (`@Async`)

- `@Async` 函数映射为 Python `asyncio` 协程
- pybind11 绑定返回 `Future` 对象，Python 端 `await`
- 需要 `PyGILState_Ensure`/`Release` 在后台线程完成时获取 GIL 设置结果
- 参照 Dart 的 `DartAsyncHelpers` 实现异步桥接

---

### Phase 6 — 输出文件结构

#### 6.1 生成文件布局

```
output/
├── python/                              # Python 源代码
│   ├── __init__.py                      # 包初始化 (COMMON)
│   ├── setup.py                         # 构建脚本 (COMMON)
│   ├── pyproject.toml                   # PEP 518 构建配置 (COMMON)
│   ├── _type_converters.py              # 内部类型转换辅助 (COMMON)
│   ├── _wrapper_cache.py                # 引用缓存 (COMMON)
│   ├── _native_base.py                  # Native base wrapper (COMMON)
│   └── src/                             # 生成的 Python 源码
│       └── <package_path>/
│           ├── __init__.py
│           ├── <module>.py              # 每个顶层 LIME 元素的 Python 接口
│           └── <module>.pyi             # 类型存根 (type stubs)
│
└── pybind11/                            # pybind11 C++ 绑定源码
    ├── <module>_bindings.cpp            # 每个顶层元素的 pybind11 绑定
    ├── _wrapper_cache.h                 # Wrapper cache (COMMON)
    ├── _type_casters.h                  # 自定义类型转换器 (COMMON)
    └── _module_init.cpp                 # 模块初始化 (COMMON)
```

#### 6.2 构建产物

构建后产生 Python 扩展模块：
- Linux: `.<module_name>.cpython-3x-x86_64-linux-gnu.so`
- macOS: `.<module_name>.cpython-3x-darwin.so`
- Windows: `.<module_name>.cp3x-win_amd64.pyd`

---

### Phase 7 — CMake 集成

#### 7.1 添加 Python 生成器到 CMake 支持列表

**文件**: `cmake/modules/gluecodium/gluecodium/KnownOptionalProperties.cmake`

添加 Python 相关 CMake target 属性：
```cmake
_gluecodium_define_target_property(
  GLUECODIUM_PYTHON_PACKAGE
  BRIEF_DOCS "The base Python package to use for generated Python sources"
  FULL_DOCS "The base Python package to use for generated Python sources."
)

_gluecodium_define_target_property(
  GLUECODIUM_PYTHON_INTERNAL_PACKAGE
  BRIEF_DOCS "The sub-package to use for internal Python code"
  FULL_DOCS "The sub-package to use for internal Python code."
)

_gluecodium_define_target_property(
  GLUECODIUM_PYTHON_MODULE_NAME
  BRIEF_DOCS "Name of the generated Python extension module"
  FULL_DOCs "Name of the generated Python extension module for pybind11."
)

_gluecodium_define_target_property(
  GLUECODIUM_PYTHON_NAMERULES
  BRIEF_DOCS "The path to a file with name rules for Python"
  FULL_DOCS "The path to a file with name rules for Python."
)
```

#### 7.2 更新生成文件列表

**文件**: `cmake/modules/gluecodium/gluecodium/details/ListGeneratedFiles.cmake`

添加 Python/pybind11 文件收集逻辑：
```cmake
if(python IN_LIST _generators)
  list(APPEND _python_generated_files
              "${_unity_dir}/${GLUECODIUM_GENERATED_python_${_group}}")
  list(APPEND _pybind11_generated_files
              "${_unity_dir}/${GLUECODIUM_GENERATED_pybind11_${_group}}")
endif()
```

#### 7.3 添加 Python 到支持生成器列表

**文件**: `cmake/modules/gluecodium/gluecodium/details/ReadRequiredProperties.cmake`

确保 `python` 在 `GLUECODIUM_SUPPORTED_GENERATORS` 列表中。

**文件**: `cmake/tests/utils/get_supported_gluecodium_generators.cmake`

```cmake
find_program(_python_exe python3)
if(_python_exe)
  list(APPEND _gluecodium_generator python)
endif()
```

#### 7.4 pybind11 CMake 集成

**新文件**: `cmake/modules/gluecodium/Python.cmake`

```cmake
# Python 模块: 查找 pybind11 并配置 Python 扩展模块构建
function(gluecodium_target_python_sources _target)
  find_package(pybind11 REQUIRED)
  
  # 获取生成的 pybind11 .cpp 文件
  get_target_property(_pybind11_sources ${_target} GLUECODIUM_PYBIND11_SOURCES)
  
  # 创建 Python 扩展模块
  pybind11_add_module(${_target}_python ${_pybind11_sources})
  target_link_libraries(${_target}_python PRIVATE ${_target})
endfunction()
```

---

### Phase 8 — 测试

#### 8.1 Smoke 测试 (单元测试)

**目录**: `gluecodium/src/test/resources/smoke/`

为每个现有 smoke 测试用例添加 `output/python/` 和 `output/pybind11/` 输出目录。

参照现有 Dart smoke 测试结构：
```
smoke/basic_types/
├── input/
│   └── BasicTypes.lime
└── output/
    ├── cpp/
    ├── dart/
    └── python/              # 新增
        └── src/
            └── smoke/
                └── basic_types.py
    └── pybind11/            # 新增
        └── basic_types_bindings.cpp
```

更新 smoke 测试的 Java 测试类，添加 Python 生成器的断言。

#### 8.2 功能测试

**新目录**: `functional-tests/functional/python/`

```
functional-tests/functional/python/
├── CMakeLists.txt
├── conftest.py                      # pytest 配置
├── pyproject.toml.in                # 模板 pyproject.toml
└── test/
    ├── basic_types_test.py
    ├── classes_test.py
    ├── enums_test.py
    ├── structs_test.py
    ├── interfaces_test.py
    ├── exceptions_test.py
    ├── lambdas_test.py
    ├── inheritance_test.py
    ├── nullable_test.py
    ├── collections_test.py
    ├── dates_test.py
    ├── durations_test.py
    ├── equatable_test.py
    ├── constants_test.py
    ├── defaults_test.py
    ├── method_overloads_test.py
    ├── nesting_test.py
    ├── properties_test.py
    ├── ref_equality_test.py
    ├── listeners_test.py
    ├── async_test.py
    ├── external_types_test.py
    └── skip_element_test.py
```

**`CMakeLists.txt`** (参照 `functional-tests/functional/dart/CMakeLists.txt`):
```cmake
cmake_minimum_required(VERSION 3.10)
project(test_python)

if(NOT FUNCTIONAL_BUILD_PYTHON_TESTS)
  return()
endif()

find_program(PYTHON_EXE python3)
find_package(pybind11 REQUIRED)

# 构建 Python 扩展模块
pybind11_add_module(functional_python ${PYBIND11_SOURCES})
target_link_libraries(functional_python PRIVATE functional)

# 运行 pytest
add_test(NAME unit_tests_python
  COMMAND ${PYTHON_EXE} -m pytest test/
  WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR})
```

#### 8.3 功能测试构建脚本

**新文件**: `functional-tests/scripts/build-python-functional`

参照 `build-dart-functional`：
```bash
#!/bin/bash
# 构建 Python 功能测试
# 1. 运行 Gluecodium 生成 C++ + Python 代码
# 2. 使用 CMake 编译 C++ 库和 pybind11 扩展模块
# 3. 运行 pytest
```

---

### Phase 9 — 文档

#### 9.1 更新用户指南

**文件**: `docs/guide.md`
- 添加 Python 生成器使用说明
- 添加 `-generators cpp,python` 使用示例

#### 9.2 更新 LimeIDL 参考

**文件**: `docs/lime_idl.md`
- 添加 `@Python` 属性说明

#### 9.3 更新属性参考

**文件**: `docs/lime_attributes.md`
- 添加 `@Python(Name=...)`, `@Python(Skip)`, `@Python(Internal)`, `@Python(Public)` 说明

#### 9.4 更新外部类型文档

**文件**: `docs/external_types.md`
- 添加 Python 外部类型描述块格式

#### 9.5 新增 Python 特定文档

**新文件**: `docs/python.md`
- Python 生成器架构说明
- pybind11 依赖和构建要求
- 类型映射表
- 异步支持说明
- GIL 和线程安全注意事项

---

### Phase 10 — Gradle 插件支持

**文件**: `gluecodium-gradle/src/main/java/com/here/gluecodium/gradle/GluecodiumExtension.kt` (或对应文件)

添加 Python 相关 Gradle 配置：
```groovy
gluecodium {
    pythonPackage = 'com.example.myapp'
    pythonModuleName = 'myapp_native'
}
```

---

## 3. 实施顺序

```
Phase 1 (LIME 模型层)
    │
    ├──→ Phase 2 (生成器骨架) ──→ Phase 3 (模板系统)
    │                                    │
    │                                    └──→ Phase 4 (类型映射)
    │                                              │
    │                                              └──→ Phase 5 (生命周期与回调)
    │                                                        │
    │                                                        └──→ Phase 6 (输出结构)
    │                                                                  │
    │                                                                  └──→ Phase 7 (CMake)
    │                                                                            │
    └──────────────────────────────────────────────────────────→ Phase 8 (测试)
                                                                                       │
                                                                                       └──→ Phase 9-10 (文档与插件)
```

**建议的分步交付里程碑**：

| 里程碑 | 内容 | 预估工作量 |
|--------|------|-----------|
| **M1** | Phase 1-2: LIME 属性 + 生成器骨架 + CLI 注册 + 基本框架能跑通 | 3-5 天 |
| **M2** | Phase 3-4: 模板 + 基本类型/struct/enum 映射 | 5-7 天 |
| **M3** | Phase 5: class/interface + 回调 + GIL + 引用相等性 | 7-10 天 |
| **M4** | Phase 4 续: 集合/异常/nullable + Phase 6: 输出结构完善 | 3-5 天 |
| **M5** | Phase 7: CMake 集成 | 2-3 天 |
| **M6** | Phase 8: Smoke 测试 + 功能测试 | 5-7 天 |
| **M7** | Phase 9-10: 文档 + Gradle 插件 | 2-3 天 |

**总预估**: 4-6 周

---

## 4. 风险与缓解措施

| 风险 | 影响 | 缓解措施 |
|------|------|----------|
| pybind11 对 `Return<T, Error>` 类型的支持需要自定义转换器 | 中 | 提前验证 `Return<T, Error>` 的 type_caster 可行性 |
| GIL 死锁风险（C++ 持有锁时回调 Python） | 高 | 在 trampoline 中严格使用 `py::gil_scoped_acquire`/`py::gil_scoped_release` |
| 引用相等性实现复杂度 | 中 | 参照 Dart `InstanceCache` 和 Swift `WrapperCache` 的成熟实现 |
| 多平台编译（Windows MSVC + pybind11） | 中 | CI 中添加 Windows 构建测试 |
| Python GIL 与 C++ 线程的交互 | 高 | 在设计文档中明确线程模型，参照 Dart 的 isolate 机制 |
| pybind11 版本兼容性 | 低 | 固定最低版本 2.11.0，CI 矩阵测试 |

---

## 5. 需要修改的文件清单

### 新增文件
| 文件路径 | 说明 |
|----------|------|
| `gluecodium/src/main/java/.../generator/python/*.kt` | Python 生成器实现 (约 10 个文件) |
| `gluecodium/src/main/resources/templates/python/*.mustache` | Mustache 模板 (约 25 个文件) |
| `gluecodium/src/main/resources/namerules/python.properties` | Python 命名规则 |
| `functional-tests/functional/python/*` | Python 功能测试 |
| `functional-tests/scripts/build-python-functional` | Python 测试构建脚本 |
| `cmake/modules/gluecodium/Python.cmake` | CMake Python 模块 |
| `docs/python.md` | Python 生成器文档 |

### 修改文件
| 文件路径 | 修改内容 |
|----------|----------|
| `lime-runtime/.../LimeAttributeType.kt` | 添加 `PYTHON` 枚举值 |
| `lime-loader/.../AntlrLimeConverter.kt` | 添加 `"Python"` 注解解析 |
| `gluecodium/.../common/GeneratorOptions.kt` | 添加 Python 选项字段 |
| `gluecodium/.../cli/OptionReader.kt` | 添加 Python CLI 选项 |
| `gluecodium/src/main/resources/META-INF/services/...Generator` | 注册 PythonGenerator |
| `cmake/.../KnownOptionalProperties.cmake` | 添加 Python CMake 属性 |
| `cmake/.../ListGeneratedFiles.cmake` | 添加 Python 文件收集 |
| `cmake/.../get_supported_gluecodium_generators.cmake` | 添加 Python 检测 |
| `docs/guide.md` | 添加 Python 使用说明 |
| `docs/lime_idl.md` | 添加 `@Python` 属性说明 |
| `docs/lime_attributes.md` | 添加 `@Python` 属性参考 |
| `docs/external_types.md` | 添加 Python 外部类型说明 |
| `AGENTS.md` | 更新支持语言列表和结构说明 |

---

## 6. 验收标准

- [ ] `./gradlew build` 通过（包含新增的 smoke 测试）
- [ ] `-generators cpp,python` 能成功生成 Python + pybind11 C++ 代码
- [ ] 生成的 pybind11 代码能在 Linux/macOS/Windows 上编译通过
- [ ] 功能测试覆盖所有现有测试用例（与 Dart/Swift 对齐）
- [ ] 引用相等性测试通过
- [ ] GIL 安全的回调测试通过
- [ ] `@Python(Skip)` / `@Python(Internal)` / `@Python(Name=...)` 属性正常工作
- [ ] 文档完整，包含使用指南和类型映射表
