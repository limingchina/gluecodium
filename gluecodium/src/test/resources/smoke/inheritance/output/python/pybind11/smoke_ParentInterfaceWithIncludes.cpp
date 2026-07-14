

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/IncludableClass.h"
#include "smoke/IncludableEnum.h"
#include "smoke/IncludableLambda.h"
#include "smoke/IncludableStruct.h"
#include "smoke/ParentInterfaceWithIncludes.h"
#include "smoke/ShouldNotInclude.h"
#include "functional"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentInterfaceWithIncludes = ::smoke::ParentInterfaceWithIncludes;

class ParentInterfaceWithIncludesTrampoline : public ParentInterfaceWithIncludes {
public:
    using ParentInterfaceWithIncludes::ParentInterfaceWithIncludes;

    ::std::shared_ptr< ::smoke::IncludableClass > root_method(
            const ::smoke::IncludableStruct& input1, ::smoke::IncludableEnum input2 ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::IncludableClass >, ParentInterfaceWithIncludes, root_method, input1, input2);
    }
    ::smoke::ShouldNotInclude not_in_java(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(::smoke::ShouldNotInclude, ParentInterfaceWithIncludes, not_in_java);
    }
    ::smoke::IncludableLambda& get_root_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::smoke::IncludableLambda&, ParentInterfaceWithIncludes, get_root_property);
    }
    void set_root_property(const ::smoke::IncludableLambda& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterfaceWithIncludes, set_root_property, value);
    }
    ::smoke::ShouldNotInclude& get_not_in_java_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::smoke::ShouldNotInclude&, ParentInterfaceWithIncludes, get_not_in_java_property);
    }
    void set_not_in_java_property(const ::smoke::ShouldNotInclude& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterfaceWithIncludes, set_not_in_java_property, value);
    }
};

void register_ParentInterfaceWithIncludes(py::module_& module) {
    py::class_<ParentInterfaceWithIncludes, std::shared_ptr<ParentInterfaceWithIncludes>, ParentInterfaceWithIncludesTrampoline>(module, "ParentInterfaceWithIncludes")
        .def(py::init<>())
        .def("root_method", [](ParentInterfaceWithIncludes& self, const ::smoke::IncludableStruct& input1, const ::smoke::IncludableEnum input2) {
            return self.root_method(input1, input2);
        }, py::arg("input1"), py::arg("input2"))
        .def("not_in_java", [](ParentInterfaceWithIncludes& self) {
            return self.not_in_java();
        })
        .def_property("root_property", py::overload_cast<>(&ParentInterfaceWithIncludes::get_root_property, py::const_), py::overload_cast<const ::smoke::IncludableLambda&>(&ParentInterfaceWithIncludes::set_root_property))
        .def_property("not_in_java_property", py::overload_cast<>(&ParentInterfaceWithIncludes::get_not_in_java_property, py::const_), py::overload_cast<const ::smoke::ShouldNotInclude&>(&ParentInterfaceWithIncludes::set_not_in_java_property))
        ;
}

