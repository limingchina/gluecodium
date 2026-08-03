

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DefaultValues.h"
#include "cstdint"
#include "optional"
#include "string"
#include "unordered_map"
#include "unordered_set"
#include "vector"

using DefaultValues = ::smoke::DefaultValues;
using StructWithDefaults = ::smoke::DefaultValues::StructWithDefaults;
using NullableStructWithDefaults = ::smoke::DefaultValues::NullableStructWithDefaults;
using StructWithSpecialDefaults = ::smoke::DefaultValues::StructWithSpecialDefaults;
using StructWithEmptyDefaults = ::smoke::DefaultValues::StructWithEmptyDefaults;
using StructWithTypedefDefaults = ::smoke::DefaultValues::StructWithTypedefDefaults;



void register_smoke_DefaultValues(py::module_& module) {
auto cls_DefaultValues = py::class_<DefaultValues, std::shared_ptr<DefaultValues>>(module, "smoke_DefaultValues")
        .def("__gluecodium_id__", [](const DefaultValues& self) {
            return reinterpret_cast<uintptr_t>(std::addressof(self));
        })
        .def_static("process_struct_with_defaults", &DefaultValues::process_struct_with_defaults, py::arg("input"))
        ;

auto cls_DefaultValuesStructWithDefaults = py::class_<StructWithDefaults>(cls_DefaultValues, "StructWithDefaults")
        .def_readwrite("int_field", &StructWithDefaults::int_field)
        .def_readwrite("uint_field", &StructWithDefaults::uint_field)
        .def_readwrite("float_field", &StructWithDefaults::float_field)
        .def_readwrite("double_field", &StructWithDefaults::double_field)
        .def_readwrite("bool_field", &StructWithDefaults::bool_field)
        .def_readwrite("string_field", &StructWithDefaults::string_field)
        .def(py::init<>())
        .def(py::init<int32_t, uint32_t, float, double, bool, ::std::string>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("double_field"), py::arg("bool_field"), py::arg("string_field"))
        ;

auto cls_DefaultValuesNullableStructWithDefaults = py::class_<NullableStructWithDefaults>(cls_DefaultValues, "NullableStructWithDefaults")
        .def_readwrite("int_field", &NullableStructWithDefaults::int_field)
        .def_readwrite("uint_field", &NullableStructWithDefaults::uint_field)
        .def_readwrite("float_field", &NullableStructWithDefaults::float_field)
        .def_readwrite("bool_field", &NullableStructWithDefaults::bool_field)
        .def_readwrite("string_field", &NullableStructWithDefaults::string_field)
        .def(py::init<>())
        .def(py::init<std::optional< int32_t >, std::optional< uint32_t >, std::optional< float >, std::optional< bool >, std::optional< ::std::string >>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("bool_field"), py::arg("string_field"))
        ;

auto cls_DefaultValuesStructWithSpecialDefaults = py::class_<StructWithSpecialDefaults>(cls_DefaultValues, "StructWithSpecialDefaults")
        .def_readwrite("float_nan_field", &StructWithSpecialDefaults::float_nan_field)
        .def_readwrite("float_infinity_field", &StructWithSpecialDefaults::float_infinity_field)
        .def_readwrite("float_negative_infinity_field", &StructWithSpecialDefaults::float_negative_infinity_field)
        .def_readwrite("double_nan_field", &StructWithSpecialDefaults::double_nan_field)
        .def_readwrite("double_infinity_field", &StructWithSpecialDefaults::double_infinity_field)
        .def_readwrite("double_negative_infinity_field", &StructWithSpecialDefaults::double_negative_infinity_field)
        .def(py::init<>())
        .def(py::init<float, float, float, double, double, double>(), py::arg("float_nan_field"), py::arg("float_infinity_field"), py::arg("float_negative_infinity_field"), py::arg("double_nan_field"), py::arg("double_infinity_field"), py::arg("double_negative_infinity_field"))
        ;

auto cls_DefaultValuesStructWithEmptyDefaults = py::class_<StructWithEmptyDefaults>(cls_DefaultValues, "StructWithEmptyDefaults")
        .def_readwrite("ints_field", &StructWithEmptyDefaults::ints_field)
        .def_readwrite("floats_field", &StructWithEmptyDefaults::floats_field)
        .def_readwrite("map_field", &StructWithEmptyDefaults::map_field)
        .def_readwrite("struct_field", &StructWithEmptyDefaults::struct_field)
        .def_readwrite("set_type_field", &StructWithEmptyDefaults::set_type_field)
        .def(py::init<>())
        .def(py::init<::std::vector< int32_t >, ::std::vector< float >, ::std::unordered_map< uint32_t, ::std::string >, ::smoke::DefaultValues::StructWithDefaults, ::std::unordered_set< ::std::string >>(), py::arg("ints_field"), py::arg("floats_field"), py::arg("map_field"), py::arg("struct_field"), py::arg("set_type_field"))
        ;

auto cls_DefaultValuesStructWithTypedefDefaults = py::class_<StructWithTypedefDefaults>(cls_DefaultValues, "StructWithTypedefDefaults")
        .def_readwrite("long_field", &StructWithTypedefDefaults::long_field)
        .def_readwrite("bool_field", &StructWithTypedefDefaults::bool_field)
        .def_readwrite("string_field", &StructWithTypedefDefaults::string_field)
        .def(py::init<>())
        .def(py::init<int64_t, bool, ::std::string>(), py::arg("long_field"), py::arg("bool_field"), py::arg("string_field"))
        ;


}
