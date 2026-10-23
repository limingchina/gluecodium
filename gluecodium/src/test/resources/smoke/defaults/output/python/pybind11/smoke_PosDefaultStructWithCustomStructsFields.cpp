

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
#include "smoke/ImmutableStructWithDefaults.h"
#include "smoke/PosDefaultStructWithCustomStructsFields.h"
#include "smoke/PosDefaultStructWithFieldUsingImmutableStruct.h"
#include "smoke/SomeMutableCustomStructWithDefaults.h"
#include "smoke/StructWithAllDefaults.h"
#include "smoke/StructWithNullableCollectionDefaults.h"
#include "cstdint"
#include "memory"
#include "string"
#include "unordered_map"
#include "vector"

using PosDefaultStructWithCustomStructsFields = ::smoke::PosDefaultStructWithCustomStructsFields;



void register_smoke_PosDefaultStructWithCustomStructsFields(py::module_& module) {
auto cls_PosDefaultStructWithCustomStructsFields = py::class_<PosDefaultStructWithCustomStructsFields>(module, "smoke_PosDefaultStructWithCustomStructsFields")
        .def_property_readonly("const_ctor_field0", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.const_ctor_field0)
            ;
        })
        .def_property_readonly("const_ctor_field1", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.const_ctor_field1)
            ;
        })
        .def_property("const_ctor_field2", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.const_ctor_field2)
            );
        }, [](PosDefaultStructWithCustomStructsFields& self, const ::std::vector< ::std::string >& value) {

                self.const_ctor_field2 = value;

        })
        .def_property("const_ctor_field3", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return gluecodium::python::to_python_regular(
                (self.const_ctor_field3)
            );
        }, [](PosDefaultStructWithCustomStructsFields& self, const ::gluecodium::optional< ::std::unordered_map< ::std::string, ::std::string > >& value) {

                self.const_ctor_field3 = value;

        })
        .def_property("const_ctor_field4", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.const_ctor_field4)
            ;
        }, [](PosDefaultStructWithCustomStructsFields& self, const int32_t value) {

                self.const_ctor_field4 = value;

        })
        .def_property("const_ctor_field5", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.const_ctor_field5)
            ;
        }, [](PosDefaultStructWithCustomStructsFields& self, const double value) {

                self.const_ctor_field5 = value;

        })
        .def_property_readonly("const_ctor_field6", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.const_ctor_field6)
            ;
        })
        .def_property_readonly("const_ctor_field7", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.const_ctor_field7)
            ;
        })
        .def_property("non_const_ctor_field0", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.non_const_ctor_field0)
            ;
        }, [](PosDefaultStructWithCustomStructsFields& self, const ::smoke::StructWithAllDefaults& value) {

                self.non_const_ctor_field0 = value;

        })
        .def_property_readonly("non_const_ctor_field1", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.non_const_ctor_field1)
            ;
        })
        .def_property("non_const_ctor_field2", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.non_const_ctor_field2)
            ;
        }, [](PosDefaultStructWithCustomStructsFields& self, const ::smoke::SomeMutableCustomStructWithDefaults& value) {

                self.non_const_ctor_field2 = value;

        })
        .def_property("non_const_ctor_field3", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.non_const_ctor_field3)
            ;
        }, [](PosDefaultStructWithCustomStructsFields& self, const ::smoke::StructWithNullableCollectionDefaults& value) {

                self.non_const_ctor_field3 = value;

        })
        .def_property("non_const_ctor_field4", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.non_const_ctor_field4)
            ;
        }, [](PosDefaultStructWithCustomStructsFields& self, const ::gluecodium::optional< ::smoke::StructWithAllDefaults >& value) {

                self.non_const_ctor_field4 = value;

        })
        .def_property("non_const_ctor_field5", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.non_const_ctor_field5)
            ;
        }, [](PosDefaultStructWithCustomStructsFields& self, const ::std::shared_ptr< ::std::vector< uint8_t > >& value) {

                self.non_const_ctor_field5 = value;

        })
        .def_property("non_const_ctor_field6", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.non_const_ctor_field6)
            ;
        }, [](PosDefaultStructWithCustomStructsFields& self, const ::std::shared_ptr< ::std::vector< uint8_t > >& value) {

                self.non_const_ctor_field6 = value;

        })
        .def_property("non_const_ctor_field7", [](const PosDefaultStructWithCustomStructsFields& self) -> decltype(auto) {
            return
                (self.non_const_ctor_field7)
            ;
        }, [](PosDefaultStructWithCustomStructsFields& self, const ::gluecodium::optional< ::std::shared_ptr< ::std::vector< uint8_t > > >& value) {

                self.non_const_ctor_field7 = value;

        })
        .def(py::init<>())
        .def(py::init<::smoke::ImmutableStructWithDefaults, ::gluecodium::optional< ::smoke::ImmutableStructWithDefaults >, ::std::vector< ::std::string >, ::gluecodium::optional< ::std::unordered_map< ::std::string, ::std::string > >, int32_t, double, ::gluecodium::optional< ::smoke::ImmutableStructWithDefaults >, ::gluecodium::optional< ::smoke::ImmutableStructWithDefaults >, ::smoke::StructWithAllDefaults, ::smoke::PosDefaultStructWithFieldUsingImmutableStruct, ::smoke::SomeMutableCustomStructWithDefaults, ::smoke::StructWithNullableCollectionDefaults, ::gluecodium::optional< ::smoke::StructWithAllDefaults >, ::std::shared_ptr< ::std::vector< uint8_t > >, ::std::shared_ptr< ::std::vector< uint8_t > >, ::gluecodium::optional< ::std::shared_ptr< ::std::vector< uint8_t > > >>(), py::arg("const_ctor_field0"), py::arg("const_ctor_field1"), py::arg("const_ctor_field2"), py::arg("const_ctor_field3"), py::arg("const_ctor_field4"), py::arg("const_ctor_field5"), py::arg("const_ctor_field6"), py::arg("const_ctor_field7"), py::arg("non_const_ctor_field0"), py::arg("non_const_ctor_field1"), py::arg("non_const_ctor_field2"), py::arg("non_const_ctor_field3"), py::arg("non_const_ctor_field4"), py::arg("non_const_ctor_field5"), py::arg("non_const_ctor_field6"), py::arg("non_const_ctor_field7"))
        ;


}
