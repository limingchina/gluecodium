

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
#include "gluecodium/VectorHash.h"
#include "smoke/Nullable.h"
#include "smoke/SomeInterface.h"
#include "cstdint"
#include "memory"
#include "string"
#include "unordered_map"
#include "vector"

using Nullable = ::smoke::Nullable;
using SomeStruct = ::smoke::Nullable::SomeStruct;
using NullableStruct = ::smoke::Nullable::NullableStruct;
using NullableIntsStruct = ::smoke::Nullable::NullableIntsStruct;
using SomeEnum = ::smoke::Nullable::SomeEnum;



void register_smoke_Nullable(py::module_& module) {
auto cls_Nullable = py::class_<Nullable, std::shared_ptr<Nullable>>(module, "smoke_Nullable")
        .def("__gluecodium_id__", [](const Nullable& self) {
            return gluecodium::python::native_identity(self);
        })
        .def("method_with_string", &Nullable::method_with_string, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def("method_with_boolean", &Nullable::method_with_boolean, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def("method_with_double", &Nullable::method_with_double, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def("method_with_int", &Nullable::method_with_int, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def("method_with_some_struct", &Nullable::method_with_some_struct, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def("method_with_some_enum", &Nullable::method_with_some_enum, py::arg("input"), py::call_guard<py::gil_scoped_release>())
                .def("method_with_some_array", [](Nullable& self, const ::gluecodium::optional< ::std::vector< ::std::string > >& input) -> py::object {
                        return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_some_array(input); }));
                }, py::arg("input"))
                .def("method_with_inline_array", [](Nullable& self, const ::gluecodium::optional< ::std::vector< ::std::string > >& input) -> py::object {
                        return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_inline_array(input); }));
                }, py::arg("input"))
                .def("method_with_some_map", [](Nullable& self, const ::gluecodium::optional< ::std::unordered_map< int64_t, ::std::string > >& input) -> py::object {
                        return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) { return self.method_with_some_map(input); }));
                }, py::arg("input"))
        .def("method_with_instance", &Nullable::method_with_instance, py::arg("input"), py::call_guard<py::gil_scoped_release>())
        .def_property("string_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_string_property();
            });
        }, [](Nullable& self, const ::gluecodium::optional< ::std::string >& value) {
            gluecodium::python::call_native([&] {
                self.set_string_property(value);
            });
        })
        .def_property("is_bool_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.is_bool_property();
            });
        }, [](Nullable& self, const ::gluecodium::optional< bool >& value) {
            gluecodium::python::call_native([&] {
                self.set_bool_property(value);
            });
        })
        .def_property("double_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_double_property();
            });
        }, [](Nullable& self, const ::gluecodium::optional< double >& value) {
            gluecodium::python::call_native([&] {
                self.set_double_property(value);
            });
        })
        .def_property("int_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_int_property();
            });
        }, [](Nullable& self, const ::gluecodium::optional< int64_t >& value) {
            gluecodium::python::call_native([&] {
                self.set_int_property(value);
            });
        })
        .def_property("struct_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_struct_property();
            });
        }, [](Nullable& self, const ::gluecodium::optional< ::smoke::Nullable::SomeStruct >& value) {
            gluecodium::python::call_native([&] {
                self.set_struct_property(value);
            });
        })
        .def_property("enum_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_enum_property();
            });
        }, [](Nullable& self, const ::gluecodium::optional< ::smoke::Nullable::SomeEnum >& value) {
            gluecodium::python::call_native([&] {
                self.set_enum_property(value);
            });
        })
        .def_property("array_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_array_property();
            }));
        }, [](Nullable& self, const ::gluecodium::optional< ::std::vector< ::std::string > >& value) {
            gluecodium::python::call_native([&] {
                self.set_array_property(value);
            });
        })
        .def_property("inline_array_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_inline_array_property();
            }));
        }, [](Nullable& self, const ::gluecodium::optional< ::std::vector< ::std::string > >& value) {
            gluecodium::python::call_native([&] {
                self.set_inline_array_property(value);
            });
        })
        .def_property("map_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_map_property();
            }));
        }, [](Nullable& self, const ::gluecodium::optional< ::std::unordered_map< int64_t, ::std::string > >& value) {
            gluecodium::python::call_native([&] {
                self.set_map_property(value);
            });
        })
        .def_property("instance_property", [](const Nullable& self) -> decltype(auto) {
            return gluecodium::python::call_native([&]() -> decltype(auto) {
                return self.get_instance_property();
            });
        }, [](Nullable& self, const ::std::shared_ptr< ::smoke::SomeInterface >& value) {
            gluecodium::python::call_native([&] {
                self.set_instance_property(value);
            });
        })
        ;

auto cls_NullableSomeStruct = py::class_<SomeStruct>(cls_Nullable, "SomeStruct")
        .def_property("string_field", [](const SomeStruct& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](SomeStruct& self, const ::std::string& value) {

                self.string_field = value;

        })
        .def(py::init<>())
        .def(py::init<::std::string>(), py::arg("string_field"))
        ;

