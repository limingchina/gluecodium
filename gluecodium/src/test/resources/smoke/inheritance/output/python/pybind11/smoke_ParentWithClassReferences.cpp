

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/ChildClassFromClass.h"
#include "smoke/ParentClass.h"
#include "smoke/ParentWithClassReferences.h"
#include "memory"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentWithClassReferences = ::smoke::ParentWithClassReferences;

class ParentWithClassReferencesTrampoline : public ParentWithClassReferences {
public:
    using ParentWithClassReferences::ParentWithClassReferences;

    ::std::shared_ptr< ::smoke::ChildClassFromClass > class_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(::std::shared_ptr< ::smoke::ChildClassFromClass >, ParentWithClassReferences, class_function);
    }
    ::std::shared_ptr< ::smoke::ParentClass >& get_class_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::shared_ptr< ::smoke::ParentClass >&, ParentWithClassReferences, get_class_property);
    }
    void set_class_property(const ::std::shared_ptr< ::smoke::ParentClass >& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentWithClassReferences, set_class_property, value);
    }
};

void register_ParentWithClassReferences(py::module_& module) {
    py::class_<ParentWithClassReferences, std::shared_ptr<ParentWithClassReferences>, ParentWithClassReferencesTrampoline>(module, "ParentWithClassReferences")
        .def(py::init<>())
        .def("class_function", [](ParentWithClassReferences& self) {
            return self.class_function();
        })
        .def_property("class_property", py::overload_cast<>(&ParentWithClassReferences::get_class_property, py::const_), py::overload_cast<const ::std::shared_ptr< ::smoke::ParentClass >&>(&ParentWithClassReferences::set_class_property))
        ;
}

