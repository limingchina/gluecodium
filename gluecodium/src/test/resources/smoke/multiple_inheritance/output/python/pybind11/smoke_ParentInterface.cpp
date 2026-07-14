

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "another/SomeCoolClassType.h"
#include "smoke/ParentInterface.h"
#include "memory"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using ParentInterface = ::smoke::ParentInterface;

class ParentInterfaceTrampoline : public ParentInterface {
public:
    using ParentInterface::ParentInterface;

    void parent_function(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, ParentInterface, parent_function);
    }
    void some_function_that_uses_type_from_another_package(
            const ::std::shared_ptr< ::another::SomeCoolClassType >& some_param ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE_PURE(void, ParentInterface, some_function_that_uses_type_from_another_package, some_param);
    }
    ::std::string& get_parent_property() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, ParentInterface, get_parent_property);
    }
    void set_parent_property(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, ParentInterface, set_parent_property, value);
    }
};

void register_ParentInterface(py::module_& module) {
    py::class_<ParentInterface, std::shared_ptr<ParentInterface>, ParentInterfaceTrampoline>(module, "ParentInterface")
        .def(py::init<>())
        .def("parent_function", [](ParentInterface& self) {
            return self.parent_function();
        })
        .def("some_function_that_uses_type_from_another_package", [](ParentInterface& self, const ::std::shared_ptr< ::another::SomeCoolClassType >& some_param) {
            return self.some_function_that_uses_type_from_another_package(some_param);
        }, py::arg("some_param"))
        .def_property("parent_property", py::overload_cast<>(&ParentInterface::get_parent_property, py::const_), py::overload_cast<const ::std::string&>(&ParentInterface::set_parent_property))
        ;
}

