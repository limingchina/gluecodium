

#include <Python.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <pybind11/chrono.h>
#include "_wrapper_cache.h"
#include "_return_caster.h"

// pybind11 3.x no longer provides the `py` namespace alias by default.
namespace py = pybind11;
#include "smoke/InternalInterface.h"
#include "string"

// Bring the generated C++ type into the global namespace so it can be referenced by its short name.
using InternalInterface = ::gluecodium::smoke::InternalInterface;

class InternalInterfaceTrampoline : public InternalInterface {
public:
    using InternalInterface::InternalInterface;

    void foo_bar(
            /* no args */ ) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, InternalInterface, foo_bar);
    }
    ::std::string& get_some_property_of_internal_interface() const override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(::std::string&, InternalInterface, get_some_property_of_internal_interface);
    }
    void set_some_property_of_internal_interface(const ::std::string& value) override {
        py::gil_scoped_acquire gil;
        PYBIND11_OVERRIDE(void, InternalInterface, set_some_property_of_internal_interface, value);
    }
};

void register_InternalInterface(py::module_& module) {
    py::class_<InternalInterface, std::shared_ptr<InternalInterface>, InternalInterfaceTrampoline>(module, "InternalInterface")
        .def(py::init<>())
        .def("foo_bar", &InternalInterface::foo_bar)
        .def_property("some_property_of_internal_interface", py::overload_cast<>(&InternalInterface::get_some_property_of_internal_interface, py::const_), py::overload_cast<const ::std::string&>(&InternalInterface::set_some_property_of_internal_interface))
        ;
}

