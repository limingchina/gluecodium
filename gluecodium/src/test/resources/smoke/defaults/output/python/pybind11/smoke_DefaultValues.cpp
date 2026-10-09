

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"
#include "_generic_caster.h"
#include "_locale_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "gluecodium/Optional.h"
#include "gluecodium/UnorderedMapHash.h"
#include "gluecodium/UnorderedSetHash.h"
#include "gluecodium/VectorHash.h"
#include "smoke/DefaultValues.h"
#include "cstdint"
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
            return gluecodium::python::native_identity(self);
        })
        .def_static("process_struct_with_defaults", &DefaultValues::process_struct_with_defaults, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        ;

auto cls_DefaultValuesStructWithDefaults = py::class_<StructWithDefaults>(cls_DefaultValues, "StructWithDefaults")
        .def_property("int_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](StructWithDefaults& self, const int32_t value) {

                self.int_field = value;

        })
        .def_property("uint_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.uint_field)
            ;
        }, [](StructWithDefaults& self, const uint32_t value) {

                self.uint_field = value;

        })
        .def_property("float_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.float_field)
            ;
        }, [](StructWithDefaults& self, const float value) {

                self.float_field = value;

        })
        .def_property("double_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.double_field)
            ;
        }, [](StructWithDefaults& self, const double value) {

                self.double_field = value;

        })
        .def_property("bool_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](StructWithDefaults& self, const bool value) {

                self.bool_field = value;

        })
        .def_property("string_field", [](const StructWithDefaults& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](StructWithDefaults& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<int32_t, uint32_t, float, double, bool, ::std::string>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("double_field"), py::arg("bool_field"), py::arg("string_field"))
        ;

auto cls_DefaultValuesNullableStructWithDefaults = py::class_<NullableStructWithDefaults>(cls_DefaultValues, "NullableStructWithDefaults")
        .def_property("int_field", [](const NullableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.int_field)
            ;
        }, [](NullableStructWithDefaults& self, const ::gluecodium::optional< int32_t >& value) {

                self.int_field = value;

        })
        .def_property("uint_field", [](const NullableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.uint_field)
            ;
        }, [](NullableStructWithDefaults& self, const ::gluecodium::optional< uint32_t >& value) {

                self.uint_field = value;

        })
        .def_property("float_field", [](const NullableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.float_field)
            ;
        }, [](NullableStructWithDefaults& self, const ::gluecodium::optional< float >& value) {

                self.float_field = value;

        })
        .def_property("bool_field", [](const NullableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](NullableStructWithDefaults& self, const ::gluecodium::optional< bool >& value) {

                self.bool_field = value;

        })
        .def_property("string_field", [](const NullableStructWithDefaults& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](NullableStructWithDefaults& self, const ::gluecodium::optional< ::std::string >& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< int32_t >, ::gluecodium::optional< uint32_t >, ::gluecodium::optional< float >, ::gluecodium::optional< bool >, ::gluecodium::optional< ::std::string >>(), py::arg("int_field"), py::arg("uint_field"), py::arg("float_field"), py::arg("bool_field"), py::arg("string_field"))
        ;

auto cls_DefaultValuesStructWithSpecialDefaults = py::class_<StructWithSpecialDefaults>(cls_DefaultValues, "StructWithSpecialDefaults")
        .def_property("float_nan_field", [](const StructWithSpecialDefaults& self) -> decltype(auto) {
            return
                (self.float_nan_field)
            ;
        }, [](StructWithSpecialDefaults& self, const float value) {

                self.float_nan_field = value;

        })
        .def_property("float_infinity_field", [](const StructWithSpecialDefaults& self) -> decltype(auto) {
            return
                (self.float_infinity_field)
            ;
        }, [](StructWithSpecialDefaults& self, const float value) {

                self.float_infinity_field = value;

        })
        .def_property("float_negative_infinity_field", [](const StructWithSpecialDefaults& self) -> decltype(auto) {
            return
                (self.float_negative_infinity_field)
            ;
        }, [](StructWithSpecialDefaults& self, const float value) {

                self.float_negative_infinity_field = value;

        })
        .def_property("double_nan_field", [](const StructWithSpecialDefaults& self) -> decltype(auto) {
            return
                (self.double_nan_field)
            ;
        }, [](StructWithSpecialDefaults& self, const double value) {

                self.double_nan_field = value;

        })
        .def_property("double_infinity_field", [](const StructWithSpecialDefaults& self) -> decltype(auto) {
            return
                (self.double_infinity_field)
            ;
        }, [](StructWithSpecialDefaults& self, const double value) {

                self.double_infinity_field = value;

        })
        .def_property("double_negative_infinity_field", [](const StructWithSpecialDefaults& self) -> decltype(auto) {
            return
                (self.double_negative_infinity_field)
            ;
        }, [](StructWithSpecialDefaults& self, const double value) {

                self.double_negative_infinity_field = value;

        })
        .def(py::init<>())
        .def(py::init<float, float, float, double, double, double>(), py::arg("float_nan_field"), py::arg("float_infinity_field"), py::arg("float_negative_infinity_field"), py::arg("double_nan_field"), py::arg("double_infinity_field"), py::arg("double_negative_infinity_field"))
        ;

auto cls_DefaultValuesStructWithEmptyDefaults = py::class_<StructWithEmptyDefaults>(cls_DefaultValues, "StructWithEmptyDefaults")
        .def_property("ints_field", [](const StructWithEmptyDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.ints_field)
            );
        }, [](StructWithEmptyDefaults& self, const ::std::vector< int32_t >& value) {

                self.ints_field = value;

        })
        .def_property("floats_field", [](const StructWithEmptyDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.floats_field)
            );
        }, [](StructWithEmptyDefaults& self, const ::std::vector< float >& value) {

                self.floats_field = value;

        })
        .def_property("map_field", [](const StructWithEmptyDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](StructWithEmptyDefaults& self, const ::std::unordered_map< uint32_t, ::std::string >& value) {

                self.map_field = value;

        })
        .def_property("struct_field", [](const StructWithEmptyDefaults& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](StructWithEmptyDefaults& self, const ::smoke::DefaultValues::StructWithDefaults& value) {

                self.struct_field = value;

        })
        .def_property("set_type_field", [](const StructWithEmptyDefaults& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.set_type_field)
            );
        }, [](StructWithEmptyDefaults& self, const ::std::unordered_set< ::std::string >& value) {

                self.set_type_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::vector< int32_t >, ::std::vector< float >, ::std::unordered_map< uint32_t, ::std::string >, ::smoke::DefaultValues::StructWithDefaults, ::std::unordered_set< ::std::string >>(), py::arg("ints_field"), py::arg("floats_field"), py::arg("map_field"), py::arg("struct_field"), py::arg("set_type_field"))
        ;

auto cls_DefaultValuesStructWithTypedefDefaults = py::class_<StructWithTypedefDefaults>(cls_DefaultValues, "StructWithTypedefDefaults")
        .def_property("long_field", [](const StructWithTypedefDefaults& self) -> decltype(auto) {
            return
                (self.long_field)
            ;
        }, [](StructWithTypedefDefaults& self, const int64_t value) {

                self.long_field = value;

        })
        .def_property("bool_field", [](const StructWithTypedefDefaults& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](StructWithTypedefDefaults& self, const bool value) {

                self.bool_field = value;

        })
        .def_property("string_field", [](const StructWithTypedefDefaults& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](StructWithTypedefDefaults& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<int64_t, bool, ::std::string>(), py::arg("long_field"), py::arg("bool_field"), py::arg("string_field"))
        ;


}