auto cls_NullableNullableStruct = py::class_<NullableStruct>(cls_Nullable, "NullableStruct")
        .def_property("string_field", [](const NullableStruct& self) -> decltype(auto) {
            return
                (self.string_field)
            ;
        }, [](NullableStruct& self, const ::gluecodium::optional< ::std::string >& value) {

                self.string_field = value;

        })
        .def_property("bool_field", [](const NullableStruct& self) -> decltype(auto) {
            return
                (self.bool_field)
            ;
        }, [](NullableStruct& self, const ::gluecodium::optional< bool >& value) {

                self.bool_field = value;

        })
        .def_property("double_field", [](const NullableStruct& self) -> decltype(auto) {
            return
                (self.double_field)
            ;
        }, [](NullableStruct& self, const ::gluecodium::optional< double >& value) {

                self.double_field = value;

        })
        .def_property("struct_field", [](const NullableStruct& self) -> decltype(auto) {
            return
                (self.struct_field)
            ;
        }, [](NullableStruct& self, const ::gluecodium::optional< ::smoke::Nullable::SomeStruct >& value) {

                self.struct_field = value;

        })
        .def_property("enum_field", [](const NullableStruct& self) -> decltype(auto) {
            return
                (self.enum_field)
            ;
        }, [](NullableStruct& self, const ::gluecodium::optional< ::smoke::Nullable::SomeEnum >& value) {

                self.enum_field = value;

        })
        .def_property("array_field", [](const NullableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.array_field)
            );
        }, [](NullableStruct& self, const ::gluecodium::optional< ::std::vector< ::std::string > >& value) {

                self.array_field = value;

        })
        .def_property("inline_array_field", [](const NullableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.inline_array_field)
            );
        }, [](NullableStruct& self, const ::gluecodium::optional< ::std::vector< ::std::string > >& value) {

                self.inline_array_field = value;

        })
        .def_property("map_field", [](const NullableStruct& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.map_field)
            );
        }, [](NullableStruct& self, const ::gluecodium::optional< ::std::unordered_map< int64_t, ::std::string > >& value) {

                self.map_field = value;

        })
        .def_property("instance_field", [](const NullableStruct& self) -> decltype(auto) {
            return
                (self.instance_field)
            ;
        }, [](NullableStruct& self, const ::std::shared_ptr< ::smoke::SomeInterface >& value) {

                self.instance_field = value;

        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< ::std::string >, ::gluecodium::optional< bool >, ::gluecodium::optional< double >, ::gluecodium::optional< ::smoke::Nullable::SomeStruct >, ::gluecodium::optional< ::smoke::Nullable::SomeEnum >, ::gluecodium::optional< ::std::vector< ::std::string > >, ::gluecodium::optional< ::std::vector< ::std::string > >, ::gluecodium::optional< ::std::unordered_map< int64_t, ::std::string > >, ::std::shared_ptr< ::smoke::SomeInterface >>(), py::arg("string_field"), py::arg("bool_field"), py::arg("double_field"), py::arg("struct_field"), py::arg("enum_field"), py::arg("array_field"), py::arg("inline_array_field"), py::arg("map_field"), py::arg("instance_field"))
        ;

auto cls_NullableNullableIntsStruct = py::class_<NullableIntsStruct>(cls_Nullable, "NullableIntsStruct")
        .def_property("int8_field", [](const NullableIntsStruct& self) -> decltype(auto) {
            return
                (self.int8_field)
            ;
        }, [](NullableIntsStruct& self, const ::gluecodium::optional< int8_t >& value) {

                self.int8_field = value;

        })
        .def_property("int16_field", [](const NullableIntsStruct& self) -> decltype(auto) {
            return
                (self.int16_field)
            ;
        }, [](NullableIntsStruct& self, const ::gluecodium::optional< int16_t >& value) {

                self.int16_field = value;

        })
        .def_property("int32_field", [](const NullableIntsStruct& self) -> decltype(auto) {
            return
                (self.int32_field)
            ;
        }, [](NullableIntsStruct& self, const ::gluecodium::optional< int32_t >& value) {

                self.int32_field = value;

        })
        .def_property("int64_field", [](const NullableIntsStruct& self) -> decltype(auto) {
            return
                (self.int64_field)
            ;
        }, [](NullableIntsStruct& self, const ::gluecodium::optional< int64_t >& value) {

                self.int64_field = value;

        })
        .def_property("uint8_field", [](const NullableIntsStruct& self) -> decltype(auto) {
            return
                (self.uint8_field)
            ;
        }, [](NullableIntsStruct& self, const ::gluecodium::optional< uint8_t >& value) {

                self.uint8_field = value;

        })
        .def_property("uint16_field", [](const NullableIntsStruct& self) -> decltype(auto) {
            return
                (self.uint16_field)
            ;
        }, [](NullableIntsStruct& self, const ::gluecodium::optional< uint16_t >& value) {

                self.uint16_field = value;

        })
        .def_property("uint32_field", [](const NullableIntsStruct& self) -> decltype(auto) {
            return
                (self.uint32_field)
            ;
        }, [](NullableIntsStruct& self, const ::gluecodium::optional< uint32_t >& value) {

                self.uint32_field = value;

        })
        .def_property("uint64_field", [](const NullableIntsStruct& self) -> decltype(auto) {
            return
                (self.uint64_field)
            ;
        }, [](NullableIntsStruct& self, const ::gluecodium::optional< uint64_t >& value) {

                self.uint64_field = value;

        })
        .def(py::init<>())
        .def(py::init<::gluecodium::optional< int8_t >, ::gluecodium::optional< int16_t >, ::gluecodium::optional< int32_t >, ::gluecodium::optional< int64_t >, ::gluecodium::optional< uint8_t >, ::gluecodium::optional< uint16_t >, ::gluecodium::optional< uint32_t >, ::gluecodium::optional< uint64_t >>(), py::arg("int8_field"), py::arg("int16_field"), py::arg("int32_field"), py::arg("int64_field"), py::arg("uint8_field"), py::arg("uint16_field"), py::arg("uint32_field"), py::arg("uint64_field"))
        ;

auto cls_NullableSomeEnum = py::enum_<SomeEnum>(cls_Nullable, "SomeEnum")
        .value("ON", SomeEnum::ON)
        .value("OFF", SomeEnum::OFF)
        ;


}
